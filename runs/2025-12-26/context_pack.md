# Context Pack — 2025-12-26

- generated_at_utc: 2025-12-21T11:06:29Z
- max_chars: 80000

说明：本文件由工具自动聚合生成，供写作与 QA 使用；若某些文件缺失，会以 [MISSING] 标记。

## Today Brief

# Daily Brief — 2025-12-26

只需填写以下三项（其余可留空）：
- chapter_id（如无特殊需要可保持默认）
- target_words（正文字符数>=3000，默认>=3200）
- chapter_goals（3–6 条）

---

chapter_id: ch007
target_words: 3200
chapter_goals:
- 承接上章钩子：}
- 推进 loop_food_shortage：本章明确短期口粮来源或可执行的换粮路径
- 推进 loop_toxic_neighbor：本章争取里正/村权态度或锁定流言扩散证据
- 种田爽点落地：落实可执行的净水/取水流程，当日见效。
- 磨难/反转升级：邻居或流言升级，名册/资源受阻。
- 结尾留钩子：抛出新的时间限制或资格风险，驱动下一章。

notes:
- 正文字符数>=3000，默认 target_words 不低于 3200
- TBD

## State Focus (meta + open_loops + locks)

{
  "continuity_locks": {},
  "meta": {
    "chapter_title": "《当众拆谣压名册》",
    "current_chapter": "ch006",
    "in_story_date": "1100-03-15",
    "total_chapters": 80,
    "words_per_chapter": 3200
  },
  "open_loops": [
    {
      "created_in": "ch001",
      "description": "林家余粮见底，需尽快找到稳定口粮",
      "id": "loop_food_shortage",
      "last_touched_in": "ch006",
      "note": "ch006 证据：林岑以黑沫源头口径换到临时取水号牌和一小把糙米，当场落袋，但需承担三日清沟劳役。",
      "owner": "lin_cen",
      "planned_payoff_window": "ch001-ch010",
      "status": "progressed",
      "trigger": "粮缸见底与口粮分配"
    },
    {
      "created_in": "ch001",
      "description": "许文淑借流言与占便宜施压林家",
      "id": "loop_toxic_neighbor",
      "last_touched_in": "ch006",
      "note": "ch006 证据：许文淑当众扣锅扩散口径，林岑携证人和黑泥当众拆谣并压回名册。",
      "owner": "xu_wenshu",
      "planned_payoff_window": "ch001-ch012",
      "status": "progressed",
      "trigger": "巷道口当众挖苦与挑衅"
    }
  ],
  "world_state": {}
}

## Recent Chapter Summary (-1) — ch006.md

# ch006｜《当众拆谣压名册》
facts:
- 巷口许文淑以“黑沫”当众扣锅，林岑坚持去村委公开对质，把口径带到里正面前。
- 里正与差役强调“只认证人”，林岑携王老拐查到上游堵塞为黑沫源头，当众展示黑泥与证人口径，拆谣压回名册。
- 林岑以查清口径换到临时取水号牌和一小把糙米，当场入袋，但被要求三日清沟劳役并把名册再压三日限期。
- 回到租屋，他与陈凤英、林国栋商量清沟与找证人，决定天一亮去桥头卡找差役线索稳住名册与水源。

emotional_arc:
- 被围堵压迫→硬顶稳住口径→当众拆谣小胜→劳役加码后转入紧绷。

conflicts:
- 流言污名与名册规则正面冲突；取水口径必须证人背书；临时资源与劳役代价捆绑。

open_loops_touched:
- {id: loop_food_shortage, how_it_moved: 以黑沫源头口径换到临时取水号牌与小把糙米，短期口粮落袋但背上三日清沟劳役}
- {id: loop_toxic_neighbor, how_it_moved: 许文淑当众挑衅扩散口径，林岑以证人与黑泥证据当众拆谣并压回名册}

本章推进的 open_loops：
- loop_food_shortage：以“黑沫源头口径+证人”换到临时取水号牌和一小把糙米，当场入袋，但代价是三日清沟劳役与名册限期。
- loop_toxic_neighbor：许文淑当众扣锅，林岑携证人和黑泥证据拆谣，口径回到名册规则内。

ending_hook:
- {type: goal_shift, payload: 被迫转向去桥头卡找差役线索与更硬证人，否则名册与取水仍会被翻案。}

## Recent Chapter Summary (-2) — ch005.md

# ch005｜《井口争水见黑沫》
facts:
- 井口限水且无回执需两名人证，许文淑当众挑衅，林岑以号牌与证人口径顶住并记名。
- 他修绳补桶、改桶口提高取水效率，挑两担水换到半桶清水和旧木桶，欠王老拐一回人情；回家沉淀过滤后勉强能煮粥，但柴火消耗与烟气暴露代价上升。
- 许文淑上门索水被拒后放话，井口随即浮出黑沫异味，疑似上游污染引发新的风险。

emotional_arc:
- 被限水与名册规矩压住 -> 小胜落袋稍稳 -> 黑沫现身危机再起

conflicts:
- 取水名额与人证规则的硬门槛
- 许文淑的当众挑衅与流言口径压迫
- 水源疑似污染导致全村用水风险升级

open_loops_touched:
- {id: loop_food_shortage, how_it_moved: 用修好的取水工具换到半桶清水和旧木桶并当场入缸，但付出两担挑水与人情债，短期口粮仍受限水约束}
- {id: loop_toxic_neighbor, how_it_moved: 许文淑在井口挑衅并散布占名额口径，林岑回击并记下人证，冲突公开化}

ending_hook:
- {type: new_info, payload: 井口水面出现黑沫异味，疑似上游污染，若不查清将牵连名册与口粮}

## Rolling Recap

# 滚动摘要（截至 ch006）

## 主线现状（当前处境/短期目标）
- 饥荒与取水限额叠加，名册与回执规则绑定生存资格，任何口径失误都可能被清退。
- ch005 修绳补桶换到半桶清水与旧木桶；ch006 以黑沫源头口径换到临时取水号牌和一小把糙米，短暂稳住口粮，但代价是三日清沟劳役与名册限期。
- 口径规则“只认证人”被里正与差役反复强调，主角必须拿到证人和可落地的证据才能保名册与取水。
- 黑沫污染已被追到上游堵塞处，水源风险未消，清沟与取水时辰冲突加剧，劳役压力持续。
- 邻居流言仍在扩散，围观村民情绪易被带动，舆论与规矩成为双重夹击。
- 短期目标转向：天一亮去桥头卡找差役线索与更硬证人，同时在限期内完成清沟，稳住名册与水源。

## 关键人物关系
- 林岑与陈凤英、林国栋等家人同舟共济，家中口粮紧绷，清沟劳役与取水时辰让全家压力上升。
- 许文淑是长期对手，善用流言与规矩挑衅，屡次当众扣锅，冲突已公开化。
- 里正掌握名册与回执规则，差役执行口径与签名，既是门槛也是争取证据的关键节点。
- 王老拐提供黑沫源头证言，被林岑欠下一回人情，成为关键证人之一。
- 周启明粮铺与强势户把控种子与粮食渠道，资源竞争持续。
- 村民围观与桥头卡口差役构成舆论与证据的双压力，桥头卡口成为新的突破点。

