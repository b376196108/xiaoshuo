from __future__ import annotations

import re
from collections import Counter
from typing import Iterable


_FALLBACK_TITLE = "荒年第一局"

_DOMAIN_KEYWORDS = [
    "断粮",
    "粮缸",
    "口粮",
    "饥荒",
    "荒年",
    "徭役",
    "名册",
    "差役",
    "邻居",
    "造谣",
    "赈灾",
    "欠债",
    "借粮",
    "换粮",
    "省柴",
    "闷煮",
    "井水",
    "水源",
    "野菜",
    "陷阱",
    "储粮",
    "种田",
    "开荒",
    "养家",
    "病",
    "咳",
    "盐",
    "粥",
]

_PRIORITY_HINTS = [
    "结尾钩子",
    "ending hook",
    "ending_hook",
    "爽点",
    "冲突",
    "危机",
    "反转",
]

_STOP_CHARS = set(
    "的了是在我他她你它们我们他们她们这那和与及而就也都又还很太更最把被给到对向为于从用"
    "一个上中下里外其并且却并非因为所以不是要而且着之"
)

_CJK_RE = re.compile(r"[\u4e00-\u9fff]")


def chapter_no_from_id(chapter_id: str) -> int:
    match = re.fullmatch(r"ch(\d+)", chapter_id.strip(), flags=re.IGNORECASE)
    if not match:
        raise ValueError(f"Invalid chapter id: {chapter_id!r}")
    return int(match.group(1))


def format_chapter_heading(chapter_id: str, title: str = "{title}") -> str:
    return f"## 第{chapter_no_from_id(chapter_id)}章：{title}"


def generate_chapter_title(
    chapter_id: str,
    chapter_text: str,
    plan_text: str,
    summary_text: str,
    project_brief: dict,
) -> str:
    _ = (chapter_id, project_brief)  # reserved for future heuristics
    primary_terms = _extract_priority_terms(plan_text)
    if not primary_terms and summary_text:
        primary_terms = _extract_keywords(summary_text)
    if not primary_terms:
        primary_terms = _extract_keywords(plan_text)

    fallback_terms = _extract_keywords(_sample_text_for_keywords(chapter_text))
    if not fallback_terms:
        fallback_terms = _top_bigrams(_sample_text_for_keywords(chapter_text))

    primary = (primary_terms or fallback_terms or [""])[0]
    secondary = (primary_terms or fallback_terms)[1] if len(primary_terms or fallback_terms) > 1 else ""
    title = _compose_title(primary, secondary)
    return title or _FALLBACK_TITLE


def _extract_priority_terms(text: str) -> list[str]:
    segments: list[str] = []
    lines = text.splitlines()
    for line in lines:
        if any(hint in line for hint in _PRIORITY_HINTS):
            segments.append(line)
    if not segments:
        segments = lines[-8:]
    return _extract_keywords("\n".join(segments))


def _extract_keywords(text: str) -> list[str]:
    hits = [kw for kw in _DOMAIN_KEYWORDS if kw in text]
    return hits


def _sample_text_for_keywords(text: str) -> str:
    if not text:
        return ""
    n = len(text)
    if n < 200:
        return text
    third = max(1, n // 3)
    return text[:third] + "\n" + text[-third:]


def _top_bigrams(text: str, *, limit: int = 6) -> list[str]:
    chars = [ch for ch in text if _is_cjk(ch)]
    counts: Counter[str] = Counter()
    for i in range(len(chars) - 1):
        bigram = chars[i] + chars[i + 1]
        if _is_noise_bigram(bigram):
            continue
        counts[bigram] += 1
    return [bg for bg, _ in counts.most_common(limit)]


def _is_cjk(ch: str) -> bool:
    return bool(_CJK_RE.fullmatch(ch))


def _is_noise_bigram(bigram: str) -> bool:
    return any(ch in _STOP_CHARS for ch in bigram)


def _compose_title(primary: str, secondary: str) -> str:
    candidates: list[str] = []

    if _has_any(primary, ("徭役", "名册", "差役")):
        candidates.extend(["徭役名册压到我家", "差役点名逼上门"])
    if _has_any(primary, ("邻居", "造谣")):
        candidates.extend(["邻居造谣我先吃亏", "井边斗嘴先忍了"])
    if _has_any(primary, ("断粮", "粮缸", "饥荒", "荒年")):
        candidates.extend(["断粮夜的一碗粥", "荒年先保一口粮"])
    if _has_any(primary, ("省柴", "闷煮", "粥")):
        candidates.append("省柴闷煮救全家")
    if _has_any(primary, ("井", "水", "水源")):
        candidates.append("井边起事我忍了")

    if primary and secondary and primary != secondary:
        candidates.append(primary + secondary)
    if primary:
        candidates.extend([primary + "逼上门", primary + "压到我家", primary + "先扛住"])

    return _choose_title(candidates)


def _choose_title(candidates: Iterable[str]) -> str:
    for title in candidates:
        compact = _compact(title)
        if 6 <= len(compact) <= 12:
            return compact
    return _FALLBACK_TITLE


def _compact(text: str) -> str:
    return re.sub(r"\s+", "", text)


def _has_any(text: str, tokens: Iterable[str]) -> bool:
    return any(token in text for token in tokens)
