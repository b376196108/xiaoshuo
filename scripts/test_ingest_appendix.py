from __future__ import annotations

"""
验收脚本：章节附录解析 + 回写 Neo4j（远端，支持 project_id 隔离）
运行前（Windows PowerShell）：
  # Neo4j 连接信息
  $env:NEO4J_URI="bolt://192.168.1.195:7687"
  $env:NEO4J_USER="neo4j"
  $env:NEO4J_PASSWORD="你的密码"

  # 项目隔离（强烈建议必设）
  $env:XIAOSHUO_MODE="dev"              # dev/prod（默认 dev）
  $env:XIAOSHUO_PROJECT_ID="book_demo_001"

运行：
  python scripts/test_ingest_appendix.py

说明：
- 本脚本写入 TEST_APPENDIX_ 前缀数据，避免污染真实数据
- 同一 project_id 下重复运行不应继续增长（幂等写入验收）
- 统计口径会强制过滤 project_id，避免被库里其它项目的数据干扰
"""

import os
import sys
from pathlib import Path


def _load_project_context() -> tuple[str, str]:
    """
    读取项目隔离上下文
    - dev：若未设置 XIAOSHUO_PROJECT_ID，则默认 dev_default（便于验收）
    - prod：必须显式设置 XIAOSHUO_PROJECT_ID，防止误写默认项目
    """
    mode = (os.getenv("XIAOSHUO_MODE", "dev") or "dev").strip().lower()
    project_id = (os.getenv("XIAOSHUO_PROJECT_ID", "") or "").strip()

    if mode not in {"dev", "prod"}:
        raise ValueError("XIAOSHUO_MODE 只能是 dev 或 prod")

    if not project_id:
        project_id = "dev_default" if mode == "dev" else ""

    if mode == "prod" and not project_id:
        raise ValueError("prod 模式必须显式设置 XIAOSHUO_PROJECT_ID（例如 book_001）")

    return mode, project_id


def _count_by_prefix(store, project_id: str, label: str, prop: str, prefix_lower: str) -> int:
    """
    按属性前缀统计（只用于验收）
    注意：
    - Neo4j 5 不支持 exists(n.prop)，用 n.prop IS NOT NULL
    - 强制过滤 project_id，避免不同项目数据互相干扰
    """
    cypher = f"""
    MATCH (n:{label})
    WHERE n.project_id = $pid
      AND n.{prop} IS NOT NULL
      AND toLower(n.{prop}) STARTS WITH $p
    RETURN count(n) AS c
    """
    with store.driver.session(database=store.cfg.database) as session:
        rec = session.run(cypher, pid=project_id, p=prefix_lower).single()
        return int(rec["c"]) if rec else 0


