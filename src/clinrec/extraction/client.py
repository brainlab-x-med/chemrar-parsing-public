from __future__ import annotations

import json
import logging
import random
import re
import time
from collections import deque
from dataclasses import dataclass
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from threading import Lock
from typing import Any, Protocol, cast

import httpx

from clinrec.core.logging import log_kv_event
from clinrec.core.settings import (
    ClinRecSettings,
    RateLimitSettings,
    RetrySettings,
    TimeoutSettings,
)

logger = logging.getLogger("clinrec.llm.deepinfra_client")


class HttpResponseLike(Protocol):
    text: str
    status_code: int

    def raise_for_status(self) -> None: ...

    def json(self) -> Any: ...


class HttpClientLike(Protocol):
    def post(
        self,
        url: str,
        *,
        headers: dict[str, str],
        json: dict[str, Any],
    ) -> HttpResponseLike: ...

    def close(self) -> None: ...


_DEFAULT_TEMPERATURE = 0.0
_DEFAULT_MAX_COMPLETION_TOKENS = 4000
_RETRYABLE_HTTP_STATUS_CODES = frozenset({408, 409, 425, 429, 500, 502, 503, 504})
_THINK_BLOCK_PATTERN = re.compile(r"<think\b[^>]*>(.*?)</think>", re.IGNORECASE | re.DOTALL)
_RATE_LIMIT_WINDOW_SECONDS = 60.0
_MIN_WAIT_ACCOUNT_SECONDS = 0.001


@dataclass(slots=True)
class DeepInfraChatResult:
    model_id: str
    content: str
    raw_response: dict[str, Any]
    finish_reason: str | None = None
    usage: dict[str, Any] | None = None
    final_text: str | None = None
    thinking_text: str | None = None


@dataclass(slots=True)
class AssistantTextPayload:
    full_text: str
    final_text: str
    thinking_text: str

    @property
    def has_thinking(self) -> bool:
        return bool(self.thinking_text.strip())


class DeepInfraRateLimitBudgetExceededError(RuntimeError):
    """Raised when HTTP 429 retries consume the configured wait budget."""

    def __init__(
        self,
        *,
        waited_seconds: float,
        attempts: int,
        status_code: int,
        max_wait_seconds: float,
        last_error: Exception,
    ) -> None:
        self.waited_seconds = max(0.0, waited_seconds)
        self.attempts = max(0, attempts)
        self.status_code = status_code
        self.max_wait_seconds = max(0.0, max_wait_seconds)
        self.last_error = last_error
        super().__init__(
            "DeepInfra rate-limit budget exhausted: "
            f"waited_seconds={self.waited_seconds:.1f} "
            f"attempts={self.attempts} "
            f"status_code={self.status_code} "
            f"max_wait_seconds={self.max_wait_seconds:.1f} "
            f"last_error={last_error}"
        )


class _ClientRateLimiter:
    """Thread-safe process-local limiter for proactive throttling and cooldowns."""

    def __init__(self, settings: RateLimitSettings) -> None:
        self._settings = settings
        self._lock = Lock()
        self._recent_requests: deque[float] = deque()
        self._blocked_until: float = 0.0

    def reserve_request_slot(self) -> tuple[float, str | None]:
        if not self._settings.enabled:
            return 0.0, None

        with self._lock:
            now = time.monotonic()
            blocked_wait = max(0.0, self._blocked_until - now)
            scheduled_now = now + blocked_wait
            self._prune_window(scheduled_now)

            rpm_wait = 0.0
            if len(self._recent_requests) >= self._settings.requests_per_minute:
                oldest = self._recent_requests[0]
                rpm_wait = max(0.0, _RATE_LIMIT_WINDOW_SECONDS - (scheduled_now - oldest))

            wait_seconds = blocked_wait + rpm_wait
            reserved_at = now + wait_seconds
            self._prune_window(reserved_at)
            self._recent_requests.append(reserved_at)

            if wait_seconds <= 0.0:
                return 0.0, None
            if blocked_wait > 0.0 and rpm_wait > 0.0:
                return wait_seconds, "proactive_blocked_until_and_rpm"
            if blocked_wait > 0.0:
                return wait_seconds, "proactive_blocked_until"
            return wait_seconds, "proactive_rpm_limit"

    def apply_cooldown(self, cooldown_seconds: float) -> None:
        if not self._settings.enabled or cooldown_seconds <= 0.0:
            return
        with self._lock:
            next_blocked_until = time.monotonic() + cooldown_seconds
            self._blocked_until = max(self._blocked_until, next_blocked_until)

    def _prune_window(self, now: float) -> None:
        while self._recent_requests and now - self._recent_requests[0] >= _RATE_LIMIT_WINDOW_SECONDS:
            self._recent_requests.popleft()


