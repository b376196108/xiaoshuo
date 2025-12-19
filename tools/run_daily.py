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
    is_codex_available,
    safe_write_text,
    setup_logger,
)


def _run_py(root: Path, script: Path, args: list[str]) -> int:
    cmd = [sys.executable, str(script)] + args
    p = subprocess.run(cmd, cwd=str(root))
    return int(p.returncode)


def _write_manual_instructions(run_dir: Path, *, run_date: str, chap: str) -> Path:
    out = run_dir / "manual_codex_instructions.md"
    text = f"""# Manual Codex Instructions — {run_date} — {chap}

> 说明：本机未检测到 `codex` CLI，无法无人值守写章。请使用 VSCode Codex 插件手动执行以下步骤；完成后再回到命令行重跑本日流水线的 QA/合并步骤。

## Step 1 — 生成章节计划
把以下信息作为上下文输入：
- `AGENTS.md`
- `runs/{run_date}/brief.md`
- `runs/{run_date}/context_pack.md`
- 角色提示词：`prompts/roles/plot_architect.md`、`prompts/roles/chapter_planner.md`

要求产出并写入：
- `runs/{run_date}/chapter_plan.md`

## Step 2 — 写作 + 行文编辑
把以下信息作为上下文输入：
- `runs/{run_date}/chapter_plan.md`
- `canon/style/style_guide.md`
- 角色提示词：`prompts/roles/drafter.md`、`prompts/roles/line_editor.md`

要求产出并写入：
- `manuscript/{chap}.md`

## Step 3 — 摘要 + 滚动摘要 + 状态补丁
把以下信息作为上下文输入：
- `manuscript/{chap}.md`
- `runs/{run_date}/chapter_plan.md`
- `state/current_state.json`
- 角色提示词：`prompts/roles/archivist.md`

要求产出并写入：
- `recap/chapter_summaries/{chap}.md`
- `recap/rolling_recap.md`
- `state/state_patch.json`（JSON 对象，仅变更字段）
- `runs/{run_date}/changelog.md`

## Step 4 — 回到命令行执行 QA 与合并（仅 PASS）
在仓库根目录运行：

```bash
python tools/continuity_checks.py --date {run_date} --chapter {int(chap[2:])}
```

若 QA_RESULT: PASS，再运行：

```bash
python tools/merge_state_patch.py --date {run_date}
```
"""
    safe_write_text(out, text + "\n", backup=True)
    return out


def _codex_prompt(run_date: str, chap: str) -> str:
    return f"""You are the Novel Studio AI writing team operating inside the `xiaoshuo/` repo.

Hard rules:
- Follow `AGENTS.md` strictly (no AI/system traces in the manuscript).
- Do NOT directly edit `state/current_state.json`. Only write `state/state_patch.json`.
- Keep POV/tense/style locked by `canon/style/style_guide.md` and `state/current_state.json`.
- Advance at least 2 open_loops; add at most 1 new open_loop; ending must have a hook.

Read:
- `runs/{run_date}/brief.md`
- `runs/{run_date}/context_pack.md`
- Role prompts under `prompts/roles/`

Produce the following files (exact paths):
- `runs/{run_date}/chapter_plan.md`
- `manuscript/{chap}.md` (start with `# {chap}`)
- `recap/chapter_summaries/{chap}.md`
- `recap/rolling_recap.md`
- `state/state_patch.json` (JSON object, delta only; include at least meta.current_chapter={int(chap[2:])})
- `runs/{run_date}/qa_report.md` (first line MUST be `QA_RESULT: PASS` or `QA_RESULT: FAIL`)
- `runs/{run_date}/changelog.md`

Do not generate any extra story samples beyond the required chapter file.
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Production daily entrypoint.")
    parser.add_argument("--date", default=iso_today(), help="Run date (YYYY-MM-DD). Default: today.")
    parser.add_argument("--chapter", type=int, default=None, help="Chapter number (NNN). If omitted, auto-infer next.")
    parser.add_argument("--words", type=int, default=None, help="Target words (optional, for brief template).")
    parser.add_argument("--max-chars", type=int, default=80000, help="Max chars for context_pack.md.")
    parser.add_argument("--force-manual", action="store_true", help="Always generate manual instructions and skip codex.")
    args = parser.parse_args()

    root = get_repo_root()
    run_dir = root / "runs" / args.date
    run_dir.mkdir(parents=True, exist_ok=True)
    log = setup_logger("run_daily", log_file=run_dir / "run_daily.log", verbose=False)

    chapter_num = args.chapter if args.chapter is not None else infer_next_chapter_num(root / "manuscript")
    chap = chapter_id(chapter_num)
    log.info("date=%s chapter=%s", args.date, chap)

    # 1) CreateRun
    rc = _run_py(
        root,
        root / "tools" / "create_daily_run.py",
        ["--date", args.date, "--chapter", str(chapter_num)] + (["--words", str(args.words)] if args.words else []),
    )
    if rc != 0:
        log.error("create_daily_run failed: rc=%s", rc)
        return rc

    # 2) BuildContext
    rc = _run_py(root, root / "tools" / "build_context_pack.py", ["--date", args.date, "--max-chars", str(args.max_chars)])
    if rc != 0:
        log.error("build_context_pack failed: rc=%s", rc)
        return rc

    # 3) Generate with codex CLI or manual instructions.
    stdout_log = run_dir / "codex_stdout.log"
    stderr_log = run_dir / "codex_stderr.log"
    if args.force_manual or not is_codex_available():
        manual = _write_manual_instructions(run_dir, run_date=args.date, chap=chap)
        log.warning("codex not available; manual instructions written: %s", manual.as_posix())
        print(f"[INFO] codex CLI not available; wrote manual instructions: {manual.as_posix()}")
        return 2

    prompt = _codex_prompt(args.date, chap)
    with stdout_log.open("w", encoding="utf-8") as out, stderr_log.open("w", encoding="utf-8") as err:
        p = subprocess.run(
            ["codex", "exec", "--full-auto"],
            input=prompt,
            text=True,
            cwd=str(root),
            stdout=out,
            stderr=err,
        )
    if p.returncode != 0:
        manual = _write_manual_instructions(run_dir, run_date=args.date, chap=chap)
        log.error("codex exec failed: rc=%s", p.returncode)
        print(f"[ERROR] codex exec failed (rc={p.returncode}). See logs in {run_dir.as_posix()}.")
        print(f"[INFO] Fallback manual instructions: {manual.as_posix()}")
        return int(p.returncode)

    # 4) continuity_checks
    rc = _run_py(root, root / "tools" / "continuity_checks.py", ["--date", args.date, "--chapter", str(chapter_num)])
    if rc != 0:
        log.error("QA failed: rc=%s", rc)
        print(f"[ERROR] QA failed. See: {(run_dir / 'qa_report.md').as_posix()}")
        return rc

    # 5) Patch + Merge (only PASS)
    patch_path = root / "state" / "state_patch.json"
    if not patch_path.exists():
        _run_py(root, root / "tools" / "extract_state_patch.py", ["--date", args.date, "--chapter", str(chapter_num)])

    rc = _run_py(root, root / "tools" / "merge_state_patch.py", ["--date", args.date])
    if rc != 0:
        log.error("merge_state_patch failed: rc=%s", rc)
    else:
        log.info("daily run completed: PASS + merged state patch")
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
