import json
import os
import py_compile
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path

try:
    import yaml
except ImportError:
    print("PyYAML 未安装，请先运行 `pip install -r requirements.txt`。")
    sys.exit(1)

REPO_ROOT = Path(__file__).resolve().parent.parent
TEXT_FILE_PATTERNS = [
    "README.md",
    "docs/**/*.md",
    "prompts/**/*.md",
    "configs/**/*.yaml",
    "schemas/chroma/**/*.yaml",
]
EXCLUDED_PATHS = {REPO_ROOT / "docs" / "repo_audit_report.md"}
MODULE_FILE_EXTENSIONS = {"md", "py", "yaml", "json", "cypher"}
FILE_REF_PATTERN = re.compile(
    r"\b(?P<path>(?:configs|docs|prompts|schemas|scripts|src|runtime|tests)[\w/.-]+?\.(?:md|py|yaml|json|cypher))\b"
)
MODULE_PATTERN = re.compile(r"(?<![\w.])([A-Za-z_][\w]*(?:\.[A-Za-z_][\w]*)+)(?![\w.])")
ALLOWED_MODULE_PREFIXES = {
    "xiaoshuo_ai",
    "config",
    "core",
    "agents",
    "memory",
    "domain",
    "storage",
    "utils",
}


def backup_file(path: Path) -> None:
    if not path.exists():
        return
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    backup_path = path.parent / f"{path.name}.bak-{timestamp}"
    shutil.copy2(path, backup_path)


def canonical_module_name(raw: str) -> str:
    if raw.startswith("xiaoshuo_ai."):
        return raw
    return f"xiaoshuo_ai.{raw}"


def module_to_file(module_name: str) -> Path:
    module_path = Path(*module_name.split("."))
    return REPO_ROOT / "src" / module_path


def module_exists(module_name: str) -> bool:
    candidate = module_to_file(module_name)
    py_file = candidate.with_suffix(".py")
    if py_file.exists():
        return True
    if candidate.is_dir() and (candidate / "__init__.py").exists():
        return True
    return False


def find_unique_candidate_for_file(basename: str) -> str | None:
    matches = list(REPO_ROOT.rglob(basename))
    if len(matches) == 1:
        return str(matches[0].relative_to(REPO_ROOT).as_posix())
    return None


def scan_text_files():
    seen = set()
    for pattern in TEXT_FILE_PATTERNS:
        for path in REPO_ROOT.glob(pattern):
            if path.is_file():
                if path in EXCLUDED_PATHS:
                    continue
                seen.add(path)
    yield from sorted(seen)


def process_file(path: Path, broken_refs, auto_fixes):
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    new_lines = []
    modified = False

    for idx, line in enumerate(lines, start=1):
        replacements = []
        # File path references
        for match in FILE_REF_PATTERN.finditer(line):
            start, end = match.span("path")
            ref = match.group("path")
            target = REPO_ROOT / Path(ref.replace("/", os.sep))
            if not target.exists():
                candidate = find_unique_candidate_for_file(Path(ref).name)
                if candidate:
                    replacements.append((start, end, candidate))
                    auto_fixes.append(
                        {
                            "file": path,
                            "line": idx,
                            "original": ref,
                            "replacement": candidate,
                        }
                    )
                    continue
                broken_refs.append(
                    {
                        "file": path,
                        "line": idx,
                        "ref": ref,
                        "reason": "目标文件不存在",
                    }
                )
        # Module references
        for match in MODULE_PATTERN.finditer(line):
            start, end = match.span(1)
            module = match.group(1)
            if module.split(".")[0] not in ALLOWED_MODULE_PREFIXES:
                continue
            if module.split(".")[-1] in MODULE_FILE_EXTENSIONS:
                continue
            if module_exists(module):
                continue
            canonical = canonical_module_name(module)
            if module == canonical:
                broken_refs.append(
                    {
                        "file": path,
                        "line": idx,
                        "ref": module,
                        "reason": "模块路径无法定位",
                    }
                )
                continue
            if module_exists(canonical):
                replacements.append((start, end, canonical))
                auto_fixes.append(
                    {
                        "file": path,
                        "line": idx,
                        "original": module,
                        "replacement": canonical,
                    }
                )
            else:
                broken_refs.append(
                    {
                        "file": path,
                        "line": idx,
                        "ref": module,
                        "reason": "模块路径无法定位",
                    }
                )
        if replacements:
            modified = True
            replacements.sort(key=lambda x: x[0], reverse=True)
            new_line = line
            for start, end, replacement in replacements:
                new_line = new_line[:start] + replacement + new_line[end:]
            new_lines.append(new_line)
        else:
            new_lines.append(line)

    if modified:
        backup_file(path)
        path.write_text("\n".join(new_lines) + "\n", encoding="utf-8")


