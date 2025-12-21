# 章纲 - ch005

chapter_id: ch005
target_words: 3200
chapter_title: 《井口争水见黑沫》
alt_titles: [《黑沫浮起谁下手》, 《争水换桶惹是非》]
chapter_goals:
- 承接上章补证压力，争取当日可执行的取水路径，稳住家里最基本的用水与煮粥量
- 推进 loop_food_shortage：本章明确“取水-净水-换粮/换人情”的短期链路与代价
- 推进 loop_toxic_neighbor：在井口正面交锋并锁定其造谣口径与人证
- 种田爽点落地：完成一项可落地的取水效率改良，当天见效但耗时与人情债增加
- 磨难升级：限水与流言双压，名额与名册风险进一步逼近
- 结尾留钩子：抛出“水源疑似污染”的新证据，迫使下一章调整目标

pov_lock: 第三人称限知（state.meta.pov 未设置，沿用风格指南）
timeline_anchor: 1100-03-15（与 state.meta.in_story_date 一致）

## 章纲爽点对齐字段
- 本章爽点类型：A 技术落地 + C 资源落袋 + B 打脸交锋
- 落袋证据句计划：主角用修好取水工具换到半桶清水和一个旧木桶，当场入缸，但要替人挑满两担水作为代价。
- 旁观者反应计划：围观的妇人先嗤笑他瞎折腾，看到清水入缸后集体噎住，眼神立刻变了。
- 开场方式：冲突开场（井口限水+许文淑当众挑衅），禁止从冷/风/灰/薄被意象起笔。
- 结尾钩子类型：新证据（取水点浮出黑沫与异味，暗示上游出问题）。

## Plot Spine
- premise_of_chapter: 在限水与流言夹击下，主角用可落地的取水改良换到当日可用的清水，但代价与风险更高。

## Open Loops
- advance:
  - {id: loop_food_shortage, starting_state: progressed, action: 用修井绳/改桶口提高取水效率并以劳换水，建立可执行的短期用水-换粮通道, new_information: 限水与水质疑虑让“换水”变成硬门槛，短期路径必须搭人情与劳力, resulting_state: progressed, summary_evidence: "loop_food_shortage：林岑用修好取水工具换到半桶清水和旧木桶，当场入缸但付出两担挑水代价，确认短期口粮路径仍受限水与水质约束"}
  - {id: loop_toxic_neighbor, starting_state: active, action: 许文淑在井口挑衅并散布“占名额”的话，主角当众反制并锁定其口径与人证, new_information: 谣言已开始围绕“名册/水名额”扩散，冲突公开化, resulting_state: progressed, summary_evidence: "loop_toxic_neighbor：许文淑当众讥讽并暗指占水名额，林岑回击并记下人证，谣言口径被锁定"}
- new_optional: null

## Scene List
- scenes:
  - {no: 1, setting: 取水点/井口(loc_river_canal), cast: 林岑、许文淑、围观村民, objective: 争到当日取水名额, conflict: 井口限水且名额紧张，许文淑当众挑衅造谣, reveal: 今日取水需“排号+人证”，口径随人变, escalation: 谣言开始围绕“名册资格”扩散, exit_hook: 林岑决定以修工具换取取水优先}
  - {no: 2, setting: 林家租屋(loc_lin_home), cast: 林岑、母亲、家人, objective: 做出可落地的取水改良方案, conflict: 材料不足、时间紧、家人担心被盯上, reveal: 旧绳+布条+桶口改造可减少漏水、提升提水效率, escalation: 需要以劳换水，代价更重, exit_hook: 他带着工具去井口找能交换的对象}
  - {no: 3, setting: 取水点/井口(loc_river_canal), cast: 林岑、挑水老汉、围观村民, objective: 以修工具换到当日清水, conflict: 老汉不信他能修好，要求先挑满两担水再给半桶, reveal: 工具修好后取水速度明显提升, escalation: 围观者注意到他“会修会算”，资源风险上升, exit_hook: 他得到半桶清水和旧木桶入手}
  - {no: 4, setting: 林家租屋(loc_lin_home), cast: 林岑、母亲、家人, objective: 当天净出可用清水, conflict: 需加柴与耗时沉淀，烟火暴露风险上升, reveal: 沉淀+滤布让水色明显变清，煮粥更稳, escalation: 代价是柴火消耗与人情债增加, exit_hook: 邻居闻风上门索水}
  - {no: 5, setting: 许家门口巷道(loc_xu_home), cast: 林岑、许文淑、围观妇人, objective: 守住取水成果与名声, conflict: 许文淑挖苦并试图占水，暗示要去村委告状, reveal: 林岑亮出记下的人证口径，逼她收敛, escalation: 她转而放话“水有问题”，冲突升级, exit_hook: 众人被“水有问题”一句拽住}
  - {no: 6, setting: 取水点/排水沟(loc_river_canal), cast: 林岑、围观村民, objective: 核实水源情况, conflict: 水面出现黑沫与异味，众人慌乱, reveal: 上游似有污染迹象，新风险浮现, escalation: 若不改水源，全村取水与口粮都受影响, exit_hook: 林岑意识到必须追查上游，否则名册与口粮一起崩}

## Ending Hook
- type: new_info
- payload: 取水点浮出黑沫和怪味，新证据指向上游出问题，若不马上查清，连“名册资格+口粮”都会被一锅端。
