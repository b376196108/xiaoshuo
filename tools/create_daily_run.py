from __future__ import annotations

import argparse
import re
from pathlib import Path

from auto_goals import generate_chapter_goals
from _common import (
    chapter_id,
    get_repo_root,
    infer_next_chapter_num,
    iso_today,
    load_json,
    normalize_chapter_id,
    parse_chapter_num_from_id,
    read_project_scale,
    read_text,
    safe_write_text,
    setup_logger,
)


def _format_goals(goals: list[str] | None) -> str:
    if not goals:
        return "- TBD\n- TBD\n- TBD"
    return "\n".join(f"- {goal}" for goal in goals)


def _brief_template(
    *, run_date: str, chapter: str, words: int | None, goals: list[str] | None
) -> str:
    words_value = str(words) if words is not None else "TBD"
    return (
        f"# Daily Brief — {run_date}\n\n"
        "只需填写以下三项（其余可留空）：\n"
        "- chapter_id（如无特殊需要可保持默认）\n"
        "- target_words（正文字符数>=3000，默认>=3200）\n"
        "- chapter_goals（3–6 条）\n\n"
        "---\n\n"
        f"chapter_id: {chapter}\n"
        f"target_words: {words_value}\n"
        "chapter_goals:\n"
        f"{_format_goals(goals)}\n\n"
        "notes:\n"
        "- 正文字符数>=3000，默认 target_words 不低于 3200\n"
        "- TBD\n"
    )


def _brief_goals_are_tbd(text: str) -> bool:
    in_goals = False
    found = False
    non_tbd = False
    for line in text.splitlines():
        if line.strip().startswith("chapter_goals"):
            in_goals = True
            continue
        if in_goals:
            if re.match(r"^\\s*notes\\s*:", line):
                break
            item = re.match(r"^\\s*[-*]\\s*(.+)$", line)
            if item:
                found = True
                value = item.group(1).strip()
                if value and value.upper() != "TBD":
                    non_tbd = True
            elif line.strip() == "":
                continue
            else:
                break
    return found and not non_tbd


def _replace_chapter_goals(text: str, goals: list[str]) -> str:
    lines = text.splitlines()
    out: list[str] = []
    in_goals = False
    replaced = False
    for line in lines:
        if not in_goals:
            out.append(line)
            if line.strip().startswith("chapter_goals"):
                in_goals = True
                out.extend(_format_goals(goals).splitlines())
                out.append("")
                replaced = True
            continue
        if re.match(r"^\\s*notes\\s*:", line):
            out.append(line)
            in_goals = False
            continue
        if re.match(r"^\\s*[-*]\\s*", line) or line.strip() == "":
            continue
        out.append(line)
        in_goals = False
    if not replaced:
        return text
    return "\n".join(out).rstrip("\n") + "\n"


def _infer_next_chapter_num_from_state(root: Path) -> int | None:
    path = root / "state" / "current_state.json"
    try:
        state = load_json(path)
    except Exception:  # noqa: BLE001
        return None
    meta = state.get("meta", {})
    if not isinstance(meta, dict):
        return None
    current = meta.get("current_chapter")
    if current is None:
        return None
    try:
        normalized = normalize_chapter_id(current)
    except ValueError:
        return None
    num = parse_chapter_num_from_id(normalized)
    if num is None:
        return None
    return num + 1


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
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--auto-goals", dest="auto_goals", action="store_true", default=True)
    group.add_argument("--no-auto-goals", dest="auto_goals", action="store_false")
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
        manuscript_next = infer_next_chapter_num(root / "manuscript")
        state_next = _infer_next_chapter_num_from_state(root)
        chapter_num = max(manuscript_next, state_next) if state_next is not None else manuscript_next
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

    default_words = max(3200, default_words)
    words = args.words if args.words is not None else default_words
    if words < 3000:
        words = 3200

    goals: list[str] | None = None
    if args.auto_goals:
        try:
            goals = generate_chapter_goals(root, chap_id)
            if not goals:
                goals = None
        except Exception as e:  # noqa: BLE001
            log.warning("auto-goals generation failed: %s", e)

    brief_path = run_dir / "brief.md"
    if brief_path.exists():
        brief_text = read_text(brief_path)
        if goals and _brief_goals_are_tbd(brief_text):
            updated = _replace_chapter_goals(brief_text, goals)
            if updated != brief_text:
                safe_write_text(brief_path, updated, backup=True)
                log.info("updated chapter_goals in brief: %s", brief_path.as_posix())
            else:
                log.info("brief goals unchanged: %s", brief_path.as_posix())
        else:
            log.info("brief already exists: %s", brief_path.as_posix())
    else:
        safe_write_text(
            brief_path,
            _brief_template(run_date=args.date, chapter=chap_id, words=words, goals=goals),
            backup=False,
        )
        log.info("created brief: %s", brief_path.as_posix())

    log.info("run_dir=%s", run_dir.as_posix())
    log.info("chapter_id=%s", chap_id)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
