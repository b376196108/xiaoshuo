from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

from _common import (
    chapter_id,
    dump_json,
    get_repo_root,
    iso_today,
    parse_chapter_num_from_filename,
    read_text,
    setup_logger,
)


def _extract_first_json_object(text: str) -> dict[str, Any] | None:
    code_blocks = re.findall(
        r"```json\\s*(\\{.*?\\})\\s*```", text, flags=re.DOTALL | re.IGNORECASE
    )
    for block in code_blocks:
        try:
            obj = json.loads(block)
        except Exception:  # noqa: BLE001
            continue
        if isinstance(obj, dict):
            return obj
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description="Extract state/state_patch.json (delta only).")
    parser.add_argument(
        "--date", default=iso_today(), help="Run date (YYYY-MM-DD), used for logging only."
    )
    parser.add_argument("--chapter", type=int, default=None, help="Chapter number (NNN).")
    parser.add_argument("--chapter-file", default=None, help="Path to manuscript/chNNN.md.")
    parser.add_argument(
        "--summary-file", default=None, help="Path to recap/chapter_summaries/chNNN.md."
    )
    parser.add_argument(
        "--output", default=None, help="Output patch path (default: state/state_patch.json)."
    )
    parser.add_argument("--verbose", action="store_true", help="Verbose logging.")
    args = parser.parse_args()

    root = get_repo_root()
    run_dir = root / "runs" / args.date
    run_dir.mkdir(parents=True, exist_ok=True)
    log = setup_logger(
        "extract_state_patch",
        log_file=run_dir / "extract_state_patch.log",
        verbose=args.verbose,
    )

    if args.chapter_file:
        chapter_path = Path(args.chapter_file)
    else:
        if args.chapter is None:
            log.error("Need --chapter or --chapter-file.")
            return 2
        chapter_path = root / "manuscript" / f"{chapter_id(args.chapter)}.md"

    if args.summary_file:
        summary_path = Path(args.summary_file)
    else:
        if args.chapter is None:
            n = parse_chapter_num_from_filename(chapter_path.name)
            if n is None:
                log.error("Cannot infer chapter number from: %s", chapter_path.name)
                return 2
            args.chapter = n
        summary_path = root / "recap" / "chapter_summaries" / f"{chapter_id(args.chapter)}.md"

    patch_out = Path(args.output) if args.output else (root / "state" / "state_patch.json")

    if args.chapter is None:
        n = parse_chapter_num_from_filename(chapter_path.name)
        if n is None:
            log.error("Cannot infer chapter number from: %s", chapter_path.name)
            return 2
        args.chapter = n

    patch: dict[str, Any] = {"meta": {"current_chapter": args.chapter}}

    summary_text = read_text(summary_path) if summary_path.exists() else ""
    extracted = _extract_first_json_object(summary_text)
    if extracted:
        patch.update(extracted)
        log.info("Merged extracted JSON object from summary into patch.")
    else:
        log.info(
            "No JSON code block found in summary; wrote minimal patch (meta.current_chapter only)."
        )

    dump_json(patch_out, patch, backup=True)
    log.info("wrote patch: %s", patch_out.as_posix())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

