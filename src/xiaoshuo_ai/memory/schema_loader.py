from __future__ import annotations

"""
Schema Loader（工程核心）
作用：
1) 读取 configs/memory_ontology_v1.yaml（本体）
2) 读取 configs/profiles/default.yaml（Profile，可覆盖模块开关）
3) 合并 modules 开关（Profile 优先）
4) 根据 enabled_if / enabled_if_all 过滤实体与关系
5) 返回“生效 Schema”，供后续：KeyBuilder / Neo4jStore / PromptBuilder 使用
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict

import yaml


@dataclass(frozen=True)
class LoadedSchema:
    """加载完成后的生效 Schema（已按模块开关过滤）"""

    ontology: Dict[str, Any]
    profile: Dict[str, Any]
    modules: Dict[str, bool]
    entities: Dict[str, Dict[str, Any]]
    relations: Dict[str, Dict[str, Any]]


def _load_yaml(path: Path) -> Dict[str, Any]:
    """读取 YAML 文件，并确保顶层是 dict"""
    if not path.exists():
        raise FileNotFoundError(f"找不到文件：{path}")
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"YAML 顶层必须是 dict：{path}")
    return data


def _eval_enabled_if(expr: Any, modules: Dict[str, bool]) -> bool:
    """
    判断 enabled_if 是否启用
    支持格式：
      enabled_if: "modules.enable_scene"
      enabled_if: true/false
    未知格式：默认放行（避免误杀），但建议用 validate_ontology.py 提示纠正。
    """
    if expr is None:
        return True
    if isinstance(expr, bool):
        return expr
    if isinstance(expr, str) and expr.startswith("modules."):
        key = expr.split(".", 1)[1]
        return bool(modules.get(key, False))
    return True


def _eval_enabled_if_all(exprs: Any, modules: Dict[str, bool]) -> bool:
    """
    判断 enabled_if_all 是否全部满足
    支持格式：
      enabled_if_all: ["modules.enable_scene", "modules.enable_chapter"]
    """
    if exprs is None:
        return True
    if isinstance(exprs, list):
        return all(_eval_enabled_if(x, modules) for x in exprs)
    return True


def _merge_modules(ontology: Dict[str, Any], profile: Dict[str, Any]) -> Dict[str, bool]:
    """
    合并模块开关：
      - 先取 ontology.modules 作为默认
      - 再用 profile.modules 覆盖（profile 优先）
    """
    onto_modules = ontology.get("modules", {}) or {}
    prof_modules = profile.get("modules", {}) or {}

    if not isinstance(onto_modules, dict):
        onto_modules = {}
    if not isinstance(prof_modules, dict):
        prof_modules = {}

    merged: Dict[str, bool] = {}
    for k, v in onto_modules.items():
        merged[str(k)] = bool(v)
    for k, v in prof_modules.items():
        merged[str(k)] = bool(v)
    return merged


def load_schema(
    project_root: Path,
    ontology_path: str = "configs/memory_ontology_v1.yaml",
    profile_path: str = "configs/profiles/default.yaml",
) -> LoadedSchema:
    """
    对外主函数：加载并返回生效 Schema
    注意：
      - profile 可不存在，不影响 ontology 默认 modules
      - entities/relations 会按 enabled_if / enabled_if_all 做过滤
    """
    ontology_file = project_root / ontology_path
    profile_file = project_root / profile_path

    ontology = _load_yaml(ontology_file)

    profile: Dict[str, Any] = {}
    if profile_file.exists():
        profile = _load_yaml(profile_file)

    modules = _merge_modules(ontology, profile)

    entities_raw = ontology.get("entities", {}) or {}
    relations_raw = ontology.get("relations", {}) or {}

    if not isinstance(entities_raw, dict):
        raise ValueError("ontology.entities 必须是 dict")
    if not isinstance(relations_raw, dict):
        raise ValueError("ontology.relations 必须是 dict")

    # 过滤实体
    entities: Dict[str, Dict[str, Any]] = {}
    for ename, edef in entities_raw.items():
        if not isinstance(edef, dict):
            continue
        if not _eval_enabled_if(edef.get("enabled_if"), modules):
            continue
        entities[str(ename)] = edef

    # 过滤关系
    relations: Dict[str, Dict[str, Any]] = {}
    for rname, rdef in relations_raw.items():
        if not isinstance(rdef, dict):
            continue
        if not _eval_enabled_if(rdef.get("enabled_if"), modules):
            continue
        if not _eval_enabled_if_all(rdef.get("enabled_if_all"), modules):
            continue
        relations[str(rname)] = rdef

    return LoadedSchema(
        ontology=ontology,
        profile=profile,
        modules=modules,
        entities=entities,
        relations=relations,
    )


# 明确导出（避免出现“文件里有函数但导入不到”的误会）
__all__ = ["LoadedSchema", "load_schema"]
