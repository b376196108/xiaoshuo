from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from _common import (
    FileHash,
    get_repo_root,
    hash_file,
    iso_today,
    iter_files,
    load_json,
    now_utc_iso,
    read_text,
    safe_write_text,
    setup_logger,
)


def _read_optional_text(path: Path) -> str:
    if not path.exists():
        return f"[MISSING] {path.as_posix()}\n"
    return read_text(path).strip() + "\n"


def _pretty_json(obj: Any) -> str:
    return json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True)


def _build_state_focus(state_path: Path) -> str:
    if not state_path.exists():
        return f"[MISSING] {state_path.as_posix()}\n"
    try:
        state = load_json(state_path)
    except Exception as e:  # noqa: BLE001
        return f"[ERROR] Failed to parse JSON: {state_path.as_posix()}: {e}\n"

    meta = state.get("meta", {})
    open_loops = state.get("open_loops", [])
    continuity_locks = state.get("continuity_locks", {})
    world_state = state.get("world_state", {})

    focus = {
        "meta": meta,
        "open_loops": open_loops,
        "world_state": world_state,
        "continuity_locks": continuity_locks,
    }
    return _pretty_json(focus) + "\n"


def _find_recent_chapter_summaries(root: Path, count: int = 2) -> list[Path]:
    summaries_dir = root / "recap" / "chapter_summaries"
    if not summaries_dir.exists():
        return []

    items: list[tuple[int, Path]] = []
    for path in summaries_dir.glob("ch*.md"):
        try:
            n = int(path.stem[2:])
        except ValueError:
            continue
        items.append((n, path))
    items.sort(key=lambda x: x[0])
    return [p for _, p in items[-count:]]


def _truncate(text: str, max_chars: int) -> tuple[str, bool]:
    if max_chars <= 0:
        return "", True
    if len(text) <= max_chars:
        return text, False
    suffix = "\n\n[TRUNCATED]\n"
    cut = max_chars - len(suffix)
    if cut <= 0:
        return suffix[:max_chars], True
    return text[:cut] + suffix, True


def _render_section(title: str, body: str) -> str:
    return f"## {title}\n\n{body.rstrip()}\n\n"


def _canon_manifest(root: Path, run_dir: Path, *, head_bytes: int = 32768) -> Path:
    canon_dir = root / "canon"
    files = sorted([p for p in iter_files(canon_dir)], key=lambda p: p.as_posix())
    manifest: dict[str, Any] = {
        "generated_at_utc": now_utc_iso(),
        "head_bytes": head_bytes,
        "files": [],
    }
    for path in files:
        fh: FileHash = hash_file(path, head_bytes=head_bytes)
        manifest["files"].append(
            {
                "path": path.relative_to(root).as_posix(),
                "size": fh.size,
                "sha256": fh.sha256,
                "head_bytes": fh.head_bytes,
                "head_sha256": fh.head_sha256,
            }
        )

    out = run_dir / "canon_manifest.json"
    safe_write_text(out, json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", backup=True)
    return out


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build runs/YYYY-MM-DD/context_pack.md from repo truth sources."
    )
    parser.add_argument(
        "--date", default=iso_today(), help="Run date (YYYY-MM-DD). Default: today."
    )
    parser.add_argument(
        "--max-chars",
        type=int,
        default=80000,
        help="Max characters for context_pack.md (default 80000).",
    )
    parser.add_argument("--verbose", action="store_true", help="Verbose logging.")
    args = parser.parse_args()

    root = get_repo_root()
    run_dir = root / "runs" / args.date
    run_dir.mkdir(parents=True, exist_ok=True)
    log = setup_logger(
        "build_context_pack",
        log_file=run_dir / "build_context_pack.log",
        verbose=args.verbose,
    )

    brief_path = run_dir / "brief.md"
    context_pack_path = run_dir / "context_pack.md"

    try:
        manifest_path = _canon_manifest(root, run_dir)
        log.info("wrote canon manifest: %s", manifest_path.as_posix())
    except Exception as e:  # noqa: BLE001
        log.warning("failed to write canon manifest: %s", e)

    recent_summaries = _find_recent_chapter_summaries(root, count=2)

    sections: list[tuple[int, str, str]] = []
    sections.append((100, "Today Brief", _read_optional_text(brief_path)))
    sections.append(
        (
            95,
            "State Focus (meta + open_loops + locks)",
            _build_state_focus(root / "state" / "current_state.json"),
        )
    )

    if recent_summaries:
        for i, p in enumerate(recent_summaries[::-1], start=1):
            sections.append(
                (90 - i, f"Recent Chapter Summary (-{i}) — {p.name}", _read_optional_text(p))
            )
    else:
        sections.append(
            (88, "Recent Chapter Summaries", "[MISSING] No chapter summaries found under recap/chapter_summaries/\n")
        )

    sections.append((85, "Rolling Recap", _read_optional_text(root / "recap" / "rolling_recap.md")))
    sections.append((80, "Master Outline", _read_optional_text(root / "outline" / "master_outline.md")))

    canon_priority = [
        ("Premise", root / "canon" / "premise.md"),
        ("Style Guide", root / "canon" / "style" / "style_guide.md"),
        ("World Rules", root / "canon" / "rules" / "world_rules.md"),
        ("Characters (YAML)", root / "canon" / "characters" / "characters.yaml"),
        ("Locations (YAML)", root / "canon" / "locations" / "locations.yaml"),
        ("Factions (YAML)", root / "canon" / "factions" / "factions.yaml"),
    ]
    for title, path in canon_priority:
        sections.append((70, f"Canon — {title}", _read_optional_text(path)))

    canon_dir = root / "canon"
    key_paths = {p for _, p in canon_priority}
    for path in sorted([p for p in iter_files(canon_dir) if p not in key_paths], key=lambda p: p.as_posix()):
        sections.append((40, f"Canon — {path.relative_to(canon_dir).as_posix()}", _read_optional_text(path)))

    sections.append((75, "Project Brief (JSON)", _read_optional_text(root / "inputs" / "project_brief.json")))

    sections.sort(key=lambda x: x[0], reverse=True)

    header = (
        f"# Context Pack — {args.date}\n\n"
        f"- generated_at_utc: {now_utc_iso()}\n"
        f"- max_chars: {args.max_chars}\n\n"
        "说明：本文件由工具自动聚合生成，供写作与 QA 使用；若某些文件缺失，会以 [MISSING] 标记。\n\n"
    )

    out = header
    truncated_any = False
    for _, title, body in sections:
        chunk = _render_section(title, body)
        remaining = args.max_chars - len(out)
        if remaining <= 0:
            truncated_any = True
            break
        chunk2, truncated = _truncate(chunk, remaining)
        out += chunk2
        truncated_any = truncated_any or truncated

    if truncated_any:
        out += "\n---\n\nNOTE: context_pack was truncated to fit max_chars.\n"

    safe_write_text(context_pack_path, out, backup=True)
    log.info("wrote context pack: %s (chars=%d)", context_pack_path.as_posix(), len(out))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

