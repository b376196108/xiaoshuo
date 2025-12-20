# 章纲 - ch002

- chapter_id: ch002
- target_words: 3200
- chapter_title: 《名册压门换活路》
- alt_titles: [《点名夜我先扛》,《换粮路被盯上》]
- chapter_goals:
  - 承接上章钩子：名册上门后明确“点卯与赈粮资格绑定”的规则与代价
  - 推进 loop_food_shortage：本章拿到短期口粮来源或可执行的换粮路径
  - 推进 loop_toxic_neighbor：压住邻居造谣，锁定她搅局的证据或对策
  - 种田爽点落地：省柴省粮的新法当天见效，让当晚更顶饱
  - 磨难升级：名册规则与邻居流言双重夹击，逼主角做出取舍
- pov_lock: 第三人称限知（主角：林岑）
- timeline_anchor: 1100-03-15 夜里至次日清晨（名册上门后到点卯前）

## Open Loops 推进
- loop_food_shortage：名册与赈粮绑定，林岑以劳力/柴火换到一份短期口粮路径，明确“能撑几日”与下一步代价。
- loop_toxic_neighbor：许文淑趁夜添油加醋，主角当场留证并制定应对话术，避免名声被压垮。

## Open Loops
- advance:
  - id: loop_food_shortage
    starting_state: 余粮见底，只能靠省柴闷煮勉强撑过一顿
    action: 林岑当夜确认名册与赈粮规则，次日清晨以劳力/柴火换得短期口粮路径
    new_information: 赈粮需按时点卯，错过即失；短期口粮只能撑数日
    resulting_state: progressed
    summary_evidence: 拿到点卯时间与换粮条件，带回可执行的短期口粮方案
  - id: loop_toxic_neighbor
    starting_state: 许文淑已放话“昨夜点火”，流言可扩散
    action: 许文淑在门外添油加醋，林岑以在场见证与回执压制其话头
    new_information: 她借里正势头逼人，流言一旦坐实将直接影响赈粮资格
    resulting_state: active
    summary_evidence: 门外当众对峙，主角拿到点卯回执以压住谣言
- new_optional: null

## Scene List
- scenes:
  - {no: 1, setting: "林家门外(loc_lin_home)", cast: "林岑(lin_cen)、许文淑(xu_wenshu)、差役(he_kaijun)、陈淑英(chen_shuying)", objective: "确认名册规则与点卯时间", conflict: "差役点名且邻居添油加醋", reveal: "赈粮资格与点卯绑定，错过即失", escalation: "许文淑暗示要散布“昨夜点火”流言", exit_hook: "林岑要求留下点卯时间的明示口头证据"}
  - {no: 2, setting: "林家屋内(loc_lin_home)", cast: "林岑(lin_cen)、林国柱(lin_guozhu)、杜桂兰(du_guilan)", objective: "确定谁去点卯与如何换粮", conflict: "父亲执意出面，体力与风险不匹配", reveal: "点卯若迟到全家失去赈粮", escalation: "林岑决定自己去并以劳力/柴火换口粮", exit_hook: "天未亮就要出门，时间被压缩"}
  - {no: 3, setting: "里正/分配处(loc_village_committee)", cast: "林岑(lin_cen)、叶守正(ye_shouzheng)、排队村民", objective: "拿到点卯确认与短期口粮路径", conflict: "排队与规则挤压，里正态度强硬", reveal: "可用劳力与柴火换取少量粗粮与回执", escalation: "林岑背上两日劳力欠账换回执", exit_hook: "回执在手，但人情债被锁死"}
  - {no: 4, setting: "村口巷道(loc_village_lane)", cast: "林岑(lin_cen)、许文淑(xu_wenshu)、围观村人", objective: "压住流言与保住名声", conflict: "许文淑借机逼他当众认错", reveal: "她借里正势头影响名单口风", escalation: "林岑亮出回执与点卯时间，暂时堵住她嘴", exit_hook: "她转而放话要盯他点卯是否迟到"}
  - {no: 5, setting: "林家灶间(loc_lin_home)", cast: "林岑(lin_cen)、陈淑英(chen_shuying)、林小棠(lin_xiaotang)", objective: "把换来的粗粮做成更顶饱的当晚饭", conflict: "粗粮难入口且柴火更紧", reveal: "浸泡+二次闷煮+细切野菜能更稠更省柴", escalation: "代价是耗时加倍且外人更易察觉", exit_hook: "门外有人盯着灶烟，隐患再起"}
  - {no: 6, setting: "林家门口(loc_lin_home)", cast: "林岑(lin_cen)、林国柱(lin_guozhu)", objective: "确认明早点卯与劳役安排", conflict: "劳役时间与家里生计冲突", reveal: "点卯提前，迟到就失赈粮资格", escalation: "不得不调整全家行动与劳力安排", exit_hook: "明早点卯逼近，主角必须转向“保名额”与“保口粮”的抉择"}

## Ending Hook
- type: goal_shift
- payload: 点卯时间提前且与赈粮绑定，林岑必须转向“保名额”的紧急行动，否则全家口粮断档