## 已发生关键事件（按时间顺序）
- ch001：粮缸见底，林岑用省柴煮粥勉强顶一顿，许文淑当众占便宜并威胁流言，夜里差役上门点名册。
- ch002：以两日劳力和半担柴换回执与少量粗粮，点卯提前到鸡鸣前；许文淑继续威胁，名册压力加重。
- ch003：鸡鸣前排队求稳口径，被迫再加劳力与柴；许文淑拖延对峙后回执失落，名额风险陡增。
- ch004：为补证奔走，记下证人名单；在粮铺修筛搬粮换得少量种子并筛出可播籽，红印公告要求回执补证。
- ch005：井口限水、无回执需人证，林岑修绳补桶换到半桶清水和旧木桶，欠王老拐人情；井口浮出黑沫异味，水源风险升级。
- ch006：巷口被当众扣“黑沫锅”，林岑去村委对质并携王老拐查到上游堵塞源头，当众拆谣压回名册，换到临时取水号牌与小把糙米，但被要求三日清沟并把名册再压三日限期，目标转向桥头卡找差役线索。

## 未解伏笔清单
- loop_food_shortage（status: progressed，planned_payoff_window: ch001-ch010）：短期口粮靠临时号牌与糙米支撑，但清沟劳役与水源风险仍在，名册一旦失守口粮路径会断。
- loop_toxic_neighbor（status: progressed，planned_payoff_window: ch001-ch012）：许文淑屡次挑衅与扩散口径，虽被当众拆谣压回，但随时可能借规矩与流言反扑。

## Master Outline

# Master Outline

- Total chapters: 80
- Target words per chapter: ~3000
- Theme: 现代中国人穿越到饥荒年的农家小人物身上，靠知识与执行力种田养家致富逆袭
- Setting anchor: 架空王朝北方旱灾饥荒年，村落资源紧缺，赈灾与徭役并存

## Three-Act Structure

### Act I (ch001-ch025) 生存立足
- 目标：活下去，稳住口粮与劳力，建立最小安全网
- 关键冲突：粮荒、徭役、邻居刁难、名册不公
- 结果：主角找到可持续的生存路径并赢得局部话语权

### Act II (ch026-ch060) 发展突围
- 目标：扩大产出与资源渠道，破解名册与地界问题
- 关键冲突：粮价控制、村权博弈、外部势力介入
- 结果：家族资源升级，但风险升级到身份与制度层面

### Act III (ch061-ch080) 逆袭定局
- 目标：打破关键瓶颈，建立稳固生计与社会位置
- 关键冲突：最终的徭役/灾年考验与势力对决
- 结果：实现家族共富与地位稳定，留下长期可持续发展路径

## Milestones (every 10 chapters)
- ch010: 找到第一条稳定口粮方案并初步反制邻居
- ch020: 徭役压力升级，主角拿到名册关键线索
- ch030: 以技术与组织手段稳住产出，出现更大外部势力
- ch040: 村权博弈公开化，家族地界问题爆发
- ch050: 粮价战与赈灾冲突升级，主角势力被挤压
- ch060: 主角完成资源渠道突破，但身份风险暴露
- ch070: 大节点对抗（徭役/灾年终局），代价与反转并存
- ch080: 家族稳固与逆袭完成，开放后续发展空间

## Chapters 1-10 Beat Sheet

### ch001
- 目标：确认穿越处境并制定活下去的第一步
- 磨难：家中粮缸见底，村里名册被卡
- 爽点：用现代常识改分粮方法，减少浪费
- 反转：邻居散布流言，里正上门盘问
- 结尾钩子类型：危机升级

### ch002
- 目标：找出可以补充口粮的可行路径
- 磨难：旱地无收成，家人质疑
- 爽点：提出可落地的节粮与混食方案
- 反转：差役宣布徭役名单将下发
- 结尾钩子类型：目标转向

### ch003
- 目标：争取徭役缓冲与家庭劳力保留
- 磨难：里正偏袒强势户
- 爽点：用证据争取延期名额
- 反转：关键证据被人拿走
- 结尾钩子类型：信息误判

### ch004
- 目标：解决春播种子与农具短缺
- 磨难：粮铺抬价，赊账被拒
- 爽点：用工换物达成折价
- 反转：邻居抢先截胡
- 结尾钩子类型：危机升级

### ch005
- 目标：找到稳定取水与灌溉替代方案
- 磨难：老井限量，水源争执升级
- 爽点：修缮取水工具提升效率
- 反转：水源出现污染迹象
- 结尾钩子类型：新线索

### ch006
- 目标：化解邻居的公开刁难
- 磨难：流言扩散，家族名声受损
- 爽点：抓到流言源头反制
- 反转：里正借机加压名册
- 结尾钩子类型：目标转向

### ch007
- 目标：建立可持续的家内分工
- 磨难：家人意见不一，劳力分配冲突
- 爽点：制定明确分工与奖惩
- 反转：徭役名单提前公布
- 结尾钩子类型：危机升级

### ch008
- 目标：查清名册背后的真实规则
- 磨难：差役设阻，外人难接近
- 爽点：通过集市情报获取突破口
- 反转：关键人物突然失约
- 结尾钩子类型：信息误判

### ch009
- 目标：争取赈灾点的实际名额
- 磨难：排队与暗箱操作并存
- 爽点：用条款漏洞拿到补给
- 反转：补给被要求以工换粮
- 结尾钩子类型：目标转向

### ch010
- 目标：完成首个稳定口粮方案并巩固地位
- 磨难：粮价继续上涨，邻居报复
- 爽点：用组织与合作反制粮价
- 反转：更大势力介入村里
- 结尾钩子类型：危机升级

## Open Loop Payoff Rule
- 每个 open_loop 必须标注 planned_payoff_window（如 ch008-ch015），并在窗口内至少一次明确推进。
- 新增 open_loop 必须写入 state/state_patch.json，并在 chapter_plan 与 summary 中体现。

## Project Brief (JSON)

{
  "project": {
    "genre": "古代穿越种田爽文（饥荒生存线）",
    "tone": "爽点密集、节奏快、苦尽甘来、温情家庭、带黑色幽默（毒舌对喷）",
    "rating": "大众向；不露骨；暴力描写克制；以生活与成长为主",
    "hook": "现代中国人穿越到饥荒年的农家小人物身上，靠现代知识从活下去开始，带全家种田养殖、储粮吃肉、翻身过上衣食无忧的日子，同时对抗天灾人祸与毒舌邻居持续刁难",
    "theme": "自救与家族共富；知识改变命运；在苦难里建立秩序与尊严",
    "setting_anchor": "架空王朝/类中国古代；北方旱灾饥荒年；偏僻村落；官府赈灾与徭役压力并存；民间资源紧缺",
    "protagonist_keywords": [
      "现代生存知识",
      "种田与养殖",
      "饥荒求生",
      "家族经营",
      "反转打脸",
      "毒舌邻居对喷",
      "从0到1致富"
    ],
    "scale": {
      "total_chapters": 80,
      "words_per_chapter": 3200
    }
  },
  "constraints": {
    "must_have": [
      "每章结尾留钩子",
      "每章推进至少2个伏笔，最多新增1个",
      "每3章至少1次小反转",
      "每10章1个大节点",
      "毒舌邻居长期出现并多次反制",
      "现代知识必须可落地合理"
    ],
    "must_avoid": [
      "跳POV",
      "无意义旁白",
      "AI/系统提示痕迹",
      "金手指过强",
      "说明书式科普长段"
    ]
  },
  "random_seed": 20251219
}

## Canon — Premise

# Premise

世界观一句话：架空王朝北方旱灾饥荒年，一个现代中国人穿越到农家小人物身上，用可落地的知识带家人活下去并翻身。

核心生存压力：
- 连年旱灾，粮荒与徭役双重压迫
- 村落资源紧缺，赈灾名册与分配不透明
- 毒舌邻居与村权结构制造持续阻力

