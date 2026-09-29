# -*- coding: utf-8 -*-
"""
com.tw 四技二專甄選交叉查榜深度抽取器 (含 Base64 影像解析與分發流向)
"""

import os, re, json, base64
from bs4 import BeautifulSoup
import subprocess

def extract_cross_data(html_path):
    with open(html_path, 'r', encoding='utf-8', errors='ignore') as f:
        html = f.read()

    soup = BeautifulSoup(html, 'html.parser')
    
    # 找到考生數據主表 (通常有 headers: 准考證號碼, 姓名, 校系名稱, 二階甄試)
    tables = soup.find_all('table')
    target_table = None
    for t in tables:
        txt = t.get_text()
        if '准考證號碼' in txt and '校系名稱' in txt:
            target_table = t
            break

    if not target_table:
        print("未找到包含考生准考證的表格")
        return {}

    rows = target_table.find_all('tr')
    
    header_title = rows[0].get_text(separator=' ', strip=True) if len(rows) > 0 else ""
    print(f"=== 分析系所表頭: {header_title} ===")
    
    candidates = []
    current_cand = None
    
    # 解析表格中的考生與其報考志願
    for r in rows[2:]:
        row_text = r.get_text(separator=' ', strip=True)
        imgs = r.find_all('img')
        
        # 判斷是否為新考生的第一列 (通常包含准考證 base64 圖片 或 '*' 號姓名分隔)
        # 在 com.tw 中，新考生列通常在第一或第二個 td 有准考證與姓名圖片，且有 '*'
        is_new_cand = '*' in row_text or any('1500' in img.get('src', '') for img in imgs) or len(r.find_all('td')) >= 15
        
        # 檢查該列是否有「分發錄取」圖標 (putdep1.png)
        has_putdep = any('putdep' in img.get('src', '') for img in imgs)
        
        # 尋找該列中的大專校系名稱 (以「大學」或「科技大學」或「學院」為特徵)
        dept_match = re.findall(r'(國立[^\s]+(?:大學|學院|科大)[^\s]+|[^\s]+(?:大學|學院|科大)[^\s]+)', row_text)
        
        if is_new_cand and ('國立' in row_text or '大學' in row_text):
            if current_cand:
                candidates.append(current_cand)
            current_cand = {
                'cand_index': len(candidates) + 1,
                'offers': [],
                'enrolled_dept': None,
                'poached_by': None
            }
            
        if current_cand:
            for dept in dept_match:
                dept_clean = re.sub(r'[\*\s]+', '', dept)
                if len(dept_clean) > 4 and dept_clean not in [o['dept'] for o in current_cand['offers']]:
                    is_this_dept_enrolled = has_putdep and (dept in row_text)
                    offer_info = {
                        'dept': dept_clean,
                        'is_enrolled': is_this_dept_enrolled
                    }
                    current_cand['offers'].append(offer_info)
                    if is_this_dept_enrolled:
                        current_cand['enrolled_dept'] = dept_clean
                        if '臺中科技大學' not in dept_clean and '國際貿易' not in dept_clean:
                            current_cand['poached_by'] = dept_clean

    if current_cand:
        candidates.append(current_cand)

    print(f"成功萃取考生總數: {len(candidates)} 名")
    
    # 統計流向
    poaching_stats = {}
    enrolled_nutc = 0
    abandoned_or_unplaced = 0
    
    for c in candidates:
        enrolled = c['enrolled_dept']
        if enrolled:
            if '臺中科技大學' in enrolled or '中科' in enrolled:
                enrolled_nutc += 1
            else:
                poaching_stats[enrolled] = poaching_stats.get(enrolled, 0) + 1
        else:
            abandoned_or_unplaced += 1
            
    summary = {
        'title': header_title,
        'total_candidates': len(candidates),
        'enrolled_nutc': enrolled_nutc,
        'abandoned_or_unplaced': abandoned_or_unplaced,
        'poaching_stats': poaching_stats,
        'candidates_detail': candidates
    }
    return summary

if __name__ == '__main__':
    path = '/Users/chenchunchih/Downloads/校務資料/113001.html'
    if os.path.exists(path):
        res = extract_cross_data(path)
        print("\n--- 考生微觀流向明細 ---")
        for c in res['candidates_detail']:
            print(f"考生 #{c['cand_index']}:")
            print(f"  重疊錄取志願: {[o['dept'] for o in c['offers']]}")
            print(f"  最終分發就讀: {c['enrolled_dept'] if c['enrolled_dept'] else '未分發/放棄'}")
            if c['poached_by']:
                print(f"  🚨 生源被奪走: {c['poached_by']}")
        print("\n--- 掠奪中科國貿生源之對手排行榜 ---")
        for dept, cnt in sorted(res['poaching_stats'].items(), key=lambda x: x[1], reverse=True):
            print(f"  - {dept}: 被搶走 {cnt} 名學生")
        print(f"  - 放棄或未分發至列出校系: {res['abandoned_or_unplaced']} 名")
