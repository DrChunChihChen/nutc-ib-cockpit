# -*- coding: utf-8 -*-
"""
中科大「國際貿易與經營系」 vs 「企業管理系」硬數字客觀比較分析
資料來源：教育部大專校院校務資訊公開平台 (https://udb.moe.edu.tw)
"""

import urllib.request
import ssl
import urllib.parse
import io
import csv
import json

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

print("1. 下載師資資料...")
h_tea, rows_tea = fetch_csv('教1-1.專任教師數-以「系(所)」統計.csv')

print("2. 下載在學學生人數資料...")
h_stu, rows_stu = fetch_csv('學1-1.正式學籍在學學生人數-以「系(所)」統計.csv')

print("3. 下載新生註冊率資料...")
h_reg, rows_reg = fetch_csv('學12-1.新生(含境外生)註冊率-以「系(所)」統計.csv')

print("4. 下載退學人數資料...")
h_drop, rows_drop = fetch_csv('學14-1.退學人數-以「系(所)」統計(111學年度起).csv')

print("5. 下載休學人數資料...")
h_sus, rows_sus = fetch_csv('學13-1.於學年底處於休學狀態之人數-以「系(所)」統計(111學年度起).csv')

# ----------------- 師資比較 -----------------
# h_tea: ['學年度', '設立別', '學校類別', '學校統計處代碼', '學校名稱', '單位代碼', '單位名稱', '專任教師數-教師總數總計', '男', '女', '教授男', '教授女', '副教授男', '副教授女', '助理教授男', '助理教授女', '講師男', '講師女', ...]
tea_nutc = [r for r in rows_tea if '臺中科技大學' in r[4]]
latest_yr_tea = sorted(list(set(r[0] for r in tea_nutc)), reverse=True)[0]
itm_tea = [r for r in tea_nutc if r[0] == latest_yr_tea and '國際貿易' in r[6]][0]
ba_tea = [r for r in tea_nutc if r[0] == latest_yr_tea and '企業管理' in r[6]][0]

itm_t_tot = int(itm_tea[7])
itm_prof = int(itm_tea[10]) + int(itm_tea[11])
itm_assoc = int(itm_tea[12]) + int(itm_tea[13])
itm_asst = int(itm_tea[14]) + int(itm_tea[15])
itm_lect = int(itm_tea[16]) + int(itm_tea[17])

ba_t_tot = int(ba_tea[7])
ba_prof = int(ba_tea[10]) + int(ba_tea[11])
ba_assoc = int(ba_tea[12]) + int(ba_tea[13])
ba_asst = int(ba_tea[14]) + int(ba_tea[15])
ba_lect = int(ba_tea[16]) + int(ba_tea[17])

print(f"\n=== 1. 專任師資結構 (最新 {latest_yr_tea} 學年度) ===")
print(f"指標                       | 國際貿易與經營系       | 企業管理系")
print(f"----------------------------------------------------------------------")
print(f"專任教師總數               | {itm_t_tot:2d} 人 (男{itm_tea[8]}/女{itm_tea[9]})       | {ba_t_tot:2d} 人 (男{ba_tea[8]}/女{ba_tea[9]})")
print(f"  - 正教授                 | {itm_prof:2d} 人 ({itm_prof/itm_t_tot*100:4.1f}%)         | {ba_prof:2d} 人 ({ba_prof/ba_t_tot*100:4.1f}%)")
print(f"  - 副教授                 | {itm_assoc:2d} 人 ({itm_assoc/itm_t_tot*100:4.1f}%)         | {ba_assoc:2d} 人 ({ba_assoc/ba_t_tot*100:4.1f}%)")
print(f"  - 助理教授               | {itm_asst:2d} 人 ({itm_asst/itm_t_tot*100:4.1f}%)         | {ba_asst:2d} 人 ({ba_asst/ba_t_tot*100:4.1f}%)")
print(f"  - 講師                   | {itm_lect:2d} 人 ({itm_lect/itm_t_tot*100:4.1f}%)         | {ba_lect:2d} 人 ({ba_lect/ba_t_tot*100:4.1f}%)")

# ----------------- 在學學生人數比較 -----------------
# h_stu: ['學年度', '設立別', '學校類別', '學校統計處代碼', '學校名稱', '系所代碼', '系所名稱', '學制班別', '在學學生數小計', '在學學生數男', '在學學生數女']
stu_nutc = [r for r in rows_stu if '臺中科技大學' in r[4]]
latest_yr_stu = sorted(list(set(r[0] for r in stu_nutc)), reverse=True)[0]

