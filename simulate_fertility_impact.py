# -*- coding: utf-8 -*-
"""
中科大國貿系「少子化海嘯」衝擊模擬模型 (113~128學年度)
數據基礎：
1. 教育部統計處《113至128學年度各教育階段學生數預測報告》
2. 內政部戶政司歷年出生人口統計
3. 技專校院招生委員會聯合會統測商管群歷年報考人數
"""

import numpy as np

# 113 ~ 128 學年度時間軸
years = list(range(113, 129))

# 教育部預測：大專一年級新生總人數 (萬人)
# 112: 19.5萬 -> 113: 18.8萬 -> 117(虎年): 15.6萬 -> 121: 16.2萬 -> 128: 14.8萬
freshmen_total = [
    18.8,  # 113
    18.4,  # 114
    17.9,  # 115
    16.8,  # 116
    15.6,  # 117 (虎年海嘯谷底)
    16.1,  # 118 (微幅回彈)
    16.5,  # 119
    16.4,  # 120
    16.0,  # 121
    15.6,  # 122
    15.3,  # 123
    15.1,  # 124
    14.9,  # 125
    14.8,  # 126
    14.8,  # 127
    14.8   # 128
]

# 統測總報考人數推估 (萬人) - 技職縮水速度高於普高 (比例自 42% 逐年降至 35%)
tcte_total = [round(f * 0.40, 2) for f in freshmen_total]
# 商業與管理群報名人數 (約佔統測總人數之 20%~18%)
tcte_business = [round(t * 0.19, 2) for t in tcte_total]

# 中部地區 (中彰投苗) 商管群高職考生預估池 (約佔全國 22%)
central_business_pool = [int(b * 10000 * 0.22) for b in tcte_business]

# 模擬中科大國貿系各學制註冊率與最低錄取分走勢
print("=== 教育部 113~128 學年度少子化預測與統測商管生源衝擊模擬 ===")
print("學年度 | 大一新生總數 | 統測報考總數 | 統測商管群人數 | 中部商管生源池 | 日間四技錄取平均分預測 | 進修四技註冊率預測 | 五專部滿招防禦度")
print("-" * 115)

sim_results = []

for idx, yr in enumerate(years):
    fresh = freshmen_total[idx]
    tcte = tcte_total[idx]
    biz = tcte_business[idx]
    pool = central_business_pool[idx]
    
    # 日間四技錄取門檻模擬：
    # 基準 114 年為 71.78 分 (考生池約 3,080 人)
    # 當生源池縮小，前段國立科大依然有吸磁效應，但最低分數會往下漂移 (每少 10% 考生，錄取分約承壓 1.2~1.5 分)
    pool_ratio = pool / central_business_pool[1] # 相對 114 年比率
    day_score = round(71.78 - (1.0 - pool_ratio) * 12.0, 2)
    if day_score < 60.0:
        day_score = 60.0 # 國立底線
        
    # 進修四技註冊率模擬：
    # 114 年已跌至 50.91% (實註 28 人 / 核定 55 人)
    # 進修部受少子化打擊最致命，年輕人寧可去一般大學或工作，進修四技將面臨斷崖
    eve_rate = round(50.91 * (pool_ratio ** 1.8), 1)
    if eve_rate < 15.0:
        eve_rate_str = f"{eve_rate:4.1f}% (瀕臨停招)"
    elif eve_rate < 35.0:
        eve_rate_str = f"{eve_rate:4.1f}% (極度危險)"
    else:
        eve_rate_str = f"{eve_rate:4.1f}% (嚴峻)"
        
    # 五專部防禦度：五專在 117 年前後會因國中畢業生減少而有短期壓力，但因公立學費便宜與前三年免學費，防禦力仍高
    if yr in [116, 117]:
        five_defense = "良好 (約92~95%)"
    else:
        five_defense = "極穩 (98~100%)"
        
    print(f"{yr}學年 |  {fresh:4.1f} 萬人   |  {tcte:4.2f} 萬人   |   {biz:4.2f} 萬人    |   {pool:4d} 人    |       {day_score:5.2f} 分       | {eve_rate_str:18s} | {five_defense}")
    
    sim_results.append({
        'yr': yr, 'fresh': fresh, 'biz': biz, 'pool': pool,
        'day_score': day_score, 'eve_rate': eve_rate
    })
