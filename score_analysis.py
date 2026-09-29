# -*- coding: utf-8 -*-
"""
四技二專聯合登記分發（統測）近 6 年（109~114學年度）商管群最低錄取分數與消長分析
資料來源：技專校院招生委員會聯合會 (https://www.jctv.ntut.edu.tw/union42/)
"""

import urllib.request
import ssl
import io
import re
from pypdf import PdfReader

ctx = ssl._create_unverified_context()

targets = [
    ('中科大國貿', '臺中科技大學', '國際貿易與經營系'),
    ('中科大企管', '臺中科技大學', '企業管理系'),
    ('雲科大企管', '雲林科技大學', '企業管理系'),
    ('北商大國際商務', '臺北商業大學', '國際商務系'),
    ('北商大企管', '臺北商業大學', '企業管理系'),
    ('勤益企管', '勤益科技大學', '企業管理系')
]

years = ['109', '110', '111', '112', '113', '114']

def parse_weight_sum(w_str):
    nums = re.findall(r'\*(\d+\.?\d*)', w_str)
    return sum(float(n) for n in nums)

results = {t[0]: {} for t in targets}

for yr in years:
    url = f'https://www.jctv.ntut.edu.tw/downloads/{yr}/union42/{yr}_up01.pdf'
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        content = urllib.request.urlopen(req, context=ctx, timeout=20).read()
        reader = PdfReader(io.BytesIO(content))
        
        all_text = ''
        for p in reader.pages:
            t = p.extract_text()
            if '09商業與管理群' in t or '商業與管理' in t:
                all_text += t + '\n'
        
        lines = all_text.splitlines()
        for label, sch, dept in targets:
            for line in lines:
                if '09商業與管理群' in line and sch in line and dept in line:
                    m = re.search(r'(國文\*.*?專業\(二\)\*\d+\.\d+)\s+(\d+)\s+(\d+)\s+([\d\.]+)', line)
                    if m:
                        weights = m.group(1)
                        w_sum = parse_weight_sum(weights)
                        admitted = int(m.group(3))
                        score = float(m.group(4))
                        avg_score = score / w_sum if w_sum > 0 else 0
                        results[label][yr] = {
                            'score': score,
                            'w_sum': w_sum,
                            'avg': avg_score,
                            'admitted': admitted
                        }
                        break
    except Exception as e:
        print(f"Error {yr}: {e}")

print("=== 近 6 年統測 09商業與管理群 折合單科平均分數比較 ===")
print("學年度 | 中科大國貿 | 中科大企管 | (企管-國貿) | 雲科大企管 | 北商國際商務 | 北商企管 | 勤益企管")
print("-" * 85)
for yr in years:
    itm = results['中科大國貿'].get(yr, {}).get('avg', 0)
    ba = results['中科大企管'].get(yr, {}).get('avg', 0)
    diff = ba - itm
    yun = results['雲科大企管'].get(yr, {}).get('avg', 0)
    ntub_ib = results['北商大國際商務'].get(yr, {}).get('avg', 0)
    ntub_ba = results['北商大企管'].get(yr, {}).get('avg', 0)
    ncut = results['勤益企管'].get(yr, {}).get('avg', 0)
    
    diff_str = f"+{diff:4.2f}" if diff >= 0 else f"{diff:4.2f}"
    print(f"{yr}學年 |  {itm:5.2f}分   |  {ba:5.2f}分   |   {diff_str}分   |  {yun:5.2f}分   |   {ntub_ib:5.2f}分   | {ntub_ba:5.2f}分 | {ncut:5.2f}分")
