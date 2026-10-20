from pathlib import Path
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

DEFAULT_DEEPINFRA_OPENAI_BASE_URL = "https://api.deepinfra.com/v1/openai"
DEFAULT_OPENAI_BASE_URL = "https://api.openai.com/v1"
DEFAULT_OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

DEFAULT_REASONING_MODEL_ID = "google/gemini-2.5-pro"
DEFAULT_REASONING_MODEL_FALLBACK_ID = "Qwen/Qwen3.5-397B-A17B"
DEFAULT_VISION_MODEL_ID = "Qwen/Qwen3-VL-235B-A22B-Instruct"
DEFAULT_VISION_MODEL_FALLBACK_ID = "zai-org/GLM-4.6V"

DEFAULT_OPENAI_REASONING_MODEL_ID = "gpt-5.4"
DEFAULT_OPENAI_VISION_MODEL_ID = "gpt-5.4-mini"

DEFAULT_PAGE_MARKER_TEMPLATE = "<!-- page: {page_number} -->"


class RetrySettings(BaseModel):
    """Low-level retry policy kept internal to config defaults."""

    model_config = ConfigDict(extra="forbid")

    max_attempts: int = Field(default=4, ge=1)
    initial_backoff_seconds: float = Field(default=1.0, ge=0.0)
    backoff_multiplier: float = Field(default=2.0, ge=1.0)
    max_backoff_seconds: float = Field(default=8.0, ge=0.0)
    jitter_seconds: float = Field(default=0.25, ge=0.0)


class RateLimitSettings(BaseModel):
    """Client-side rate-limit hardening for DeepInfra calls."""

    model_config = ConfigDict(extra="forbid")

    enabled: bool = True
    requests_per_minute: int = Field(default=12, ge=1)
    max_wait_seconds: float = Field(default=1200.0, ge=0.0)
    default_retry_after_seconds: float = Field(default=15.0, ge=0.0)
    max_retry_after_seconds: float = Field(default=180.0, ge=0.0)


class TimeoutSettings(BaseModel):
    """Timeout defaults for future API and file-processing modules."""

    model_config = ConfigDict(extra="forbid")

    connect_seconds: float = Field(default=30.0, ge=0.0)
    read_seconds: float = Field(default=90.0, ge=0.0)
    total_seconds: float = Field(default=150.0, ge=0.0)


class PipelineDefaults(BaseModel):
    """Non-user-facing defaults.

    These values intentionally live in config so that the future CLI can keep a
    minimal surface and ordinary runs only require input_dir and output_dir.
    """

    model_config = ConfigDict(extra="forbid")

    pdf_glob: str = "*.pdf"
    html_glob: str = "*.html"
    markdown_dirname: str = "markdown"
    augmented_markdown_dirname: str = "markdown_augmented"
    images_dirname: str = "images"
    manifests_dirname: str = "manifests"
    json_dirname: str = "json"
    text_preparation_dirname: str = "text_preparation"
    trees_dirname: str = "trees"
    logs_dirname: str = "logs"
    extracted_images_subdir: str = "embedded"
    image_format: str = "png"
    page_marker_template: str = DEFAULT_PAGE_MARKER_TEMPLATE
    max_image_size_bytes: int = Field(default=8 * 1024 * 1024, ge=1)
    page_text_excerpt_characters: int = Field(default=1000, ge=1)
    emit_page_manifest: bool = True
    embed_image_data_uri_in_requests: bool = True


class DeepInfraModelIds(BaseModel):
    """Canonical default model IDs used by the project."""

    model_config = ConfigDict(extra="forbid")

    reasoning_default: str = DEFAULT_REASONING_MODEL_ID
    reasoning_fallback: str = DEFAULT_REASONING_MODEL_FALLBACK_ID
    vision_default: str = DEFAULT_VISION_MODEL_ID
    vision_fallback: str = DEFAULT_VISION_MODEL_FALLBACK_ID




class WholeDocumentSettings(BaseModel):
    """Whole-document mode controls.

    These knobs only affect text extraction when
    ``text_extraction.document_loading_mode="whole_document"``. They are kept
    separate on purpose so chunk-only fields do not look active for this mode.
    """

    model_config = ConfigDict(extra="forbid")

    glossary_max_entries: int = Field(default=20, ge=0)
    glossary_max_characters: int = Field(default=2500, ge=0)
    max_input_characters: int | None = Field(default=1000000, ge=1)
    fail_on_input_limit_exceeded: bool = False


