# Windows 任务计划程序（每日 08:00）配置指南

> 重要：真正“无人值守写章”需要本机安装 `codex` CLI。仅靠 VSCode 插件无法被任务计划程序直接调用来生成章节内容（插件运行在编辑器交互环境中）。

## 方案 A（推荐）：调度 `scripts\\run_daily.bat`

1) 打开：任务计划程序（Task Scheduler）
2) 选择：创建基本任务（Create Basic Task）
3) 触发器（Trigger）：每日（Daily），时间设置为 08:00
4) 操作（Action）：启动程序（Start a program）
   - 程序/脚本（Program/script）：
     - `C:\\path\\to\\xiaoshuo\\scripts\\run_daily.bat`
   - 添加参数（Add arguments，可选）：
     - 例：`--words 2000`
   - 起始于（Start in）：
     - `C:\\path\\to\\xiaoshuo`

## 方案 B：直接调度 Python（可选）

若希望直接调用 Python（不通过 bat），请确保填写“起始于”：

- 程序/脚本：`C:\\path\\to\\python.exe`
- 添加参数：`tools\\run_daily.py --words 2000`
- 起始于：`C:\\path\\to\\xiaoshuo`

## 运行结果与排障

- 当日目录：`runs\\YYYY-MM-DD\\`
- codex 执行日志：
  - `runs\\YYYY-MM-DD\\codex_stdout.log`
  - `runs\\YYYY-MM-DD\\codex_stderr.log`
- QA 报告：`runs\\YYYY-MM-DD\\qa_report.md`

### 常见情况
- 未安装 `codex` CLI：`tools\\run_daily.py` 会生成 `runs\\YYYY-MM-DD\\manual_codex_instructions.md` 并返回非 0（任务计划程序会显示“失败”，这是预期行为）。
- QA_RESULT: FAIL：不会合并 `state\\state_patch.json`，请按 `qa_report.md` 的返工步骤修复后重跑。