主角穿越设定：
- 现代中国人记忆与意识接管原身（保留原身情感底色）
- 没有系统、没有金手指，只有知识与执行力
- 现代知识必须依赖材料与工艺，无法凭空造物

家庭目标：
- 先活下去，建立稳定口粮与劳动力
- 通过种田、养殖与储粮实现家族共富
- 在村落规则中争取话语权与安全

禁改规则（不可突破）：
- 世界规则：赈灾、徭役与村权结构真实有效，不能被一句话解决
- 主角核心缺陷：初期体弱、人脉薄、行动受限，必须付出成本
- 时代技术边界：工具与材料受限，现代知识必须可落地

## Canon — Style Guide

# Style Guide

## POV & Tense
- 人称：第三人称限知（主角：林岑）
- 视角：不跳 POV，不写全知旁白；不提前揭露主角未知信息。
- 时态：以过去时叙述为主，保持统一

## 语言与质感（硬约束）
- 用“具体名词 + 动词 + 结果”写法，少抽象形容词堆叠。
- 描写只服务三件事：推进冲突 / 提供线索 / 增强压迫感（缺一就删）。
- 每个关键场景至少出现 2 类感官（气味/触感/声音/光影/温度/重量感），但不堆砌。
- 禁止“讲道理式解释世界观”；信息必须通过冲突、交易、代价、误会、证据呈现。

## 节奏与密度（硬约束）
- 节奏：快节奏、爽点密集、信息密度高
- 对话比例：约 30%-45%，对话必须推进情节，对话必须产生以下至少一项作用：
  ① 逼迫表态/做选择；② 抛证据/设陷阱；③ 交换资源/谈代价；④ 引发旁人站队变化。
- 对话中每 3–6 句必须插入一次动作/环境干扰（避免“站桩聊天”）。
- 叙述原则：行动驱动，少空镜与无意义感叹

## 场景写法（强制：每章至少 3 个场景）
每个场景必须具备四件事（缺一即弱）：
1) **小目标**：主角要拿到什么/证明什么/逼退谁（必须明确）。
2) **阻力**：对手/规矩/资源短缺/时间限制（必须具体）。
3) **代价**：付出体力/人情/名声/资源/风险（必须落地）。
4) **结果反转**：场景结束时局面必须“变”——要么拿到东西但埋雷，要么失败但摸到线索。
> 场景末尾必须留一句“下一步指向句”（主角下一步要做什么/去找谁/查什么）。



## 爽点密度规则（强制）
- 每章至少满足四类中的 2 类：A 技术落地 / B 打脸交锋 / C 资源落袋 / D 反转钩子。
- 必须出现“落袋证据句”（明确写清本章主角拿到什么，以及代价或交换方式）。
-打脸交锋必须出现“三拍”：对方压人（立规矩/扣帽子）→ 主角反击（证据/操作/逼问）→ 旁观者态度变化（噎住/退让/转向）。
-反转钩子必须是“新增威胁或新增真相”，且能直接危及本章落袋成果。

## 开头与结尾（硬约束）
- 开头 180–250 字内必须进入**直接冲突**：敲门/对峙/点卯/逼债/插队/丢证据/当众质疑等。
- 禁止开头复用“冷/风/灰/薄被/饥/饿”等模板意象；如出现，必须改成冲突开场。
- 结尾必须抛出**能驱动下一章的明确问题**（谁干的/从哪来/怎么查/明天怎么办等）

## 连续性（硬约束）
- 每章至少推进 2 条已存在矛盾线（open loops），且不得“重置问题”（前章结论不能被无故抹掉）。
- 关键承诺/交易/证据必须在文本中留下可引用的句子（可被下一章直接拿来当“口径”）。


## 章节结构（强制）
每章必须符合“四段骨架”，并在正文中可识别：

1) 开场钩子（前 180–250 字内完成）
- 必须进入直接冲突（对峙/点卯/逼债/插队/丢证据/当众质疑等）
- 必须明确本章小目标（主角今天要拿到什么/证明什么）

2) 推进（中段前半）
- 主角为小目标采取 ≥2 次具体行动（跑腿/换人/修物/谈条件/找证人）
- 每次行动都要带来“新信息或新限制”，避免原地踏步

3) 升级（中段后半）
- 阻力加码：规矩变严 / 对手加压 / 时间变短 / 代价变大（至少命中一项）
- 必须出现一次“优势交换或立场翻转”（谁站队变了/口径变了/筹码变了）

4) 结尾钩子（最后 1–3 段）
- 必须抛出新增威胁或新增真相，直接危及本章落袋成果
- 必须给出下一步指向句：主角下一步要去查什么/找谁/对抗谁

## 禁用写法（硬约束）
- 灌水与无意义旁白；“情绪自嗨式感叹”。
- 现代网络梗堆砌；跳出现代口语系统（除非角色设定明确允许）。
- 说明书式长段科普；作者点评式总结。
- AI/系统提示或作者自述痕迹；“像在写提示词”的句子。
- 重复同义句堆叠（同一信息换三种说法）。

## Canon — World Rules

# World Rules

## 硬规则
- 农时：春播秋收，旱年需抢墒播种，误时则全年减产
- 作物：以小麦、黍、豆为主，需按季节与土壤轮作
- 储粮：粮缸与谷囤是生存底线，赊粮有高额利息
- 稀缺品：盐、铁、布、药材稀缺且价格波动大
- 物价与赊账：灾年物价飞涨，赊账需要人情或抵押
- 徭役与差役：征粮、修渠、修路、服役随时加压
- 赈灾逻辑：名册由里正/族老掌控，分配易被挤占
- 村落权力结构：里正、族老、宗族与外来差役共治
- 工具材料：铁器、牲口稀缺，修造需材料与匠人

## 不可突破项
- 不能无成本获得大量资源或口粮
- 不能凭空造物或跳过工艺链
- 现代知识必须依赖材料、工艺与时间验证
- 官府规则与村约不能被轻易无视

## Canon — Characters (YAML)

