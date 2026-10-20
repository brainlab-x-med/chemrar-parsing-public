#!/usr/bin/env python3
"""Download clinical recommendation HTMLs from a clinrec API.

Reads document_ids.csv, fetches each document, assembles a full HTML file
from its sections, and saves to api-cached/{id}.html.

The API URL is a template with an {id} placeholder. Pass it with --api-url
or set CLINREC_API_URL. The API must return JSON of the form
{"name": ..., "obj": {"sections": [{"title": ..., "content": <html>}, ...]}}.

Usage:
    CLINREC_API_URL="https://example.org/api?id={id}" \
    python scripts/download_htmls.py --csv document_ids.csv --out api-cached
"""
from __future__ import annotations

import argparse
import csv
import html as html_lib
import os
import sys
import time
from pathlib import Path
from typing import Any

import httpx

API_URL_ENV = "CLINREC_API_URL"


def fetch_clinrec(api_url: str, clinrec_id: str, client: httpx.Client) -> dict[str, Any]:
    url = api_url.replace("{id}", clinrec_id)
    r = client.get(url)
    r.raise_for_status()
    return r.json()


def get_sections(doc: dict[str, Any]) -> list[dict[str, Any]]:
    obj = doc.get("obj") or {}
    sections = obj.get("sections") or []
    return [s for s in sections if isinstance(s, dict)]


def build_html(doc: dict[str, Any]) -> str:
    name = html_lib.escape(doc.get("name") or "")
    sections = get_sections(doc)
    parts: list[str] = [
        "<!DOCTYPE html>",
        "<html>",
        f"<head><meta charset='utf-8'><title>{name}</title></head>",
        "<body>",
        f"<h1>{name}</h1>",
    ]
    for section in sections:
        title = section.get("title") or ""
        content = section.get("content") or ""
        if title:
            parts.append(f"<h2>{html_lib.escape(title)}</h2>")
        if content:
            parts.append(content)
    parts += ["</body>", "</html>"]
    return "\n".join(parts)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--csv", required=True, help="Path to document_ids.csv")
    parser.add_argument(
        "--api-url",
        default=os.environ.get(API_URL_ENV),
        help=f"API URL template with an {{id}} placeholder (default: ${API_URL_ENV})",
    )
    parser.add_argument("--out", default="api-cached", help="Output directory")
    parser.add_argument("--timeout", type=float, default=30.0)
    parser.add_argument("--delay", type=float, default=0.3, help="Seconds between requests")
    parser.add_argument("--skip-existing", action="store_true", default=True)
    args = parser.parse_args()
    if not args.api_url:
        parser.error(f"set --api-url or {API_URL_ENV}")
    if "{id}" not in args.api_url:
        parser.error("the API URL must contain an {id} placeholder")

    csv_path = Path(args.csv)
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    with open(csv_path, newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))

    print(f"{len(rows)} documents to process → {out_dir}/", flush=True)
    ok = skipped = failed = 0

    with httpx.Client(timeout=args.timeout) as client:
        for row in rows:
            doc_id = row["id"].strip()
            out_path = out_dir / f"{doc_id}.html"

            if args.skip_existing and out_path.exists():
                skipped += 1
                print(f"  skip  {doc_id}", flush=True)
                continue

            try:
                doc = fetch_clinrec(args.api_url, doc_id, client)
                html = build_html(doc)
                out_path.write_text(html, encoding="utf-8")
                ok += 1
                print(f"  ok    {doc_id}  ({len(html):,} chars)", flush=True)
            except Exception as exc:
                failed += 1
                print(f"  FAIL  {doc_id}  {exc}", file=sys.stderr, flush=True)

            time.sleep(args.delay)

    print(f"\ndone: {ok} ok, {skipped} skipped, {failed} failed")


if __name__ == "__main__":
    main()
