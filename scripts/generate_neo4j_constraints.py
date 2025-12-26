from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any, Dict, List

try:
    import yaml  # type: ignore
except Exception:
    print("错误：缺少依赖 'pyyaml'。请先安装：pip install pyyaml", file=sys.stderr)
    sys.exit(2)


SAFE_NAME_RE = re.compile(r"[^0-9A-Za-z_]")


def load_yaml(path: Path) -> Dict[str, Any]:
    """读取 YAML 文件并确保顶层为 dict。"""
    if not path.exists():
        raise FileNotFoundError(f"未找到文件：{path}")
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("YAML 顶层必须是 dict")
    return data


def sanitize(name: str) -> str:
    """把名称转换为 Neo4j 可用的安全标识符（字母数字下划线）。"""
    name = SAFE_NAME_RE.sub("_", name)
    name = re.sub(r"_+", "_", name).strip("_")
    if not name:
        return "x"
    return name


def eval_enabled_if(cond: Any, modules: Dict[str, Any]) -> bool:
    """
    支持 enabled_if:
      - true/false
      - "modules.xxx"
    其它情况默认 True（尽量容错）。
    """
    if cond is None:
        return True
    if isinstance(cond, bool):
        return cond
    if isinstance(cond, str) and cond.startswith("modules."):
        key = cond.split(".", 1)[1]
        return bool(modules.get(key, False))
    return True


def eval_enabled_if_all(conds: Any, modules: Dict[str, Any]) -> bool:
    """支持 enabled_if_all: [cond1, cond2, ...]"""
    if conds is None:
        return True
    if isinstance(conds, list):
        return all(eval_enabled_if(c, modules) for c in conds)
    return True


def entity_enabled(e: Dict[str, Any], modules: Dict[str, Any]) -> bool:
    """实体是否启用。"""
    return eval_enabled_if(e.get("enabled_if"), modules) and eval_enabled_if_all(e.get("enabled_if_all"), modules)


def make_unique_constraint(label: str, props: List[str], suffix: str) -> str:
    """
    Neo4j 5+ 语法：
      - 单字段：REQUIRE n.p IS UNIQUE
      - 多字段：REQUIRE (n.p1, n.p2) IS UNIQUE
    """
    cname = sanitize(f"{label}_{suffix}_unique")
    if len(props) == 1:
        return f"CREATE CONSTRAINT {cname} IF NOT EXISTS FOR (n:{label}) REQUIRE n.{props[0]} IS UNIQUE;"
    inside = ", ".join([f"n.{p}" for p in props])
    return f"CREATE CONSTRAINT {cname} IF NOT EXISTS FOR (n:{label}) REQUIRE ({inside}) IS UNIQUE;"


def make_index(label: str, props: List[str], suffix: str) -> str:
    """
    Neo4j 5+ 语法：
      - 单字段：ON (n.p)
      - 多字段：ON (n.p1, n.p2)
    """
    iname = sanitize(f"{label}_{suffix}_idx")
    inside = ", ".join([f"n.{p}" for p in props])
    return f"CREATE INDEX {iname} IF NOT EXISTS FOR (n:{label}) ON ({inside});"


def scoped(props: List[str], project_prop: str, enable_project_scope: bool) -> List[str]:
    """
    将约束/索引字段“按项目隔离”：
    - 开启：在最前面加 project_prop（默认 project_id）
    - 关闭：保持原样（兼容旧库）
    """
    if not enable_project_scope:
        return props
    # 避免重复
    if project_prop in props:
        return props
    return [project_prop] + props