characters:
  - id: lin_cen
    name: 林岑
    aliases:
      - 阿岑
      - 林二郎
    goal: "带家人活下去并建立稳定口粮"
    flaw: "初期体弱且缺乏当地人脉"
    secret: "现代人记忆接管原身，身份风险极高"
    arc: "从求生到掌控资源与话语权"
    relationships:
      - target_id: chen_shuying
        type: 母子
        note: "母亲谨慎保守，既支持又担忧"
      - target_id: lin_guozhu
        type: 父子
        note: "父亲在压力下情绪摇摆"
      - target_id: xu_wenshu
        type: 冲突
        note: "毒舌邻居频繁刁难"
    status: "谨慎试探、以活下去为先"
    location: loc_lin_home
    knowledge_flags:
      - modern_survival
      - basic_agriculture
      - ration_planning

  - id: chen_shuying
    name: 陈淑英
    aliases:
      - 陈嫂
    goal: "守住一家口粮与孩子们的安全"
    flaw: "过度谨慎，容易错过机会"
    secret: "曾欠下旧人情债"
    arc: "从守成到与主角协作"
    relationships:
      - target_id: lin_guozhu
        type: 夫妻
        note: "共同扛住灾年压力"
      - target_id: lin_cen
        type: 母子
        note: "信任但不完全理解"
    status: "持家节粮"
    location: loc_lin_home
    knowledge_flags:
      - household_management
      - village_rumors

  - id: lin_guozhu
    name: 林国柱
    aliases:
      - 林叔
    goal: "保住田地与劳力，稳住一家根基"
    flaw: "自尊强、抗拒求助"
    secret: "地界争议未了"
    arc: "从硬撑到接受新策略"
    relationships:
      - target_id: chen_shuying
        type: 夫妻
        note: "夫妻同心但意见不一"
      - target_id: lin_cen
        type: 父子
        note: "担心儿子的异常改变"
    status: "身体透支"
    location: loc_fields
    knowledge_flags:
      - traditional_farming
      - soil_knowledge

  - id: lin_yushu
    name: 林玉书
    aliases:
      - 大姐
    goal: "为家里争取粮食与人情"
    flaw: "心软易被利用"
    secret: "与集市粮铺有私下交易"
    arc: "从被动付出到主动定价"
    relationships:
      - target_id: lin_cen
        type: 兄妹
        note: "对主角的变化最敏感"
      - target_id: zhou_qiming
        type: 交易
        note: "私下换取粮票"
    status: "在集市周旋"
    location: loc_market
    knowledge_flags:
      - market_pricing
      - negotiation

  - id: lin_xiaohe
    name: 林小河
    aliases:
      - 小河
    goal: "守住家里仅有的牲口与工具"
    flaw: "冲动好胜"
    secret: "偷偷与邻居打赌换粮"
    arc: "从莽撞到学会克制"
    relationships:
      - target_id: lin_cen
        type: 兄弟
        note: "崇拜但不服气"
    status: "急于证明自己"
    location: loc_lin_home
    knowledge_flags:
      - livestock_care

  - id: lin_xiaotang
    name: 林小棠
    aliases:
      - 小棠
    goal: "照看幼弟与家务"
    flaw: "胆小怕事"
    secret: "听到里正家内情"
    arc: "从胆怯到敢于发声"
    relationships:
      - target_id: du_guilan
        type: 祖孙
        note: "常被祖母照看"
    status: "疲惫但坚韧"
    location: loc_lin_home
    knowledge_flags:
      - household_support

  - id: du_guilan
    name: 杜桂兰
    aliases:
      - 林奶奶
    goal: "保住家族香火与粮缸"
    flaw: "固执守旧"
    secret: "知道老井失修的真相"
    arc: "从排斥新法到接受改变"
    relationships:
      - target_id: lin_guozhu
        type: 母子
        note: "以家法约束"
    status: "年迈体弱"
    location: loc_lin_home
    knowledge_flags:
      - village_history
      - water_source_history

  - id: xu_wenshu
    name: 许文淑
    aliases:
      - 许嫂
    goal: "维持自家优先权并压过林家"
    flaw: "刻薄好斗"
    secret: "曾盗取赈灾名册碎页"
    arc: "从挑衅到被反制"
    relationships:
      - target_id: lin_cen
        type: 冲突
        note: "长期对手"
      - target_id: ye_shouzheng
        type: 利用
        note: "靠流言换取好处"
    status: "挑事中"
    location: loc_neighbor_home
    knowledge_flags:
      - gossip_network
      - ration_loopholes

  - id: ye_shouzheng
    name: 叶守正
    aliases:
      - 里正
    goal: "稳住村里秩序并保住官面差事"
    flaw: "偏袒强势户"
    secret: "赈灾名册有暗箱"
    arc: "从压制到被迫平衡"
    relationships:
      - target_id: he_kaijun
        type: 对接
        note: "负责交接徭役与名册"
      - target_id: zhou_qiming
        type: 利益
        note: "与粮商互相输送"
    status: "在压力中维稳"
    location: loc_headman_home
    knowledge_flags:
      - relief_process
      - village_power

  - id: he_kaijun
    name: 何开军
    aliases:
      - 差役何
    goal: "按上级要求完成征粮与徭役"
    flaw: "只看结果不问后果"
    secret: "私下收取粮钱"
    arc: "从强硬到出现动摇"
    relationships:
      - target_id: ye_shouzheng
        type: 上下
        note: "通过里正执行名单"
    status: "执行任务"
    location: loc_yamen_outer
    knowledge_flags:
      - levy_rules
      - enforcement

  - id: zhou_qiming
    name: 周启明
    aliases:
      - 周掌柜
    goal: "控制粮价与村中流通"
    flaw: "贪婪且轻视小户"
    secret: "囤粮规模超出明面"
    arc: "从操控到被迫让利"
    relationships:
      - target_id: ye_shouzheng
        type: 利益
        note: "与里正互通消息"
      - target_id: lin_yushu
        type: 交易
        note: "用高价换劳力"
    status: "囤粮观望"
    location: loc_grain_shop
    knowledge_flags:
      - supply_chain
      - price_manipulation

## Canon — Locations (YAML)

locations:
  - id: loc_lin_home
    name: 林家土院
    atmosphere: "土墙低矮，粮缸见底，灶火微弱"
    rules:
      - "夜间不得随意外出"
      - "粮食按人分配，禁止私藏"

  - id: loc_village_lane
    name: 村口巷道
    atmosphere: "尘土飞扬，风沙裹着饥饿的议论"
    rules:
      - "白日可通行，夜里需报备"

  - id: loc_fields
    name: 村外旱地
    atmosphere: "地皮干裂，庄稼萎黄"
    rules:
      - "轮作与抢墒必须按村约"

  - id: loc_water_point
    name: 老井水点
    atmosphere: "井绳磨损，水量忽涨忽落"
    rules:
      - "每日取水限量"
      - "不得私自改井"

  - id: loc_hills
    name: 山林河沟
    atmosphere: "荒草丛生，柴薪与野菜稀少"
    rules:
      - "采集需排队登记"

  - id: loc_market
    name: 乡集
    atmosphere: "人声嘈杂，物价日涨"
    rules:
      - "赊账必须有人担保"

  - id: loc_clan_hall
    name: 祠堂
    atmosphere: "香火冷清，族规悬挂"
    rules:
      - "族规决定地界与分配"

  - id: loc_headman_home
    name: 里正家
    atmosphere: "门庭紧闭，出入有差役"
    rules:
      - "非召不得入"

  - id: loc_neighbor_home
    name: 许家院
    atmosphere: "冷嘲热讽四处传"
    rules:
      - "邻里纠纷易被放大"

  - id: loc_county_gate
    name: 县城口
    atmosphere: "盘查严格，行人寥落"
    rules:
      - "无路引不得进城"

  - id: loc_yamen_outer
    name: 县衙外围
    atmosphere: "差役巡走，公告张贴"
    rules:
      - "民众只能在外等候"

  - id: loc_relief_point
    name: 赈灾点
    atmosphere: "队伍漫长，怨声四起"
    rules:
      - "按名册领取"
      - "不得代领"

  - id: loc_grain_shop
    name: 粮铺
    atmosphere: "门口排队，柜台冷硬"
    rules:
      - "现银优先"

## Canon — Factions (YAML)

factions:
  - id: faction_clan
    name: 村落宗族与里正
    motive: "维持秩序与既得利益"
    resources: "名册、人情账、村规"
    public_face: "稳定乡里、照顾弱小"
    secret: "名册与分配可被操控"

  - id: faction_official
    name: 官府差役体系
    motive: "完成征粮与徭役指标"
    resources: "路引、差役、惩罚权"
    public_face: "依法办事"
    secret: "暗中收取粮钱"

  - id: faction_grain
    name: 粮商与地主势力
    motive: "掌控粮价与劳力"
    resources: "粮仓、货路、银钱"
    public_face: "救济与施粮"
    secret: "囤积居奇、操纵市场"

## Canon — characters/characters.yaml.bak

schema:
  - id
  - name
  - aliases
  - age
  - appearance
  - voice
  - flaw
  - goal
  - fear
  - secret
  - arc
  - relationships
  - inventory
  - knowledge_flags
  - status
  - location