def ensure_init_files():
    created = []
    base = REPO_ROOT / "src" / "xiaoshuo_ai"
    for dirpath, dirnames, filenames in os.walk(base):
        if "__pycache__" in dirpath:
            continue
        dir_path = Path(dirpath)
        init_file = dir_path / "__init__.py"
        if not init_file.exists():
            init_file.write_text("# Placeholder package initializer.\n", encoding="utf-8")
            created.append(init_file.relative_to(REPO_ROOT))
    return created


def run_compile_check() -> list[dict]:
    errors = []
    targets = [REPO_ROOT / "src", REPO_ROOT / "scripts"]
    for target in targets:
        if not target.exists():
            continue
        for py_file in target.rglob("*.py"):
            try:
                py_compile.compile(str(py_file), doraise=True)
            except py_compile.PyCompileError as exc:
                errors.append(
                    {
                        "file": py_file,
                        "error": str(exc),
                    }
                )
    return errors


def validate_json() -> list[dict]:
    results = []
    for path in sorted((REPO_ROOT / "schemas" / "json").glob("*.json")):
        try:
            json.loads(path.read_text(encoding="utf-8-sig"))
            results.append({"file": path, "result": "PASS"})
        except Exception as exc:
            results.append({"file": path, "result": "FAIL", "reason": str(exc)})
    return results


def validate_yaml() -> list[dict]:
    results = []
    yaml_paths = sorted((REPO_ROOT / "configs").glob("*.yaml")) + sorted(
        (REPO_ROOT / "schemas" / "chroma").glob("*.yaml")
    )
    for path in yaml_paths:
        try:
            yaml.safe_load(path.read_text(encoding="utf-8"))
            results.append({"file": path, "result": "PASS"})
        except Exception as exc:
            results.append({"file": path, "result": "FAIL", "reason": str(exc)})
    return results


def generate_report(
    broken_refs,
    auto_fixes,
    compile_errors,
    json_results,
    yaml_results,
    init_created,
):
    errors = len(broken_refs) + len(compile_errors) + sum(
        1 for item in json_results if item["result"] == "FAIL"
    ) + sum(1 for item in yaml_results if item["result"] == "FAIL")
    warnings = 0
    report_path = REPO_ROOT / "docs" / "repo_audit_report.md"
    backup_file(report_path)
    lines = [
        "# Repository Audit Report",
        "",
        "## Summary",
        f"- Result: {'PASS' if errors == 0 else 'FAIL'}",
        f"- Errors: {errors}",
        f"- Warnings: {warnings}",
        "",
        "## Broken references",
        "",
    ]
    if broken_refs:
        for ref in broken_refs:
            rel = ref["file"].relative_to(REPO_ROOT).as_posix()
            lines.append(f"- `{rel}`:{ref['line']} ({ref['ref']}) - {ref['reason']}")
    else:
        lines.append("- None")
    lines.extend(
        [
            "",
            "## Auto-fixed references",
            "",
        ]
    )
    if auto_fixes:
        for fix in auto_fixes:
            rel = fix["file"].relative_to(REPO_ROOT).as_posix()
            lines.append(
                f"- `{rel}`:{fix['line']} - `{fix['original']}` -> `{fix['replacement']}`"
            )
    else:
        lines.append("- None")
    lines.extend(
        [
            "",
            "## Python compile results",
            "",
        ]
    )
    if compile_errors:
        for err in compile_errors:
                rel = err["file"].relative_to(REPO_ROOT).as_posix()
                lines.append(f"- `{rel}` - {err['error']}")
    else:
        lines.append("- All python files compile successfully.")
    lines.extend(
        [
            "",
            "## JSON validation",
            "",
        ]
    )
    if json_results:
        for item in json_results:
            rel = item["file"].relative_to(REPO_ROOT).as_posix()
            lines.append(
                f"- `{rel}` - {item['result']}"
                + (f" ({item.get('reason')})" if item.get("reason") else "")
            )
    else:
        lines.append("- No JSON files found.")
    lines.extend(
        [
            "",
            "## YAML validation",
            "",
        ]
    )
    if yaml_results:
        for item in yaml_results:
            rel = item["file"].relative_to(REPO_ROOT).as_posix()
            lines.append(
                f"- `{rel}` - {item['result']}"
                + (f" ({item.get('reason')})" if item.get("reason") else "")
            )
    else:
        lines.append("- No YAML files found.")
    if init_created:
        lines.extend(
            [
                "",
                "## Generated __init__.py files",
                "",
            ]
        )
        for path in init_created:
            lines.append(f"- `{path.as_posix()}`")
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return errors


def main():
    broken_refs = []
    auto_fixes = []
    for path in scan_text_files():
        process_file(path, broken_refs, auto_fixes)

    init_created = ensure_init_files()
    compile_errors = run_compile_check()
    json_results = validate_json()
    yaml_results = validate_yaml()

    errors = generate_report(
        broken_refs,
        auto_fixes,
        compile_errors,
        json_results,
        yaml_results,
        init_created,
    )
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
