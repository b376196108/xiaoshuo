from __future__ import annotations

"""
章节附录回写（Ingest Appendix）
目标：
1) 从章节正文中抽取附录 YAML（由 begin/end 标记包裹）
2) 解析 YAML，得到 entities / relations
3) 按 ontology（schema_loader 输出的生效 schema）将实体/关系幂等写入 Neo4j
4) 允许关系引用未显式声明的实体：可自动“最小创建”（只写 unique_keys + 审计字段）
5) 【新增】project_id 项目隔离：所有写入必须带 project_id（避免多本书互相污染）

附录格式（推荐）：

===MEMORY_APPENDIX_BEGIN===
entities:
  Character:
    - name: "张三"
      gender: "male"
  Location:
    - name: "京城"
relations:
  - type: LOCATED_IN
    from:
      label: Character
      name: "张三"
    to:
      label: Location
      name: "京城"
    properties:
      chapter_no: 1
===MEMORY_APPENDIX_END===

说明：
- entities 的 key 用实体名（Character/Location/Item...）
- relations 里 from/to 需包含 label + unique_keys 对应字段（例如 Character 需要 name）
- properties 可选，用于给关系加属性（chapter_no、note 等）
"""

import os
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

import yaml

from xiaoshuo_ai.memory.schema_loader import LoadedSchema
from xiaoshuo_ai.memory.key_builder import augment_node_props
from xiaoshuo_ai.memory.neo4j_store import Neo4jStore