def main() -> None:
    project_root = Path(__file__).resolve().parents[1]
    src_root = project_root / "src"

    # src 布局：把 <root>/src 加入 sys.path，保证 import 正常
    if src_root.exists() and str(src_root) not in sys.path:
        sys.path.insert(0, str(src_root))
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))

    from xiaoshuo_ai.memory.schema_loader import load_schema  # noqa: E402
    from xiaoshuo_ai.memory.neo4j_store import Neo4jStore, load_neo4j_config_from_env  # noqa: E402
    from xiaoshuo_ai.memory.ingest_appendix import ingest_chapter_appendix_to_neo4j  # noqa: E402

    mode, project_id = _load_project_context()

    schema = load_schema(project_root)
    store = Neo4jStore(load_neo4j_config_from_env())

    chapter_no = 2
    key_prefix = f"ch{chapter_no}_".lower()  # 统计 Event/Scene 的 key 前缀（小写）

    # 重要：这里不要用 f-string，避免 YAML 内部出现 {label: ...} 时被 Python 解析
    chapter_template = """
第{chapter_no}章：铜牌

夜雨把旧城洗得发亮。阿九在巷口拾到一块铜牌，冰凉，像是从谁的命里掉出来的。
他抬头，看见墙角的影子动了一下——青衣会的人，来了。

===MEMORY_APPENDIX_BEGIN===
entities:
  Character:
    - name: "TEST_APPENDIX_阿九"
      gender: "unknown"
      occupation: "跑腿"
  Location:
    - name: "TEST_APPENDIX_旧城"
      type: "城区"
      region: "本市"
  Item:
    - name: "TEST_APPENDIX_铜牌"
      type: "道具"
      notes: "背面有划痕"
  Skill:
    - name: "TEST_APPENDIX_踏雪无痕"
  Faction:
    - name: "TEST_APPENDIX_青衣会"
  PlotThread:
    - key: "PT001"
      name: "铜牌之谜"
  Event:
    - key: "CH{chapter_no}_E001"
      chapter_no: {chapter_no}
      summary: "阿九在旧城拾到铜牌"
  Scene:
    - key: "CH{chapter_no}_S001"
      chapter_no: {chapter_no}
      location_name: "TEST_APPENDIX_旧城"
  Chapter:
    - chapter_no: {chapter_no}
      title: "铜牌"
      hook: "夜雨里的一块铜牌"

relations:
  - type: LOCATED_IN
    from:
      label: Character
      name: "TEST_APPENDIX_阿九"
    to:
      label: Location
      name: "TEST_APPENDIX_旧城"
    properties:
      chapter_no: {chapter_no}

  - type: OWNS
    from:
      label: Character
      name: "TEST_APPENDIX_阿九"
    to:
      label: Item
      name: "TEST_APPENDIX_铜牌"
      type: "道具"
    properties:
      chapter_no: {chapter_no}
      note: "拾到并藏起"

  - type: HAS_SKILL
    from:
      label: Character
      name: "TEST_APPENDIX_阿九"
    to:
      label: Skill
      name: "TEST_APPENDIX_踏雪无痕"
    properties:
      chapter_no: {chapter_no}

  - type: MEMBER_OF
    from:
      label: Character
      name: "TEST_APPENDIX_阿九"
    to:
      label: Faction
      name: "TEST_APPENDIX_青衣会"
    properties:
      chapter_no: {chapter_no}
      role: "外围"

  - type: PARTICIPATES_IN
    from:
      label: Character
      name: "TEST_APPENDIX_阿九"
    to:
      label: Event
      key: "CH{chapter_no}_E001"
    properties:
      chapter_no: {chapter_no}

  - type: TAKES_PLACE_IN
    from:
      label: Event
      key: "CH{chapter_no}_E001"
    to:
      label: Location
      name: "TEST_APPENDIX_旧城"
    properties:
      chapter_no: {chapter_no}

  - type: HAS_EVENT
    from:
      label: Chapter
      chapter_no: {chapter_no}
    to:
      label: Event
      key: "CH{chapter_no}_E001"
    properties:
      chapter_no: {chapter_no}

  - type: HAS_SCENE
    from:
      label: Chapter
      chapter_no: {chapter_no}
    to:
      label: Scene
      key: "CH{chapter_no}_S001"
    properties:
      chapter_no: {chapter_no}

  - type: SCENE_LOCATED_IN
    from:
      label: Scene
      key: "CH{chapter_no}_S001"
    to:
      label: Location
      name: "TEST_APPENDIX_旧城"
    properties:
      chapter_no: {chapter_no}

  - type: INVOLVES_THREAD
    from:
      label: Event
      key: "CH{chapter_no}_E001"
    to:
      label: PlotThread
      key: "PT001"
    properties:
      chapter_no: {chapter_no}
===MEMORY_APPENDIX_END===
"""

    chapter_text = chapter_template.format(chapter_no=chapter_no)

    try:
        # 显式传入 project_id，确保写入与统计口径完全一致
        report = ingest_chapter_appendix_to_neo4j(
            chapter_text=chapter_text,
            schema=schema,
            store=store,
            chapter_no=chapter_no,
            project_id=project_id,
        )

        print("========== Ingest 验收输出 ==========")
        print("mode:", mode)
        print("project_id:", project_id)
        print("nodes_upserted:", report.nodes_upserted)
        print("relations_upserted:", report.relations_upserted)
        print("nodes_by_label:", report.nodes_by_label)
        print("relations_by_type:", report.relations_by_type)

        # 只按 TEST_APPENDIX_ + project_id 口径验收（不受库里其他数据影响）
        prefix = "test_appendix_"
        print("\n========== TEST_APPENDIX_ 口径统计（按 project_id 过滤） ==========")
        print("Character:", _count_by_prefix(store, project_id, "Character", "name", prefix))
        print("Location :", _count_by_prefix(store, project_id, "Location", "name", prefix))
        print("Item     :", _count_by_prefix(store, project_id, "Item", "name", prefix))
        print("Skill    :", _count_by_prefix(store, project_id, "Skill", "name", prefix))
        print("Faction  :", _count_by_prefix(store, project_id, "Faction", "name", prefix))

        # Event/Scene 是按 key 前缀统计
        print("Event(key CHx_):", _count_by_prefix(store, project_id, "Event", "key", key_prefix))
        print("Scene(key CHx_):", _count_by_prefix(store, project_id, "Scene", "key", key_prefix))
        print("===================================")

    finally:
        store.close()


if __name__ == "__main__":
    main()
