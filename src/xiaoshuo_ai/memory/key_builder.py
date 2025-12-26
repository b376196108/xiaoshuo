from __future__ import annotations

"""
Key Builder（工程核心）

用途：
- 为所有实体生成稳定、可重复、可幂等写入的关键字段：
  - _key  ：自然键（由 label + unique_keys 拼接，Neo4j 写入时用于 MERGE）
  - _id   ：稳定哈希 ID（用于日志追踪/跨系统引用）
  - _hash ：用于快速一致性校验（可选）

【生产级关键升级：project_id 项目隔离】
- _id 的哈希输入加入 project_id，确保“多本书/多项目”同名同键不会撞车
- props 强制写入 project_id，便于查询过滤与约束迁移

兼容策略：
- augment_node_props 支持不传 project_id（为兼容老代码）：
  - dev：默认使用环境变量 XIAOSHUO_PROJECT_ID，否则用 dev_default
  - prod：必须显式设置 XIAOSHUO_PROJECT_ID，且不能是默认值
"""

import hashlib
import os
import re
import time
from typing import Any, Dict, List, Optional, Tuple


# ---------------------------
# 1) 文本规范化（基础实现）
# ---------------------------

_WS_RE = re.compile(r"\s+")
_QUOTE_RE = re.compile(r"[“”‘’]")
_DASH_RE = re.compile(r"[–—－]")


def _to_halfwidth(s: str) -> str:
    """全角转半角（覆盖常见字符范围）"""
    out: List[str] = []
    for ch in s:
        code = ord(ch)
        if code == 0x3000:  # 全角空格
            out.append(" ")
        elif 0xFF01 <= code <= 0xFF5E:  # 全角标点/字母/数字
            out.append(chr(code - 0xFEE0))
        else:
            out.append(ch)
    return "".join(out)


def normalize_text(s: str) -> str:
    """
    文本规范化（基础版本）：
    - trim
    - 全角转半角
    - 多空白折叠
    - 引号统一
    - 破折号统一
    - 英文大小写折叠（casefold；中文不受影响）
    """
    s = (s or "").strip()
    s = _to_halfwidth(s)
    s = _WS_RE.sub(" ", s)
    s = _QUOTE_RE.sub('"', s)
    s = _DASH_RE.sub("-", s)
    s = s.casefold()
    return s


# ---------------------------
# 2) project_id / mode 读取
# ---------------------------

def _load_project_context() -> Tuple[str, str]:
    """
    读取运行模式与项目 ID
    环境变量：
      - XIAOSHUO_MODE: dev/prod（默认 dev）
      - XIAOSHUO_PROJECT_ID: 项目ID（dev 可默认；prod 必须显式设置）
    """
    mode = (os.getenv("XIAOSHUO_MODE", "dev") or "dev").strip().lower()
    project_id = (os.getenv("XIAOSHUO_PROJECT_ID", "") or "").strip()

    if mode not in {"dev", "prod"}:
        raise ValueError("XIAOSHUO_MODE 只能是 dev 或 prod")

    if not project_id:
        project_id = "dev_default" if mode == "dev" else ""

    # prod 下强制要求显式设置，且不能用默认值（防止误写）
    if mode == "prod" and project_id in {"", "dev_default", "default", "demo"}:
        raise ValueError("prod 模式必须显式设置一个非默认的 XIAOSHUO_PROJECT_ID（例如 book_001）")

    return mode, project_id


# ---------------------------
# 3) _key / _id / _hash
# ---------------------------

def build_key(label: str, unique_keys: List[str], data: Dict[str, Any]) -> str:
    """
    构建自然键 _key
    格式：Label|k1=v1|k2=v2

    注意：
    - _key 不强制包含 project_id
    - 在 Neo4j 侧建议用 (project_id, _key) 做组合唯一与 MERGE 条件
    """
    parts = [label]
    for k in unique_keys:
        if k not in data:
            raise ValueError(f"缺少 unique_keys 字段：label={label}, missing={k}")
        v = data.get(k)
        if isinstance(v, str):
            v_str = normalize_text(v)
        else:
            v_str = str(v)
        parts.append(f"{k}={v_str}")
    return "|".join(parts)


def build_id(project_id: str, label: str, key: str, length: int = 12) -> str:
    """
    构建稳定 ID（加入 project_id，确保跨项目不撞车）
    格式：{label}_{sha1(project_id|label|key)[:length]}
    """
    if not project_id:
        raise ValueError("project_id 不能为空（用于项目隔离）")

    h = hashlib.sha1(f"{project_id}|{label}|{key}".encode("utf-8")).hexdigest()[:length]
    return f"{label}_{h}"


def build_hash(key: str, length: int = 12) -> str:
    """构建辅助哈希（用于一致性校验）"""
    return hashlib.sha1(key.encode("utf-8")).hexdigest()[:length]


def now_ms() -> int:
    """当前毫秒时间戳（审计字段使用）"""
    return int(time.time() * 1000)


def augment_node_props(
    label: str,
    unique_keys: List[str],
    data: Dict[str, Any],
    *,
    project_id: Optional[str] = None,
    source_type: str = "manual",
    source_chapter_no: Optional[int] = None,
    confidence: Optional[float] = None,
) -> Tuple[str, Dict[str, Any]]:
    """
    将原始 data 扩展为可直接写入 Neo4j 的 props
    - 写入 project_id/_key/_id/_hash
    - 写入 updated_at/source_type/source_chapter_no/confidence

    兼容说明：
    - 若不传 project_id，则从环境变量读取（dev 默认 dev_default；prod 强约束）
    """
    mode, env_pid = _load_project_context()
    pid = (project_id or env_pid).strip()
    if mode == "prod" and pid in {"", "dev_default", "default", "demo"}:
        raise ValueError("prod 模式下 project_id 不允许为空或默认值，请设置 XIAOSHUO_PROJECT_ID")

    key = build_key(label, unique_keys, data)
    _id = build_id(pid, label, key)
    _hash = build_hash(key)

    props = dict(data)

    # 项目隔离字段（强制写入）
    props["project_id"] = pid

    # 内部稳定键
    props["_key"] = key
    props["_id"] = _id
    props["_hash"] = _hash

    # 审计字段：updated_at 每次写入都刷新；created_at 在 store 层首次创建时写入
    props["updated_at"] = now_ms()
    props["source_type"] = source_type

    if source_chapter_no is not None:
        props["source_chapter_no"] = int(source_chapter_no)
    if confidence is not None:
        props["confidence"] = float(confidence)

    return key, props