class DeepInfraChatClient:
    def __init__(
        self,
        api_key: str,
        base_url: str,
        timeouts: TimeoutSettings,
        retries: RetrySettings,
        rate_limit: RateLimitSettings | None = None,
        http_client: Any | None = None,
        provider: str = "deepinfra",
    ) -> None:
        if not api_key.strip():
            raise ValueError("DeepInfra API key must not be empty.")
        self._api_key = api_key.strip()
        self._provider = provider
        self._base_url = base_url.rstrip("/")
        self._timeouts = timeouts
        self._retries = retries
        self._rate_limit = rate_limit or RateLimitSettings()
        self._rate_limiter = _ClientRateLimiter(self._rate_limit)
        self._http_client = http_client
        self._owned_client: httpx.Client | None = None

    @classmethod
    def from_settings(
        cls,
        settings: ClinRecSettings,
        http_client: Any | None = None,
    ) -> "DeepInfraChatClient":
        api_key = settings.effective_api_key
        if api_key is None:
            provider = settings.provider
            env_var_map = {"openai": "OPENAI_API_KEY", "openrouter": "OPENROUTER_API_KEY"}
            env_var = env_var_map.get(provider, "DEEPINFRA_API_KEY")
            raise ValueError(f"{env_var} is required for provider '{provider}'.")
        return cls(
            api_key=api_key,
            base_url=settings.effective_base_url,
            timeouts=settings.timeouts,
            retries=settings.retries,
            rate_limit=settings.rate_limit,
            http_client=http_client,
            provider=settings.provider,
        )

    def create_completion(
        self,
        *,
        model_id: str,
        messages: list[dict[str, Any]],
        temperature: float = _DEFAULT_TEMPERATURE,
        max_completion_tokens: int = _DEFAULT_MAX_COMPLETION_TOKENS,
        request_context: dict[str, Any] | None = None,
        response_format: dict[str, Any] | None = None,
        use_streaming: bool | None = None,
    ) -> DeepInfraChatResult:
        tokens_key = "max_completion_tokens" if self._provider in ("openai", "openrouter") else "max_tokens"
        payload: dict[str, Any] = {
            "model": model_id,
            "messages": messages,
            "temperature": temperature,
            tokens_key: max_completion_tokens,
        }
        if response_format is not None:
            payload["response_format"] = response_format

        response_payload = self._post_with_retries(
            "/chat/completions",
            payload,
            request_context=request_context,
            use_streaming=use_streaming,
        )
        choices = response_payload.get("choices") or []
        if not choices:
            raise ValueError("DeepInfra response does not contain choices.")

        first_choice = choices[0]
        if not isinstance(first_choice, dict):
            raise ValueError("DeepInfra choice payload is not a JSON object.")
        finish_reason = _normalize_finish_reason(first_choice.get("finish_reason"))
        if response_format == {"type": "json_object"}:
            _ensure_valid_finish_reason(finish_reason)
        try:
            assistant_payload = extract_assistant_payload(first_choice)
        except ValueError as exc:
            recovered_payload = self._maybe_recover_streaming_json_response(
                path="/chat/completions",
                payload=payload,
                response_payload=response_payload,
                request_context=request_context,
                response_format=response_format,
                use_streaming=use_streaming,
                original_error=exc,
            )
            if recovered_payload is None:
                raise

            response_payload = recovered_payload
            choices = response_payload.get("choices") or []
            if not choices:
                raise ValueError(
                    "DeepInfra recovery response does not contain choices."
                )
            first_choice = choices[0]
            if not isinstance(first_choice, dict):
                raise ValueError(
                    "DeepInfra recovery choice payload is not a JSON object."
                )
            finish_reason = _normalize_finish_reason(first_choice.get("finish_reason"))
            if response_format == {"type": "json_object"}:
                _ensure_valid_finish_reason(finish_reason)
            assistant_payload = extract_assistant_payload(first_choice)

        response_payload = _enrich_response_payload_with_assistant_content(
            response_payload,
            assistant_payload,
        )

        return DeepInfraChatResult(
            model_id=str(response_payload.get("model") or model_id),
            content=assistant_payload.final_text or assistant_payload.full_text,
            raw_response=response_payload,
            finish_reason=finish_reason,
            usage=(
                response_payload.get("usage")
                if isinstance(response_payload.get("usage"), dict)
                else None
            ),
            final_text=assistant_payload.final_text or None,
            thinking_text=assistant_payload.thinking_text or None,
        )


    def create_json_completion(
        self,
        *,
        model_id: str,
        system_prompt: str,
        user_prompt: str,
        temperature: float = _DEFAULT_TEMPERATURE,
        max_completion_tokens: int = _DEFAULT_MAX_COMPLETION_TOKENS,
        request_context: dict[str, Any] | None = None,
        use_streaming: bool | None = None,
    ) -> DeepInfraChatResult:
        return self.create_completion(
            model_id=model_id,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=temperature,
            max_completion_tokens=max_completion_tokens,
            request_context=request_context,
            response_format={"type": "json_object"},
            use_streaming=use_streaming,
        )

    def close(self) -> None:
        if self._owned_client is None:
            return
        self._owned_client.close()
        self._owned_client = None

    def __del__(self) -> None:  # pragma: no cover - best effort cleanup only
        try:
            self.close()
        except Exception:
            pass

    def _post_with_retries(
        self,
        path: str,
        payload: dict[str, Any],
        *,
        request_context: dict[str, Any] | None = None,
        use_streaming: bool | None = None,
    ) -> dict[str, Any]:
        last_error: Exception | None = None
        context = dict(request_context or {})
        context.setdefault("model", payload.get("model"))
        waited_seconds = 0.0
        attempt = 0

        while True:
            attempt += 1
            try:
                return self._post_once(
                    path=path,
                    payload=payload,
                    use_streaming=use_streaming,
                    context=context,
                )
            except Exception as exc:  # pragma: no cover - mostly exercised through tests
                last_error = exc
                if not _is_retryable_error(exc):
                    break

                is_rate_limited = self._rate_limit.enabled and _is_http_429_error(exc)
                if is_rate_limited:
                    sleep_seconds, retry_after, sleep_reason = self._compute_429_sleep_seconds(exc)
                    budget_remaining = max(
                        0.0, self._rate_limit.max_wait_seconds - waited_seconds
                    )
                    if sleep_seconds > budget_remaining:
                        raise DeepInfraRateLimitBudgetExceededError(
                            waited_seconds=waited_seconds,
                            attempts=attempt,
                            status_code=429,
                            max_wait_seconds=self._rate_limit.max_wait_seconds,
                            last_error=exc,
                        ) from exc
                    self._rate_limiter.apply_cooldown(sleep_seconds)
                    self._sleep_with_logging(
                        sleep_seconds=sleep_seconds,
                        context=context,
                        attempt=attempt,
                        max_attempts=None,
                        error=exc,
                        retry_after=retry_after,
                        sleep_reason=sleep_reason,
                        wait_budget_remaining=max(
                            0.0, budget_remaining - sleep_seconds
                        ),
                        throttled=True,
                    )
                    waited_seconds += max(sleep_seconds, _MIN_WAIT_ACCOUNT_SECONDS)
                    continue

                if attempt >= self._retries.max_attempts:
                    break
                sleep_seconds = self._compute_sleep_seconds(attempt)
                self._sleep_with_logging(
                    sleep_seconds=sleep_seconds,
                    context=context,
                    attempt=attempt,
                    max_attempts=self._retries.max_attempts,
                    error=exc,
                    retry_after=None,
                    sleep_reason="retry_backoff",
                    wait_budget_remaining=None,
                    throttled=False,
                )
        raise RuntimeError(
            f"DeepInfra request failed after {attempt} attempts: {last_error}"
        )

    def _post_once(
        self,
        path: str,
        payload: dict[str, Any],
        *,
        use_streaming: bool | None,
        context: dict[str, Any],
    ) -> dict[str, Any]:
        self._throttle_before_request(context=context)
        client = self._get_client()
        should_stream = _supports_streaming(client) if use_streaming is None else use_streaming
        if should_stream and _supports_streaming(client):
            return self._post_once_streaming(
                path=path,
                payload=payload,
                client=cast(Any, client),
            )
        return self._post_once_json(path=path, payload=payload, client=client)

    def _post_once_json(
        self,
        *,
        path: str,
        payload: dict[str, Any],
        client: Any,
    ) -> dict[str, Any]:
        try:
            response = client.post(
                f"{self._base_url}{path}",
                headers=self._build_headers(),
                json=payload,
            )
            response.raise_for_status()
            data = response.json()
            if not isinstance(data, dict):
                raise ValueError("DeepInfra response is not a JSON object.")
            return data
        except httpx.HTTPStatusError as exc:
            raise _wrap_http_status_error(exc) from exc
        except httpx.TimeoutException as exc:
            raise _RetryableDeepInfraError(f"DeepInfra timeout: {exc}") from exc
        except httpx.TransportError as exc:
            raise _RetryableDeepInfraError(f"DeepInfra transport error: {exc}") from exc
        except json.JSONDecodeError as exc:
            raise ValueError("DeepInfra returned non-JSON response body.") from exc

    def _post_once_streaming(
        self,
        *,
        path: str,
        payload: dict[str, Any],
        client: Any,
    ) -> dict[str, Any]:
        stream_payload = dict(payload)
        stream_payload["stream"] = True

        try:
            with client.stream(
                "POST",
                f"{self._base_url}{path}",
                headers=self._build_headers(streaming=True),
                json=stream_payload,
            ) as response:
                response.raise_for_status()
                return _collect_streaming_response(
                    response,
                    fallback_model_id=str(payload.get("model") or ""),
                )
        except httpx.HTTPStatusError as exc:
            raise _wrap_http_status_error(exc) from exc
        except httpx.TimeoutException as exc:
            raise _RetryableDeepInfraError(f"DeepInfra timeout: {exc}") from exc
        except httpx.TransportError as exc:
            raise _RetryableDeepInfraError(f"DeepInfra transport error: {exc}") from exc
        except json.JSONDecodeError as exc:
            raise ValueError(
                "DeepInfra returned invalid JSON while streaming completion events."
            ) from exc

    def _get_client(self) -> Any:
        if self._http_client is not None:
            return self._http_client
        if self._owned_client is None:
            client_kwargs: dict[str, Any] = {
                "timeout": self._build_timeout(),
                "follow_redirects": True,
                "http2": True,
            }
            try:
                self._owned_client = httpx.Client(**client_kwargs)
            except ImportError:
                client_kwargs["http2"] = False
                self._owned_client = httpx.Client(**client_kwargs)
        return self._owned_client

    def _build_headers(self, *, streaming: bool = False) -> dict[str, str]:
        accept_value = "text/event-stream" if streaming else "application/json"
        return {
            "Authorization": f"Bearer {self._api_key}",
            "Content-Type": "application/json",
            "Accept": accept_value,
            "Connection": "keep-alive",
        }

    def _build_timeout(self) -> httpx.Timeout:
        total = self._timeouts.total_seconds
        read = (
            min(self._timeouts.read_seconds, total)
            if total > 0
            else self._timeouts.read_seconds
        )
        connect = (
            min(self._timeouts.connect_seconds, total)
            if total > 0
            else self._timeouts.connect_seconds
        )
        return httpx.Timeout(
            timeout=total,
            connect=connect,
            read=read,
            write=read,
            pool=connect,
        )

    def _compute_sleep_seconds(self, attempt: int) -> float:
        base = self._retries.initial_backoff_seconds * (
            self._retries.backoff_multiplier ** (attempt - 1)
        )
        bounded = min(base, self._retries.max_backoff_seconds)
        jitter = random.uniform(0.0, self._retries.jitter_seconds)
        return bounded + jitter

    def _compute_429_sleep_seconds(
        self, exc: Exception
    ) -> tuple[float, float | None, str]:
        retry_after = _extract_retry_after_seconds(exc)
        if retry_after is not None:
            bounded_retry_after = min(
                max(retry_after, 0.0),
                self._rate_limit.max_retry_after_seconds,
            )
            return bounded_retry_after, retry_after, "http_429_retry_after_header"

        default_sleep = min(
            self._rate_limit.default_retry_after_seconds,
            self._rate_limit.max_retry_after_seconds,
        )
        jitter = random.uniform(0.0, self._retries.jitter_seconds)
        return (
            min(default_sleep + jitter, self._rate_limit.max_retry_after_seconds),
            None,
            "http_429_default_retry_after",
        )

    def _throttle_before_request(self, *, context: dict[str, Any]) -> None:
        sleep_seconds, sleep_reason = self._rate_limiter.reserve_request_slot()
        if sleep_seconds <= 0.0:
            return
        self._sleep_with_logging(
            sleep_seconds=sleep_seconds,
            context=context,
            attempt=None,
            max_attempts=None,
            error=None,
            retry_after=None,
            sleep_reason=sleep_reason,
            wait_budget_remaining=None,
            throttled=True,
            message="DeepInfra request throttled",
            level=logging.INFO,
        )

    def _sleep_with_logging(
        self,
        *,
        sleep_seconds: float,
        context: dict[str, Any],
        attempt: int | None,
        max_attempts: int | None,
        error: Exception | None,
        retry_after: float | None,
        sleep_reason: str | None,
        wait_budget_remaining: float | None,
        throttled: bool,
        message: str = "DeepInfra request retry scheduled",
        level: int = logging.WARNING,
    ) -> None:
        attempt_label: str | None = None
        if attempt is not None and max_attempts is not None:
            attempt_label = f"{attempt}/{max_attempts}"
        elif attempt is not None:
            attempt_label = str(attempt)

        log_kv_event(
            logger,
            message,
            level=level,
            doc_id=context.get("doc_id"),
            chunk=_format_chunk_label(context),
            model=context.get("model"),
            attempt=attempt_label,
            error=str(error) if error is not None else None,
            retry_in=f"{sleep_seconds:.1f}s",
            retry_after=f"{retry_after:.1f}s" if retry_after is not None else None,
            sleep_reason=sleep_reason,
            wait_budget_remaining=(
                round(wait_budget_remaining, 3)
                if wait_budget_remaining is not None
                else None
            ),
            throttled=throttled,
        )
        if sleep_seconds > 0.0:
            time.sleep(sleep_seconds)

    def _maybe_recover_streaming_json_response(
        self,
        *,
        path: str,
        payload: dict[str, Any],
        response_payload: dict[str, Any],
        request_context: dict[str, Any] | None,
        response_format: dict[str, Any] | None,
        use_streaming: bool | None,
        original_error: Exception,
    ) -> dict[str, Any] | None:
        if response_format != {"type": "json_object"}:
            return None
        if response_payload.get("_transport") != "streaming":
            return None
        if use_streaming is False:
            return None

        context = dict(request_context or {})
        context["streaming_recovery"] = "json_non_streaming"
        model_id = str(payload.get("model") or "")
        log_kv_event(
            logger,
            "Recovering DeepInfra JSON completion after empty streaming payload",
            level=logging.WARNING,
            doc_id=context.get("doc_id"),
            chunk=_format_chunk_label(context),
            model=model_id or None,
            error=str(original_error),
        )
        return self._post_with_retries(
            path,
            payload,
            request_context=context,
            use_streaming=False,
        )


