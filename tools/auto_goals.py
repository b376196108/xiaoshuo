from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from _common import (
    chapter_id,
    load_json,
    normalize_chapter_id,
    parse_chapter_num_from_id,
    read_text,
)


def _read_optional_text(path: Path) -> str:
    if not path.exists():
        return ""
    try:
        return read_text(path)
    except OSError:
        return ""


def _load_open_loops(root: Path) -> list[dict[str, Any]]:
    path = root / "state" / "current_state.json"
    try:
        state = load_json(path)
    except Exception:  # noqa: BLE001
        return []
    loops = state.get("open_loops", [])
    if not isinstance(loops, list):
        return []
    return [loop for loop in loops if isinstance(loop, dict)]


def _select_loops(loops: list[dict[str, Any]], min_count: int = 2) -> list[dict[str, Any]]:
    preferred = [
        loop
        for loop in loops
        if str(loop.get("status", "")).lower() in {"progressed", "open", "active"}
    ]
    selected = preferred[:min_count]
    if len(selected) < min_count:
        for loop in loops:
            if loop not in selected:
                selected.append(loop)
            if len(selected) >= min_count:
                break
    return selected


def _extract_hook(summary_text: str) -> str | None:
    if not summary_text.strip():
        return None
    for line in summary_text.splitlines():
        if "结尾钩子" in line:
            match = re.search(r"结尾钩子[:：]\s*(.+)", line)
            if match:
                return match.group(1).strip()
        if line.strip().lower().startswith("ending_hook"):
            match = re.search(r"ending_hook\s*[:：]\s*(.+)", line, re.IGNORECASE)
            if match:
                return match.group(1).strip()

    cleaned: list[str] = []
    for line in summary_text.splitlines():
        if line.lstrip().startswith("#"):
            continue
        line = re.sub(r"^[-*]\s*", "", line).strip()
        if line:
            cleaned.append(line)
    text = " ".join(cleaned)
    parts = [p.strip() for p in re.split(r"[。！？!?]", text) if p.strip()]
    return parts[-1] if parts else None


def _trim_hook(text: str, max_len: int = 60) -> str:
    if len(text) <= max_len:
        return text
    trimmed = text[:max_len].rstrip("，。")
    return trimmed + "..."


def _loop_text(loop: dict[str, Any]) -> str:
    pieces = []
    for key in ("id", "description", "note", "owner"):
        value = loop.get(key)
        if isinstance(value, str) and value:
            pieces.append(value)
    return " ".join(pieces)


def _goal_for_loop(loop: dict[str, Any]) -> str:
    text = _loop_text(loop)
    keyword_map = [
        (["粮", "口粮", "断粮", "粮缸"], "本章明确短期口粮来源或可执行的换粮路径"),
        (["流言", "造谣", "邻居", "许文淑"], "本章争取里正/村权态度或锁定流言扩散证据"),
        (["徭役", "名册", "点名", "差役"], "本章摸清名册规则并争取缓冲或替代方案"),
        (["种子", "春播", "农具"], "本章锁定种子/农具来源或替代办法"),
        (["水", "井", "取水", "污染"], "本章确认水源问题并落实临时净水/取水办法"),
        (["身份", "异常", "风险"], "本章稳住对外说辞，降低身份暴露风险"),
    ]
    for keywords, goal in keyword_map:
        if any(k in text for k in keywords):
            return goal
    return "本章推进该问题进入可执行阶段，明确下一步行动"


def _pick_payoff(text_blob: str) -> str:
    if any(k in text_blob for k in ["水", "井", "取水", "污染"]):
        return "落实可执行的净水/取水流程，当日见效"
    if any(k in text_blob for k in ["粮", "口粮", "饥", "断粮"]):
        return "省柴/省粮流程当天见效，保证当晚更顶饱"
    if any(k in text_blob for k in ["种子", "春播", "农具"]):
        return "找到替代种子/工具的办法，带来即时小收益"
    return "用现代流程改造带来当日可见的小成果（省柴/净水/换粮其一）"


def _pick_hardship(text_blob: str) -> str:
    if any(k in text_blob for k in ["邻居", "流言", "许文淑"]):
        return "邻居或流言升级，名册/资源受阻"
    if any(k in text_blob for k in ["徭役", "名册", "差役", "点名"]):
        return "差役或名册压力加码，时间更紧"
    return "村权/天灾压力加码，迫使方案调整"


def _previous_summary_path(root: Path, chapter_id_value: str) -> Path | None:
    num = parse_chapter_num_from_id(chapter_id_value)
    if num is None or num <= 1:
        return None
    prev_id = chapter_id(num - 1)
    return root / "recap" / "chapter_summaries" / f"{prev_id}.md"


def generate_chapter_goals(root: Path, chapter_id_value: str) -> list[str]:
    chap = normalize_chapter_id(chapter_id_value)
    loops = _load_open_loops(root)
    selected = _select_loops(loops, min_count=2)

    prev_summary_path = _previous_summary_path(root, chap)
    hook = None
    if prev_summary_path is not None:
        hook = _extract_hook(_read_optional_text(prev_summary_path))
    if hook:
        hook = _trim_hook(hook)
        hook_line = f"承接上章钩子：{hook}"
    else:
        hook_line = "承接上章钩子：延续上章未解的紧迫事件并明确当下应对。"

    goals: list[str] = [hook_line]

    if selected:
        for loop in selected[:2]:
            loop_id = str(loop.get("id") or "open_loop").strip()
            goals.append(f"推进 {loop_id}：{_goal_for_loop(loop)}")
    else:
        goals.append("推进关键矛盾：明确规则/线索/资源中的至少一项。")
        goals.append("推进关键矛盾：让问题进入可执行的下一步。")

    blob = " ".join(_loop_text(loop) for loop in selected)
    goals.append(f"种田爽点落地：{_pick_payoff(blob)}。")
    goals.append(f"磨难/反转升级：{_pick_hardship(blob)}。")

    if len(goals) < 6:
        goals.append("结尾留钩子：抛出新的时间限制或资格风险，驱动下一章。")

    deduped: list[str] = []
    seen: set[str] = set()
    for item in goals:
        text = item.strip()
        if not text or text in seen:
            continue
        seen.add(text)
        deduped.append(text)

    while len(deduped) < 3:
        deduped.append("本章明确一个可执行的当日目标并落地。")

    return deduped[:6]

