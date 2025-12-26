from __future__ import annotations

"""
验收脚本：Neo4j 幂等写入（远端）
目标：
1) 插入 1 个角色 + 1 个地点 + 1 条 LOCATED_IN 关系
2) 连续写入 3 次
3) 最终数据库里仍然是：角色=1、地点=1、关系=1（同一 project_id 下）

运行前请先设置环境变量（Windows PowerShell 示例）：
  $env:NEO4J_URI="bolt://192.168.1.195:7687"
  $env:NEO4J_USER="neo4j"
  $env:NEO4J_PASSWORD="你的密码"

【新增：项目隔离】
  $env:XIAOSHUO_MODE="dev"
  $env:XIAOSHUO_PROJECT_ID="book_demo_001"
"""

import os
import sys
from pathlib import Path


def _load_project_context() -> tuple[str, str]:
    """读取项目隔离上下文（与 ingest_appendix 保持一致）"""
    mode = (os.getenv("XIAOSHUO_MODE", "dev") or "dev").strip().lower()
    project_id = (os.getenv("XIAOSHUO_PROJECT_ID", "") or "").strip()

    if mode not in {"dev", "prod"}:
        raise ValueError("XIAOSHUO_MODE 只能是 dev 或 prod")

    if not project_id:
        project_id = "dev_default" if mode == "dev" else ""

    if mode == "prod" and not project_id:
        raise ValueError("prod 模式必须显式设置 XIAOSHUO_PROJECT_ID（例如 book_001）")

    return mode, project_id


def main() -> None:
    project_root = Path(__file__).resolve().parents[1]
    src_root = project_root / "src"

    # src 布局：把 <root>/src 加入 sys.path，保证能 import 包
    if src_root.exists() and str(src_root) not in sys.path:
        sys.path.insert(0, str(src_root))
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))

    from xiaoshuo_ai.memory.schema_loader import load_schema  # noqa: E402
    from xiaoshuo_ai.memory.key_builder import augment_node_props  # noqa: E402
    from xiaoshuo_ai.memory.neo4j_store import Neo4jStore, load_neo4j_config_from_env  # noqa: E402

    _, project_id = _load_project_context()
    schema = load_schema(project_root)

    # 取实体定义（用 ontology 中的 unique_keys 生成 _key）
    char_def = schema.entities["Character"]
    loc_def = schema.entities["Location"]

    char_label = char_def.get("label", "Character")
    loc_label = loc_def.get("label", "Location")

    char_ukeys = list(char_def["unique_keys"])
    loc_ukeys = list(loc_def["unique_keys"])

    # 固定测试数据（避免污染真实数据与重名冲突）
    char = {
        "name": "TEST_角色_001",
        "gender": "unknown",
        "age_range": "未知",
        "occupation": "测试角色",
        "status": "active",
        "notes": "仅用于幂等写入验收",
    }
    loc = {
        "name": "TEST_地点_001",
        "type": "测试地点",
        "region": "测试区域",
        "security_level": "unknown",
        "notes": "仅用于幂等写入验收",
    }

    c_key, c_props = augment_node_props(
        char_label,
        char_ukeys,
        char,
        project_id=project_id,
        source_type="manual",
        source_chapter_no=1,
        confidence=1.0,
    )
    l_key, l_props = augment_node_props(
        loc_label,
        loc_ukeys,
        loc,
        project_id=project_id,
        source_type="manual",
        source_chapter_no=1,
        confidence=1.0,
    )

    store = Neo4jStore(load_neo4j_config_from_env())
    try:
        # 连续写入 3 次（验收幂等）
        for _ in range(3):
            store.upsert_node(char_label, project_id, c_key, c_props)
            store.upsert_node(loc_label, project_id, l_key, l_props)

            store.upsert_relation(
                rel_type="LOCATED_IN",
                project_id=project_id,
                from_label=char_label,
                from_key=c_key,
                to_label=loc_label,
                to_key=l_key,
                props={"chapter_no": 1, "note": "测试关系"},
            )

        print("========== Neo4j 幂等写入验收输出（按项目隔离） ==========")
        print("project_id:", project_id)
        print("Character 节点数:", store.count_nodes("Character", project_id))
        print("Location  节点数:", store.count_nodes("Location", project_id))
        print("LOCATED_IN 关系数:", store.count_rels("LOCATED_IN", project_id))
        print("========================================================")

    finally:
        store.close()


if __name__ == "__main__":
    main()
