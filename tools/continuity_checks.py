from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any

from _common import (
    chapter_id,
    get_repo_root,
    iso_today,
    load_json,
    normalize_chapter_id,
    parse_chapter_num_from_id,
    read_text,
    safe_write_text,
    setup_logger,
)


def _extract_style_locks(style_text: str) -> dict[str, str]:
    locks: dict[str, str] = {}
    for line in style_text.splitlines():
        line = line.strip()
        if line.startswith("- 人称："):
            locks["person"] = line.split("：", 1)[1].strip()
        if line.startswith("- 视角："):
            locks["pov"] = line.split("：", 1)[1].strip()
        if line.startswith("- 时态："):
            locks["tense"] = line.split("：", 1)[1].strip()
    return locks


def _extract_character_names(characters_yaml_text: str) -> set[str]:
    names: set[str] = set()
    for line in characters_yaml_text.splitlines():
        line = line.strip()
        if line.startswith("name:"):
            v = line.split(":", 1)[1].strip()
            if v and v.upper() != "TBD":
                names.add(v)
    return names


def _detect_capitalized_names(chapter_text: str) -> set[str]:
    return set(re.findall(r"\\b[A-Z][a-z]{2,}\\b", chapter_text))


def _planned_open_loop_ids(chapter_plan_text: str, known_loop_ids: set[str]) -> list[str]:
    return [loop_id for loop_id in sorted(known_loop_ids) if loop_id and (loop_id in chapter_plan_text)]


