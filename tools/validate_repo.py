from __future__ import annotations

import compileall
from pathlib import Path

from _common import (
    get_repo_root,
    is_codex_available,
    load_json,
    now_utc_iso,
    parse_chapter_num_from_id,
    read_text,
    safe_write_text,
)


REQUIRED_DIRS = [
    "inputs",
    "canon",
    "canon/characters",
    "canon/locations",
    "canon/factions",
    "canon/rules",
    "canon/style",
    "outline",
    "state",
    "state/backups",
    "recap",
    "recap/chapter_summaries",
    "manuscript",
    "prompts",
    "prompts/roles",
    "pipelines",
    "tools",
    "runs",
    "scripts",
    "logs",
]

REQUIRED_FILES = [
    ".xiaoshuo_repo_root",
    "AGENTS.md",
    "README.md",
    ".gitignore",
    "inputs/project_brief.json",
    "canon/premise.md",
    "canon/style/style_guide.md",
    "canon/characters/characters.yaml",
    "canon/locations/locations.yaml",
    "canon/factions/factions.yaml",
    "canon/rules/world_rules.md",
    "outline/master_outline.md",
    "state/current_state.json",
    "recap/rolling_recap.md",
    "pipelines/daily_pipeline.md",
    "prompts/roles/worldbuilder.md",
    "prompts/roles/character_designer.md",
    "prompts/roles/plot_architect.md",
    "prompts/roles/chapter_planner.md",
    "prompts/roles/drafter.md",
    "prompts/roles/line_editor.md",
    "prompts/roles/continuity_qa.md",
    "prompts/roles/archivist.md",
    "tools/_common.py",
    "tools/create_daily_run.py",
    "tools/build_context_pack.py",
    "tools/extract_state_patch.py",
    "tools/merge_state_patch.py",
    "tools/continuity_checks.py",
    "tools/run_daily.py",
    "tools/validate_repo.py",
]


def _check_json(path: Path) -> tuple[bool, str]:
    try:
        obj = load_json(path)
    except Exception as e:  # noqa: BLE001
        return False, f"JSON parse failed: {e}"
    if not isinstance(obj, dict):
        return False, "JSON root must be an object/dict."
    return True, "OK"


def _check_chapter_titles(root: Path) -> list[str]:
    warnings: list[str] = []
    manuscript_dir = root / "manuscript"
    if not manuscript_dir.exists():
        return warnings

    for path in manuscript_dir.glob("ch*.md"):
        chap_id = path.stem
        expected_first = f"# {chap_id}"
        try:
            text = read_text(path)
        except OSError as exc:
            warnings.append(f"{path.as_posix()}: read failed ({exc})")
            continue
        lines = text.splitlines()
        if not lines:
            warnings.append(f"{path.as_posix()}: empty file")
            continue
        if lines[0].strip() != expected_first:
            warnings.append(f"{path.as_posix()}: first line should be '{expected_first}'")

        if len(lines) > 1 and lines[1].strip().startswith("##"):
            chapter_num = parse_chapter_num_from_id(chap_id)
            if chapter_num is None:
                if not lines[1].strip().startswith("## 第"):
                    warnings.append(f"{path.as_posix()}: second line should match '## 第N章：...'")
            else:
                expected_prefix = f"## 第{chapter_num}章："
                if not lines[1].strip().startswith(expected_prefix):
                    warnings.append(
                        f"{path.as_posix()}: second line should start with '{expected_prefix}'"
                    )

    return warnings


def main() -> int:
    root = get_repo_root()
    report_path = root / "runs" / "BOOTSTRAP_REPORT.md"

    missing_dirs: list[str] = []
    for d in REQUIRED_DIRS:
        if not (root / d).exists():
            missing_dirs.append(d)

    missing_files: list[str] = []
    for f in REQUIRED_FILES:
        if not (root / f).exists():
            missing_files.append(f)

    json_checks: list[tuple[str, bool, str]] = []
    for rel in ["inputs/project_brief.json", "state/current_state.json"]:
        ok, msg = _check_json(root / rel)
        json_checks.append((rel, ok, msg))

    tools_dir = root / "tools"
    compile_ok = compileall.compile_dir(str(tools_dir), quiet=1)
    title_warnings = _check_chapter_titles(root)

    ok_overall = (
        not missing_dirs
        and not missing_files
        and all(ok for _, ok, _ in json_checks)
        and compile_ok
    )

    lines: list[str] = []
    lines.append("# BOOTSTRAP_REPORT")
    lines.append("")
    lines.append(f"- generated_at_utc: {now_utc_iso()}")
    lines.append(f"- repo_root: {root.as_posix()}")
    lines.append(f"- codex_cli_detected: {str(is_codex_available())}")
    lines.append("")

    lines.append("## Directory Check")
    if missing_dirs:
        lines.append("- RESULT: FAIL")
        for d in missing_dirs:
            lines.append(f"- missing: `{d}/`")
    else:
        lines.append("- RESULT: PASS")

    lines.append("")
    lines.append("## File Check")
    if missing_files:
        lines.append("- RESULT: FAIL")
        for f in missing_files:
            lines.append(f"- missing: `{f}`")
    else:
        lines.append("- RESULT: PASS")

    lines.append("")
    lines.append("## JSON Parse Check")
    for rel, ok, msg in json_checks:
        lines.append(f"- `{rel}`: {'PASS' if ok else 'FAIL'} — {msg}")

    lines.append("")
    lines.append("## Python Compile Check")
    lines.append(f"- `python -m compileall tools`: {'PASS' if compile_ok else 'FAIL'}")

    lines.append("")
    lines.append("## Chapter Title Check")
    if title_warnings:
        lines.append("- RESULT: WARNING")
        for warning in title_warnings:
            lines.append(f"- WARNING: {warning}")
    else:
        lines.append("- RESULT: PASS")

    lines.append("")
    lines.append("## Directory Tree (top)")
    lines.append("- `inputs/` (edit `inputs/project_brief.json`)")
    lines.append("- `canon/` (truth source; append-only by default)")
    lines.append("- `state/` (truth source; patch+merge only)")
    lines.append("- `recap/` (summaries)")
    lines.append("- `manuscript/` (chapters)")
    lines.append("- `runs/` (daily artifacts)")
    lines.append("")

    lines.append("## Next Steps")
    lines.append("1) 填写 `inputs/project_brief.json`：最少需要设置以下字段即可开始每日流水线：")
    lines.append("   - `project.genre`, `project.tone`, `project.rating`, `project.hook`, `project.theme`, `project.setting_anchor`")
    lines.append("   - `project.scale.total_chapters`, `project.scale.words_per_chapter`")
    lines.append("   - `constraints.must_have[]`, `constraints.must_avoid[]`（可为空数组）")
    lines.append("   - `random_seed`（建议稳定）")
    lines.append("2) 运行每日入口：`python tools/run_daily.py`")
    lines.append("")
    lines.append("### Commands")
    lines.append("```bash")
    lines.append("python -m compileall tools")
    lines.append("python tools/validate_repo.py")
    lines.append("python tools/run_daily.py --date YYYY-MM-DD --chapter NNN --words 2000")
    lines.append("```")
    lines.append("")

    safe_write_text(report_path, "\n".join(lines) + "\n", backup=True)
    return 0 if ok_overall else 1


if __name__ == "__main__":
    raise SystemExit(main())
