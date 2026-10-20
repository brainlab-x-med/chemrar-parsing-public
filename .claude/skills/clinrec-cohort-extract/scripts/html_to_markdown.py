"""
html_to_markdown.py — convert a clinrec HTML doc to Markdown, transcribing
embedded images (data: URIs) to text via a vision LLM.

Why this exists: the cohort-first extraction (BRA-92) reads Markdown, not raw
HTML. Tables and algorithm flowcharts in clinrec docs are often *images*
(Приложение Б), so they must be transcribed to text or the cohorts are lost.

Output:
  <out_dir>/<doc_id>.md                  full markdown, images inlined as text
  <out_dir>/<doc_id>.images/<hash>.json  per-image transcription cache (reused)

Usage:
  uv run python .claude/skills/clinrec-cohort-extract/scripts/html_to_markdown.py \
      api-cached/475_3.html --out-dir output-cohort

Image src types handled:
  - data:image/...;base64,...  -> transcribed via vision model
  - file:///...                -> skipped (external, not embedded), marker left
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

from bs4 import BeautifulSoup, NavigableString, Tag

# Reuse project LLM client + settings.
sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "src"))
from clinrec.core.settings import ClinRecSettings  # noqa: E402
from clinrec.extraction.client import DeepInfraChatClient  # noqa: E402

HEADING_TAGS = {"h1", "h2", "h3", "h4", "h5", "h6"}
VISION_MODEL = "google/gemini-3.1-flash-lite"

TRANSCRIBE_PROMPT = """Перед тобой изображение из российской онкологической клинической рекомендации.
Это может быть таблица режимов терапии, блок-схема (алгоритм ведения пациента) или текст.

Перепиши ВСЁ содержимое изображения в Markdown максимально точно:
- таблицы -> Markdown-таблицы (сохрани все столбцы: когорта/стадия, схема, препараты, дозы, дни, циклы, УУР, УДД);
- блок-схемы -> вложенный список «когорта -> вариант лечения», сохрани стрелки/ветвления;
- сохрани все цифры, дозировки (мг/м², AUC, мг/кг), TNM, ECOG, PD-L1, названия препаратов и схем.

