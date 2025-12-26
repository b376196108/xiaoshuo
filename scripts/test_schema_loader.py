from __future__ import annotations

"""
验收脚本：测试 Schema Loader 是否能正常加载并过滤实体/关系
运行：
  python scripts/test_schema_loader.py
"""

import sys
from pathlib import Path


def main() -> None:
    # 项目根目录：scripts 的上一级
    project_root = Path(__file__).resolve().parents[1]
    src_root = project_root / "src"

    # 兼容两种结构：
    # 1) src 布局：优先把 <root>/src 放到 sys.path
    # 2) 非 src 布局：再把 <root> 放到 sys.path 兜底
    if src_root.exists() and str(src_root) not in sys.path:
        sys.path.insert(0, str(src_root))
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))

    from xiaoshuo_ai.memory.schema_loader import load_schema  # noqa: E402

    schema = load_schema(project_root)

    print("========== Schema Loader 验收输出 ==========")
    print(f"Profile: {schema.profile.get('profile', 'N/A')}")
    print("Modules（最终生效）:")
    for k in sorted(schema.modules.keys()):
        print(f"  - {k}: {schema.modules[k]}")

    print("\nEntities（启用）:")
    for ename in sorted(schema.entities.keys()):
        label = schema.entities[ename].get("label", ename)
        ukeys = schema.entities[ename].get("unique_keys", [])
        print(f"  - {ename} (label={label}, unique_keys={ukeys})")

    print("\nRelations（启用）:")
    for rname in sorted(schema.relations.keys()):
        r = schema.relations[rname]
        frm = r.get("from")
        to = r.get("to")
        print(f"  - {rname}: {frm} -> {to}")

    print("\n统计：")
    print(f"  entities_count = {len(schema.entities)}")
    print(f"  relations_count = {len(schema.relations)}")
    print("===========================================")


if __name__ == "__main__":
    main()
