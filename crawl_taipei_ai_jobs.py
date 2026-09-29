import requests
import json
import time
import re
import csv
import os

API_URL = 'https://www.104.com.tw/jobs/search/api/jobs'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
    'Referer': 'https://www.104.com.tw/jobs/search/',
    'Accept': 'application/json, text/plain, */*'
}

AREAS = {
    '6001001000': '台北市',
    '6001002000': '新北市'
}

CATEGORIES = {
    '2004000000': '行銷/企劃/專案管理',
    '2005000000': '客服/業務/電商/貿易',
    '2002000000': '行政/總務/法務',
    '2013000000': '傳播藝術/設計',
    '2014000000': '文字/傳媒工作',
    '2001000000': '經營/人資'
}

KEYWORDS = ['ChatGPT', '生成式AI', 'AI工具', 'Gemini', 'Claude', 'Midjourney', 'Copilot']

def parse_salary(salary_str):
    """Parse salary string to normalized monthly min and max in TWD"""
    salary_str = salary_str.replace(',', '').strip()
    
    # 1. Monthly (月薪)
    m = re.search(r'月薪\s*(\d+)(?:[~至]\s*(\d+))?元', salary_str)
    if m:
        low = int(m.group(1))
        high = int(m.group(2)) if m.group(2) else low
        return low, high, '月薪'
        
    # 2. Hourly (時薪) -> convert approx to full-time 160h
    m_hour = re.search(r'時薪\s*(\d+)(?:[~至]\s*(\d+))?元', salary_str)
    if m_hour:
        low = int(m_hour.group(1)) * 160
        high = (int(m_hour.group(2)) if m_hour.group(2) else int(m_hour.group(1))) * 160
        return low, high, '時薪折算'
        
    # 3. Annual (年薪) -> convert / 13.5
    m_yr = re.search(r'年薪\s*(\d+)(?:[~至]\s*(\d+))?元', salary_str)
    if m_yr:
        low = int(int(m_yr.group(1)) / 13.5)
        high = int(int(m_yr.group(2)) / 13.5) if m_yr.group(2) else low
        return low, high, '年薪折算'
        
    # 4. Negotiable (面議)
    if '面議' in salary_str:
        return 40000, None, '面議'
        
    return None, None, '其他'

def classify_target_industry(ind_desc, comp_name, job_name, desc):
    text = f"{ind_desc} {comp_name} {job_name} {desc}".lower()
    
    if any(k in text for k in ['生技', '生物科技', '醫療', '醫藥', '藥局', '保健', '醫學', '診所', '健康']):
        return '生技/醫療保健'
    if any(k in text for k in ['電商', '電子商務', '網購', '蝦皮', 'momo', '零售', '團購', '選品', '網路購物']):
        return '電子商務/數位零售'
    if any(k in text for k in ['製造', '機械', '五金', '金屬', '模具', '塑膠', '加工', '精密', '汽機車', '自行車', '工具機', '工業', '紡織', '傳產']):
        return '傳統製造/精密工業'
    if any(k in text for k in ['補習', '文教', '教育', '補教', '美語', '留學', '學校', '升學', '安親', '培訓']):
        return '文教/補教培訓'
    if any(k in text for k in ['廣告', '公關', '行銷顧問', '設計公司', '室內設計', '整合行銷', '傳播']):
        return '廣告行銷/公關顧問'
    if any(k in text for k in ['軟體', '網際網路', '資訊服務', '系統整合', '科技', 'saas', 'app']):
        return '資訊科技/軟體網路'
        
    return '其他工商服務/金融貿易'

def extract_tools(desc):
    tools = []
    tool_keywords = [
        'ChatGPT', 'Gemini', 'Claude', 'Midjourney', 'Copilot', 
        '生成式AI', 'AI工具', 'Prompt', 'Canva', 'Notion AI', 'Stable Diffusion', 'DALL-E'
    ]
    for t in tool_keywords:
        if re.search(r'\b' + re.escape(t) + r'\b', desc, re.I) or t in desc:
            tools.append(t)
    return list(set(tools))

def classify_requirement_type(desc):
    req_patterns = ['必備', '熟悉.*操作', '須具備.*能力', '條件.*要求', '要求.*使用', '會使用.*為佳', '需會']
    bonus_patterns = ['加分', '優先', '熟.*尤佳', '會.*更佳', '加值']
    
    is_req = any(re.search(p, desc) for p in req_patterns)
    is_bonus = any(re.search(p, desc) for p in bonus_patterns)
    
    if is_req and not is_bonus:
        return '必備條件'
    elif is_bonus:
        return '加分/優先'
    else:
        return '工作內容應用'