Только содержимое изображения в Markdown. Без вступлений и комментариев."""


def _img_to_text(client: DeepInfraChatClient, data_uri: str, cache_path: Path) -> str:
    if cache_path.exists():
        return json.loads(cache_path.read_text(encoding="utf-8"))["text"]
    try:
        result = client.create_completion(
            model_id=VISION_MODEL,
            messages=[{
                "role": "user",
                "content": [
                    {"type": "text", "text": TRANSCRIBE_PROMPT},
                    {"type": "image_url", "image_url": {"url": data_uri}},
                ],
            }],
            max_completion_tokens=3000,
            temperature=0.0,
        )
        text = result.content.strip()
    except Exception as e:  # noqa: BLE001
        text = f"<!-- image transcription failed: {e} -->"
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    cache_path.write_text(json.dumps({"text": text}, ensure_ascii=False), encoding="utf-8")
    return text


def _table_to_md(table: Tag) -> str:
    rows = []
    for tr in table.find_all("tr"):
        cells = tr.find_all(["td", "th"])
        if not cells:
            continue
        rows.append([" ".join(c.get_text(" ", strip=True).split()) for c in cells])
    if not rows:
        return ""
    width = max(len(r) for r in rows)
    rows = [r + [""] * (width - len(r)) for r in rows]
    out = ["| " + " | ".join(rows[0]) + " |", "| " + " | ".join(["---"] * width) + " |"]
    for r in rows[1:]:
        out.append("| " + " | ".join(c.replace("|", "\\|") for c in r) + " |")
    return "\n".join(out)


BLOCK_TAGS = {
    "p", "div", "table", "tbody", "thead", "tr", "td", "th",
    "ul", "ol", "li", "section", "img", *HEADING_TAGS,
}
INLINE_TAGS = {"strong", "b", "em", "i", "u", "span", "a", "sup", "sub"}


def _shallow_inline(node: Tag) -> str:
    """Inline text of a node, stopping at block-level descendants.

    Word-export HTML often has a malformed unclosed heading wrapping the whole
    document; a naive recursive get_text would pull the entire doc into one
    heading line. This collects only the heading's own inline text.
    """
    parts: list[str] = []
    for child in node.children:
        if isinstance(child, NavigableString):
            parts.append(str(child))
        elif isinstance(child, Tag) and child.name in INLINE_TAGS:
            t = _shallow_inline(child)
            if t.strip():  # skip empty <strong>/<em> that would litter ** / *
                if child.name in ("strong", "b"):
                    t = f"**{t}**"
                elif child.name in ("em", "i"):
                    t = f"*{t}*"
            parts.append(t)
        # block-level children are skipped here; walk() renders them
    return " ".join(" ".join(parts).split())


def _inline(node: Tag) -> str:
    parts: list[str] = []
    for child in node.children:
        if isinstance(child, NavigableString):
            parts.append(str(child))
        elif isinstance(child, Tag):
            inner = _inline(child)
            if child.name in ("strong", "b"):
                parts.append(f"**{inner}**" if inner.strip() else "")
            elif child.name in ("em", "i"):
                parts.append(f"*{inner}*" if inner.strip() else "")
            elif child.name == "br":
                parts.append("\n")
            else:
                parts.append(inner)
    return " ".join(" ".join(parts).split())


def convert(html_path: Path, out_dir: Path) -> Path:
    doc_id = html_path.stem
    settings = ClinRecSettings(
        _env_file=str(Path(__file__).resolve().parents[4] / ".env"),
        provider="openrouter",
    )
    client = DeepInfraChatClient.from_settings(settings)
    img_cache = out_dir / f"{doc_id}.images"

    soup = BeautifulSoup(html_path.read_text(encoding="utf-8"), "html.parser")
    body = soup.body or soup
    out: list[str] = []
    section = "0"  # running section number from numbered headings
    img_idx = 0

    def handle_img(el: Tag) -> None:
        nonlocal img_idx
        src = el.get("src", "")
        if src.startswith("data:image/"):
            h = hashlib.sha1(src.encode()).hexdigest()[:16]
            text = _img_to_text(client, src, img_cache / f"{h}.json")
            out.append(
                f"\n<!-- image {img_idx} (section {section}) transcription start -->\n"
                f"{text}\n"
                f"<!-- image {img_idx} transcription end -->\n"
            )
        else:
            out.append(f"\n<!-- image {img_idx}: external src skipped ({src[:60]}) -->\n")
        img_idx += 1

    def walk(node: Tag) -> None:
        nonlocal section, img_idx
        for el in node.children:
            if isinstance(el, NavigableString):
                continue
            if not isinstance(el, Tag):
                continue
            name = el.name
            if name in HEADING_TAGS:
                txt = _shallow_inline(el)
                m = re.match(r"^(\d+(?:\.\d+)*)", txt.strip())
                if m:
                    section = m.group(1)
                level = "#" * int(name[1])
                if txt:
                    out.append(f"\n{level} {txt}\n")
                # Malformed Word headings wrap block content — render it.
                if any(isinstance(c, Tag) and c.name in BLOCK_TAGS for c in el.children):
                    walk(el)
            elif name == "table":
                # MS-Word HTML wraps the whole doc in layout tables. A table
                # that contains a nested table is a layout wrapper -> recurse;
                # only leaf tables are real data tables worth flattening.
                if el.find("table") is not None:
                    walk(el)
                else:
                    md = _table_to_md(el)
                    if md:
                        out.append(f"\n<!-- section {section} -->\n{md}\n")
            elif name in ("p", "li"):
                txt = _inline(el)
                if txt:
                    prefix = "- " if name == "li" else ""
                    out.append(f"{prefix}{txt}")
                for img in el.find_all("img"):
                    handle_img(img)
            elif name == "img":
                handle_img(el)
            elif name in ("div", "ul", "ol", "tbody", "thead", "tr", "td", "section"):
                walk(el)

    walk(body)
    out_dir.mkdir(parents=True, exist_ok=True)
    md_path = out_dir / f"{doc_id}.md"
    text = "\n".join(out)
    # drop lines that are only leftover emphasis markers / whitespace
    text = re.sub(r"(?m)^[ \t]*[*_]+[ \t]*$", "", text)
    # squeeze 3+ blank lines to one
    text = re.sub(r"\n{3,}", "\n\n", text)
    md_path.write_text(text.strip() + "\n", encoding="utf-8")
    # Phase 1 STARTS the per-doc pipeline log fresh (mode "w"): the log then
    # contains only this run's extraction steps — Phase-1 line + Phase-2
    # provenance (via audit.py). No agent/skill-dev noise, scoped to one doc.
    log = out_dir / f"{doc_id}.extraction.log"
    from datetime import datetime
    with log.open("w", encoding="utf-8") as fh:
        fh.write(
            f"[{datetime.now():%F %T}] phase1 html->md :: {html_path} "
            f"-> {md_path} ({len(text.splitlines())} lines, {img_idx} images)\n"
        )
    print(f"  {doc_id}: {img_idx} images, markdown -> {md_path}")
    return md_path


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("html", nargs="+", help="HTML file(s) under api-cached/")
    ap.add_argument("--out-dir", default="output-cohort")
    args = ap.parse_args()
    out_dir = Path(args.out_dir)
    for h in args.html:
        convert(Path(h), out_dir)


if __name__ == "__main__":
    main()