def _collect_streaming_response(
    response: Any,
    *,
    fallback_model_id: str,
) -> dict[str, Any]:
    model_id = fallback_model_id
    usage: dict[str, Any] | None = None
    finish_reason: str | None = None
    delta_parts: list[str] = []
    last_complete_payload: AssistantTextPayload | None = None
    saw_event = False
    event_count = 0

    for raw_line in response.iter_lines():
        line = raw_line.decode("utf-8") if isinstance(raw_line, bytes) else str(raw_line)
        stripped = line.strip()
        if not stripped or stripped.startswith(":"):
            continue
        if stripped.startswith("data:"):
            stripped = stripped[5:].strip()
        if not stripped:
            continue
        if stripped == "[DONE]":
            break

        event = json.loads(stripped)
        if not isinstance(event, dict):
            raise ValueError("DeepInfra streaming event is not a JSON object.")
        saw_event = True
        event_count += 1
        model_id = str(event.get("model") or model_id)
        if isinstance(event.get("usage"), dict):
            usage = event["usage"]

        for choice in event.get("choices") or []:
            if not isinstance(choice, dict):
                continue
            choice_finish_reason = _normalize_finish_reason(choice.get("finish_reason"))
            if choice_finish_reason is not None:
                finish_reason = choice_finish_reason
            fragment = _extract_choice_delta_fragment(choice)
            if fragment:
                delta_parts.append(fragment)
            complete_payload = _extract_choice_complete_payload(choice)
            if complete_payload is not None and complete_payload.full_text:
                last_complete_payload = complete_payload

    if not saw_event:
        raise ValueError("DeepInfra streaming response did not contain any events.")

    if last_complete_payload is not None:
        assistant_payload = last_complete_payload
    else:
        joined_text = "".join(delta_parts)
        assistant_payload = (
            extract_assistant_payload({"message": {"content": joined_text}})
            if joined_text
            else AssistantTextPayload(full_text="", final_text="", thinking_text="")
        )

    payload: dict[str, Any] = {
        "model": model_id,
        "choices": [
            {
                "message": {"content": assistant_payload.full_text},
                "finish_reason": finish_reason,
            }
        ],
        "_transport": "streaming",
        "_streaming_diagnostics": {
            "event_count": event_count,
            "fragment_count": len(delta_parts),
            "message_content_characters": len(assistant_payload.full_text),
            "thinking_characters": len(assistant_payload.thinking_text),
        },
    }
    if usage is not None:
        payload["usage"] = usage
    return _enrich_response_payload_with_assistant_content(payload, assistant_payload)


