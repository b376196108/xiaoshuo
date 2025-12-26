from __future__ import annotations

"""
运行时配置（工程级）
目的：
1) 统一读取环境变量：XIAOSHUO_MODE / XIAOSHUO_PROJECT_ID
2) 用于项目隔离：所有写入 Neo4j 的数据必须带 project_id
3) 生产安全阀：prod 模式必须显式指定 project_id，防止误写“默认项目”
"""

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class RuntimeConfig:
    """运行时配置"""
    mode: str          # dev / prod
    project_id: str    # 项目唯一标识（建议：book_xxx 或 project_xxx）


def load_runtime_config() -> RuntimeConfig:
    """
    读取运行时配置
    环境变量：
      - XIAOSHUO_MODE: dev/prod（默认 dev）
      - XIAOSHUO_PROJECT_ID: 项目ID（dev 默认 dev_default；prod 必须显式设置）
    """
    mode = (os.getenv("XIAOSHUO_MODE", "dev") or "dev").strip().lower()
    project_id = (os.getenv("XIAOSHUO_PROJECT_ID", "") or "").strip()

    if mode not in {"dev", "prod"}:
        raise ValueError("XIAOSHUO_MODE 只能是 dev 或 prod")

    # dev 模式允许自动落到 dev_default，方便验收
    if not project_id:
        project_id = "dev_default"

    # prod 模式必须显式指定项目ID，避免误写同一个默认项目
    if mode == "prod" and project_id in {"dev_default", "default", "demo"}:
        raise ValueError("prod 模式必须显式设置一个非默认的 XIAOSHUO_PROJECT_ID（例如 book_001）")

    return RuntimeConfig(mode=mode, project_id=project_id)