def _load_project_context() -> Tuple[str, str]:
    """
    读取项目隔离上下文（最小可用版本，避免额外依赖）
    环境变量：
      - XIAOSHUO_MODE: dev/prod（默认 dev）
      - XIAOSHUO_PROJECT_ID: 项目ID（dev 默认 dev_default；prod 必须显式设置）
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


@dataclass(frozen=True)
class AppendixMarkers:
    """附录标记（建议固定，便于程序稳定抽取）"""
    begin: str = "===MEMORY_APPENDIX_BEGIN==="
    end: str = "===MEMORY_APPENDIX_END==="


@dataclass(frozen=True)
class IngestReport:
    """回写报告（用于验收与日志）"""
    nodes_upserted: int
    relations_upserted: int
    nodes_by_label: Dict[str, int]
    relations_by_type: Dict[str, int]


def extract_appendix_yaml(chapter_text: str, markers: AppendixMarkers = AppendixMarkers()) -> Optional[str]:
    """
    从章节文本中抽取附录 YAML 文本（不解析）
    返回：
      - 找到则返回 YAML 字符串
      - 找不到则返回 None
    """
    if not chapter_text:
        return None

    s = chapter_text
    b = s.find(markers.begin)
    if b < 0:
        return None

    b2 = b + len(markers.begin)
    e = s.find(markers.end, b2)
    if e < 0:
        raise ValueError(f"章节附录缺少结束标记：{markers.end}")

    block = s[b2:e].strip()
    if not block:
        return None
    return block


def parse_appendix_yaml(yaml_text: str) -> Dict[str, Any]:
    """解析 YAML 文本为 dict（并做基础校验）"""
    data = yaml.safe_load(yaml_text)
    if data is None:
        return {}
    if not isinstance(data, dict):
        raise ValueError("附录 YAML 顶层必须是 dict（例如包含 entities/relations）")
    return data


def _build_label_maps(schema: LoadedSchema) -> Tuple[Dict[str, str], Dict[str, Dict[str, Any]]]:
    """
    构建映射：
    - label_to_entity_name：label -> entity_name（通常相同，但保持通用）
    - entity_defs：entity_name -> entity_def
    """
    label_to_entity_name: Dict[str, str] = {}
    entity_defs: Dict[str, Dict[str, Any]] = {}
    for entity_name, edef in schema.entities.items():
        label = str(edef.get("label", entity_name))
        label_to_entity_name[label] = entity_name
        label_to_entity_name[str(entity_name)] = entity_name
        entity_defs[entity_name] = edef
    return label_to_entity_name, entity_defs


def _resolve_entity_name(label_or_name: str, label_to_entity_name: Dict[str, str]) -> str:
    """把附录中的 label（或实体名）解析为 schema.entities 中的 entity_name"""
    if label_or_name in label_to_entity_name:
        return label_to_entity_name[label_or_name]
    raise KeyError(f"附录引用了未知实体：{label_or_name}")


def _ensure_node_exists(
    *,
    store: Neo4jStore,
    schema: LoadedSchema,
    label_to_entity_name: Dict[str, str],
    project_id: str,
    entity_label: str,
    node_spec: Dict[str, Any],
    chapter_no: int,
    default_confidence: float,
    source_type: str,
) -> Tuple[str, str]:
    """
    确保节点存在（幂等）：
    - node_spec 至少包含 unique_keys 对应字段
    - 返回 (label, _key)
    """
    entity_name = _resolve_entity_name(entity_label, label_to_entity_name)
    edef = schema.entities[entity_name]
    label = str(edef.get("label", entity_name))
    ukeys: List[str] = list(edef.get("unique_keys", []))

    # 允许用户直接提供 _key（高级用法）
    if "_key" in node_spec and node_spec["_key"]:
        # 注意：这里不自动创建节点；若你传 _key，默认你已确保节点存在
        return label, str(node_spec["_key"])

    minimal: Dict[str, Any] = {}
    for k in ukeys:
        if k not in node_spec:
            raise ValueError(f"关系端点缺少唯一键字段：label={label}, missing={k}")
        minimal[k] = node_spec[k]

    extra_props = {k: v for k, v in node_spec.items() if k not in {"label", "_key"}}
    minimal.update(extra_props)

    key, props = augment_node_props(
        label=label,
        unique_keys=ukeys,
        data=minimal,
        project_id=project_id,
        source_type=source_type,
        source_chapter_no=chapter_no,
        confidence=node_spec.get("confidence", default_confidence),
    )
    store.upsert_node(label, project_id, key, props)
    return label, key


def ingest_chapter_appendix_to_neo4j(
    *,
    chapter_text: str,
    schema: LoadedSchema,
    store: Neo4jStore,
    chapter_no: int,
    markers: AppendixMarkers = AppendixMarkers(),
    default_confidence: float = 0.85,
    strict_rel_endpoints: bool = True,
    ensure_nodes_for_relations: bool = True,
    project_id: Optional[str] = None,
) -> IngestReport:
    """
    主入口：从章节文本抽取附录并回写 Neo4j

    project_id：
    - 传入则优先使用
    - 不传则从环境变量 XIAOSHUO_PROJECT_ID 读取（dev 默认 dev_default）
    """
    _, env_pid = _load_project_context()
    pid = (project_id or env_pid).strip()
    if not pid:
        raise ValueError("project_id 不能为空（用于项目隔离）")

    yaml_text = extract_appendix_yaml(chapter_text, markers=markers)
    if not yaml_text:
        return IngestReport(0, 0, {}, {})

    payload = parse_appendix_yaml(yaml_text)
    label_to_entity_name, _ = _build_label_maps(schema)

    nodes_upserted = 0
    rels_upserted = 0
    nodes_by_label: Dict[str, int] = {}
    rels_by_type: Dict[str, int] = {}

    # ---------- 1) 写入实体 ----------
    entities_section = payload.get("entities", {}) or {}
    if entities_section and not isinstance(entities_section, dict):
        raise ValueError("entities 必须是 dict，例如 entities: {Character: [...], Location: [...]}")

    for entity_label, records in entities_section.items():
        entity_label = str(entity_label)
        entity_name = _resolve_entity_name(entity_label, label_to_entity_name)
        edef = schema.entities[entity_name]
        label = str(edef.get("label", entity_name))
        ukeys: List[str] = list(edef.get("unique_keys", []))

        if records is None:
            continue
        if not isinstance(records, list):
            raise ValueError(f"entities.{entity_label} 必须是 list")

        for rec in records:
            if not isinstance(rec, dict):
                raise ValueError(f"entities.{entity_label} 的元素必须是 dict")

            confidence = rec.get("confidence", default_confidence)

            key, props = augment_node_props(
                label=label,
                unique_keys=ukeys,
                data=rec,
                project_id=pid,
                source_type="appendix",
                source_chapter_no=chapter_no,
                confidence=confidence,
            )
            store.upsert_node(label, pid, key, props)
            nodes_upserted += 1
            nodes_by_label[label] = nodes_by_label.get(label, 0) + 1

    # ---------- 2) 写入关系 ----------
    relations_section = payload.get("relations", []) or []
    if relations_section and not isinstance(relations_section, list):
        raise ValueError("relations 必须是 list")

    for rel in relations_section:
        if not isinstance(rel, dict):
            raise ValueError("relations 的每一项必须是 dict")

        rel_type = rel.get("type")
        if not rel_type:
            raise ValueError("relation 缺少 type")
        rel_type = str(rel_type)

        if rel_type not in schema.relations:
            raise KeyError(f"附录引用了未知关系类型：{rel_type}")

        rel_def = schema.relations[rel_type]
        def_from = str(rel_def.get("from"))
        def_to = str(rel_def.get("to"))

        from_spec = rel.get("from")
        to_spec = rel.get("to")
        if not isinstance(from_spec, dict) or not isinstance(to_spec, dict):
            raise ValueError(f"relation({rel_type}) 的 from/to 必须是 dict")

        from_label = str(from_spec.get("label", def_from))
        to_label = str(to_spec.get("label", def_to))

        from_entity = _resolve_entity_name(from_label, label_to_entity_name)
        to_entity = _resolve_entity_name(to_label, label_to_entity_name)

        if strict_rel_endpoints:
            if from_entity != def_from or to_entity != def_to:
                raise ValueError(
                    f"关系端点不匹配：{rel_type} 期望 {def_from}->{def_to}，实际 {from_entity}->{to_entity}"
                )

        if ensure_nodes_for_relations:
            from_node_label, from_key = _ensure_node_exists(
                store=store,
                schema=schema,
                label_to_entity_name=label_to_entity_name,
                project_id=pid,
                entity_label=from_entity,
                node_spec=from_spec,
                chapter_no=chapter_no,
                default_confidence=default_confidence,
                source_type="appendix_ref",
            )
            to_node_label, to_key = _ensure_node_exists(
                store=store,
                schema=schema,
                label_to_entity_name=label_to_entity_name,
                project_id=pid,
                entity_label=to_entity,
                node_spec=to_spec,
                chapter_no=chapter_no,
                default_confidence=default_confidence,
                source_type="appendix_ref",
            )
        else:
            from_node_label, from_key = _ensure_node_exists(
                store=store,
                schema=schema,
                label_to_entity_name=label_to_entity_name,
                project_id=pid,
                entity_label=from_entity,
                node_spec=from_spec,
                chapter_no=chapter_no,
                default_confidence=default_confidence,
                source_type="appendix_ref",
            )
            to_node_label, to_key = _ensure_node_exists(
                store=store,
                schema=schema,
                label_to_entity_name=label_to_entity_name,
                project_id=pid,
                entity_label=to_entity,
                node_spec=to_spec,
                chapter_no=chapter_no,
                default_confidence=default_confidence,
                source_type="appendix_ref",
            )

        props = rel.get("properties", {}) or {}
        if props and not isinstance(props, dict):
            raise ValueError(f"relation({rel_type}).properties 必须是 dict")

        store.upsert_relation(
            rel_type=rel_type,
            project_id=pid,
            from_label=from_node_label,
            from_key=from_key,
            to_label=to_node_label,
            to_key=to_key,
            props=props,
        )
        rels_upserted += 1
        rels_by_type[rel_type] = rels_by_type.get(rel_type, 0) + 1

    return IngestReport(
        nodes_upserted=nodes_upserted,
        relations_upserted=rels_upserted,
        nodes_by_label=nodes_by_label,
        relations_by_type=rels_by_type,
    )
