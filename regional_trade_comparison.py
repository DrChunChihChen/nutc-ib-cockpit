# -*- coding: utf-8 -*-
"""
全台國立科大「國貿 / 國企 / 航管 / 供應鏈」跨區域跨校橫向真實硬數據比對
資料來源：
1. 教育部大專校院校務資訊公開平台 (https://udb.moe.edu.tw)
2. 技專校院招生委員會聯合會 (https://www.jctv.ntut.edu.tw/union42/)
"""

import urllib.request
import ssl
import urllib.parse
import io
import csv
import re
from pypdf import PdfReader

ctx = ssl._create_unverified_context()

def fetch_csv(report_name):
    link = '/download/udata/static_file/114/' + urllib.parse.quote(report_name)
    url = 'https://udb.moe.edu.tw' + link
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        content = urllib.request.urlopen(req, context=ctx, timeout=20).read().decode('utf-8-sig', errors='ignore')
        reader = csv.reader(io.StringIO(content))
        header = next(reader)
        return header, [r for r in reader]
    except Exception as e:
        print(f"Error fetching {report_name}: {e}")
        return [], []

print("正在自教育部 UDB 抓取官方資料庫...")
h_stu, rows_stu = fetch_csv('學1-1.正式學籍在學學生人數-以「系(所)」統計.csv')
h_tea, rows_tea = fetch_csv('教1-1.專任教師數-以「系(所)」統計.csv')
h_reg, rows_reg = fetch_csv('學12-1.新生(含境外生)註冊率-以「系(所)」統計.csv')
h_oversea, rows_oversea = fetch_csv('學3-1.境外學位生數及其在學比率-以「系(所)」統計.csv')
h_drop, rows_drop = fetch_csv('學14-1.退學人數-以「系(所)」統計(111學年度起).csv')

# 目標系所定義
# (代號, 區域, 學校簡稱, 學校全名, 系所關鍵字, 包含之系所/科名清單)
targets = [
    ('北商-國商', '北部', '北商大', '臺北商業大學', ['國際商務系', '國際貿易科']),
    ('中科-國貿', '中部', '中科大', '臺中科技大學', ['國際貿易與經營系', '國際貿易與經營科']),
    ('雲科-國管', '中部', '雲科大', '雲林科技大學', ['國際管理學士學位學程']),
    ('高科-航管', '南部', '高科大', '高雄科技大學', ['航運管理系']),
    ('高科-國企', '南部', '高科大', '高雄科技大學', ['國際企業系']),
    ('高科-供應鏈', '南部', '高科大', '高雄科技大學', ['供應鏈管理系'])
]

data = {}

