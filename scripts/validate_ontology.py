# scripts/validate_ontology.py
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

try:
    import yaml  # type: ignore
except Exception:
    print("ERROR: Missing dependency 'pyyaml'. Install: pip install pyyaml", file=sys.stderr)
    sys.exit(2)


ALLOWED_FIELD_TYPES = {
    "str",
    "int",
    "float",
    "bool",
    "object",
    "enum",
    "list[str]",
    "list[int]",
    "list[object]",
}

# 允许的关系/实体字段 spec key（防止写错 key 名）
ALLOWED_FIELD_SPEC_KEYS = {"type", "required", "default", "desc", "enum", "min", "max"}
ALLOWED_REL_PROP_SPEC_KEYS = {"type", "required", "default", "desc", "enum", "min", "max"}


def eprint(msg: str) -> None:
    print(msg, file=sys.stderr)


def load_yaml(path: Path) -> Dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("Top-level YAML must be a mapping/dict.")
    return data


def eval_enabled_if(cond: Any, modules: Dict[str, Any]) -> bool:
    """
    支持：
      enabled_if: "modules.enable_scene"
      enabled_if_all: ["modules.enable_scene", "modules.enable_chapter"]
    """
    if cond is None:
        return True
    if isinstance(cond, bool):
        return cond
    if isinstance(cond, str):
        if cond.startswith("modules."):
            key = cond.split(".", 1)[1]
            return bool(modules.get(key, False))
        # 其他字符串一律视为 True（避免误杀）；但会在校验里提示
        return True
    return True


def eval_enabled_if_all(conds: Any, modules: Dict[str, Any]) -> bool:
    if conds is None:
        return True
    if isinstance(conds, list):
        for c in conds:
            if not eval_enabled_if(c, modules):
                return False
        return True
    # 非 list 的写法当作 True，但会报错提示
    return True


def validate_field_spec(
    who: str, field_name: str, spec: Dict[str, Any], errors: List[str], warnings: List[str], allowed_keys: set
) -> None:
    # unknown keys
    for k in spec.keys():
        if k not in allowed_keys:
            warnings.append(f"{who}.{field_name}: unknown spec key '{k}' (typo?)")

    ftype = spec.get("type")
    if ftype not in ALLOWED_FIELD_TYPES:
        errors.append(f"{who}.{field_name}: invalid type '{ftype}', allowed={sorted(ALLOWED_FIELD_TYPES)}")
        return

    required = bool(spec.get("required", False))
    if required and "default" in spec:
        # required 允许 default，但提示你确认语义
        warnings.append(f"{who}.{field_name}: required=true with default set; confirm intent.")

    if ftype == "enum":
        enum_vals = spec.get("enum")
        if not isinstance(enum_vals, list) or len(enum_vals) == 0:
            errors.append(f"{who}.{field_name}: enum must be non-empty list[str]")
        else:
            if not all(isinstance(v, str) for v in enum_vals):
                errors.append(f"{who}.{field_name}: enum values must be strings")
        if "default" in spec and isinstance(enum_vals, list) and enum_vals:
            dv = spec.get("default")
            if dv is not None and dv not in enum_vals:
                warnings.append(f"{who}.{field_name}: default '{dv}' not in enum list")

    if ftype == "int":
        if "min" in spec and not isinstance(spec["min"], int):
            errors.append(f"{who}.{field_name}: min must be int")
        if "max" in spec and not isinstance(spec["max"], int):
            errors.append(f"{who}.{field_name}: max must be int")
        if "min" in spec and "max" in spec:
            if isinstance(spec["min"], int) and isinstance(spec["max"], int) and spec["min"] > spec["max"]:
                errors.append(f"{who}.{field_name}: min > max")