def _extract_choice_delta_fragment(choice_payload: dict[str, Any]) -> str:
    delta = _ensure_dict(choice_payload.get("delta"))
    if not delta:
        return ""
    for key in ("content", "text", "output_text", "parts", "items"):
        value = delta.get(key)
        if isinstance(value, str):
            return value
        text = _extract_text_from_candidate(value)
        if text:
            return text
    return ""


def _extract_choice_complete_payload(choice_payload: dict[str, Any]) -> AssistantTextPayload | None:
    try:
        return extract_assistant_payload(choice_payload)
    except ValueError:
        return None


def _normalize_finish_reason(value: Any) -> str | None:
    if value is None:
        return None
    if isinstance(value, str):
        stripped = value.strip()
        return stripped or None
    return str(value)



def _ensure_valid_finish_reason(finish_reason: str | None) -> None:
    if finish_reason in {None, "stop"}:
        return
    if finish_reason == "length":
        raise ValueError(
            "DeepInfra completion was truncated before a reliable JSON object could be returned."
        )
    if finish_reason == "content_filter":
        raise ValueError(
            "DeepInfra completion was blocked by content filtering and cannot be trusted for structured parsing."
        )
    raise ValueError(
        f"DeepInfra completion finished with unsupported finish_reason={finish_reason!r}."
    )


