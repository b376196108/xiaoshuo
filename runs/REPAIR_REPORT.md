# REPAIR_REPORT

- regenerated_at_utc: 2025-12-19T14:37:50Z
- repo_root: E:/Lianghuagit/xiaoshuo

## 说明
- 原报告存在乱码，已用 UTF-8 重写。
- 编码审计由 `tools/encoding_audit_and_fix.py` 生成 `runs/ENCODING_AUDIT.md`。

FINAL_RESULT: PASS

## AutoTitle Update
- appended_at_utc: 2025-12-20T01:29:07Z
- ?? AutoTitle ???`tools/chapter_title.py` ??????? chapter_plan/manuscript/summary
- ????????????????????
- UTF-8 ???open(..., encoding="utf-8", newline="
")/`safe_write_text`
- ?????`python -m compileall tools` PASS?`python tools/validate_repo.py` PASS

## Min Body Length Update
- appended_at_utc: 2025-12-20T01:44:15Z
- default_words_per_chapter: 3200 (project_brief + create_daily_run)
- hard_min_body_chars: 3000 (continuity_checks QA FAIL if below)
- run_daily target_words clamp: <3000 -> 3200
- drafter prompt: body >=3000 chars, no filler padding
- self_check: compileall PASS; validate_repo PASS
