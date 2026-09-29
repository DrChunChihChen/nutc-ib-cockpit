# -*- coding: utf-8 -*-
"""
四技二專甄選入學交叉查榜數據解析器 (com.tw vtech)
目標：國立臺中科技大學 國際貿易與經營系 (113001) vs 企業管理系 (113002)
解析指標：核定名額、正備取人數、報到率、正取放棄率、備取遞補深度、被外校掠奪矩陣 (Poaching Matrix)
"""

import os
import re
import json
from bs4 import BeautifulSoup

def parse_com_tw_html(file_path_or_html):
    if os.path.exists(file_path_or_html):
        with open(file_path_or_html, 'r', encoding='utf-8', errors='ignore') as f:
            html = f.read()
    else:
        html = file_path_or_html

    soup = BeautifulSoup(html, 'html.parser')
    
    # 提取系所基本資訊
    page_title = soup.title.string if soup.title else ""
    header_text = soup.get_text()
    
    # 判斷是國貿還是企管
    dept_name = "國際貿易與經營系" if ("國際貿易" in header_text or "113001" in file_path_or_html) else "企業管理系"
    
    candidates = []
    # com.tw 榜單表格分析
    # 通常每列代表一個考生，欄位包含：准考證號、姓名、本系錄取狀態(正/備取)、其他錄取校系(含分發標記)
    rows = soup.find_all('tr')
    
    total_main = 0
    total_reserve = 0
    main_enrolled = 0
    reserve_enrolled = 0
    max_reserve_enrolled_rank = 0
    
    poached_destinations = {} # 搶走本系學生的他校系
    won_from_destinations = {} # 選擇本系而放棄的他校系
    
    for r in rows:
        cells = r.find_all(['td', 'th'])
        if len(cells) < 3:
            continue
        row_text = r.get_text(separator=' ', strip=True)
        
        # 判斷是否為考生列 (含有正取或備取)
        is_main = '正取' in row_text
        is_reserve = '備取' in row_text
        
        if not (is_main or is_reserve):
            continue
            
        cand_info = {
            'text': row_text,
            'is_main': is_main,
            'is_reserve': is_reserve,
            'reserve_rank': 0,
            'final_choice': None,
            'is_enrolled_here': False,
            'other_offers': []
        }
        
        # 解析備取名次
        if is_reserve:
            total_reserve += 1
            m_rank = re.search(r'備取\s*(\d+)', row_text)
            if m_rank:
                cand_info['reserve_rank'] = int(m_rank.group(1))
        elif is_main:
            total_main += 1
            
        # 檢查本系是否分發就讀
        # com.tw 中通常以「分發錄取」、「就讀」或特殊 class/tag 標註最終去向
        if '分發錄取' in row_text or '就讀' in row_text:
            # 判斷是分發到本系，還是分發到其他學校
            # 例如：中科國貿 欄位後面帶有 (分發錄取)
            if re.search(r'(臺中科技大學|中科).*?(國際貿易|企管|本系).*?(分發|錄取|★)', row_text):
                cand_info['is_enrolled_here'] = True
                if is_main:
                    main_enrolled += 1
                elif is_reserve:
                    reserve_enrolled += 1
                    if cand_info['reserve_rank'] > max_reserve_enrolled_rank:
                        max_reserve_enrolled_rank = cand_info['reserve_rank']
            else:
                # 被其他學校搶走，提取最終錄取學校
                m_dest = re.search(r'([^\s]+(?:大學|學院|科大)[^\s]+).*?(?:分發錄取|就讀|★)', row_text)
                if m_dest:
                    dest = m_dest.group(1).strip()
                    cand_info['final_choice'] = dest
                    poached_destinations[dest] = poached_destinations.get(dest, 0) + 1
        
        candidates.append(cand_info)
        
    return {
        'dept_name': dept_name,
        'total_candidates': len(candidates),
        'total_main': total_main,
        'total_reserve': total_reserve,
        'main_enrolled': main_enrolled,
        'reserve_enrolled': reserve_enrolled,
        'max_reserve_depth': max_reserve_enrolled_rank,
        'poached_destinations': poached_destinations
    }

if __name__ == '__main__':
    print("交叉查榜解析引擎已就緒。")