class _RetryableDeepInfraError(RuntimeError):
    """Internal marker for transient DeepInfra/API transport failures."""

    def __init__(
        self,
        message: str,
        *,
        status_code: int | None = None,
        retry_after_seconds: float | None = None,
    ) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.retry_after_seconds = retry_after_seconds



def extract_assistant_text(choice_payload: dict[str, Any]) -> str:
    return extract_assistant_payload(choice_payload).full_text


def extract_assistant_payload(choice_payload: dict[str, Any]) -> AssistantTextPayload:
    message = _ensure_dict(choice_payload.get("message"))
    primary_candidates = [
        message.get("content"),
        message.get("parts"),
        message.get("items"),
        choice_payload.get("output_text"),
        choice_payload.get("text"),
        choice_payload.get("content"),
    ]
    reasoning_candidates = [
        message.get("reasoning"),
        message.get("reasoning_content"),  # DeepSeek-v4 uses this field name
        message.get("analysis"),
        choice_payload.get("reasoning"),
        choice_payload.get("reasoning_content"),
        choice_payload.get("analysis"),
    ]

    selected_payload: AssistantTextPayload | None = None
    for candidate in primary_candidates:
        payload = _assistant_payload_from_candidate(candidate)
        if payload.full_text:
            selected_payload = payload
            break

    if selected_payload is None:
        for candidate in reasoning_candidates:
            payload = _assistant_payload_from_candidate(candidate)
            if payload.full_text:
                selected_payload = payload
                break

    if selected_payload is None or not selected_payload.full_text:
        raise ValueError(
            "DeepInfra response does not contain a usable assistant text payload. "
            f"choice_keys={sorted(choice_payload.keys())}"
        )

    if not selected_payload.thinking_text:
        extra_thinking = []
        for candidate in reasoning_candidates:
            payload = _assistant_payload_from_candidate(candidate)
            if payload.thinking_text:
                extra_thinking.append(payload.thinking_text)
        if extra_thinking:
            thinking_text = "\n\n".join(part for part in extra_thinking if part.strip())
            full_text = selected_payload.full_text
            if thinking_text and "<think" not in full_text.lower():
                full_text = _combine_thinking_and_final_text(
                    thinking_text=thinking_text,
                    final_text=selected_payload.final_text or selected_payload.full_text,
                )
            selected_payload = AssistantTextPayload(
                full_text=full_text,
                final_text=selected_payload.final_text or _strip_thinking_blocks(full_text),
                thinking_text=thinking_text,
            )

    return selected_payload


