# RESET_REPORT

- generated_at_utc: 2025-12-19T14:37:50Z
- repo_root: E:/Lianghuagit/xiaoshuo

## 修改文件清单
- `inputs/project_brief.json`
- `canon/premise.md`
- `canon/style/style_guide.md`
- `canon/rules/world_rules.md`
- `canon/characters/characters.yaml`
- `canon/locations/locations.yaml`
- `canon/factions/factions.yaml`
- `outline/master_outline.md`
- `state/current_state.json`
- `tools/_common.py`
- `tools/run_daily.py`
- `tools/merge_state_patch.py`
- `tools/continuity_checks.py`
- `tools/create_daily_run.py`
- `tools/extract_state_patch.py`
- `tools/encoding_audit_and_fix.py`
- `runs/ENCODING_AUDIT.md`

## 关键一致性修复点
- 章节号统一为字符串 `"chNNN"`（run_daily / extract_state_patch / merge_state_patch / continuity_checks）。
- 固定全书 80 章、每章约 2500 字（project_brief + outline + state.meta）。
- project_brief 仅以 `inputs/project_brief.json` 为准（严格 JSON）。
- 默认字数优先级：`--words` > `brief.md` > `project_brief.json` > 2500。

## 自检
- `python -m compileall tools`: PASS
- `python tools/validate_repo.py`: PASS

FINAL_RESULT: PASS