class TextExtractionSettings(BaseModel):
    """Tunable text-extraction hyperparameters and acceptance guards."""

    model_config = ConfigDict(extra="forbid")

    document_loading_mode: Literal["chunks", "whole_document"] = "whole_document"

    # Chunk-mode controls. They are ignored when document_loading_mode=whole_document.
    target_chunk_characters: int = Field(default=8000, ge=1)
    max_chunk_characters: int = Field(default=10000, ge=1)
    chunk_overlap_characters: int = Field(default=1000, ge=0)

    # Shared LLM controls. They affect both chunk and whole-document modes.
    temperature: float = Field(default=0.3, ge=0.0, le=2.0)
    max_completion_tokens: int = Field(default=60000, ge=1)
    transport_contract_mode: Literal["compact", "canonical"] = "compact"
    use_vision_augmented_markdown: bool = True
    include_image_warnings_in_augmented_markdown: bool = False
    max_image_evidence_lines_per_insight: int = Field(default=6, ge=0)
    enable_document_glossary: bool = False
    glossary_max_entries_per_chunk: int = Field(default=20, ge=0)
    glossary_max_characters_per_chunk: int = Field(default=1000, ge=0)
    glossary_max_definition_characters: int = Field(default=200, ge=16)
    whole_document: WholeDocumentSettings = Field(default_factory=WholeDocumentSettings)

    enable_field_fixup_pass: bool = False
    extraction_attempts: int = Field(default=1, ge=1, le=10)

    drop_regimens_without_any_anchor: bool = True
    require_evidence_for_accepted_regimens: bool = True
    verify_evidence_quotes_present_in_chunk: bool = True
    min_evidence_quotes_per_regimen: int = Field(default=1, ge=0)
    anchor_gate_min_signals: int = Field(default=2, ge=1, le=3)
    merge_min_score: int = Field(default=7, ge=1)
    merge_require_name_or_source_match: bool = True
    evidence_fallback_max_items_per_regimen: int = Field(default=2, ge=0)


class VisionExtractionSettings(BaseModel):
    """Tunable vision-extraction hyperparameters and acceptance guards."""

    model_config = ConfigDict(extra="forbid")

    temperature: float = Field(default=0.3, ge=0.0, le=2.0)
    max_completion_tokens: int = Field(default=4000, ge=1)
    include_page_text_context: bool = True
    page_text_context_characters: int = Field(default=2000, ge=0)
    require_non_empty_summary: bool = True


class MergeSettings(BaseModel):
    """Tunable image-insight to regimen matching hyperparameters."""

    model_config = ConfigDict(extra="forbid")

    attach_min_score: float = Field(default=0.72, ge=0.0, le=1.0)
    attach_min_matched_weight: float = Field(default=0.35, ge=0.0)
    attach_min_margin: float = Field(default=0.10, ge=0.0, le=1.0)

    regimen_name_available_weight: float = Field(default=0.40, ge=0.0)
    regimen_name_exact_threshold: float = Field(default=0.95, ge=0.0, le=1.0)
    regimen_name_exact_weight: float = Field(default=0.40, ge=0.0)
    regimen_name_close_threshold: float = Field(default=0.80, ge=0.0, le=1.0)
    regimen_name_close_weight: float = Field(default=0.32, ge=0.0)
    regimen_name_token_overlap_threshold: float = Field(default=0.70, ge=0.0, le=1.0)
    regimen_name_token_overlap_weight: float = Field(default=0.22, ge=0.0)

    drug_set_available_weight: float = Field(default=0.25, ge=0.0)
    drug_set_exact_threshold: float = Field(default=1.0, ge=0.0, le=1.0)
    drug_set_exact_weight: float = Field(default=0.25, ge=0.0)
    drug_set_high_overlap_threshold: float = Field(default=0.66, ge=0.0, le=1.0)
    drug_set_high_overlap_weight: float = Field(default=0.20, ge=0.0)
    drug_set_partial_overlap_threshold: float = Field(default=0.40, ge=0.0, le=1.0)
    drug_set_partial_overlap_weight: float = Field(default=0.12, ge=0.0)

    disease_weight: float = Field(default=0.10, ge=0.0)
    stage_weight: float = Field(default=0.06, ge=0.0)
    clinical_situation_weight: float = Field(default=0.06, ge=0.0)
    histology_weight: float = Field(default=0.05, ge=0.0)
    line_of_therapy_weight: float = Field(default=0.08, ge=0.0)
    exact_similarity_threshold: float = Field(default=0.95, ge=0.0, le=1.0)
    close_similarity_threshold: float = Field(default=0.80, ge=0.0, le=1.0)
    close_similarity_weight_multiplier: float = Field(default=0.75, ge=0.0)

    biomarkers_available_weight: float = Field(default=0.05, ge=0.0)
    biomarkers_exact_threshold: float = Field(default=1.0, ge=0.0, le=1.0)
    biomarkers_exact_weight: float = Field(default=0.05, ge=0.0)
    biomarkers_partial_threshold: float = Field(default=0.50, ge=0.0, le=1.0)
    biomarkers_partial_weight: float = Field(default=0.03, ge=0.0)

    inclusion_available_weight: float = Field(default=0.05, ge=0.0)
    inclusion_high_overlap_threshold: float = Field(default=0.50, ge=0.0, le=1.0)
    inclusion_high_overlap_weight: float = Field(default=0.05, ge=0.0)
    inclusion_partial_overlap_threshold: float = Field(default=0.25, ge=0.0, le=1.0)
    inclusion_partial_overlap_weight: float = Field(default=0.02, ge=0.0)