def _assistant_payload_from_candidate(candidate: Any) -> AssistantTextPayload:
    if isinstance(candidate, str):
        if not candidate:
            return AssistantTextPayload(full_text="", final_text="", thinking_text="")
        thinking_parts = [part.strip() for part in _THINK_BLOCK_PATTERN.findall(candidate) if part.strip()]
        thinking_text = "\n\n".join(thinking_parts)
        final_text = _strip_thinking_blocks(candidate) if thinking_parts else candidate
        return AssistantTextPayload(
            full_text=candidate,
            final_text=final_text if thinking_parts else candidate,
            thinking_text=thinking_text,
        )

    segments = _extract_text_segments(candidate)
    if not segments:
        return AssistantTextPayload(full_text="", final_text="", thinking_text="")
    thinking_parts = [text for kind, text in segments if kind == "thinking" and text.strip()]
    final_parts = [text for kind, text in segments if kind == "text" and text.strip()]
    thinking_text = "\n\n".join(part.strip() for part in thinking_parts if part.strip())
    final_text = "\n".join(part.rstrip() for part in final_parts if part.strip())
    full_text = _combine_thinking_and_final_text(
        thinking_text=thinking_text,
        final_text=final_text,
    )
    return AssistantTextPayload(
        full_text=full_text.strip(),
        final_text=final_text.strip(),
        thinking_text=thinking_text.strip(),
    )


