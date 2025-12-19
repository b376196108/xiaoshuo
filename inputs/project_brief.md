# Project Brief（字段说明）

> 系统以 `inputs/project_brief.json` 为准；`inputs/project_brief.yaml` 仅供人类阅读与修改参考。
> 本仓库内提供的默认值均为“默认可改”，可随时按项目需要调整。

## project
- `project.genre`：题材类型（例如：都市悬疑、科幻、奇幻、历史等）。默认可改。
- `project.tone`：整体气质（语言与节奏的倾向，例如写实/克制/幽默/阴郁）。默认可改。
- `project.rating`：内容分级与边界（暴力、成人内容、恐怖强度等）。默认可改。
- `project.hook`：一句话卖点/核心吸引点（面向读者的“为什么要看”）。默认可改。
- `project.theme`：核心主题（反复被剧情验证的命题）。默认可改。
- `project.setting_anchor`：时空锚点（时代/地点/季节/社会切面，帮助连续性）。默认可改。
- `project.protagonist_keywords[]`：主角标签数组（身份、性格、缺陷、欲望等关键词）。默认可改。

### project.scale（数值必须为 int）
- `project.scale.total_chapters`：全书总章数（用于节拍与里程碑规划）。默认可改。
- `project.scale.words_per_chapter`：单章目标字数（用于当日 brief 的目标字数参考）。默认可改。

## constraints
- `constraints.must_have[]`：写作硬要求清单（必须出现/必须做到的规则）。默认可改。
- `constraints.must_avoid[]`：禁用清单（必须避免的写法或风险）。默认可改。

## random_seed（数值必须为 int）
- `random_seed`：随机种子（用于需要“可复现选择”的场景；保持稳定有助于一致性）。默认可改。

## 如何改成其它类型小说（≤200字）
先改 `project.genre/tone/hook/theme/setting_anchor` 定位类型与卖点；再用 `constraints.must_have/must_avoid` 写清视角、尺度、节奏等硬规则；最后按节奏调整 `project.scale.words_per_chapter/total_chapters`（短篇降低总章数与字数，长篇相反）。