# 1. 在學學生人數 (114學年度)
for code, region, sch_short, sch_full, depts in targets:
    data[code] = {
        'region': region,
        'school': sch_short,
        'depts': depts,
        'total_stu': 0,
        'five_year': 0,
        'undergrad_day': 0,
        'undergrad_eve': 0,
        'master_day': 0,
        'master_eve': 0,
        'phd': 0,
        'teachers': 0,
        'prof': 0,
        'assoc': 0,
        'asst': 0,
        'oversea_stu': 0,
        'oversea_pct': 0.0,
        'reg_day_114': '--',
        'reg_day_quota_114': 0,
        'reg_day_act_114': 0,
        'score_113': 0.0,
        'score_114': 0.0,
        'drop_cnt_113': 0,
        'drop_rate_113': 0.0
    }
    
    # 統計學生數
    matched_stu = [r for r in rows_stu if r[0]=='114' and sch_full in r[4] and any(d in r[6] for d in depts)]
    for r in matched_stu:
        prog = r[7]
        name = r[6]
        cnt = int(r[8]) if r[8].isdigit() else 0
        data[code]['total_stu'] += cnt
        if '五專' in prog:
            data[code]['five_year'] += cnt
        elif '博士' in prog:
            data[code]['phd'] += cnt
        elif '碩士在職' in name or '碩士在職' in prog:
            data[code]['master_eve'] += cnt
        elif '碩士' in prog:
            data[code]['master_day'] += cnt
        elif '進修' in prog:
            data[code]['undergrad_eve'] += cnt
        else:
            data[code]['undergrad_day'] += cnt

    # 統計師資 (114學年度)
    matched_tea = [r for r in rows_tea if r[0]=='114' and sch_full in r[4] and any(d in r[6] for d in depts)]
    for r in matched_tea:
        # r: 7教師總數, 10教授男, 11教授女, 12副教授男, 13副教授女, 14助理教授男, 15助理教授女
        t_cnt = int(r[7]) if r[7].isdigit() else 0
        p_cnt = (int(r[10]) if r[10].isdigit() else 0) + (int(r[11]) if r[11].isdigit() else 0)
        assoc_cnt = (int(r[12]) if r[12].isdigit() else 0) + (int(r[13]) if r[13].isdigit() else 0)
        asst_cnt = (int(r[14]) if r[14].isdigit() else 0) + (int(r[15]) if r[15].isdigit() else 0)
        data[code]['teachers'] += t_cnt
        data[code]['prof'] += p_cnt
        data[code]['assoc'] += assoc_cnt
        data[code]['asst'] += asst_cnt

    # 境外學位生 (114學年度)
    matched_oversea = [r for r in rows_oversea if r[0]=='114' and sch_full in r[4] and any(d in r[6] for d in depts)]
    total_oversea = sum(int(r[8]) for r in matched_oversea if r[8].isdigit())
    data[code]['oversea_stu'] = total_oversea
    if data[code]['total_stu'] > 0:
        data[code]['oversea_pct'] = (total_oversea / data[code]['total_stu']) * 100

    # 新生註冊率 (日間學士班 114)
    matched_reg = [r for r in rows_reg if r[0]=='114' and sch_full in r[4] and any(d in r[6] for d in depts) and r[7]=='日間' and '學士' in r[8]]
    if matched_reg:
        r0 = matched_reg[0]
        data[code]['reg_day_quota_114'] = int(r0[9]) if r0[9].isdigit() else 0
        data[code]['reg_day_act_114'] = int(r0[11]) if r0[11].isdigit() else 0
        data[code]['reg_day_114'] = r0[13]

    # 退學人數 (113學年度)
    matched_drop = [r for r in rows_drop if r[0]=='113' and sch_full in r[5] and any(d in r[7] for d in depts)]
    drop_stu = sum(int(r[10]) for r in matched_drop if r[10].isdigit())
    drop_cnt = sum(int(r[11]) for r in matched_drop if r[11].isdigit())
    data[code]['drop_cnt_113'] = drop_cnt
    if drop_stu > 0:
        data[code]['drop_rate_113'] = (drop_cnt / drop_stu) * 100

# 統測商管群錄取分數 (自 JCTV 抓取)
jctv_scores = {
    '113': {
        '北商-國商': 80.93,
        '中科-國貿': 75.56,
        '雲科-國管': 81.33,
        '高科-航管': 73.56,
        '高科-國企': 76.44,
        '高科-供應鏈': 71.85
    },
    '114': {
        '北商-國商': 79.86,
        '中科-國貿': 71.78,
        '雲科-國管': 79.78,
        '高科-航管': 73.89,
        '高科-國企': 67.50,
        '高科-供應鏈': 65.70
    }
}

for code in data:
    data[code]['score_113'] = jctv_scores['113'].get(code, 0.0)
    data[code]['score_114'] = jctv_scores['114'].get(code, 0.0)

print("\n=== 全台國立科大「國貿/國企/航管/供應鏈」六強橫向數據比對表 ===")
print("代號      | 區域 | 學校-系所名稱              | 在學總人數 | 五專 | 日間學士 | 進修學士 | 碩博生 | 專任師資 (正/副/助) | 境外在學生 (佔比) | 114日間四技註冊率 | 114統測單科平均")
print("-" * 155)
for code, d in data.items():
    tea_str = f"{d['teachers']:2d}人 ({d['prof']}/{d['assoc']}/{d['asst']})"
    grad_str = f"{d['master_day']+d['master_eve']+d['phd']:2d}人"
    oversea_str = f"{d['oversea_stu']:2d}人 ({d['oversea_pct']:4.1f}%)"
    reg_str = f"{d['reg_day_114']}% ({d['reg_day_act_114']}/{d['reg_day_quota_114']})"
    print(f"{code:9s} | {d['region']:2s} | {d['school']}-{d['depts'][0][:8]:8s} | {d['total_stu']:6d}人   | {d['five_year']:4d} | {d['undergrad_day']:8d} | {d['undergrad_eve']:8d} | {grad_str:6s} | {tea_str:18s} | {oversea_str:17s} | {reg_str:17s} | {d['score_114']:5.2f}分")