def _extract_text_segments(candidate: Any) -> list[tuple[str, str]]:
    if isinstance(candidate, str):
        payload = _assistant_payload_from_candidate(candidate)
        segments: list[tuple[str, str]] = []
        if payload.thinking_text:
            segments.append(("thinking", payload.thinking_text))
        if payload.final_text:
            segments.append(("text", payload.final_text))
        elif payload.full_text:
            segments.append(("text", payload.full_text))
        return segments

    if isinstance(candidate, dict):
        item_type = str(candidate.get("type") or "").lower()
        kind = "thinking" if any(marker in item_type for marker in ("reason", "analysis", "thought")) else None
        for key in ("text", "content", "value", "output_text", "parts", "items", "delta", "data"):
            nested_segments = _extract_text_segments(candidate.get(key))
            if not nested_segments:
                continue
            if kind is None:
                return nested_segments
            return [(kind, text) for _, text in nested_segments if text.strip()]
        return []

    if isinstance(candidate, list):
        collected_segments: list[tuple[str, str]] = []
        for item in candidate:
            collected_segments.extend(_extract_text_segments(item))
        return collected_segments

    return []


def _combine_thinking_and_final_text(*, thinking_text: str, final_text: str) -> str:
    parts: list[str] = []
    if thinking_text.strip():
        parts.append(f"<think>\n{thinking_text.strip()}\n</think>")
    if final_text.strip():
        parts.append(final_text.strip())
    return "\n\n".join(parts).strip()


