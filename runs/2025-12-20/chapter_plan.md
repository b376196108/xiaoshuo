# 章纲 - ch001

- chapter_id: ch001
- target_words: 3200
- chapter_title: 《名册夜逼上门》
- chapter_goals:
  - 确认穿越处境与粮荒底线，做出本章第一步活命决策
  - 推进 loop_food_shortage：评估存粮并建立当日可执行的节粮方案
  - 推进 loop_toxic_neighbor：毒舌邻居主动挑衅，主角首次交锋但先吃小亏
  - 落地一个当天见效的小爽点并付出代价（节柴省粮的煮粥法）
- pov_lock: 第三人称限知（主角：林岑）
- timeline_anchor: 乾元九年二月初三清晨（春寒未退、旱荒加剧；作为故事开局时间锚）

## Open Loops 推进
- loop_food_shortage：家中断粮压力坐实，明确“余粮撑两三日”的事实并提出节粮方案。
- loop_toxic_neighbor：毒舌邻居当众挖苦占便宜，主角先忍让吃亏，为后续反制埋钩。

## Open Loops
- advance:
  - id: loop_food_shortage
    starting_state: 林家粮缸见底，具体余粮不清
    action: 林岑清点存粮并提出按人头定量、浸泡淘洗与闷煮节柴的方案
    new_information: 家中余粮最多撑两三日，必须立刻寻找替代口粮
    resulting_state: progressed
    summary_evidence: 量粮分配、试做稀粥并记录可节省柴火
  - id: loop_toxic_neighbor
    starting_state: 许文淑盯上林家，伺机挑事
    action: 许文淑当众挖苦并借机占便宜，林岑忍让却记下对方手段
    new_information: 许文淑借流言挟迫，邻里对林家指指点点
    resulting_state: active
    summary_evidence: 巷道口对喷与流言种子埋下
- new_optional: null

## Scene List
- scenes:
  - {no: 1, setting: "林家土院(loc_lin_home)", cast: "林岑(lin_cen)、陈淑英(chen_shuying)、杜桂兰(du_guilan)、林小棠(lin_xiaotang)", objective: "确认家中粮食与当日口粮底线", conflict: "粮缸见底，家人各执一词：卖工具还是节口", reveal: "余粮不足数日，赈粮名册又将下发", escalation: "林岑提出按量分粮与节柴煮粥方案但遭质疑", exit_hook: "决定白天去巷道与山沟找食并探名册消息"}
  - {no: 2, setting: "村口巷道(loc_village_lane)", cast: "林岑(lin_cen)、许文淑(xu_wenshu)、林小河(lin_xiaohe)", objective: "打听名册消息并借口换取一点盐柴", conflict: "许文淑当众挖苦并趁机占便宜", reveal: "她暗示名册今晚送达且里正偏向她", escalation: "林岑被迫退让一次，名声受损", exit_hook: "听到‘今晚点名’传言，危机逼近"}
  - {no: 3, setting: "山林河沟(loc_hills)", cast: "林岑(lin_cen)、林小河(lin_xiaohe)", objective: "寻找可食野菜补口粮", conflict: "可食野菜稀少且需登记，巡查脚步逼近", reveal: "林岑用现代识别法避开毒草并找到一小片可食植物", escalation: "为躲巡查绕路，耗时且露出行踪", exit_hook: "听见有人议论徭役名册已在路上"}
  - {no: 4, setting: "林家灶间(loc_lin_home)", cast: "林岑(lin_cen)、陈淑英(chen_shuying)、杜桂兰(du_guilan)", objective: "把野菜与余粮做成能顶饱的当日饭", conflict: "柴火紧缺且老人担心新法伤身", reveal: "先浸泡淘洗、灰水去涩再闷煮，粥更稠更省柴", escalation: "代价是耗掉半捆柴并暴露新做法", exit_hook: "邻居孩子看见冒烟的锅，风声可能传开"}
  - {no: 5, setting: "里正家门口(loc_headman_home)", cast: "林岑(lin_cen)、林国柱(lin_guozhu)、叶守正(ye_shouzheng)", objective: "确认名册动向并争取缓期", conflict: "里正要人情或劳力才肯通融", reveal: "名册与赈粮绑定，今晚必送到户", escalation: "林岑被迫允诺送柴或出力换取缓口", exit_hook: "里正放话：今晚点名，早做准备"}
  - {no: 6, setting: "林家门外(loc_lin_home)", cast: "林岑(lin_cen)、陈淑英(chen_shuying)、许文淑(xu_wenshu)、差役(he_kaijun)", objective: "撑到夜里并等名册结果", conflict: "差役敲门，邻居旁观添油加醋", reveal: "名册点名落到林家，赈粮资格与徭役风险并至", escalation: "一旦应下就要付出劳力与名声代价", exit_hook: "门一开，名册上的名字刺眼亮出"}

## Ending Hook
- type: crisis_escalation
- payload: 名册夜里逼上门，林家被点名，赈粮与徭役的代价同时压下来