def get_dept_students(dept_keyword):
    d = {'五專': 0, '日間四技': 0, '進修四技': 0, '日間碩士': 0, '碩士在職': 0, '技優領航': 0, '其他': 0, '總計': 0, '男': 0, '女': 0}
    rows = [r for r in stu_nutc if r[0] == latest_yr_stu and dept_keyword in r[6]]
    for r in rows:
        name = r[6]
        program = r[7]
        cnt = int(r[8]) if len(r) > 8 and r[8].isdigit() else 0
        male = int(r[9]) if len(r) > 9 and r[9].isdigit() else 0
        female = int(r[10]) if len(r) > 10 and r[10].isdigit() else 0
        d['總計'] += cnt
        d['男'] += male
        d['女'] += female
        if '五專' in program:
            d['五專'] += cnt
        elif '碩士在職' in name or '碩士在職' in program:
            d['碩士在職'] += cnt
        elif '碩士' in program:
            d['日間碩士'] += cnt
        elif '技優' in name:
            d['技優領航'] += cnt
        elif '日間' in program:
            d['日間四技'] += cnt
        elif '進修' in program:
            d['進修四技'] += cnt
        else:
            d['其他'] += cnt
    return d

itm_students = get_dept_students('國際貿易')
ba_students = get_dept_students('企業管理')

print(f"\n=== 2. 在學學生規模比較 (最新 {latest_yr_stu} 學年度) ===")
print(f"學制類別                   | 國際貿易與經營系(科)   | 企業管理系(科)")
print(f"----------------------------------------------------------------------")
print(f"全系在學學生總人數         | {itm_students['總計']:4d} 人 (男{itm_students['男']}/女{itm_students['女']})  | {ba_students['總計']:4d} 人 (男{ba_students['男']}/女{ba_students['女']})")
print(f"  - 五專部                 | {itm_students['五專']:4d} 人 (一班制)        | {ba_students['五專']:4d} 人 (二班制)")
print(f"  - 日間學士班(四技/二技)  | {itm_students['日間四技']:4d} 人               | {ba_students['日間四技']:4d} 人")
print(f"  - 技優專班               | {itm_students['技優領航']:4d} 人               | {ba_students['技優領航']:4d} 人")
print(f"  - 進修學士班(四技/二技)  | {itm_students['進修四技']:4d} 人               | {ba_students['進修四技']:4d} 人")
print(f"  - 日間碩士班             | {itm_students['日間碩士']:4d} 人 (無)          | {ba_students['日間碩士']:4d} 人")
print(f"  - 碩士在職專班 (EMBA)    | {itm_students['碩士在職']:4d} 人 (無)          | {ba_students['碩士在職']:4d} 人")
print(f"生師比 (學生數 / 專任師)   | {itm_students['總計']/itm_t_tot:4.1f}                   | {ba_students['總計']/ba_t_tot:4.1f}")

# ----------------- 招生與註冊率比較 (113 vs 114) -----------------
reg_nutc = [r for r in rows_reg if '臺中科技大學' in r[4]]

def get_reg_stats(dept_kw, year):
    # returns list of (prog,核定,实注,境外,注册率)
    res = []
    for r in reg_nutc:
        if r[0] == str(year) and dept_kw in r[6]:
            prog = f"{r[7]}{r[8]}"
            h_quota = int(r[9]) if r[9].isdigit() else 0
            act_reg = int(r[11]) if r[11].isdigit() else 0
            oversea = int(r[12]) if r[12].isdigit() else 0
            rate = r[13]
            res.append({
                'prog': prog,
                'name': r[6],
                'quota': h_quota,
                'reg': act_reg,
                'oversea': oversea,
                'rate': rate
            })
    return res

print(f"\n=== 3. 招生與新生註冊率詳細比對 (113 vs 114 學年度) ===")
for yr in ['113', '114']:
    print(f"\n--- 【{yr} 學年度】招生績效比對 ---")
    itm_r = get_reg_stats('國際貿易', yr)
    ba_r = get_reg_stats('企業管理', yr)
    
    print(f"國際貿易與經營系(科):")
    for item in itm_r:
        print(f"  [{item['prog']}] 核定:{item['quota']:2d} | 實註:{item['reg']:2d} | 境外:{item['oversea']:2d} | 註冊率: {item['rate']}%")
    print(f"企業管理系(科):")
    for item in ba_r:
        print(f"  [{item['prog']}] 核定:{item['quota']:2d} | 實註:{item['reg']:2d} | 境外:{item['oversea']:2d} | 註冊率: {item['rate']}%")

