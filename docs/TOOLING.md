# TOOLING

## story_metrics（写作指标报告）
用于扫描 `manuscript/` 下章节并生成指标报告。

示例：
```bash
python tools/story_metrics.py
python tools/story_metrics.py --chapter ch004
python tools/story_metrics.py --date 2025-12-23 --window 5
```

输出：
- 不带 `--date`：`runs/_metrics/metrics_report.md`
- 带 `--date`：`runs/YYYY-MM-DD/metrics_report.md`

报告指标包含：正文字符数、对话占比、开头 200 字、与前章开头相似度及警告提示等。

## build_book（拼接全书）
把 `manuscript/ch001...` 按章节顺序拼接输出为 `dist/book.txt`。

示例：
```bash
python tools/build_book.py
```

输出说明：
- 章节标题行格式：`第NNN章 《标题》`
- 正文保留，去掉 Markdown 的 `# chNNN` 与 `## 《标题》` 两行
- 章节之间用两个换行分隔

## guard_diff（手动步骤改动守卫）
用于限制手动步骤允许改动的文件范围，避免写错路径或越权修改。

示例：
```bash
python tools/guard_diff.py --step 1 --date 2025-12-23 --chapter ch004
python tools/guard_diff.py --step 2 --date 2025-12-23 --chapter ch004
python tools/guard_diff.py --step 3 --date 2025-12-23 --chapter ch004
```

说明：
- step 1 仅允许 `runs/YYYY-MM-DD/chapter_plan.md`
- step 2 仅允许 `manuscript/chNNN.md`
- step 3 仅允许 recap、state_patch 与 changelog 对应文件

## check_placeholders（占位内容检查）
用于检查关键产物是否含占位内容或替换字符，并检测编码问题。

示例：
```bash
python tools/check_placeholders.py --date 2025-12-23 --chapter ch004
```

说明：
- 仅扫描指定产物文件（缺失会提示，但不崩溃）
- 命中占位内容或替换字符将返回失败

## Windows 换行与编码建议
建议 Windows 用户执行以下配置，减少 CRLF 与编码干扰：
```bash
git config core.autocrlf false
```

## cleanup_baks（清理 .bak 备份）
按原文件分组，仅保留每组最新 2 份备份（默认预览，不执行删除）。

示例：
```bash
python tools/cleanup_baks.py
python tools/cleanup_baks.py --apply
python tools/cleanup_baks.py --keep-latest 3 --apply
```