def _load_optional_json(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    try:
        obj = load_json(path)
    except Exception:  # noqa: BLE001
        return None
    return obj if isinstance(obj, dict) else None


def _canon_change_watch(root: Path, run_dir: Path) -> tuple[list[str], list[str]]:
    manifest_path = run_dir / "canon_manifest.json"
    if not manifest_path.exists():
        return [], []

    try:
        manifest = load_json(manifest_path)
    except Exception:  # noqa: BLE001
        return [], []
    files = manifest.get("files", [])
    if not isinstance(files, list):
        return [], []

    append_like: list[str] = []
    rewrite_like: list[str] = []

    for entry in files:
        if not isinstance(entry, dict):
            continue
        rel = entry.get("path")
        old_sha = entry.get("sha256")
        old_head = entry.get("head_sha256")
        head_bytes = entry.get("head_bytes")
        if not isinstance(rel, str) or not isinstance(old_sha, str) or not isinstance(old_head, str):
            continue
        if not isinstance(head_bytes, int) or head_bytes <= 0:
            head_bytes = 32768

        path = root / rel
        if not path.exists():
            continue

        data = path.read_bytes()
        new_sha = hashlib.sha256(data).hexdigest()
        if new_sha == old_sha:
            continue

        new_head = hashlib.sha256(data[:head_bytes]).hexdigest()
        if new_head == old_head:
            append_like.append(rel)
        else:
            rewrite_like.append(rel)

    return append_like, rewrite_like


def _calc_body_chars(chapter_text: str, chap: str) -> int:
    lines = chapter_text.splitlines()
    start = 0
    if lines and lines[0].strip() == f"# {chap}":
        start = 1
        if start < len(lines) and lines[start].lstrip().startswith("## 第"):
            start += 1
    body_lines = []
    for line in lines[start:]:
        if line.lstrip().startswith("#"):
            continue
        body_lines.append(line)
    body_text = "".join(body_lines)
    body_text = "".join(ch for ch in body_text if not ch.isspace())
    return len(body_text)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run continuity and hard-rule checks; write runs/YYYY-MM-DD/qa_report.md."
    )
    parser.add_argument("--date", default=iso_today(), help="Run date (YYYY-MM-DD). Default: today.")
    parser.add_argument("--chapter", type=str, required=True, help="Chapter id (chNNN) or number (NNN).")
    parser.add_argument("--verbose", action="store_true", help="Verbose logging.")
    args = parser.parse_args()

    root = get_repo_root()
    run_dir = root / "runs" / args.date
    run_dir.mkdir(parents=True, exist_ok=True)
    log = setup_logger(
        "continuity_checks", log_file=run_dir / "continuity_checks.log", verbose=args.verbose
    )

    try:
        chap = normalize_chapter_id(args.chapter)
    except ValueError as e:
        log.error("Invalid --chapter: %s (%s)", args.chapter, e)
        return 2

    if parse_chapter_num_from_id(chap) is None:
        log.error("Invalid chapter id after normalization: %s", chap)
        return 2
    chapter_path = root / "manuscript" / f"{chap}.md"
    summary_path = root / "recap" / "chapter_summaries" / f"{chap}.md"
    plan_path = run_dir / "chapter_plan.md"
    patch_path = root / "state" / "state_patch.json"
    qa_path = run_dir / "qa_report.md"

    failures: list[dict[str, str]] = []
    warnings: list[dict[str, str]] = []

    body_chars: int | None = None
    if not chapter_path.exists():
        failures.append(
            {
                "rule": "artifact_missing: manuscript",
                "evidence": f"Missing {chapter_path.as_posix()}",
                "fix": "Generate `manuscript/chNNN.md` first.",
            }
        )
        chapter_text = ""
    else:
        chapter_text = read_text(chapter_path)
        body_chars = _calc_body_chars(chapter_text, chap)
        if body_chars < 3000:
            failures.append(
                {
                    "rule": "BodyTooShort",
                    "evidence": f"BodyTooShort: {body_chars}/3000",
                    "fix": "Expand the manuscript body to >=3000 chars (excluding headers/whitespace).",
                }
            )
        if "TBD" in chapter_text:
            failures.append(
                {
                    "rule": "no_TBD_in_manuscript",
                    "evidence": "Found 'TBD' placeholder in manuscript.",
                    "fix": "Replace all placeholders in manuscript with actual narrative text.",
                }
            )

    style_path = root / "canon" / "style" / "style_guide.md"
    style_text = read_text(style_path) if style_path.exists() else ""
    locks = _extract_style_locks(style_text)

    state_path = root / "state" / "current_state.json"
    state_obj = _load_optional_json(state_path) or {}
    meta = state_obj.get("meta", {}) if isinstance(state_obj.get("meta", {}), dict) else {}
    meta_pov = str(meta.get("pov", "")).strip()
    pov_lock = meta_pov if meta_pov and meta_pov.upper() != "TBD" else locks.get("pov", "")

    if not pov_lock or pov_lock.upper() == "TBD":
        warnings.append(
            {
                "topic": "pov_lock_missing",
                "evidence": "state.meta.pov / style guide POV is TBD or missing.",
                "suggestion": "Set `state/current_state.json.meta.pov` and `canon/style/style_guide.md` to a concrete POV lock.",
            }
        )
    else:
        first_person_markers = chapter_text.count("我") + chapter_text.count("我们")
        if ("第三" in pov_lock) or ("third" in pov_lock.lower()):
            if first_person_markers >= 20:
                failures.append(
                    {
                        "rule": "pov_consistency_third_person",
                        "evidence": f"Third-person POV lock but many first-person markers found (count={first_person_markers}).",
                        "fix": "Revise narration to remove first-person viewpoint drift.",
                    }
                )

    state_current_raw = meta.get("current_chapter")
    state_current = None
    if state_current_raw is not None:
        try:
            state_current = normalize_chapter_id(state_current_raw)
        except ValueError:
            warnings.append(
                {
                    "topic": "state_current_chapter_invalid",
                    "evidence": f"state.meta.current_chapter invalid: {state_current_raw!r}",
                    "suggestion": "Ensure state/current_state.json uses chapter id format like ch001.",
                }
            )

    if state_current:
        if chapter_path.exists():
            if chap != state_current:
                failures.append(
                    {
                        "rule": "chapter_id_mismatch",
                        "evidence": f"manuscript={chap}.md vs state.meta.current_chapter={state_current}",
                        "fix": "Align state meta current_chapter with the manuscript chapter id before merging.",
                    }
                )
        else:
            warnings.append(
                {
                    "topic": "chapter_id_check_skipped",
                    "evidence": f"Missing {chapter_path.as_posix()} so chapter-id consistency not verified.",
                    "suggestion": "Generate manuscript and re-run QA.",
                }
            )

    characters_path = root / "canon" / "characters" / "characters.yaml"
    known_names = _extract_character_names(read_text(characters_path) if characters_path.exists() else "")
    if known_names:
        unknown_caps = _detect_capitalized_names(chapter_text) - known_names
        if unknown_caps:
            warnings.append(
                {
                    "topic": "unknown_capitalized_names",
                    "evidence": f"Found potential unknown names: {', '.join(sorted(list(unknown_caps))[:20])}",
                    "suggestion": "If these are core characters, add them to `canon/characters/characters.yaml` (append-only).",
                }
            )
    else:
        warnings.append(
            {
                "topic": "character_catalog_TBD",
                "evidence": "No concrete character names found in canon/characters/characters.yaml (all TBD).",
                "suggestion": "Fill characters.yaml with real names to enable stronger QA checks.",
            }
        )

    in_story_date = str(meta.get("in_story_date", "")).strip()
    if not in_story_date or in_story_date.upper() == "TBD":
        warnings.append(
            {
                "topic": "timeline_anchor_missing",
                "evidence": "state.meta.in_story_date is TBD/missing.",
                "suggestion": "Set an ISO-like in_story_date and keep it monotonic; update via state_patch.",
            }
        )

    open_loops = state_obj.get("open_loops", []) if isinstance(state_obj.get("open_loops", []), list) else []
    known_loop_ids = {str(x.get("id")) for x in open_loops if isinstance(x, dict) and x.get("id")}

    if not plan_path.exists():
        failures.append(
            {
                "rule": "artifact_missing: chapter_plan",
                "evidence": f"Missing {plan_path.as_posix()}",
                "fix": "Generate `runs/YYYY-MM-DD/chapter_plan.md` before QA.",
            }
        )
        planned: list[str] = []
    else:
        plan_text = read_text(plan_path)
        planned = _planned_open_loop_ids(plan_text, known_loop_ids)
        if len(planned) < 2:
            failures.append(
                {
                    "rule": "open_loops_advance_min_2",
                    "evidence": f"Planned open_loops detected in chapter_plan: {planned}",
                    "fix": "Update chapter_plan to advance at least 2 open_loops (explicitly mention their ids).",
                }
            )

    summary_text = read_text(summary_path) if summary_path.exists() else ""
    patch_obj = _load_optional_json(patch_path)
    patch_text = json.dumps(patch_obj, ensure_ascii=False) if patch_obj is not None else ""

    if planned:
        if not summary_path.exists():
            failures.append(
                {
                    "rule": "artifact_missing: chapter_summary",
                    "evidence": f"Missing {summary_path.as_posix()}",
                    "fix": "Write `recap/chapter_summaries/chNNN.md` before QA.",
                }
            )
        if patch_obj is None:
            failures.append(
                {
                    "rule": "artifact_missing_or_invalid: state_patch",
                    "evidence": f"Missing or invalid {patch_path.as_posix()}",
                    "fix": "Generate `state/state_patch.json` (JSON object) before QA.",
                }
            )

        for loop_id in planned:
            if summary_text and (loop_id not in summary_text):
                failures.append(
                    {
                        "rule": "open_loop_evidence_in_summary",
                        "evidence": f"Planned loop '{loop_id}' not found in chapter summary.",
                        "fix": "Update chapter summary to explicitly mention how this loop moved.",
                    }
                )
            if patch_text and (loop_id not in patch_text):
                failures.append(
                    {
                        "rule": "open_loop_evidence_in_state_patch",
                        "evidence": f"Planned loop '{loop_id}' not found in state_patch.json.",
                        "fix": "Update state_patch to reflect this loop's status/progress (by id).",
                    }
                )

    append_like, rewrite_like = _canon_change_watch(root, run_dir)
    if rewrite_like:
        failures.append(
            {
                "rule": "canon_rewrite_detected",
                "evidence": f"**CANON_REWRITE_DETECTED**: {', '.join(rewrite_like)}",
                "fix": "Revert unintended canon rewrites, or explicitly record rationale/impact in this QA report and changelog.",
            }
        )
    if append_like:
        warnings.append(
            {
                "topic": "canon_changed_append_like",
                "evidence": f"Canon changed (append-like): {', '.join(append_like)}",
                "suggestion": "Ensure changelog records the append and QA reviews consistency.",
            }
        )

    qa_result = "PASS" if not failures else "FAIL"

    report_lines: list[str] = []
    report_lines.append(f"QA_RESULT: {qa_result}")
    report_lines.append("")
    report_lines.append(f"# QA Report — {args.date} — {chap}")
    report_lines.append("")

    report_lines.append("## Hard Failures")
    if failures:
        for item in failures:
            report_lines.append(f"- rule: {item['rule']}")
            report_lines.append(f"  evidence: {item['evidence']}")
            report_lines.append(f"  fix: {item['fix']}")
    else:
        report_lines.append("- (none)")

    report_lines.append("")
    report_lines.append("## Warnings")
    if warnings:
        for item in warnings:
            report_lines.append(f"- topic: {item['topic']}")
            report_lines.append(f"  evidence: {item['evidence']}")
            report_lines.append(f"  suggestion: {item['suggestion']}")
    else:
        report_lines.append("- (none)")

    report_lines.append("")
    report_lines.append("## Body Length")
    if body_chars is None:
        report_lines.append("- body_chars: N/A")
    else:
        report_lines.append(f"- body_chars: {body_chars}")
        report_lines.append("- min_required: 3000")

    report_lines.append("")
    report_lines.append("## Open Loop Verification")
    report_lines.append(f"- planned_advances: {planned}")
    report_lines.append(f"- chapter_plan_path: {plan_path.as_posix()}")
    report_lines.append(f"- summary_path: {summary_path.as_posix()}")
    report_lines.append(f"- state_patch_path: {patch_path.as_posix()}")

    report_lines.append("")
    report_lines.append("## Recommended Rework Steps (if FAIL)")
    report_lines.append("1) Fix missing artifacts (chapter_plan / manuscript / summary / patch).")
    report_lines.append("2) Ensure chapter_plan advances >=2 open_loops and cites their ids.")
    report_lines.append("3) Update summary + state_patch so each planned loop id is explicitly present.")
    report_lines.append(f"4) Re-run: `python tools/continuity_checks.py --date {args.date} --chapter {chap}`")

    safe_write_text(qa_path, "\n".join(report_lines) + "\n", backup=True)
    log.info("wrote qa report: %s (result=%s)", qa_path.as_posix(), qa_result)
    return 0 if qa_result == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
