from __future__ import annotations

import argparse

from _common import (
    chapter_id,
    load_json,
    normalize_chapter_id,
    parse_chapter_num_from_id,
    read_project_scale,
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
        "- target_words（正文字符数>=3000，推荐3200）\n"
        "- chapter_goals（3–6 条）\n\n"
        "---\n\n"
        f"chapter_id: {chapter}\n"
        f"target_words: {words_value}\n"
        "chapter_goals:\n"
        "- TBD\n"
        "- TBD\n"
        "- TBD\n\n"
        "notes:\n"
        "- 正文字符数>=3000，推荐 target_words=3200\n"
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
        type=str,
        default=None,
        help="Chapter id (chNNN) or number (NNN). If omitted, auto-infer next.",
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

    if args.chapter is not None:
        chap_id = normalize_chapter_id(args.chapter)
        chapter_num = parse_chapter_num_from_id(chap_id)
    else:
        chapter_num = infer_next_chapter_num(root / "manuscript")
        chap_id = chapter_id(chapter_num)

    if chapter_num is None:
        log.error("Invalid --chapter: %s", args.chapter)
        return 2

    default_words = 3200
    try:
        project_brief = load_json(root / "inputs" / "project_brief.json")
        _, words_per_chapter = read_project_scale(project_brief)
        if words_per_chapter is not None:
            default_words = words_per_chapter
    except Exception as e:  # noqa: BLE001
        log.warning("Failed to read inputs/project_brief.json for defaults: %s", e)

    default_words = max(3000, default_words)
    words = args.words if args.words is not None else default_words
    if words < 3000:
        words = 3200

    brief_path = run_dir / "brief.md"
    if brief_path.exists():
        log.info("brief already exists: %s", brief_path.as_posix())
    else:
        safe_write_text(
            brief_path,
            _brief_template(run_date=args.date, chapter=chap_id, words=words),
            backup=False,
        )
        log.info("created brief: %s", brief_path.as_posix())

    log.info("run_dir=%s", run_dir.as_posix())
    log.info("chapter_id=%s", chap_id)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
