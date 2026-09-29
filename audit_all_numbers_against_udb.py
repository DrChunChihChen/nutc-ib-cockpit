# -*- coding: utf-8 -*-
"""
Auditing all numbers against official cached MOE UDB CSVs
"""
import os
import csv
import pandas as pd
from collections import defaultdict

CACHE_DIR = '/Users/chenchunchih/Downloads/校務資料/moe_udb_cache'

print("=" * 80)
print("【審計 1】國立臺中科技大學 國際貿易與經營系（科）在教育部 UDB 的完整官方原始數據")
print("=" * 80)

# 1. 教1-1: 專任教師數
f_tea = os.path.join(CACHE_DIR, '教1-1.專任教師數-以「系(所)」統計.csv')
with open(f_tea, 'r', encoding='utf-8-sig', errors='ignore') as f:
    reader = csv.reader(f)
    h_tea = next(reader)
    rows_tea = [r for r in reader if '臺中科技大學' in str(r) and '國際貿易' in str(r)]

print("\n--- 1. 教1-1 專任教師數 (最新年份) ---")
print("欄位:", h_tea)
for r in sorted(rows_tea, key=lambda x: x[0], reverse=True)[:5]:
    print(f"學年度: {r[0]} | 學校: {r[4]} | 單位: {r[6]} | 總數: {r[7]} | 男: {r[8]} | 女: {r[9]} | 教授: {int(r[10])+int(r[11])} | 副教授: {int(r[12])+int(r[13])} | 助理教授: {int(r[14])+int(r[15])} | 講師: {int(r[16])+int(r[17])}")

# 2. 學1-1: 正式學籍在學學生人數
f_stu = os.path.join(CACHE_DIR, '學1-1.正式學籍在學學生人數-以「系(所)」統計.csv')
with open(f_stu, 'r', encoding='utf-8-sig', errors='ignore') as f:
    reader = csv.reader(f)
    h_stu = next(reader)
    rows_stu = [r for r in reader if '臺中科技大學' in str(r) and '國際貿易' in str(r)]

print("\n--- 2. 學1-1 在學學生人數 (最新學年度) ---")
print("欄位:", h_stu)
latest_yr_stu = max(r[0] for r in rows_stu)
print(f"最新學年度: {latest_yr_stu}")
nutc_itm_stu_rows = [r for r in rows_stu if r[0] == latest_yr_stu]
for r in nutc_itm_stu_rows:
    print(f"  系所: {r[6]} | 學制: {r[7]} | 總在學: {r[8]} | 男: {r[9]} | 女: {r[10]}")

# 3. 學12-1: 新生註冊率
f_reg = os.path.join(CACHE_DIR, '學12-1.新生(含境外生)註冊率-以「系(所)」統計.csv')
with open(f_reg, 'r', encoding='utf-8-sig', errors='ignore') as f:
    reader = csv.reader(f)
    h_reg = next(reader)
    rows_reg = [r for r in reader if '臺中科技大學' in str(r) and '國際貿易' in str(r)]

print("\n--- 3. 學12-1 新生註冊率 (111~114 學年度) ---")
print("欄位:", h_reg[:15])
for yr in sorted(list(set(r[0] for r in rows_reg)), reverse=True):
    if int(yr) >= 111:
        print(f"\n【{yr} 學年度】")
        for r in [x for x in rows_reg if x[0] == yr]:
            print(f"  系所: {r[6]} | 日夜: {r[7]} | 學制: {r[8]} | 核定: {r[9]} | 保留: {r[10]} | 實註: {r[11]} | 境外: {r[12]} | 註冊率: {r[13]}%")

# 4. 學13-1: 休學人數
f_sus = os.path.join(CACHE_DIR, '學13-1.於學年底處於休學狀態之人數-以「系(所)」統計(111學年度起).csv')
with open(f_sus, 'r', encoding='utf-8-sig', errors='ignore') as f:
    reader = csv.reader(f)
    h_sus = next(reader)
    rows_sus = [r for r in reader if '臺中科技大學' in str(r) and '國際貿易' in str(r)]

print("\n--- 4. 學13-1 於學年底處於休學狀態之人數 ---")
print("欄位:", h_sus[:15])
for yr in sorted(list(set(r[0] for r in rows_sus)), reverse=True)[:3]:
    print(f"\n【{yr} 學年度】")
    for r in [x for x in rows_sus if x[0] == yr]:
        print(f"  系所: {r[7]} | 學制: {r[8]} | 性別: {r[9]} | 在學生數: {r[10]} | 休學總計: {r[11]}")

# 5. 學14-1: 退學人數
f_drop = os.path.join(CACHE_DIR, '學14-1.退學人數-以「系(所)」統計(111學年度起).csv')
with open(f_drop, 'r', encoding='utf-8-sig', errors='ignore') as f:
    reader = csv.reader(f)
    h_drop = next(reader)
    rows_drop = [r for r in reader if '臺中科技大學' in str(r) and '國際貿易' in str(r)]

print("\n--- 5. 學14-1 退學人數與退學原因 ---")
print("欄位:", h_drop[:22])
for yr in sorted(list(set(r[0] for r in rows_drop)), reverse=True)[:2]:
    print(f"\n【{yr} 學年度】")
    by_prog = defaultdict(lambda: {'students': 0, 'drop_tot': 0, 'reasons': defaultdict(int)})
    for r in [x for x in rows_drop if x[0] == yr]:
        prog = r[8]
        stu = int(r[10]) if r[10].isdigit() else 0
        drp = int(r[11]) if r[11].isdigit() else 0
        by_prog[prog]['students'] += stu
        by_prog[prog]['drop_tot'] += drp
        # check specific reasons
        # r[13]: 就讀不符期待, r[17]: 經濟困難, r[18]: 工作, r[23]: 逾期未註冊, r[24]: 休學逾期未復學
        for idx, col_name in [(13, '志趣不合/不符期待'), (17, '經濟困難'), (18, '工作就業'), (23, '逾期未註冊'), (24, '休學逾期未復學')]:
            if len(r) > idx and r[idx].isdigit():
                by_prog[prog]['reasons'][col_name] += int(r[idx])
    
    for prog, d in by_prog.items():
        rate = (d['drop_tot'] / d['students'] * 100) if d['students'] > 0 else 0
        print(f"  學制: {prog:15s} | 在學數: {d['students']:4d} | 退學數: {d['drop_tot']:3d} | 退學率: {rate:5.2f}% | 原因分析: {dict(d['reasons'])}")

