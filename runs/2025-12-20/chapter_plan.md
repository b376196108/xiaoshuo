# Chapter Plan - ch001

chapter_id: ch001
target_words: 2500
chapter_goals:
- 穿越醒来：从“陌生身体+饥饿眩晕”切入，立起饥荒现实
- 家庭困境具象化：断粮与病弱/孩子挨饿至少命中两项，点出“今天不解决就出事”的紧迫
- 毒舌邻居首挑衅：许文淑登场挑衅并与主角第一次正面交锋（主角先吃亏）
- 本章爽点：主角落地一个“当天可见效”的节粮/止饿改良，今晚能吃上像样的东西，但要付代价
- 结尾钩子：危机升级（徭役名册/差役点名）逼迫下一章行动
pov_lock: 第三人称限知（主角：林岑）
timeline_anchor: 乾元九年二月

## One-Sentence Goal
- 林岑在饥荒与家庭濒临断粮的压力下立刻盘点口粮、争取当晚止饿，同时被毒舌邻居挑衅并迎来徭役名册的危机升级。

## Open Loops
- advance:
  - {id: loop_food_shortage, starting_state: 粮缸见底且家人虚弱, action: 盘点口粮并制定当日定量方案+节柴闷煮, new_information: 仅够撑两顿且必须尽快找稳定粮源, resulting_state: 短期止饿但口粮危机更紧, summary_evidence: 粮缸见底+定量刻线+当晚稠粥}
  - {id: loop_neighbor_sabotage, starting_state: 邻里已有闲话, action: 井边/路上许文淑挑衅并散布“林家藏粮/占水”谣言, new_information: 流言可能影响赈灾名册与徭役选择, resulting_state: 公开对立开端, summary_evidence: 井边争执+邻居放话}
  - {id: loop_labor_levy, starting_state: 徭役名册将下发, action: 里正口风+差役现身透露名册将贴并点名, new_information: 林家可能被点名且需次日集合, resulting_state: 徭役压力逼近, summary_evidence: 差役到村+口头点名}
- new_optional: null

## Escalation Plan
- misbelief_or_reversal: 以为靠省粮能多撑几天，但流言与名册让“今日省下的口粮”变成明日被抓丁的代价
- cost_or_consequence: 家中用掉最后的盐/柴，且父亲被差役盯上，家庭安全感下降
- ending_hook_type: crisis_escalation
- ending_hook_payload: 差役夜里点名，明日卯时必须报到，若不到将连累赈灾资格

## Scene List
- scenes:
  - {no: 1, setting: 林家土屋内（loc_lin_home）, cast: 林岑/陈淑英/杜桂兰/林小棠/林小河, objective: 立刻确认生存处境并稳住家人, conflict: 饥饿眩晕+粮缸见底+孩子挨饿, reveal: 行动=用现代“清单+定量”思路盘点口粮并在碗上刻线定量, escalation: 代价=份额太少引发家人不满且林岑言行显得异常, exit_hook: 父亲从田里回来带来坏消息, words: 360}
  - {no: 2, setting: 院里与灶间, cast: 林岑/林国柱/陈淑英, objective: 说服父亲接受当日止饿方案, conflict: 父亲体力透支+柴火不足+对“新法”不信, reveal: 行动=提出“浸泡粗粮+闷煮余热”省柴法并量化分粥, escalation: 代价=需要额外取水与占用灶口时间，父亲勉强点头但心生戒备, exit_hook: 需要去井边取水, words: 420}
  - {no: 3, setting: 村口老井, cast: 林岑/陈淑英/杜桂兰/许文淑/村民, objective: 取到够用的清水并避开冲突, conflict: 许文淑插队抢水并阴阳怪气造谣, reveal: 行动=用“沉淀+布过滤”挑清水并当场解释水变浑原因, escalation: 代价=仍被邻居压一头且流言扩散，第一次正面对冲先吃亏, exit_hook: 村道上传来里正与差役的动静, words: 420}
  - {no: 4, setting: 里正家门口/村道, cast: 林岑/林国柱/叶守正/何开军/许文淑(旁观), objective: 打探徭役名册规则与时间, conflict: 里正含糊其辞+差役不耐烦+流言影响态度, reveal: 行动=用现代“时间节点+流程清单”提问获取名册张贴与集合时间, escalation: 代价=差役记住林家且父亲更焦虑, exit_hook: 必须今晚先让家人吃上东西, words: 400}
  - {no: 5, setting: 林家灶间（傍晚）, cast: 林岑/陈淑英/林小棠/林小河/杜桂兰, objective: 把当晚一顿做成“能顶饿”的小成果, conflict: 粮少水浑柴紧, reveal: 行动=按刻线定量+粗粮先泡后闷+野菜焯水去涩, escalation: 代价=用掉最后的盐/柴并暴露“懂法子”引来家人担忧, exit_hook: 刚端上粥就传来门外急促敲门声, words: 450}
  - {no: 6, setting: 林家门口（夜）, cast: 林岑/林国柱/陈淑英/何开军或差役/许文淑, objective: 稳住局面争取缓冲, conflict: 差役点名上门，口气强硬, reveal: 行动=林岑冷静确认名册与集合时间并尝试争取延期, escalation: 代价=对方拒绝且明确“明日卯时报到”，危机升级, exit_hook: 差役留下最后通牒，家人惶然, words: 450}

## Ending Hook
- type: crisis_escalation
- payload: 差役夜里点名，林国柱被要求次日卯时到衙外围集合，若不到将影响赈灾资格，逼迫下一章立即应对。