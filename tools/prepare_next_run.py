from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

from _common import (
    chapter_id,
    get_repo_root,
    infer_next_chapter_num,
    iso_today,
    load_json,
    normalize_chapter_id,
    parse_chapter_num_from_id,
    read_project_scale,
)


def _run_py(root: Path, script: Path, args: list[str]) -> int:
    cmd = [sys.executable, str(script)] + args
    p = subprocess.run(cmd, cwd=str(root))
    return int(p.returncode)


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


def _resolve_chapter_id(root: Path, cli_value: str | None) -> str:
    if cli_value:
        return normalize_chapter_id(cli_value)
    manuscript_next = infer_next_chapter_num(root / "manuscript")
    state_next = _infer_next_chapter_num_from_state(root)
    next_num = max(manuscript_next, state_next) if state_next is not None else manuscript_next
    return chapter_id(next_num)


def _resolve_words(root: Path, cli_words: int | None) -> int:
    default_words = 3200
    try:
        project_brief = load_json(root / "inputs" / "project_brief.json")
        _, words_per_chapter = read_project_scale(project_brief)
        if words_per_chapter is not None:
            default_words = words_per_chapter
    except Exception:  # noqa: BLE001
        pass

    default_words = max(3200, default_words)
    if cli_words is None:
        return default_words
    if cli_words < 3000:
        return 3200
    return cli_words


def main() -> int:
    parser = argparse.ArgumentParser(description="Prepare next run in one command (no drafting).")
    parser.add_argument("--date", default=iso_today(), help="Run date (YYYY-MM-DD). Default: today.")
    parser.add_argument("--chapter", type=str, default=None, help="Chapter id (chNNN) or number (NNN).")
    parser.add_argument("--words", type=int, default=None, help="Target words (min 3000).")
    args = parser.parse_args()

    root = get_repo_root()
    run_date = args.date
    chap = _resolve_chapter_id(root, args.chapter)
    target_words = _resolve_words(root, args.words)

    rc = _run_py(
        root,
        root / "tools" / "create_daily_run.py",
        [
            "--date",
            run_date,
            "--chapter",
            chap,
            "--words",
            str(target_words),
            "--auto-goals",
        ],
    )
    if rc != 0:
        return rc

    rc = _run_py(
        root,
        root / "tools" / "build_context_pack.py",
        ["--date", run_date],
    )
    if rc != 0:
        return rc

    rc = _run_py(
        root,
        root / "tools" / "run_daily.py",
        [
            "--date",
            run_date,
            "--chapter",
            chap,
            "--words",
            str(target_words),
            "--force-manual",
        ],
    )
    if rc not in (0, 2):
        return rc

    print(f"已生成 runs/{run_date}/brief.md（已自动填 chapter_goals）")
    print(f"已生成 runs/{run_date}/context_pack.md")
    print(f"已生成 runs/{run_date}/manual_codex_instructions.md")
    print("提示：chapter_plan.md 必须包含 chapter_title；正文第二行必须为 ## 《章节标题》")
    print("下一步：打开 manual_codex_instructions.md 在 VSCode Codex 扩展执行 Step1-3，然后再跑 QA 与 merge")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