def main() -> None:
    parser = argparse.ArgumentParser(description="根据 memory ontology 生成 Neo4j 约束/索引（支持 project_id 隔离）")
    parser.add_argument("--ontology", default="configs/memory_ontology_v1.yaml")
    parser.add_argument("--out", default="scripts/neo4j_constraints.cypher")
    parser.add_argument(
        "--with-unique-keys-constraints",
        action="store_true",
        help="额外生成实体 unique_keys 的唯一约束（建议生产打开）。",
    )

    # 新增：项目隔离开关
    parser.add_argument(
        "--no-project-scope",
        action="store_true",
        help="关闭 project_id 隔离（回退为旧的全局唯一约束/索引）。不建议在多项目写作场景使用。",
    )
    parser.add_argument(
        "--project-prop",
        default="project_id",
        help="项目隔离字段名，默认 project_id。",
    )

    args = parser.parse_args()

    enable_project_scope = not args.no_project_scope
    project_prop = str(args.project_prop).strip() or "project_id"

    root = Path(__file__).resolve().parents[1]
    onto_path = (root / args.ontology).resolve()
    out_path = (root / args.out).resolve()

    try:
        onto = load_yaml(onto_path)
    except Exception as ex:
        print(f"[generate_neo4j_constraints] 错误：{ex}", file=sys.stderr)
        sys.exit(2)

    modules = onto.get("modules", {}) or {}
    entities: Dict[str, Any] = onto.get("entities", {}) or {}

    lines: List[str] = []
    lines.append("// 自动生成：scripts/generate_neo4j_constraints.py")
    lines.append("// 用途：在 Neo4j Browser 或 cypher-shell 中执行。可重复执行（IF NOT EXISTS）。")
    if enable_project_scope:
        lines.append(f"// 当前模式：开启项目隔离（组合唯一/组合索引），隔离字段：{project_prop}")
        lines.append("// 重要：若旧库存在“全局唯一约束”（例如 _key 唯一），需要先 DROP 再应用本文件。")
        lines.append("// 建议：先为历史数据补齐 project_id（例如 legacy_default），再做约束迁移。")
    else:
        lines.append("// 当前模式：关闭项目隔离（旧模式：全局唯一约束/索引）")
    lines.append("")

    for ename, e in entities.items():
        if not isinstance(e, dict):
            continue
        if not entity_enabled(e, modules):
            continue

        label = e.get("label") or ename
        fields = e.get("fields", {}) or {}
        ukeys = e.get("unique_keys", []) or []

        # 1) 基础唯一约束（推荐）
        #    说明：为兼容“旧数据/旧版本 _id 生成逻辑”，这里也按 project_id 做组合唯一更稳妥
        lines.append(make_unique_constraint(label, scoped(["_id"], project_prop, enable_project_scope), "id"))
        lines.append(make_unique_constraint(label, scoped(["_key"], project_prop, enable_project_scope), "key"))

        # 2) 可选：把 ontology 里声明的 unique_keys 也做 DB 级唯一（强烈建议生产打开）
        if args.with_unique_keys_constraints:
            if isinstance(ukeys, list) and all(isinstance(x, str) for x in ukeys) and len(ukeys) > 0:
                if isinstance(fields, dict) and all(k in fields for k in ukeys):
                    suffix = "ukeys_" + "_".join(ukeys)
                    lines.append(
                        make_unique_constraint(
                            label,
                            scoped(list(ukeys), project_prop, enable_project_scope),
                            suffix,
                        )
                    )

        # 3) 建议索引（非唯一）
        #    注意：若你开启了 unique_keys 唯一约束，Neo4j 会自动建索引；这里的索引主要为“未启用 unique_keys 约束”时兜底
        if isinstance(fields, dict):
            # 按项目隔离的组合索引（更符合查询习惯：WHERE project_id=... AND name/key=...）
            if enable_project_scope and project_prop in (fields.keys() | {project_prop}):
                # project_id 本身也给个索引（便于过滤）
                lines.append(make_index(label, [project_prop], "project"))

            if "name" in fields:
                lines.append(make_index(label, scoped(["name"], project_prop, enable_project_scope), "name"))
            if "key" in fields:
                lines.append(make_index(label, scoped(["key"], project_prop, enable_project_scope), "key"))
            if "chapter_no" in fields:
                lines.append(make_index(label, scoped(["chapter_no"], project_prop, enable_project_scope), "chapter_no"))
            if "location_name" in fields:
                lines.append(
                    make_index(label, scoped(["location_name"], project_prop, enable_project_scope), "location_name")
                )

        lines.append("")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"[generate_neo4j_constraints] 已生成：{out_path}")

    print("\n下一步：")
    print("  1) 打开并检查 cypher 文件：")
    print(f"     - {out_path}")
    print("  2) 在 Neo4j Browser（或 cypher-shell）中执行该文件内容。")
    if not args.with_unique_keys_constraints:
        print("  提示：加上 --with-unique-keys-constraints 可把 ontology 的 unique_keys 也升级为 DB 级唯一（生产建议开启）。")
    if enable_project_scope:
        print("  注意：若当前库仍存在旧的“全局唯一约束”（例如 _key 唯一），请先 DROP 旧约束再应用组合唯一。")
        print("        （你之前的迁移脚本就是为了解决这个冲突。）")


if __name__ == "__main__":
    main()