characters:
  - id: lin_cen
    name: 林岑
    aliases: [阿岑]
    age: 26
    appearance: 瘦高，雨衣常年带泥点，手背有旧茧
    voice: 说话快、嘴硬，关键处会停顿
    flaw: 回避承担、遇到好心软、对权威本能抵触
    goal: 活下去并把家从债务与困局里拖出来，同时弄清失踪案真相
    fear: 连累家人、把人命当成代价、自己最终也变成“那类人”
    secret: 他对“循环”并非完全无辜利用，曾做过一次自私选择
    arc: 从只求自保到愿意承担代价，学会用规则与证据对抗权力
    relationships:
      - with: chen_shuying
        type: 母子
        note: 相依为命，彼此都在隐瞒压力
      - with: lin_xiaoyu
        type: 兄妹
        note: 互怼但护短
      - with: lin_yong
        type: 亲属
        note: 怨与不得不管并存
      - with: xu_wenshu
        type: 邻里
        note: 互相看不顺眼但有真实关切
      - with: qiu_liyang
        type: 被管辖/交易
        note: 需要通行与资源时绕不开
      - with: zhou_qiming
        type: 对立
        note: 围绕粮与线索的博弈
      - with: he_kaijun
        type: 摩擦
        note: 在封控与巡查中多次起冲突
      - with: song_lei
        type: 合作/互疑
        note: 线索交换但互设底线
    inventory: [旧手机, 防水袋, 电动车钥匙, 记号笔, 便携充电宝]
    knowledge_flags: [knows_city_routes, knows_village_backroads, loop_memory_retained]
    status: 高压运转
    location: loc_delivery_station

  - id: chen_shuying
    name: 陈淑英
    aliases: [陈姨]
    age: 48
    appearance: 手指粗糙，常背布袋，眼神警惕
    voice: 话少，句子短，常用反问压住情绪
    flaw: 过度忍耐、把一切揽到自己身上
    goal: 保住一家人的底线与名声，不让债务拖垮生活
    fear: 家里有人“走歪路”、被宗族与邻里彻底孤立
    secret: 她与宗族长辈有旧账，牵扯到一份“人情债”
    arc: 从隐忍到敢于公开谈条件，学会把风险摊在阳光下
    relationships:
      - with: lin_cen
        type: 母子
        note: 互相保护，互相隐瞒
      - with: lin_xiaoyu
        type: 母女
        note: 管得紧，怕她被卷进去
      - with: lin_guangyuan
        type: 宗族/人情
        note: 受制于旧人情与舆论
    inventory: [粮票/配给卡, 旧账本, 小药盒]
    knowledge_flags: [knows_family_history, knows_neighbors_gossip]
    status: 谨慎自保
    location: loc_lin_home

  - id: lin_xiaoyu
    name: 林小雨
    aliases: [小雨]
    age: 17
    appearance: 校服旧但干净，耳机常挂脖子
    voice: 讥讽式幽默，情绪来得快去得也快
    flaw: 冲动、嘴快、喜欢逞强
    goal: 读书离开困局，同时守住家人不被吞噬
    fear: 自己成为负担、哥哥走上不可回头的路
    secret: 她掌握一条与失踪案相关的“目击碎片”，但不敢说全
    arc: 从逞强到学会与家人协作，把勇气用在关键处
    relationships:
      - with: lin_cen
        type: 兄妹
        note: 互怼与同盟并存
      - with: chen_shuying
        type: 母女
        note: 争执背后是担心
      - with: luo_yan
        type: 朋友/熟人
        note: 关系的断裂引发不安
    inventory: [旧耳机, 课本, 共享雨伞]
    knowledge_flags: [knows_school_rumors, knows_shortcut_paths]
    status: 表面叛逆，内心警惕
    location: loc_lin_home

  - id: lin_yong
    name: 林勇
    aliases: [阿勇, 勇哥]
    age: 39
    appearance: 啤酒肚，手腕有纹身，雨天爱戴帽
    voice: 嘴上圆滑，关键时刻躲闪
    flaw: 贪小便宜、逃避后果、惯性撒谎
    goal: 把欠账“熬过去”，继续维持体面与自由
    fear: 被债主与官方两头夹击、被家族彻底除名
    secret: 他替人跑过一次“灰色运输”，留下可追溯痕迹
    arc: 从投机到被迫站队，选择承担或彻底沉没
    relationships:
      - with: lin_cen
        type: 亲属
        note: 需要他帮忙又恨他惹事
      - with: zhou_qiming
        type: 债务/交易
        note: 被捏着把柄
      - with: qiu_liyang
        type: 交情
        note: 靠人情躲麻烦
    inventory: [旧摩托钥匙, 两部手机, 烟]
    knowledge_flags: [knows_black_market, knows_warehouse_routes]
    status: 四处周旋
    location: loc_market

  - id: xu_wenshu
    name: 许文淑
    aliases: [许婶, 许姐]
    age: 55
    appearance: 眼线很重，嗓门大，手指常夹着塑料扇
    voice: 毒舌、刻薄、句句带刺，但信息密度高
    flaw: 爱控制、爱评判、情绪绑架
    goal: 保住自家口粮与地盘，维持“我说了算”的邻里秩序
    fear: 自己也被当成可牺牲的一份子、失去话语权
    secret: 她曾参与过一次“分配名单”的操作，欠下人命人情
    arc: 从操控者到被迫面对后果，学会用真话换安全
    relationships:
      - with: lin_cen
        type: 邻里
        note: 互相刺探与互相利用
      - with: qiu_liyang
        type: 小圈子
        note: 通过小道消息换资源
      - with: deng_meihua
        type: 信息竞争
        note: 争夺集市话语权
    inventory: [小本子, 老式收音机]
    knowledge_flags: [knows_village_network, knows_distribution_gossip]
    status: 高调强硬
    location: loc_xu_home

  - id: qiu_liyang
    name: 邱立扬
    aliases: [邱里正, 邱主任]
    age: 46
    appearance: 皮鞋永远擦亮，雨天也不沾泥
    voice: 官腔稳，笑里带压
    flaw: 习惯交易、把人当筹码
    goal: 维持“稳定”，同时把资源与功劳都握在手里
    fear: 上级问责、秩序崩塌、自己被当替罪羊
    secret: 他与粮商的“配给回扣”链条有关联
    arc: 从操盘者到被反噬，最终被迫选择公开或自保
    relationships:
      - with: lin_guangyuan
        type: 利益同盟/制衡
        note: 宗族与行政互相借力
      - with: zhou_qiming
        type: 交易
        note: 资源互换，各留把柄
      - with: song_lei
        type: 合作/博弈
        note: 以“稳定”压住调查
      - with: he_kaijun
        type: 指挥/借刀
        note: 执行压力转嫁给基层
    inventory: [公章, 名片夹, 两张“内部通行证”]
    knowledge_flags: [knows_relief_process, knows_control_points]
    status: 稳中带险
    location: loc_village_committee

  - id: lin_guangyuan
    name: 林广元
    aliases: [林族老, 广元叔公]
    age: 72
    appearance: 眼神浑浊但锐利，拄拐，衣服永远整齐
    voice: 慢、硬、讲规矩
    flaw: 固执、以“名声”压人、牺牲个体换秩序
    goal: 让宗族在危机里不散架，保住地界与规则
    fear: 族里出丑、祠堂被关、年轻人彻底不信这套
    secret: 他知道一段旧案的关键线索，选择沉默换安稳
    arc: 从守旧到理解新秩序的必然，学会放手或承担
    relationships:
      - with: lin_cen
        type: 族亲/压力
        note: 以名声与规矩约束他
      - with: chen_shuying
        type: 人情旧账
        note: 彼此都不愿挑明
      - with: qiu_liyang
        type: 借力
        note: 互相需要
    inventory: [族谱册, 木印章]
    knowledge_flags: [knows_old_case, knows_lineage_assets]
    status: 威望尚在
    location: loc_clan_hall

  - id: zhou_qiming
    name: 周启明
    aliases: [周老板, 周记]
    age: 41
    appearance: 指甲修得很干净，笑意不达眼底
    voice: 温和，但每句话都在算账
    flaw: 控制欲强、善于恐吓与收买、缺乏同理心
    goal: 垄断关键物资与信息流，把危机变成筹码
    fear: 仓库账目暴露、运输链断裂、被上面“清理”
    secret: 他掌握失踪案的关键证物去向
    arc: 从赢家到被围猎，最终要么被揭穿要么反咬一口
    relationships:
      - with: qiu_liyang
        type: 合作
        note: 互相背书也互相提防
      - with: lin_yong
        type: 债务控制
        note: 通过欠账牵住人
      - with: he_kaijun
        type: 利益输送
        note: 用“好处”换巡查松动
      - with: lin_cen
        type: 对立
        note: 把他当可利用的棋子
    inventory: [仓库钥匙串, 账本复印件, 对讲机]
    knowledge_flags: [knows_supply_chain, knows_hoarding_nodes]
    status: 表面慈善，暗中强势
    location: loc_grain_warehouse

  - id: he_kaijun
    name: 何凯军
    aliases: [何队, 凯军]
    age: 33
    appearance: 肩宽，制服常湿，脸上有一道旧疤
    voice: 口气硬，命令句多
    flaw: 崇尚强力、习惯粗暴解决、容易被功绩诱惑
    goal: 把封控与治安做出“成绩”，换晋升与体面
    fear: 失控引发事故、自己成为背锅的那一个
    secret: 他私下收过“便利费”，留下证据链
    arc: 从强硬执行到被事实逼迫，学会守底线或彻底越线
    relationships:
      - with: song_lei
        type: 上下级
        note: 表面服从，暗地盘算
      - with: qiu_liyang
        type: 借力
        note: 互相给台阶
      - with: zhou_qiming
        type: 利益牵扯
        note: 不愿深陷但已踩线
    inventory: [执勤本, 对讲机, 手电]
    knowledge_flags: [knows_checkpoint_schedule]
    status: 强硬执勤
    location: loc_police_station

  - id: song_lei
    name: 宋磊
    aliases: [宋警官]
    age: 35
    appearance: 眼下青黑，雨披随手一披，走路很快
    voice: 冷静、短句、偏事实
    flaw: 过度理性、对人情敏感度低、容易被程序拖慢
    goal: 破案并维持秩序，在压力下守住证据与程序
    fear: 案子被压下去、证据链断、无辜者被牺牲
    secret: 他曾在一次旧案里妥协过，留下心理阴影
    arc: 从只信程序到学会借民间证据破局，但不越底线
    relationships:
      - with: he_kaijun
        type: 管理
        note: 约束他的冲动
      - with: qiu_liyang
        type: 监督/摩擦
        note: 彼此都不信对方动机
      - with: lin_cen
        type: 线索协作
        note: 不信“直觉”，只要证据
    inventory: [文件袋, 证物手套]
    knowledge_flags: [knows_case_procedure]
    status: 睡眠不足
    location: loc_police_station

  - id: deng_meihua
    name: 邓梅花
    aliases: [梅花姐]
    age: 44
    appearance: 围裙永远干净，手腕戴红绳
    voice: 笑着说狠话，爱用比喻
    flaw: 爱占便宜、口风不严、情绪化
    goal: 让摊子活下去，守住一家人的口粮与安全
    fear: 集市被封、货源断、被牵连成替罪羊
    secret: 她曾帮人藏过一包“不该有的东西”，不敢承认
    arc: 从旁观者到关键证人，学会把话说在该说的时候
    relationships:
      - with: xu_wenshu
        type: 竞争/互助
        note: 斗嘴但会互相通风
      - with: lin_cen
        type: 信息交换
        note: 用消息换跑腿与保护
      - with: zhou_qiming
        type: 供货依赖
        note: 不愿得罪
    inventory: [小秤, 记账本, 红绳]
    knowledge_flags: [knows_market_prices, knows_gossip_network]
    status: 表面热闹，内心焦虑
    location: loc_market

  - id: luo_yan
    name: 罗妍
    aliases: [阿妍]
    age: 24
    appearance: 头发总是扎得很紧，指甲有被咬的痕迹
    voice: 说话谨慎，常用“我不确定”开头
    flaw: 过度自责、对危险信号反应迟钝
    goal: 把自己从某个系统性困境里抽离出来
    fear: 牵连他人、真相曝光后失去一切
    secret: 她掌握一份“名单/流向”的片段信息
    arc: 从沉默到开口，成为推动真相的一块关键拼图
    relationships:
      - with: lin_xiaoyu
        type: 朋友/熟人
        note: 彼此知道对方的一点秘密
      - with: qiu_liyang
        type: 被管控
        note: 在资源分配上受制
    inventory: [旧U盘, 纸条]
    knowledge_flags: [knows_distribution_list_fragment]
    status: 失踪（未确认）
    location: loc_chengzhongcun

