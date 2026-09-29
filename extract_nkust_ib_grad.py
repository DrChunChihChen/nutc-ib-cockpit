# -*- coding: utf-8 -*-
import os, csv
from collections import defaultdict

CACHE_DIR = '/Users/chenchunchih/Downloads/校務資料/moe_udb_cache'

# 1. Registration (學12-1)
f_reg = os.path.join(CACHE_DIR, '學12-1.新生(含境外生)註冊率-以「系(所)」統計.csv')
reg_data = []
with open(f_reg, 'r', encoding='utf-8-sig', errors='ignore') as fp:
    reader = csv.DictReader(fp)
    for r in reader:
        if r['學校統計處代碼'] == '0053' and r['系所代碼'] == '04141023':
            if '碩士' in r['學制班別'] or '博士' in r['學制班別'] or '碩士' in r['系所名稱'] or '博士' in r['系所名稱']:
                reg_data.append({
                    'yr': r['學年度'],
                    'name': r['系所名稱'],
                    'day_eve': r['日間/進修'],
                    'prog': r['學制班別'],
                    'quota': int(r['當學年度總量內核定新生招生名額(A)']) if r['當學年度總量內核定新生招生名額(A)'].isdigit() else 0,
                    'reg': int(r['當學年度總量內新生招生核定名額之實際註冊人數(C)']) if r['當學年度總量內新生招生核定名額之實際註冊人數(C)'].isdigit() else 0,
                    'overseas': int(r['當學年度各學系境外(新生)學生實際註冊人數 (E)']) if r['當學年度各學系境外(新生)學生實際註冊人數 (E)'].isdigit() else 0,
                    'rate': float(r['當學年度新生註冊率(%)D=〔(C+E)/(A-B+E)〕＊100％']) if r['當學年度新生註冊率(%)D=〔(C+E)/(A-B+E)〕＊100％'].replace('.','',1).isdigit() else 0.0,
                    'note': r['當學年度系所招生特色說明'],
                    'url': r['當學年度招生特色說明資訊網']
                })

# 2. Enrollment (學1-1)
f_stu = os.path.join(CACHE_DIR, '學1-1.正式學籍在學學生人數-以「系(所)」統計.csv')
stu_data = []
with open(f_stu, 'r', encoding='utf-8-sig', errors='ignore') as fp:
    reader = csv.DictReader(fp)
    for r in reader:
        if r['學校統計處代碼'] == '0053' and r['系所代碼'] == '04141023':
            if '碩士' in r['學制班別'] or '博士' in r['學制班別']:
                tot = int(r['在學學生數小計']) if r['在學學生數小計'].isdigit() else 0
                m = int(r['在學學生數男']) if r['在學學生數男'].isdigit() else 0
                w = int(r['在學學生數女']) if r['在學學生數女'].isdigit() else 0
                stu_data.append({
                    'yr': r['學年度'],
                    'name': r['系所名稱'],
                    'prog': r['學制班別'],
                    'total': tot,
                    'male': m,
                    'female': w,
                    'female_pct': round((w / tot * 100), 2) if tot > 0 else 0.0
                })

# 3. Foreign Students (學3-2)
f_for = os.path.join(CACHE_DIR, '學3-2.外國學生數及其在學比率-以「系(所)」統計.csv')
for_data = []
with open(f_for, 'r', encoding='utf-8-sig', errors='ignore') as fp:
    reader = csv.DictReader(fp)
    for r in reader:
        if r['學校統計處代碼'] == '0053' and r['系所代碼'] == '04141023':
            if '碩士' in r['學制班別(日間)'] or '博士' in r['學制班別(日間)']:
                tot = int(r['外國學生小計']) if r['外國學生小計'].isdigit() else 0
                m = int(r['外國學生數男']) if r['外國學生數男'].isdigit() else 0
                w = int(r['外國學生女']) if r['外國學生女'].isdigit() else 0
                rate = float(r['外國學生數之在學比率(%)']) if r['外國學生數之在學比率(%)'].replace('.','',1).isdigit() else 0.0
                for_data.append({
                    'yr': r['學年度'],
                    'name': r['系所名稱'],
                    'prog': r['學制班別(日間)'],
                    'total': tot,
                    'male': m,
                    'female': w,
                    'rate': rate
                })

# 4. Graduates (學2-1)
f_grad = os.path.join(CACHE_DIR, '學2-1.畢業生數及其取得輔系、雙主修資格人數-以「系(所)」統計.csv')
grad_data = []
with open(f_grad, 'r', encoding='utf-8-sig', errors='ignore') as fp:
    reader = csv.DictReader(fp)
    for r in reader:
        if r['學校統計處代碼'] == '0053' and r['系所代碼'] == '04141023':
            if '碩士' in r['學制班別'] or '博士' in r['學制班別']:
                tot = int(r['畢業生數小計']) if r['畢業生數小計'].isdigit() else 0
                m = int(r['畢業生數男']) if r['畢業生數男'].isdigit() else 0
                w = int(r['畢業生數女']) if r['畢業生數女'].isdigit() else 0
                grad_data.append({
                    'yr': r['學年度'],
                    'name': r['系所名稱'],
                    'prog': r['學制班別'],
                    'total': tot,
                    'male': m,
                    'female': w,
                    'female_pct': round((w / tot * 100), 2) if tot > 0 else 0.0
                })

# 5. Faculty (教1-1)
f_tea = os.path.join(CACHE_DIR, '教1-1.專任教師數-以「系(所)」統計.csv')
tea_data = []
with open(f_tea, 'r', encoding='utf-8-sig', errors='ignore') as fp:
    reader = csv.DictReader(fp)
    for r in reader:
        if r['學校統計處代碼'] == '0053' and r['單位代碼'] == '04141023':
            tea_data.append({
                'yr': r['學年度'],
                'total': int(r['專任教師數-教師總數總計']),
                'male': int(r['專任教師數-教師總數男']),
                'female': int(r['專任教師數-教師總數女']),
                'prof': int(r['專任教師數-教授男']) + int(r['專任教師數-教授女']),
                'assoc': int(r['專任教師數-副教授男']) + int(r['專任教師數-副教授女']),
                'asst': int(r['專任教師數-助理教授男']) + int(r['專任教師數-助理教授女']),
                'lect': int(r['專任教師數-講師男']) + int(r['專任教師數-講師女'])
            })

print(f"Loaded: reg={len(reg_data)}, stu={len(stu_data)}, foreign={len(for_data)}, grad={len(grad_data)}, tea={len(tea_data)}")