class ParallelismSettings(BaseModel):
    """Concurrency limits kept configurable even when current execution is serial."""

    model_config = ConfigDict(extra="forbid")

    document_workers: int = Field(default=1, ge=1)
    vision_workers: int = Field(default=2, ge=1)
    chunk_workers: int = Field(default=3, ge=1)


class ArtifactReuseSettings(BaseModel):
    """Controls whether existing stage artifacts may be reused on restart."""

    model_config = ConfigDict(extra="forbid")

    reuse_existing_artifacts: bool = True


class CohortExtractionSettings(BaseModel):
    """Settings for the cohort-first two-pass extraction pipeline.

    When ``enabled=True`` the pipeline inserts a cohort extraction stage
    before text LLM extraction. The extracted cohorts are injected into the
    LLM prompt so each regimen is matched to a known patient population.

    ``appb_cohorts_filename`` is the name of the optional pre-extracted
    appendix-B cohorts JSON (produced by the vision stage). If the file does
    not exist the cohort extractor falls back to heuristic HTML parsing only.
    """

    model_config = ConfigDict(extra="forbid")

    enabled: bool = False
    appb_cohorts_filename: str = "{doc_id}_appb_cohorts.json"


class ClinRecSettings(BaseSettings):
    """Project settings with a thin user-facing layer.

    Intended user inputs for a normal run:
    - input_dir
    - output_dir
    - optional reasoning_model
    - optional DEEPINFRA_API_KEY from .env

    Everything else should remain defaulted unless an engineering workflow
    explicitly overrides it.
    """

    model_config = SettingsConfigDict(
        env_file=(".env", str(Path(__file__).resolve().parents[2] / ".env")),
        env_file_encoding="utf-8",
        env_prefix="CLINREC_",
        env_nested_delimiter="__",
        extra="ignore",
        validate_assignment=True,
    )

    input_dir: Path | None = None
    output_dir: Path | None = None

    provider: Literal["deepinfra", "openai", "openrouter"] = "deepinfra"

    deepinfra_api_key: str | None = Field(default=None, alias="DEEPINFRA_API_KEY")
    deepinfra_base_url: str = DEFAULT_DEEPINFRA_OPENAI_BASE_URL

    openai_api_key: str | None = Field(default=None, alias="OPENAI_API_KEY")
    openai_base_url: str = DEFAULT_OPENAI_BASE_URL

    openrouter_api_key: str | None = Field(default=None, alias="OPENROUTER_API_KEY")
    openrouter_base_url: str = DEFAULT_OPENROUTER_BASE_URL

    reasoning_model: str = DEFAULT_REASONING_MODEL_ID
    reasoning_fallback_model: str = DEFAULT_REASONING_MODEL_FALLBACK_ID
    vision_model: str = DEFAULT_VISION_MODEL_ID
    vision_fallback_model: str = DEFAULT_VISION_MODEL_FALLBACK_ID
    progress_bar_enabled: bool = False

    timeouts: TimeoutSettings = Field(default_factory=TimeoutSettings)
    retries: RetrySettings = Field(default_factory=RetrySettings)
    rate_limit: RateLimitSettings = Field(default_factory=RateLimitSettings)
    defaults: PipelineDefaults = Field(default_factory=PipelineDefaults)
    model_ids: DeepInfraModelIds = Field(default_factory=DeepInfraModelIds)
    text_extraction: TextExtractionSettings = Field(
        default_factory=TextExtractionSettings
    )
    vision_extraction: VisionExtractionSettings = Field(
        default_factory=VisionExtractionSettings
    )
    merge: MergeSettings = Field(default_factory=MergeSettings)
    parallelism: ParallelismSettings = Field(default_factory=ParallelismSettings)
    artifact_reuse: ArtifactReuseSettings = Field(default_factory=ArtifactReuseSettings)
    cohort_extraction: CohortExtractionSettings = Field(default_factory=CohortExtractionSettings)

    @property
    def effective_api_key(self) -> str | None:
        if self.provider == "openai":
            return self.openai_api_key
        if self.provider == "openrouter":
            return self.openrouter_api_key
        return self.deepinfra_api_key

    @property
    def effective_base_url(self) -> str:
        if self.provider == "openai":
            return self.openai_base_url
        if self.provider == "openrouter":
            return self.openrouter_base_url
        return self.deepinfra_base_url

    @field_validator("input_dir", "output_dir", mode="before")
    @classmethod
    def _coerce_paths(cls, value: str | Path | None) -> Path | None:
        if value is None or isinstance(value, Path):
            return value
        return Path(value)

    @field_validator(
        "reasoning_model",
        "reasoning_fallback_model",
        "vision_model",
        "vision_fallback_model",
    )
    @classmethod
    def _strip_non_empty_model_ids(cls, value: str) -> str:
        stripped = value.strip()
        if not stripped:
            raise ValueError("Model id must not be empty.")
        return stripped

    @property
    def markdown_dir(self) -> Path | None:
        if self.output_dir is None:
            return None
        return self.output_dir / self.defaults.markdown_dirname

    @property
    def augmented_markdown_dir(self) -> Path | None:
        if self.output_dir is None:
            return None
        return self.output_dir / self.defaults.augmented_markdown_dirname

    @property
    def images_dir(self) -> Path | None:
        if self.output_dir is None:
            return None
        return self.output_dir / self.defaults.images_dirname

    @property
    def manifests_dir(self) -> Path | None:
        if self.output_dir is None:
            return None
        return self.output_dir / self.defaults.manifests_dirname

    @property
    def json_dir(self) -> Path | None:
        if self.output_dir is None:
            return None
        return self.output_dir / self.defaults.json_dirname

    @property
    def trees_dir(self) -> Path | None:
        if self.output_dir is None:
            return None
        return self.output_dir / self.defaults.trees_dirname

    @property
    def text_preparation_dir(self) -> Path | None:
        if self.output_dir is None:
            return None
        return self.output_dir / self.defaults.text_preparation_dirname

    @property
    def logs_dir(self) -> Path | None:
        if self.output_dir is None:
            return None
        return self.output_dir / self.defaults.logs_dirname

    def output_subdirs(self) -> dict[str, Path]:
        if self.output_dir is None:
            return {}
        return {
            "markdown": self.markdown_dir or self.output_dir,
            "markdown_augmented": self.augmented_markdown_dir or self.output_dir,
            "images": self.images_dir or self.output_dir,
            "manifests": self.manifests_dir or self.output_dir,
            "json": self.json_dir or self.output_dir,
            "text_preparation": self.text_preparation_dir or self.output_dir,
            "trees": self.trees_dir or self.output_dir,
            "logs": self.logs_dir or self.output_dir,
        }


Settings = ClinRecSettings


def load_settings(
    input_dir: str | Path | None = None,
    output_dir: str | Path | None = None,
    reasoning_model: str | None = None,
    **overrides: Any,
) -> ClinRecSettings:
    """Load settings from .env and optional explicit overrides.

    The function intentionally exposes only the small set of inputs that should
    matter in ordinary runs. Advanced overrides remain possible for tests and
    internal engineering workflows through ``**overrides``.
    """

    payload: dict[str, Any] = dict(overrides)
    if input_dir is not None:
        payload["input_dir"] = input_dir
    if output_dir is not None:
        payload["output_dir"] = output_dir
    if reasoning_model is not None:
        payload["reasoning_model"] = reasoning_model
    return ClinRecSettings(**payload)