## Canon — factions/factions.yaml.bak

schema:
  - id
  - name
  - motive
  - resources
  - methods
  - public_face
  - secret

factions:
  - id: faction_clan_network
    name: 宗族与邻里互助网络（城中村）
    motive: 保住地界、名声与内部秩序，在危机中先保自己人
    resources: [人情债, 祠堂威望, 调解机制, 灰色信息渠道]
    methods: [舆论施压, 私下调解, 资源优先分配, 冷处理外人]
    public_face: 互助与守望相助、照顾老弱
    secret: 以“规矩”掩盖不公分配与旧案沉默，必要时牺牲个体换整体稳定

  - id: faction_enforcement
    name: 街道-派出所-协勤联动体系
    motive: 稳定优先、减少事故与舆情，同时完成上级指标
    resources: [执法权, 盘查卡口, 监控与登记, 临时封控令]
    methods: [限行封控, 现场处置, 以程序压争议, 选择性放行]
    public_face: 防灾救援、治安维护、打击哄抬物价
    secret: 执行口径随风向变化，易被地方关系与物资链条影响

  - id: faction_grain_network
    name: 粮商与仓储运输圈（周记为核心）
    motive: 在供给危机中垄断关键物资与信息，最大化利润与控制力
    resources: [仓库, 运输车队关系, 下游摊贩网络, 现金流]
    methods: [囤货控价, 以货换人情, 威胁收买, 制造短缺与谣言]
    public_face: “保供”与慈善捐赠、稳定市场
    secret: 通过名单与卡口打通灰色通道，关键时刻可把责任甩给基层

  - id: faction_relief_volunteers
    name: 民间救援与志愿者小队（松散）
    motive: 让物资真正到达需要的人，减少混乱与伤害
    resources: [人手, 地形熟悉, 小道消息, 临时交通工具]
    methods: [转运分发, 收集证据, 护送弱者, 与官方周旋]
    public_face: 纯公益、互助自救
    secret: 内部也会因资源不足产生分裂与“先救谁”的道德冲突

## Canon — locations/locations.yaml.bak

schema:
  - id
  - name
  - type
  - tags
  - atmosphere
  - key_objects
  - rules
  - connected_to

