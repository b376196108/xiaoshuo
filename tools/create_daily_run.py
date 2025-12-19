from __future__ import annotations

import argparse

from _common import (
    chapter_id,
    get_repo_root,
    infer_next_chapter_num,
    iso_today,
    safe_write_text,
    setup_logger,
)


def _brief_template(*, run_date: str, chapter: str, words: int | None) -> str:
    words_value = str(words) if words is not None else "TBD"
    return (
        f"# Daily Brief — {run_date}\n\n"
        "只需填写以下三项（其余可留空）：\n"
        "- chapter_id（如无特殊需要可保持默认）\n"
        "- target_words\n"
        "- chapter_goals（3–6 条）\n\n"
        "---\n\n"
        f"chapter_id: {chapter}\n"
        f"target_words: {words_value}\n"
        "chapter_goals:\n"
        "- TBD\n"
        "- TBD\n"
        "- TBD\n\n"
        "notes:\n"
        "- TBD\n"
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Create runs/YYYY-MM-DD/ and brief.md template."
    )
    parser.add_argument(
        "--date", default=iso_today(), help="Run date (YYYY-MM-DD). Default: today."
    )
    parser.add_argument(
        "--chapter",
        type=int,
        default=None,
        help="Chapter number (NNN). If omitted, auto-infer next.",
    )
    parser.add_argument("--words", type=int, default=None, help="Target words.")
    parser.add_argument("--verbose", action="store_true", help="Verbose logging.")
    args = parser.parse_args()

    root = get_repo_root()
    run_dir = root / "runs" / args.date
    run_dir.mkdir(parents=True, exist_ok=True)
    log = setup_logger(
        "create_daily_run",
        log_file=run_dir / "create_daily_run.log",
        verbose=args.verbose,
    )

    chapter_num = (
        args.chapter
        if args.chapter is not None
        else infer_next_chapter_num(root / "manuscript")
    )
    chap_id = chapter_id(chapter_num)

    brief_path = run_dir / "brief.md"
    if brief_path.exists():
        log.info("brief already exists: %s", brief_path.as_posix())
    else:
        safe_write_text(
            brief_path,
            _brief_template(run_date=args.date, chapter=chap_id, words=args.words),
            backup=False,
        )
        log.info("created brief: %s", brief_path.as_posix())

    log.info("run_dir=%s", run_dir.as_posix())
    log.info("chapter_id=%s", chap_id)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

