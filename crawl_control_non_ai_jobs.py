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
    '6001008000': ('台中市', 8),    # ~8 pages per category -> ~960 jobs
    '6001001000': ('台北市', 10),   # ~10 pages per category -> ~1200 jobs
    '6001002000': ('新北市', 7)     # ~7 pages per category -> ~840 jobs
}

CATEGORIES = {
    '2004000000': '行銷/企劃/專案管理',
    '2005000000': '客服/業務/電商/貿易',
    '2002000000': '行政/總務/法務',
    '2013000000': '傳播藝術/設計',
    '2014000000': '文字/傳媒工作',
    '2001000000': '經營/人資'
}

# Strict AI regex to filter out ANY job that touches AI
AI_REGEX = re.compile(
    r'(chatgpt|gemini|claude|copilot|midjourney|prompt|生成式ai|生成式人工智慧|ai工具|ai應用|人工智慧|'
    r'stable diffusion|canva ai|dall-e|suno|runway|comfyui|gpt-4|llm|自然語言|機器學習|deep learning)',
    re.IGNORECASE
)

# Tech filter to exclude pure software engineers
TECH_FILTER = ['軟體工程師', 'programmer', '前端工程師', '後端工程師', 'firmware', '演算法工程師', '系統工程師', '架構師', 'devops']

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
    return '其他服務/工商貿易'

def crawl_control_jobs():
    collected = []
    seen_ids = set()
    output_path = '/Users/chenchunchih/Downloads/校務資料/104_control_non_ai_jobs.csv'
    
    print("Starting Control Group (Pure Traditional Non-AI) jobs crawling...")
    
    for area_code, (area_name, max_pages) in AREAS.items():
        region_label = '台中' if area_name == '台中市' else '雙北'
        is_tp = 0 if area_name == '台中市' else 1
        
        for cat_code, cat_name in CATEGORIES.items():
            for page in range(1, max_pages + 1):
                params = {
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
                        if any(t in title.lower() for t in TECH_FILTER):
                            continue
                            
                        desc = j.get('description', '')
                        
                        # CRUCIAL FILTER: Exclude any job that mentions AI
                        if AI_REGEX.search(title) or AI_REGEX.search(desc):
                            continue
                            
                        seen_ids.add(jid)
                        
                        cust_name = j.get('custName', '')
                        co_ind = j.get('coIndustryDesc') or '未分類'
                        
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
                        ind_tag = classify_target_industry(co_ind, cust_name, title, desc)
                        
                        has_lang = 1 if any(w in (title + ' ' + desc).lower() for w in ['英文', '英語', 'toeic', '多益', '外語', '外銷', '日文', '日語']) else 0
                        has_trade = 1 if any(w in (title + ' ' + desc).lower() for w in ['國貿', '貿易', '海外業務', '跨境', '進出口', '報關', '船務', 'rfq', 'incoterms']) else 0
                        has_auto = 1 if any(w in (title + ' ' + desc).lower() for w in ['自動化', '流程優化', 'api', 'make', 'zapier', 'n8n', 'webhook', '串接']) else 0
                        
                        collected.append({
                            'job_id': jid,
                            'job_name': title,
                            'company': cust_name,
                            'region': region_label,
                            'city': area_name,
                            'district': district,
                            'category': cat_name,
                            'target_industry': ind_tag,
                            'salary_raw': salary_raw,
                            'salary_type': sal_type,
                            'min_monthly_salary': monthly_min,
                            'max_monthly_salary': monthly_max,
                            'is_negotiable': 1 if (monthly_min is None or monthly_min <= 0) else 0,
                            'is_ai_job': 0,
                            'requirement_type': '傳統無AI',
                            'ai_tools': '無',
                            'tool_count': 0,
                            'has_foreign_language': has_lang,
                            'has_international_trade': has_trade,
                            'has_workflow_automation': has_auto,
                            'description_snippet': desc[:300].replace('\n', ' ').replace('\r', ' ')
                        })
                except Exception as e:
                    print(f"Error on {area_name}-{cat_name}-p{page}: {e}")
                    break
                time.sleep(0.12)
            
            print(f"[{area_name} - {cat_name}] Collected {len(collected)} clean non-AI jobs...")

    # Write to CSV
    if collected:
        keys = list(collected[0].keys())
        with open(output_path, 'w', encoding='utf-8-sig', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(collected)
        print(f"\nSUCCESS! Exported {len(collected)} clean Control Group jobs to {output_path}")
        return len(collected)
    return 0

if __name__ == '__main__':
    crawl_control_jobs()