locations:
  - id: loc_chengzhongcun
    name: 海禾城中村
    type: urban_village
    tags: [雨季, 拥挤, 宗族, 灰色经济]
    atmosphere: 雨水顺着电线滴落，巷子窄、灯牌闪烁，湿气里混着油烟与霉味
    key_objects: [巷口栏杆, 监控盲区, 共享雨棚]
    rules:
      - 夜间临时封控不定时升级，出入需“熟面孔/通行证”
      - 口粮与救助物资在此被二次分配，信息差极大
      - 任何冲突都容易被“规矩/面子/宗族”放大
    connected_to: [loc_market, loc_village_committee, loc_clan_hall, loc_police_station]

  - id: loc_delivery_station
    name: 飞骑外卖站点
    type: workplace
    tags: [外卖, 订单, 充电, 临时通知]
    atmosphere: 雨衣一排排挂着滴水，手机提示音此起彼伏，焦虑被算法放大
    key_objects: [充电排插, 保温箱, 站长公告栏]
    rules:
      - 雨季与封控期间订单与路线频繁变更
      - 站点口头通知往往比官方公告更快
      - 迟到/差评会直接影响收入与生存
    connected_to: [loc_chengzhongcun, loc_cbd, loc_market]

  - id: loc_lin_home
    name: 林家租屋（顶楼小单间）
    type: home
    tags: [逼仄, 漏雨, 家庭压力]
    atmosphere: 墙皮起泡，雨点敲铁皮窗，屋里永远有股潮味
    key_objects: [塑料桶接水, 旧风扇, 一叠收据]
    rules:
      - 屋内储粮有限，情绪与冲突容易被放大
      - 任何外来敲门都可能带来风险或机会
    connected_to: [loc_chengzhongcun, loc_xu_home]

  - id: loc_xu_home
    name: 许家门口楼道
    type: home
    tags: [邻里, 监视, 流言]
    atmosphere: 楼道昏暗潮湿，鞋架杂乱，细碎的家常话像刀子一样划人
    key_objects: [猫眼, 楼道小凳, 旧收音机]
    rules:
      - 这里的“消息”比新闻更早抵达
      - 说错一句话会被迅速传播并变形
    connected_to: [loc_lin_home, loc_chengzhongcun]

  - id: loc_market
    name: 东港集市
    type: market
    tags: [物价, 传闻, 交易, 纠纷]
    atmosphere: 雨棚下吵闹拥挤，菜叶带泥，价签被水打湿又贴回去
    key_objects: [小秤, 价签, 临时巡查点]
    rules:
      - 价格随消息波动，囤货与抢购引发冲突
      - 巡查时段会临时清场或限购
    connected_to: [loc_chengzhongcun, loc_grain_warehouse, loc_relief_point]

  - id: loc_village_committee
    name: 村委/里正办公室
    type: government
    tags: [分配, 通行, 名单, 稳定]
    atmosphere: 空调很冷，墙上标语很热，文件夹整齐得像一排刀刃
    key_objects: [公章, 名单夹, 临时通行证]
    rules:
      - 资源分配以“名单/证明/关系”三者共同决定
      - 任何投诉都可能被引导到“维稳”框架里处理
    connected_to: [loc_chengzhongcun, loc_police_station, loc_relief_point]

  - id: loc_clan_hall
    name: 林氏祠堂
    type: shrine
    tags: [宗族, 规矩, 祭祀, 调解]
    atmosphere: 香火味混着潮木味，门槛被踩得发亮，低声议论像潮水
    key_objects: [族谱, 木印章, 供桌]
    rules:
      - “家丑不外扬”是硬规矩，公开对抗会遭集体压力
      - 调解优先于报警，但代价往往落在弱者身上
    connected_to: [loc_chengzhongcun, loc_village_committee]

  - id: loc_police_station
    name: 派出所（衙门）
    type: police
    tags: [治安, 询问, 程序, 封控]
    atmosphere: 白炽灯刺眼，雨披堆在角落，记录本一页页翻得像审判
    key_objects: [询问室, 值班台, 公告栏]
    rules:
      - 以程序与证据为准，但会受“稳定”目标影响优先级
      - 夜间出入与聚集会被重点关注
    connected_to: [loc_village_committee, loc_chengzhongcun, loc_bridge]

  - id: loc_grain_warehouse
    name: 周记粮仓
    type: warehouse
    tags: [囤货, 账本, 运输, 危险]
    atmosphere: 铁门锈水往下流，仓内干燥得不正常，空气里有粉尘味
    key_objects: [铁门锁, 叉车, 账本柜]
    rules:
      - 进出受严格控制，夜间更敏感
      - 任何“盘点/查账”都会引发反弹
    connected_to: [loc_market, loc_bridge, loc_village_committee]

  - id: loc_river_canal
    name: 排水渠与取水点
    type: water_source
    tags: [雨季, 水患, 污染, 线索]
    atmosphere: 水流浑浊，漂着杂物，雨声盖过争吵，危险被隐藏在水面下
    key_objects: [临时沙袋, 破损井盖, 水位刻度]
    rules:
      - 水位变化决定封控与通行
      - 水源可能污染，谣言与恐慌传播极快
    connected_to: [loc_chengzhongcun, loc_farmland, loc_bridge]

  - id: loc_farmland
    name: 近郊菜地与棚区
    type: farmland
    tags: [农时, 供应, 偷采, 抢地]
    atmosphere: 泥泞、湿冷，塑料棚啪啪作响，作物被雨打得东倒西歪
    key_objects: [塑料棚, 水泵, 简易工具房]
    rules:
      - 产出受农时与天气限制，短期无法凭意志“增产”
      - 工具/化肥/燃料短缺会直接压低产量
    connected_to: [loc_river_canal, loc_market]

  - id: loc_cbd
    name: 海禾CBD雨幕高楼群
    type: cbd
    tags: [对比, 玻璃, 秩序, 冷漠]
    atmosphere: 玻璃幕墙反射灰天，雨伞像黑点移动，秩序干净但疏离
    key_objects: [写字楼大堂, 地下通道, 安检闸机]
    rules:
      - 安检与登记更严格，陌生面孔更容易被拦
      - 信息公开但不透明：公告多，解释少
    connected_to: [loc_delivery_station, loc_bridge]

  - id: loc_relief_point
    name: 赈灾物资发放点
    type: relief
    tags: [排队, 名单, 摩擦, 希望]
    atmosphere: 队伍在雨里拉长，塑料雨衣窸窣作响，怨气与期待交织
    key_objects: [登记台, 物资箱, 临时围栏]
    rules:
      - 物资按“名单+时段”发放，错过即视为放弃
      - 现场冲突会被迅速以治安名义处理
    connected_to: [loc_village_committee, loc_market]

  - id: loc_bridge
    name: 港湾桥与检查卡口
    type: checkpoint
    tags: [卡口, 通行, 盘查, 运输]
    atmosphere: 雨幕下红蓝灯闪烁，水汽把人脸糊成一团，车辆一辆辆挪
    key_objects: [路障, 临检岗亭, 反光锥桶]
    rules:
      - 关键时段限行，货车优先级取决于“证明/关系”
      - 盘查以临时口径为准，规则会随消息变
    connected_to: [loc_police_station, loc_grain_warehouse, loc_river_canal, loc_cbd]

## Canon — premise.md.bak

# Premise（可执行）

## 世界观一句话
- 当代沿海城市雨季，供应链与基层秩序在灾害压力下失衡；一个外卖员被困在“同一天三次循环”里，逼近一桩失踪案真相。

## 主题 / 基调
- 主题：选择与代价
- 基调：写实、紧张、克制（信息靠行动与后果呈现，不靠说教）