def _strip_thinking_blocks(text: str) -> str:
    return _THINK_BLOCK_PATTERN.sub("", text or "").strip()


def _enrich_response_payload_with_assistant_content(
    response_payload: dict[str, Any],
    assistant_payload: AssistantTextPayload,
) -> dict[str, Any]:
    enriched = dict(response_payload)
    enriched["_assistant_content"] = assistant_payload.full_text
    enriched["_assistant_final_text"] = assistant_payload.final_text
    enriched["_assistant_thinking_text"] = assistant_payload.thinking_text
    enriched["_assistant_has_thinking"] = assistant_payload.has_thinking
    return enriched


def _extract_text_from_candidate(candidate: Any) -> str:
    return _assistant_payload_from_candidate(candidate).full_text


def _ensure_dict(value: Any) -> dict[str, Any]:
    return cast(dict[str, Any], value) if isinstance(value, dict) else {}



def _is_retryable_error(exc: Exception) -> bool:
    if isinstance(exc, _RetryableDeepInfraError):
        return True
    return isinstance(exc, (httpx.TimeoutException, httpx.TransportError))


def _is_http_429_error(exc: Exception) -> bool:
    return isinstance(exc, _RetryableDeepInfraError) and exc.status_code == 429


def _extract_retry_after_seconds(exc: Exception) -> float | None:
    if not isinstance(exc, _RetryableDeepInfraError):
        return None
    value = exc.retry_after_seconds
    if value is None:
        return None
    return max(0.0, value)



def _format_chunk_label(context: dict[str, Any]) -> str | None:
    chunk_index = context.get("chunk_index")
    if chunk_index is None:
        return None
    total_chunks = context.get("total_chunks")
    if total_chunks is None:
        return str(chunk_index)
    return f"{chunk_index}/{total_chunks}"



def _supports_streaming(client: Any) -> bool:
    stream_method = getattr(client, "stream", None)
    return callable(stream_method)



def _wrap_http_status_error(exc: httpx.HTTPStatusError) -> Exception:
    detail = _safe_response_text(exc.response)
    status_code = exc.response.status_code
    message = f"DeepInfra HTTP {status_code}: {detail}"
    if status_code in _RETRYABLE_HTTP_STATUS_CODES:
        return _RetryableDeepInfraError(
            message,
            status_code=status_code,
            retry_after_seconds=_parse_retry_after_header(exc.response),
        )
    return RuntimeError(message)


def _safe_response_text(response: httpx.Response) -> str:
    try:
        response.read()
    except Exception:
        pass
    try:
        return response.text[:1000]
    except Exception:
        return "<response body unavailable>"


def _parse_retry_after_header(response: httpx.Response) -> float | None:
    header_value = response.headers.get("Retry-After")
    if header_value is None:
        return None
    raw_value = header_value.strip()
    if not raw_value:
        return None
    try:
        return max(0.0, float(raw_value))
    except ValueError:
        pass
    try:
        retry_after_datetime = parsedate_to_datetime(raw_value)
    except (TypeError, ValueError):
        return None

    if retry_after_datetime.tzinfo is None:
        retry_after_datetime = retry_after_datetime.replace(tzinfo=timezone.utc)

    delta = (retry_after_datetime - datetime.now(timezone.utc)).total_seconds()
    return max(0.0, delta)
