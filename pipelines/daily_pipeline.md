# Daily Pipeline（每日流水线定义）

> 目的：保证连续性、可追溯、可返工、可上线。

## 0) CreateRun
- 输入：`manuscript/`（用于推断下一章号）
- 输出：`runs/YYYY-MM-DD/brief.md`
- 失败条件：无法创建当日目录；章号推断失败且未提供 `--chapter`
- 返工策略：手动指定 `--date` 与 `--chapter` 重试

## 1) BuildContext
- 输入：`inputs/project_brief.json`、`canon/**`、`outline/master_outline.md`、`state/current_state.json`、`recap/rolling_recap.md`、最近 2 章摘要、`runs/YYYY-MM-DD/brief.md`
- 输出：`runs/YYYY-MM-DD/context_pack.md`
- 失败条件：关键输入缺失（脚本应提示但不中断）；输出超长且未能截断
- 返工策略：补齐缺失文件或降低 context_pack 长度上限

## 2) World/Character（可选增量）
- 输入：`runs/YYYY-MM-DD/context_pack.md` + 相关 `canon/` 文件
- 输出：仅允许对 `canon/` 追加；任何改写必须记录到 QA 报告与 `runs/YYYY-MM-DD/changelog.md`
- 失败条件：引入与既有设定冲突；改写未记录
- 返工策略：撤销冲突增量，仅保留一致内容

## 3) Outline/Plan
- 输入：`runs/YYYY-MM-DD/brief.md`、`runs/YYYY-MM-DD/context_pack.md`、`state/current_state.json`
- 输出：`runs/YYYY-MM-DD/chapter_plan.md`
- 失败条件：未明确标注推进的 `open_loops`；计划与风格/视角锁冲突
- 返工策略：重写计划并明确：推进哪些 `open_loops`、新增是否 <= 1

## 4) Draft
- 输入：`runs/YYYY-MM-DD/chapter_plan.md`、`canon/style/style_guide.md`
- 输出：`manuscript/chNNN.md`
- 失败条件：出现 AI 痕迹；无推进；结尾无钩子
- 返工策略：按计划重写关键段落，补足推进与钩子

## 5) Edit
- 输入：`manuscript/chNNN.md`
- 输出：覆盖更新 `manuscript/chNNN.md`
- 失败条件：改动导致视角/时态漂移；事实与状态冲突
- 返工策略：以 `state/` 与 `canon/` 为准修正

## 6) QA（ContinuityQA）
- 输入：`manuscript/chNNN.md`、`canon/**`、`state/current_state.json`（以及若已生成的 `state/state_patch.json`）
- 输出：`runs/YYYY-MM-DD/qa_report.md`
- 失败条件：任一硬规则不满足
- 返工策略：按 QA 报告逐条修复后重新 QA

## 7) Archive
- 输入：`manuscript/chNNN.md`、`runs/YYYY-MM-DD/chapter_plan.md`
- 输出：`recap/chapter_summaries/chNNN.md`、更新 `recap/rolling_recap.md`、`runs/YYYY-MM-DD/changelog.md`
- 失败条件：摘要未覆盖本章事实；滚动摘要超长
- 返工策略：压缩旧摘要、补齐缺失事实

## 8) Patch
- 输入：`manuscript/chNNN.md` + `recap/chapter_summaries/chNNN.md`
- 输出：`state/state_patch.json`（只包含变更字段）
- 失败条件：patch 不是 dict；含无关字段；试图直接写 current_state
- 返工策略：重建 patch，仅保留增量字段

## 9) Merge（仅 PASS）
- 前置条件：`runs/YYYY-MM-DD/qa_report.md` 第一行必须为 `QA_RESULT: PASS`
- 输入：`state/state_patch.json`
- 输出：更新 `state/current_state.json`，并在合并前备份到 `state/backups/YYYY-MM-DD_current_state.json`

### QA_FAIL 规则（零容忍）
- QA_FAIL：不得合并 `state/state_patch.json`；不得标记发布；必须先返工修复再重跑 QA。

