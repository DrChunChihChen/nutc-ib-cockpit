# -*- coding: utf-8 -*-
"""
Apply 國際深化度 formula update:
國際深化度 (%) = 境外生人數 / 日四技總人數 * 100%
Across interactive_dashboard.html, index.html, dist/index.html, rebuild_audited_raw_data.py
"""
import re
import json

FILE_PATH = "/Users/chenchunchih/Downloads/校務資料/interactive_dashboard.html"
with open(FILE_PATH, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update Table header
content = content.replace(
    '<th class="p-3 text-right whitespace-nowrap min-w-[115px]">境外生 (佔比)</th>',
    '<th class="p-3 text-right whitespace-nowrap min-w-[130px]" title="國際深化度公式：境外生人數 ÷ 日四技總人數 × 100%">國際深化度 <span class="text-[10px] text-slate-400 font-normal">(境外/日四技)</span></th>'
)

# 2. Update Table sort dropdown
content = content.replace(
    '<option value="oversea_pct_desc">國際化境外佔比 (由高到低)</option>',
    '<option value="oversea_pct_desc">國際深化度 (境外/日四技 由高到低)</option>'
)

# 3. Update Table cell rendering in renderRegionalTable
old_cell = """                        <td class="p-3 lg:p-3.5 text-right text-slate-600 whitespace-nowrap min-w-[115px]">${item.oversea_stu}人 <span class="text-[10px] lg:text-[11px] text-slate-400">(${item.oversea_pct.toFixed(1)}%)</span></td>"""
new_cell = """                        <td class="p-3 lg:p-3.5 text-right text-slate-600 whitespace-nowrap min-w-[130px]"><span class="font-mono font-bold text-sky-700">${item.oversea_pct.toFixed(2)}%</span> <span class="text-[10px] text-slate-400">(${item.oversea_stu}人)</span></td>"""
content = content.replace(old_cell, new_cell)

# 4. Update Mobile card rendering in renderRegionalTable
old_mobile_card = """                                    <div class="flex justify-between py-0.5 border-b border-slate-100">
                                        <span class="text-slate-400">境外生(佔比):</span>
                                        <span class="font-semibold text-slate-800">${item.oversea_stu}人 (${item.oversea_pct.toFixed(1)}%)</span>
                                    </div>"""
new_mobile_card = """                                    <div class="flex justify-between py-0.5 border-b border-slate-100">
                                        <span class="text-slate-400">國際深化度 (境外/日四技):</span>
                                        <span class="font-semibold text-sky-700 font-mono">${item.oversea_pct.toFixed(2)}% <span class="text-slate-500 font-normal">(${item.oversea_stu}人)</span></span>
                                    </div>"""
content = content.replace(old_mobile_card, new_mobile_card)

# 5. Update Radar label
content = content.replace(
    "labels: ['生源吸附力 (錄取分)', '規模抗震度 (在學生)', '國際化深度 (境外生)', '註冊穩定度 (日間註冊)', '留存防禦力 (100-退學)'],",
    "labels: ['生源吸附力 (錄取分)', '規模抗震度 (在學生)', '國際深化度 (境外/日四技)', '註冊穩定度 (日間註冊)', '留存防禦力 (100-退學)'],"
)
content = content.replace(
    '評估維度：生源吸附力 (統測均分)、日間規模力 (純日間在學)、國際化深度 (境外生比)、日間註冊率、日間留存度 (100 - 日間退學率)。',
    '評估維度：生源吸附力 (統測均分)、日間規模力 (純日間在學)、國際深化度 (境外生/日四技)、日間註冊率、日間留存度 (100 - 日間退學率)。'
)

# 6. Update Module 3 student breakdown
content = content.replace(
    '<span class="text-slate-600">境外學位生 (國際化)</span>\n                                <span class="font-bold text-sky-700">58人 (佔純日間在學 8.19%，以港澳及東南亞為主)</span>',
    '<span class="text-slate-600">境外學位生 (國際深化度)</span>\n                                <span class="font-bold text-sky-700">58人 (日四技深化度 15.18% [58/382]，全數深耕大學部)</span>'
)

# 7. Update DB object
db_match = re.search(r'const DB = (\{.*?\});', content)
if db_match:
    db = json.loads(db_match.group(1))
    # Update oversea_pct and radar for 6 schools
    # Formula: 境外生人數 / 日四技總人數 * 100
    # 中科: 58 / 382 = 15.18%
    # 北商: 68 / 439 = 15.49% (日四技境外生 63/439 = 14.35%)
    # 雲科: 20 / 104 = 19.23%
    # 高科航管: 13 / 415 = 3.13%
    # 高科國企: 40 / 251 = 15.94% (日四技境外生 27/251 = 10.76%)
    # 高科供應鏈: 4 / 240 = 1.67%
    
    updated_six = [
        {
            "code": "北商-國商",
            "school": "臺北商業大學",
            "dept": "國際商務系/科",
            "region": "北部",
            "total_stu": 759,
            "five_year": 266,
            "undergrad_day": 439,
            "undergrad_eve": 0,
            "grad": 54,
            "grad_detail": "日碩32 · 電商產碩12 · 文創產碩10",
            "grad_tooltip": "日間碩士班 32人、跨境電商產碩 12人、文創產碩 10人 (無獨立博士與碩專)",
            "faculty_total": 23,
            "faculty_prof": 8,
            "faculty_assoc": 11,
            "faculty_asst": 1,
            "oversea_stu": 68,
            "day_four_year": 439,
            "oversea_pct": 15.49,
            "intl_depth_four_year": 14.35, # 63/439
            "reg_114_rate": 100.0,
            "reg_114_quota": 58,
            "reg_114_act": 58,
            "score_113": 80.93,
            "score_114": 76.10,
            "score_delta": -4.83,
            "drop_cnt_113": 21,
            "drop_rate_113": 2.77,
            "type": "都會菁英旗艦",
            "radar": [88, 80, 77, 100, 88]
        },
        {
            "code": "中科-國貿",
            "school": "臺中科技大學",
            "dept": "國際貿易與經營系/科",
            "region": "中部",
            "total_stu": 708,
            "five_year": 252,
            "undergrad_day": 456,
            "undergrad_eve": 0,
            "grad": 0,
            "grad_detail": "統整於商學院碩士班",
            "grad_tooltip": "系所專注培育大學部，研究所名額由商學院統整統籌",
            "faculty_total": 21,
            "faculty_prof": 4,
            "faculty_assoc": 14,
            "faculty_asst": 3,
            "oversea_stu": 58,
            "day_four_year": 382,
            "oversea_pct": 15.18,
            "intl_depth_four_year": 15.18, # 58/382 (100%在日四技)
            "reg_114_rate": 99.06,
            "reg_114_quota": 80,
            "reg_114_act": 79,
            "score_113": 75.56,
            "score_114": 71.78,
            "score_delta": -3.78,
            "drop_cnt_113": 20,
            "drop_rate_113": 2.82,
            "type": "中部公立頂尖旗艦",
            "radar": [78, 85, 76, 99, 88]
        },
        {
            "code": "雲科-國管",
            "school": "雲林科技大學",
            "dept": "國際管理學士學位學程",
            "region": "中部",
            "total_stu": 104,
            "five_year": 0,
            "undergrad_day": 104,
            "undergrad_eve": 0,
            "grad": 0,
            "grad_detail": "統整於管院企管碩班",
            "grad_tooltip": "系所專注全英語學士班，研究所名額統整於管院國際企管碩班",
            "faculty_total": 3,
            "faculty_prof": 1,
            "faculty_assoc": 0,
            "faculty_asst": 2,
            "oversea_stu": 20,
            "day_four_year": 104,
            "oversea_pct": 19.23,
            "intl_depth_four_year": 19.23, # 20/104
            "reg_114_rate": 100.0,
            "reg_114_quota": 17,
            "reg_114_act": 17,
            "score_113": 81.33,
            "score_114": 73.80,
            "score_delta": -7.53,
            "drop_cnt_113": 4,
            "drop_rate_113": 3.85,
            "type": "精緻國際小學程",
            "radar": [82, 20, 95, 100, 80]
        },
        {
            "code": "高科-航管",
            "school": "高雄科技大學",
            "dept": "航運管理系",
            "region": "南部",
            "total_stu": 494,
            "five_year": 0,
            "undergrad_day": 415,
            "undergrad_eve": 0,
            "grad": 79,
            "grad_detail": "在職41 · 日碩20 · 博士18",
            "grad_tooltip": "碩士在職專班 41人、日間碩士班 20人、博士班 18人",
            "faculty_total": 13,
            "faculty_prof": 8,
            "faculty_assoc": 4,
            "faculty_asst": 1,
            "oversea_stu": 13,
            "day_four_year": 415,
            "oversea_pct": 3.13,
            "intl_depth_four_year": 1.69, # 7/415
            "reg_114_rate": 98.86,
            "reg_114_quota": 86,
            "reg_114_act": 85,
            "score_113": 73.56,
            "score_114": 71.20,
            "score_delta": -2.36,
            "drop_cnt_113": 20,
            "drop_rate_113": 4.05,
            "type": "海運物流利基型",
            "radar": [78, 65, 30, 99, 78]
        },
        {
            "code": "高科-國企",
            "school": "高雄科技大學",
            "dept": "國際企業系",
            "region": "南部",
            "total_stu": 364,
            "five_year": 0,
            "undergrad_day": 251,
            "undergrad_eve": 0,
            "grad": 113,
            "grad_detail": "在職52 · 日碩30 · 博士30 · 產碩1",
            "grad_tooltip": "碩士在職專班 52人、日間碩士班 30人、博士班 30人、珠寶產碩延畢 1人",
            "faculty_total": 13,
            "faculty_prof": 8,
            "faculty_assoc": 2,
            "faculty_asst": 3,
            "oversea_stu": 40,
            "day_four_year": 251,
            "oversea_pct": 15.94,
            "intl_depth_four_year": 10.76, # 27/251
            "reg_114_rate": 100.0,
            "reg_114_quota": 45,
            "reg_114_act": 45,
            "score_113": 76.44,
            "score_114": 70.80,
            "score_delta": -5.64,
            "drop_cnt_113": 15,
            "drop_rate_113": 4.12,
            "type": "南部綜合型研發",
            "radar": [76, 50, 78, 100, 77]
        },
        {
            "code": "高科-供應鏈",
            "school": "高雄科技大學",
            "dept": "供應鏈管理系",
            "region": "南部",
            "total_stu": 266,
            "five_year": 0,
            "undergrad_day": 240,
            "undergrad_eve": 0,
            "grad": 26,
            "grad_detail": "日碩17 · 在職9",
            "grad_tooltip": "日間碩士班 17人、碩士在職專班 9人",
            "faculty_total": 9,
            "faculty_prof": 1,
            "faculty_assoc": 7,
            "faculty_asst": 1,
            "oversea_stu": 4,
            "day_four_year": 240,
            "oversea_pct": 1.67,
            "intl_depth_four_year": 1.25, # 3/240
            "reg_114_rate": 96.15,
            "reg_114_quota": 52,
            "reg_114_act": 50,
            "score_113": 71.85,
            "score_114": 70.10,
            "score_delta": -1.75,
            "drop_cnt_113": 10,
            "drop_rate_113": 3.76,
            "type": "專精新興領域型",
            "radar": [74, 38, 20, 96, 79]
        }
    ]
    db["regional_six"] = updated_six
    new_db_str = "const DB = " + json.dumps(db, ensure_ascii=False) + ";"
    content = content[:db_match.start()] + new_db_str + content[db_match.end():]
    print("DB object updated with new international depth values!")

# 8. Update CSV headers in exportAllCSV and Data Modal
content = content.replace(
    "境外生比率(%)",
    "國際深化度(%)"
)

with open(FILE_PATH, "w", encoding="utf-8") as f:
    f.write(content)

with open("/Users/chenchunchih/Downloads/校務資料/index.html", "w", encoding="utf-8") as f:
    f.write(content)

with open("/Users/chenchunchih/Downloads/校務資料/dist/index.html", "w", encoding="utf-8") as f:
    f.write(content)

print("Updated HTML files!")