## 叙事视角约束
- 视角：第三人称限知（紧贴主角），不得跳 POV；必要信息通过对话、现场细节与可验证线索呈现。
- 结构：章节以“目标->阻力->升级->钩子”推进；循环元素必须服务悬疑与人物选择，不做炫技展示。

## 尺度边界（内容分级）
- 面向：大众向
- 暴力/血腥：可出现冲突与危险，但描写克制，避免细节化血腥。
- 成人内容：不露骨，必要时点到即止。
- 恐怖/压迫：可有紧张与压迫感，但避免持续性虐待细节与过度生理恐怖。
- 其它敏感点：不美化违法犯罪；不浪漫化胁迫；不以“神秘设定”替代因果推理。

## 禁改规则（项目硬约束）
- 世界规则：同一天最多三次循环；循环有明确限制（见 `canon/rules/world_rules.md`），不可被随意扩容为“无限重来”。
- 主角核心缺陷：嘴硬心软、回避代价与责任（不可被抹掉，只能被推动与转化）。
- 主题底色：所有关键推进必须让人物“做选择并付出代价”，不得变调为纯爽文碾压或金手指解题。

## Canon — rules/world_rules.md.bak

# World Rules（可执行）

## 世界规则（不可随意突破）
- 现实主义因果：信息、资源、权力都会留下痕迹；“好结果”必须付出可感知代价。
- 资源稀缺优先：物资短缺会放大人性与秩序裂缝；任何人都无法凭空变出粮与工具。
- 基层秩序逻辑：名单、通行、封控、面子与关系是现实的“门槛系统”，比口号更有效。

## 科技 / 超自然体系
- 科技水平：当代城市社会（手机、监控、外卖平台、短视频传播）。
- 异常机制：存在“同一天最多三次循环”的异常现象（与人物有关，但不公开化、不成体系化魔法）。

## 饥荒年（供应危机年）生存与生产硬规则

### 1) 农时与产出
- 近郊菜地/棚区受雨季影响：连续降雨会导致烂根、病害，产出不是“想要就有”。
- 增产需要输入：种子、肥料、塑料棚、水泵、燃料与人力；短缺会形成连锁下滑。
- 采收与运输决定实际供给：路断、卡口、积水会让“有产出”变成“到不了市场”。

### 2) 粮价与市场
- 价格受三件事驱动：供给（仓与田）、消息（谣言/公告）、执法（查仓/限购）。
- 市场不是透明的：同一物资在不同圈层有“关系价/名单价/黑价”。
- 囤货与抛货都会留下痕迹：仓库进出、摊贩供货、运输路线可被追溯。

### 3) 配给、粮票与名单
- 配给只能解决“分配”，不能解决“短缺”；名单决定谁先饿、谁后饿。
- 名单的漏洞：代领、冒名、重复登记、内部口径变更；都需要现实证据才能推翻。
- 任何“通融”都有对价：人情、劳务、沉默、或未来的一个要求。

### 4) 徭役（强制劳务）与征用
- 形式：清障排涝、搬运物资、夜间值守、临时征用车辆/人手。
- 规则：谁去、去多久、是否算工分/补贴，往往由基层口径决定；拒绝会触发惩罚（封控、通行受限、口粮优先级下降）。
- 现实后果：体力透支、受伤风险、与家人分离带来的次生灾害。

### 5) 赈灾与救助
- 赈灾物资有链条：来源->仓储->发放点->到户；每一段都有截流与误差空间。
- 发放以“证件/名单/时段”三件套为核心；错过时段通常不补发。
- 现场秩序优先：冲突会被以治安名义处理，弱者更容易失去资格。

### 6) 治安、封控与卡口
- 封控的目标是“减少不可控变量”，因此规则会突然升级或临时变化。
- 卡口的权力来自“解释权”：同一证明在不同人手里会得到不同结果。
- 灰色通道永远存在，但每次使用都增加暴露概率与人情债。

### 7) 工具与材料获取限制
- 雨季硬通货：电（充电/照明）、燃料（机动/水泵）、防水材料、药品。
- 维修与替换困难：电动车/手机等关键工具损坏会立刻影响生存能力与行动半径。
- 物资获取要么靠钱，要么靠关系，要么靠风险（偷、抢、灰色交易）；三者必取其一。

## 时间循环规则（用于悬疑，但必须受限）
- 次数上限：同一天最多三次循环；超过则不发生（不可无限重来）。
- 记忆与信息：允许保留主角的记忆与可记录信息，但“他人认知”不会随循环保留。
- 物理与伤害：身体状态随循环重置，但精神疲劳与判断偏差会累积（表现为焦虑、冲动、迟钝）。
- 证据约束：靠循环获得的结论必须落到可验证证据上，否则无法说服任何体系内的人。

## 硬边界（不可突破项）
- 不可无限循环；不可随意新增“第四次/第五次”。
- 不可凭空创造物资；不可无成本获得权力与通行。
- 不可“全知破案”：关键推理必须来自可见证据链。
- 不可用超自然一笔抹平现实矛盾（关系、资源、制度压力必须在场）。

## 代价与后果（强制体现）
- 每一次选择都必须带来后果：失去时间、失去信任、失去资源、或承担风险升级。
- 危机不会因为主角努力就自动缓解：雨季、物价、封控等外部压力会持续挤压。

## Canon — style/style_guide.md.bak

# Style Guide（可执行）

## 人称 / 视角 / 时态（锁定）
- 人称：第三人称
- 视角：第三人称限知（主角近距离跟拍）；不得跳 POV、不得全知旁白
- 时态：叙述以“过去时/完成体”表达为主；同章内避免无理由切换（尤其避免“现在时直播感”）

## 段落长度 / 对话比例 / 节奏（约束）
- 段落长度：每段 2–5 句为主；超过 8 句必须拆段（避免信息堆叠）
- 对话比例：30%–45%（用对话承载博弈与信息，但不靠解释性对白灌输设定）
- 节奏：每 500–800 字至少一次“推进/转折/信息增量/风险升级”之一；避免长时间原地踏步

## 禁用写法（硬禁）
- 灌水：重复信息、无推进场景、无新冲突的对白拉扯
- 跳 POV：同一章随意切换视角/内心
- 旁白说教：用作者口吻解释主题/价值观
- “剧透式总结”：直接告诉读者下一步如何、人物如何改变而不通过行动呈现
- 设定抛洒：用大段解释代替线索与后果；设定必须被“用起来”并产生代价
- 金手指碾压：循环/信息优势必须伴随成本与反噬，不得直接开挂通关

## 每章结构建议（默认模板）
1) 开场钩子：立即给读者一个问题/不安/目标
2) 推进：围绕本章目标推动行动与信息
3) 升级：代价、误判、阻力、或新线索引发更大压力
4) 结尾钩子：`新信息/误判/危机升级/目标转向` 四选一（必须落到剧情层面）

## 时间循环书写规范（避免读者混乱）
- 每次循环开始必须给出清晰时间锚点（例如“同一上午/同一地点/同一声提示音”），但不得出现元叙事解释。
- 同一事件的重复呈现：只保留“与上次不同的关键差异”，其余用一句话压缩带过。
- 线索呈现：任何关键推理链条必须由可见证据支撑（现场细节、对话矛盾、交易痕迹），禁止凭空顿悟。

## 禁止出现 AI 痕迹（零容忍）
- 正文不得出现：系统提示、模型、AI、提示词、生成、工具链、作者自述等任何痕迹。
- 任何“流程说明/任务分解/检查清单”只能出现在 `runs/` 与 QA 报告中，不得进入正文。

