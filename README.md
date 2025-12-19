# Novel Studio

“AI 小说创作团队”工程骨架（不包含任何小说正文示例）。本仓库用于组织：设定真相源（canon）、剧情状态（state）、滚动摘要（recap）、每日流水线（pipelines）、角色分工提示词（prompts/roles）与可执行工具脚本（tools）。

## 快速开始

1) 填写生产输入：`inputs/project_brief.json`
2)（可选）完善：`canon/`、`outline/master_outline.md`
3) 每日运行（生产入口）：

```bash
python tools/run_daily.py --date YYYY-MM-DD --chapter NNN --words 2000
```

或使用便捷脚本：
- Windows：`scripts\\run_daily.bat`
- Linux/macOS/WSL：`bash scripts/run_daily.sh`

## 产物位置（固定路径）

- 当日运行：`runs/YYYY-MM-DD/`
- 正文：`manuscript/chNNN.md`
- 摘要：`recap/chapter_summaries/chNNN.md` 与 `recap/rolling_recap.md`
- 状态：`state/current_state.json`（只允许通过 `state/state_patch.json` 合并更新）

## 规范

团队章程见：`AGENTS.md`