def crawl_taipei_jobs():
    collected = []
    seen_ids = set()
    output_path = '/Users/chenchunchih/Downloads/校務資料/104_taipei_ai_noncoding_jobs.csv'
    
    print(f"Starting crawl for Taipei & New Taipei non-coding AI jobs...")
    
    total_queries = len(AREAS) * len(CATEGORIES) * len(KEYWORDS)
    query_count = 0
    
    for area_code, area_name in AREAS.items():
        for cat_code, cat_name in CATEGORIES.items():
            for kw in KEYWORDS:
                query_count += 1
                # fetch top 3 pages for each combination
                for page in range(1, 4):
                    params = {
                        'keyword': kw,
                        'area': area_code,
                        'jobcat': cat_code,
                        'page': page,
                        'pagesize': 20,
                        'ro': 0,
                        'order': 15,
                        'asc': 0,
                        'mode': 's',
                        'jobsource': '2018indexpoc'
                    }
                    try:
                        r = requests.get(API_URL, params=params, headers=HEADERS, timeout=8)
                        if r.status_code != 200:
                            break
                        data = r.json()
                        jobs = data.get('data', [])
                        if not jobs:
                            break
                            
                        for j in jobs:
                            jid = str(j.get('jobNo', ''))
                            if jid in seen_ids:
                                continue
                                
                            title = j.get('jobName', '')
                            # Exclude purely technical / developer jobs
                            tech_filter = ['軟體工程師', 'programmer', '前端工程師', '後端工程師', 'firmware', '演算法工程師', '系統工程師', '架構師', 'devops']
                            if any(t in title.lower() for t in tech_filter):
                                continue
                                
                            seen_ids.add(jid)
                            
                            desc = j.get('description', '')
                            cust_name = j.get('custName', '')
                            co_ind = j.get('coIndustryDesc') or '未分類'
                            
                            # Salary extraction from 104 API fields
                            s_low = j.get('salaryLow', 0)
                            s_high = j.get('salaryHigh', 0)
                            period = j.get('period', 0)
                            
                            monthly_min = None
                            monthly_max = None
                            sal_type = '面議'
                            
                            if s_low and s_low > 10000 and s_low < 300000:
                                monthly_min = s_low
                                monthly_max = s_high if (s_high and s_high > 10000 and s_high < 500000) else s_low
                                sal_type = '月薪'
                            elif s_low and s_low > 100 and s_low < 2000:  # 時薪
                                monthly_min = s_low * 160
                                monthly_max = (s_high * 160) if (s_high and s_high < 2000) else monthly_min
                                sal_type = '時薪折算'
                            elif s_low and s_low >= 300000:  # 年薪
                                monthly_min = round(s_low / 13.5)
                                monthly_max = round(s_high / 13.5) if (s_high and s_high > s_low and s_high < 10000000) else monthly_min
                                sal_type = '年薪折算'
                            else:
                                sal_type = '面議'
                                
                            salary_raw = f"{s_low}~{s_high} (period={period})" if (s_low or s_high) else "面議"
                            
                            district = j.get('jobAddrNoDesc', '')
                            matched_tools = extract_tools(desc)
                            req_type = classify_requirement_type(desc)
                            ind_tag = classify_target_industry(co_ind, cust_name, title, desc)
                            
                            # Language flag
                            has_lang = any(w in desc.lower() for w in ['英文', '英語', 'toeic', '多益', '外語', '外銷', '日文', '日語'])
                            # International trade flag
                            has_trade = any(w in desc.lower() for w in ['國貿', '貿易', '海外業務', '跨境', '進出口', '報關', '船務', 'rfq', 'incoterms'])
                            # Automation flag
                            has_auto = any(w in desc.lower() for w in ['自動化', '流程優化', 'api', 'make', 'zapier', 'n8n', 'webhook', '串接'])
                            
                            collected.append({
                                'job_id': jid,
                                'job_name': title,
                                'company': cust_name,
                                'city': area_name,
                                'district': district,
                                'category': cat_name,
                                'industry_104': co_ind,
                                'target_industry': ind_tag,
                                'salary_raw': salary_raw,
                                'salary_type': sal_type,
                                'min_monthly_salary': monthly_min,
                                'max_monthly_salary': monthly_max,
                                'requirement_type': req_type,
                                'ai_tools': '; '.join(matched_tools),
                                'tool_count': len(matched_tools),
                                'has_foreign_language': 1 if has_lang else 0,
                                'has_international_trade': 1 if has_trade else 0,
                                'has_workflow_automation': 1 if has_auto else 0,
                                'description_snippet': desc[:300].replace('\n', ' ').replace('\r', ' ')
                            })
                            
                    except Exception as e:
                        print(f"Error on {area_name}-{cat_name}-{kw}-p{page}: {e}")
                        break
                        
                    time.sleep(0.15)
                
                if query_count % 15 == 0:
                    print(f"[{query_count}/{total_queries}] Collected {len(collected)} unique jobs in Taipei/New Taipei...")

    # Write to CSV
    if collected:
        keys = list(collected[0].keys())
        with open(output_path, 'w', encoding='utf-8-sig', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(collected)
        print(f"\nSUCCESS! Exported {len(collected)} unique Taipei/New Taipei non-coding AI jobs to {output_path}")
    else:
        print("No jobs collected.")

if __name__ == '__main__':
    crawl_taipei_jobs()
