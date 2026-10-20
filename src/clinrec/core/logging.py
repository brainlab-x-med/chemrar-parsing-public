from __future__ import annotations

import json
import logging
import sys
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

DEFAULT_LOGGER_NAME = "clinrec"
LOG_FORMAT = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

try:  # pragma: no cover - optional dependency
    from tqdm.auto import tqdm as _tqdm
except Exception:  # noqa: BLE001
    _tqdm = None


@dataclass(slots=True)
class MonotonicTimer:
    started_at: float

    @classmethod
    def start(cls) -> "MonotonicTimer":
        return cls(started_at=time.perf_counter())

    def elapsed_seconds(self) -> float:
        return max(0.0, time.perf_counter() - self.started_at)


@dataclass(slots=True)
class ProgressMetrics:
    total: int
    completed: int = 0
    elapsed_seconds_total: float = 0.0

    def observe(self, duration_seconds: float) -> dict[str, float | int | None]:
        self.completed += 1
        self.elapsed_seconds_total += max(duration_seconds, 0.0)
        avg_chunk_time = (
            self.elapsed_seconds_total / self.completed if self.completed > 0 else 0.0
        )
        speed = (
            self.completed / self.elapsed_seconds_total
            if self.elapsed_seconds_total > 0
            else 0.0
        )
        remaining = max(self.total - self.completed, 0)
        eta_seconds = int(round(remaining * avg_chunk_time)) if self.completed > 0 else None
        return {
            "completed": self.completed,
            "total": self.total,
            "remaining": remaining,
            "avg_seconds": avg_chunk_time,
            "speed_per_second": speed,
            "eta_seconds": eta_seconds,
        }


class NullProgressBar:
    def update(self, _: int = 1) -> None:
        return None

    def close(self) -> None:
        return None


def configure_logging(
    *,
    level: str | int = "INFO",
    logs_dir: Path | None = None,
    logger_name: str = DEFAULT_LOGGER_NAME,
) -> logging.Logger:
    numeric_level = _coerce_log_level(level)
    root_logger = logging.getLogger()
    root_logger.setLevel(numeric_level)

    formatter = logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT)

    for handler in list(root_logger.handlers):
        root_logger.removeHandler(handler)
        try:
            handler.close()
        except Exception:  # noqa: BLE001
            pass

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(numeric_level)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    if logs_dir is not None:
        logs_dir.mkdir(parents=True, exist_ok=True)
        log_path = logs_dir / f"clinrec_pipeline_{utc_now_compact()}.log"
        file_handler = logging.FileHandler(log_path, encoding="utf-8")
        file_handler.setLevel(numeric_level)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)

    logger = logging.getLogger(logger_name)
    logger.debug("Logging is configured. level=%s", logging.getLevelName(numeric_level))
    return logger


def get_logger(name: str | None = None) -> logging.Logger:
    if name is None:
        return logging.getLogger(DEFAULT_LOGGER_NAME)
    return logging.getLogger(name)


def log_kv_event(
    logger: logging.Logger,
    message: str,
    *,
    level: int = logging.INFO,
    **fields: Any,
) -> None:
    suffix = format_kv_pairs(**fields)
    if suffix:
        logger.log(level, "%s %s", message, suffix)
        return
    logger.log(level, "%s", message)


def format_kv_pairs(**fields: Any) -> str:
    parts: list[str] = []
    for key, value in fields.items():
        if value is None:
            continue
        parts.append(f"{key}={_format_log_value(value)}")
    return " ".join(parts)


def build_progress_bar(*, total: int, enabled: bool, description: str = "documents"):
    if not enabled or total <= 0 or _tqdm is None:
        return NullProgressBar()
    return _tqdm(total=total, desc=description, unit="doc", leave=True)


def utc_now_compact() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _coerce_log_level(level: str | int) -> int:
    if isinstance(level, int):
        return level

    normalized = level.strip().upper()
    numeric_level = getattr(logging, normalized, None)
    if not isinstance(numeric_level, int):
        raise ValueError(f"Unsupported log level: {level}")
    return numeric_level


def _format_log_value(value: Any) -> str:
    if isinstance(value, bool):
        return str(value).lower()
    if isinstance(value, float):
        return f"{value:.2f}".rstrip("0").rstrip(".") or "0"
    if isinstance(value, Path):
        return value.as_posix()
    if isinstance(value, datetime):
        return value.isoformat()
    if isinstance(value, (list, tuple, set)):
        return json.dumps(list(value), ensure_ascii=False, separators=(",", ":"))
    if isinstance(value, dict):
        return json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    text = str(value).replace("\n", " ").strip()
    return text