def validate_ontology(onto: Dict[str, Any]) -> Tuple[bool, List[str], List[str]]:
    errors: List[str] = []
    warnings: List[str] = []

    # ---- top-level required keys ----
    for k in ["version", "name", "global", "entities", "relations"]:
        if k not in onto:
            errors.append(f"Missing top-level key: {k}")
    if errors:
        return False, errors, warnings

    modules = onto.get("modules", {}) or {}
    if not isinstance(modules, dict):
        errors.append("modules must be a dict if present")

    entities = onto.get("entities")
    relations = onto.get("relations")
    if not isinstance(entities, dict):
        errors.append("entities must be a dict")
        return False, errors, warnings
    if not isinstance(relations, dict):
        errors.append("relations must be a dict")
        return False, errors, warnings

    # ---- enabled entities map ----
    enabled_entities: Dict[str, Dict[str, Any]] = {}
    for ename, e in entities.items():
        if not isinstance(e, dict):
            errors.append(f"Entity '{ename}' must be a dict")
            continue

        if "enabled_if" in e and isinstance(e["enabled_if"], str) and not e["enabled_if"].startswith("modules."):
            warnings.append(f"Entity '{ename}': enabled_if='{e['enabled_if']}' not supported format; treated as enabled.")

        if not eval_enabled_if(e.get("enabled_if"), modules):
            continue

        enabled_entities[ename] = e

        # label
        label = e.get("label", ename)
        if not isinstance(label, str) or not label:
            errors.append(f"Entity '{ename}': label must be non-empty string")

        # unique_keys
        ukeys = e.get("unique_keys")
        if not isinstance(ukeys, list) or not all(isinstance(x, str) for x in ukeys) or len(ukeys) == 0:
            errors.append(f"Entity '{ename}': unique_keys must be non-empty list[str]")

        # fields
        fields = e.get("fields")
        if not isinstance(fields, dict) or len(fields) == 0:
            errors.append(f"Entity '{ename}': fields must be non-empty dict")
            continue

        # unique_keys must exist in fields
        if isinstance(ukeys, list) and all(isinstance(x, str) for x in ukeys):
            for k in ukeys:
                if k not in fields:
                    errors.append(f"Entity '{ename}': unique_keys '{k}' not found in fields")

        # validate each field spec
        for fname, fspec in fields.items():
            if not isinstance(fspec, dict):
                errors.append(f"Entity '{ename}' field '{fname}': spec must be dict")
                continue
            validate_field_spec(f"Entity:{ename}", fname, fspec, errors, warnings, ALLOWED_FIELD_SPEC_KEYS)

    # ---- relations ----
    for rname, r in relations.items():
        if not isinstance(r, dict):
            errors.append(f"Relation '{rname}' must be a dict")
            continue

        # enabled_if / enabled_if_all
        if "enabled_if" in r and isinstance(r["enabled_if"], str) and not r["enabled_if"].startswith("modules."):
            warnings.append(f"Relation '{rname}': enabled_if='{r['enabled_if']}' not supported format; treated as enabled.")
        if "enabled_if_all" in r and not isinstance(r["enabled_if_all"], list):
            errors.append(f"Relation '{rname}': enabled_if_all must be list[str]")

        if not eval_enabled_if(r.get("enabled_if"), modules):
            continue
        if not eval_enabled_if_all(r.get("enabled_if_all"), modules):
            continue

        frm = r.get("from")
        to = r.get("to")
        if frm not in entities:
            errors.append(f"Relation '{rname}': from='{frm}' not found in entities")
        if to not in entities:
            errors.append(f"Relation '{rname}': to='{to}' not found in entities")

        # 如果 from/to 对应实体被关闭模块禁用，也提示（避免你以为生效）
        if frm in entities and frm not in enabled_entities:
            warnings.append(f"Relation '{rname}': from entity '{frm}' is disabled by modules/enabled_if.")
        if to in entities and to not in enabled_entities:
            warnings.append(f"Relation '{rname}': to entity '{to}' is disabled by modules/enabled_if.")

        directed = r.get("directed", True)
        if not isinstance(directed, bool):
            errors.append(f"Relation '{rname}': directed must be bool")

        props = r.get("properties", {})
        if props is not None and not isinstance(props, dict):
            errors.append(f"Relation '{rname}': properties must be dict")
        elif isinstance(props, dict):
            for pname, pspec in props.items():
                if not isinstance(pspec, dict):
                    errors.append(f"Relation '{rname}' property '{pname}': spec must be dict")
                    continue
                validate_field_spec(f"Relation:{rname}", pname, pspec, errors, warnings, ALLOWED_REL_PROP_SPEC_KEYS)

    # ---- prompt_hard_memory ----
    phm = onto.get("prompt_hard_memory")
    if phm is not None:
        if not isinstance(phm, dict):
            errors.append("prompt_hard_memory must be dict[label -> list[field]]")
        else:
            for label_name, fields_list in phm.items():
                # 这里 label_name 是实体名（Character/Location/Item…）
                if label_name not in entities:
                    warnings.append(f"prompt_hard_memory: entity '{label_name}' not found in entities")
                    continue
                if not isinstance(fields_list, list) or not all(isinstance(x, str) for x in fields_list):
                    errors.append(f"prompt_hard_memory.{label_name}: must be list[str]")
                    continue
                ent_fields = entities[label_name].get("fields", {})
                if isinstance(ent_fields, dict):
                    for f in fields_list:
                        if f not in ent_fields:
                            warnings.append(f"prompt_hard_memory.{label_name}: field '{f}' not in entity fields")

    # ---- ingest_rules_v1 basic sanity ----
    ingest = onto.get("ingest_rules_v1")
    if ingest is None:
        warnings.append("Missing ingest_rules_v1: recommend defining deterministic chapter appendix ingest rules.")
    else:
        if not isinstance(ingest, dict):
            errors.append("ingest_rules_v1 must be dict")
        else:
            for k in ["require_end_of_chapter_appendix", "appendix_marker_begin", "appendix_marker_end"]:
                if k not in ingest:
                    warnings.append(f"ingest_rules_v1 missing key: {k}")

    ok = len(errors) == 0
    return ok, errors, warnings


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate memory_ontology_v1.yaml (engineering-grade sanity checks)")
    parser.add_argument(
        "--ontology",
        default="configs/memory_ontology_v1.yaml",
        help="Path to ontology yaml (default: configs/memory_ontology_v1.yaml)",
    )
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    onto_path = (root / args.ontology).resolve()

    try:
        onto = load_yaml(onto_path)
    except Exception as ex:
        eprint(f"[validate_ontology] ERROR: {ex}")
        sys.exit(2)

    ok, errors, warnings = validate_ontology(onto)

    for w in warnings:
        eprint(f"[validate_ontology] WARN: {w}")
    for e in errors:
        eprint(f"[validate_ontology] ERROR: {e}")

    if not ok:
        eprint("[validate_ontology] FAILED")
        sys.exit(1)

    print("[validate_ontology] OK")
    if warnings:
        print(f"[validate_ontology] OK with {len(warnings)} warning(s).")


if __name__ == "__main__":
    main()