# ----------------- 休退學率比較 -----------------
# h_drop: ['學年度', '學期', '設立別', '學校類別', '學校統計處代碼', '學校名稱', '系所代碼', '系所名稱', '學制班別', '性別', '在學學生數', '學期間退學人數-總計', '學生自請退學-小計', '就讀學校、科系不符期待', ...]
drop_nutc = [r for r in rows_drop if len(r)>5 and '臺中科技大學' in r[5]]
latest_yr_drop = sorted(list(set(r[0] for r in drop_nutc)), reverse=True)[0]

def analyze_drop(dept_kw):
    rows = [r for r in drop_nutc if r[0] == latest_yr_drop and dept_kw in r[7]]
    total_students = sum(int(r[10]) for r in rows if r[10].isdigit())
    total_drop = sum(int(r[11]) for r in rows if r[11].isdigit())
    self_drop = sum(int(r[12]) for r in rows if r[12].isdigit())
    mismatch_drop = sum(int(r[13]) for r in rows if r[13].isdigit())
    work_drop = sum(int(r[18]) for r in rows if r[18].isdigit())
    forced_drop = sum(int(r[20]) for r in rows if r[20].isdigit()) # 勒令退学
    return {
        'students': total_students,
        'drop': total_drop,
        'rate': (total_drop / total_students * 100) if total_students > 0 else 0,
        'self': self_drop,
        'mismatch': mismatch_drop,
        'work': work_drop,
        'forced': forced_drop
    }

itm_drop = analyze_drop('國際貿易')
ba_drop = analyze_drop('企業管理')

print(f"\n=== 4. 學期間退學與流失情況比對 (最新 {latest_yr_drop} 學年度) ===")
print(f"指標                       | 國際貿易與經營系       | 企業管理系")
print(f"----------------------------------------------------------------------")
print(f"在學學生母數 (含兩學期人次)| {itm_drop['students']:5d} 人              | {ba_drop['students']:5d} 人")
print(f"退學總人數                 | {itm_drop['drop']:5d} 人              | {ba_drop['drop']:5d} 人")
print(f"整體退學率                 | {itm_drop['rate']:5.2f}%               | {ba_drop['rate']:5.2f}%")
print(f"  - 學生自請退學小計       | {itm_drop['self']:5d} 人              | {ba_drop['self']:5d} 人")
print(f"    * 因科系不符期待自請   | {itm_drop['mismatch']:5d} 人              | {ba_drop['mismatch']:5d} 人")
print(f"    * 因工作需求自請       | {itm_drop['work']:5d} 人              | {ba_drop['work']:5d} 人")
print(f"  - 學校勒令退學 (逾期等)  | {itm_drop['forced']:5d} 人              | {ba_drop['forced']:5d} 人")

# ----------------- 休學人數比較 -----------------
# h_sus: ['學年度', '設立別', '學校類別', '學校統計處代碼', '學校名稱', '系所代碼', '系所名稱', '日間/進修', '學制班別', '在學學生數', '休學學生數', ...]
sus_nutc = [r for r in rows_sus if len(r)>4 and '臺中科技大學' in r[4]]
latest_yr_sus = sorted(list(set(r[0] for r in sus_nutc)), reverse=True)[0]
itm_sus_rows = [r for r in sus_nutc if r[0] == latest_yr_sus and '國際貿易' in r[6]]
ba_sus_rows = [r for r in sus_nutc if r[0] == latest_yr_sus and '企業管理' in r[6]]

itm_sus_stu = sum(int(r[9]) for r in itm_sus_rows if r[9].isdigit())
itm_sus_cnt = sum(int(r[10]) for r in itm_sus_rows if r[10].isdigit())

ba_sus_stu = sum(int(r[9]) for r in ba_sus_rows if r[9].isdigit())
ba_sus_cnt = sum(int(r[10]) for r in ba_sus_rows if r[10].isdigit())

print(f"\n=== 5. 學年底處於休學狀態人數比對 ({latest_yr_sus} 學年度) ===")
print(f"指標                       | 國際貿易與經營系       | 企業管理系")
print(f"----------------------------------------------------------------------")
print(f"在學人數                   | {itm_sus_stu:5d} 人              | {ba_sus_stu:5d} 人")
print(f"處於休學狀態人數           | {itm_sus_cnt:5d} 人              | {ba_sus_cnt:5d} 人")
print(f"休學比率                   | {(itm_sus_cnt/itm_sus_stu*100) if itm_sus_stu>0 else 0:5.2f}%               | {(ba_sus_cnt/ba_sus_stu*100) if ba_sus_stu>0 else 0:5.2f}%")
