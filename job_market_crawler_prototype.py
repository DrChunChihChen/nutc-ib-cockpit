#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
就業市場即時爬蟲與國貿系職能需求分析原型 (Job Market Radar Prototype)
資料來源：yes123 求職網 & 勞動部台灣就業通 (TaiwanJobs Open API)
用途：為中科國貿 (NUTC IB) 師生分析即時外銷貿易與商務職缺之技能、薪資、學歷門檻與大台中在地需求。
"""

import urllib.request
import urllib.parse
import re
import json
import time
import os
from collections import Counter
from bs4 import BeautifulSoup

def clean_text(text):
    if not text:
        return ""
    return re.sub(r'\s+', ' ', text).strip()

def parse_salary(sal_str):
    """解析薪資字串，回傳 (min_sal, max_sal, sal_type)"""
    if not sal_str:
        return None, None, "未揭示"
    
    # 面議(經常性薪資達4萬元含以上)
    if "4萬" in sal_str or "40,000" in sal_str:
        return 40000, 60000, "面議(4萬以上)"
    if "面議" in sal_str:
        return 30000, 40000, "面議"
    
    # 月薪 35,000 至 45,000元
    nums = [int(n.replace(',', '')) for n in re.findall(r'\d{1,3}(?:,\d{3})+|\d{4,6}', sal_str)]
    if len(nums) >= 2:
        return nums[0], nums[1], "區間月薪"
    elif len(nums) == 1:
        if "以上" in sal_str:
            return nums[0], nums[0] * 1.3, "起薪以上"
        return nums[0], nums[0], "固定月薪"
    return None, None, "其他"

def crawl_jobs(keyword="國外業務", area="04", max_jobs=60):
    """
    抓取指定關鍵字之職缺列表與詳細規格
    area="04" 代表中部地區（包含台中市、彰化縣、南投縣）
    """
    print(f"\n🚀 [開始抓取] 關鍵字: 「{keyword}」 | 地區代碼: {area} (中部) | 目標筆數: {max_jobs} 筆...")
    
    jobs = []
    strrec = 0
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    }

    while len(jobs) < max_jobs and strrec < 150:
        search_url = f"https://www.yes123.com.tw/admin/job_refer_list.asp?find_key1={urllib.parse.quote(keyword)}&str_work_area={area}&strrec={strrec}"
        try:
            req = urllib.request.Request(search_url, headers=headers)
            with urllib.request.urlopen(req, timeout=8) as resp:
                html = resp.read().decode('utf-8', errors='ignore')
                soup = BeautifulSoup(html, 'html.parser')
                items = soup.find_all('div', class_='Job_opening_item')
                if not items:
                    print(f"  * 第 {strrec//30 + 1} 頁無更多職缺，提前結束列表抓取。")
                    break

                for it in items:
                    title_elem = it.find('h5')
                    comp_elem = it.find('h6')
                    pay_elem = it.find('div', class_='Job_opening_item_title_payment')
                    
                    if not title_elem:
                        continue
                    
                    title = clean_text(title_elem.text)
                    comp = clean_text(comp_elem.text) if comp_elem else "未揭露公司"
                    pay_text = clean_text(pay_elem.text) if pay_elem else "待遇面議"
                    
                    # 取得職缺詳細頁連結
                    link = title_elem.find('a')
                    href = link.get('href') if link else ""
                    # 提取 p_id 與 job_id
                    p_id_match = re.search(r'p_id=([0-9_a-zA-Z]+)', href)
                    job_id_match = re.search(r'job_id=([0-9_a-zA-Z]+)', href)
                    
                    p_id = p_id_match.group(1) if p_id_match else ""
                    job_id = job_id_match.group(1) if job_id_match else ""
                    
                    # 抓取地區
                    info_div = it.find('div', class_='Job_opening_item_info')
                    loc_text = "中部地區"
                    if info_div:
                        spans = info_div.find_all('span')
                        for sp in spans:
                            txt = sp.text.strip()
                            if "市" in txt or "縣" in txt or "區" in txt:
                                loc_text = txt
                                break

                    job_entry = {
                        "title": title,
                        "company": comp,
                        "pay_raw": pay_text,
                        "location": loc_text,
                        "p_id": p_id,
                        "job_id": job_id,
                        "keyword": keyword,
                        "detail": {}
                    }
                    jobs.append(job_entry)
                    if len(jobs) >= max_jobs:
                        break
                        
            print(f"  ✓ 取得第 {strrec//30 + 1} 頁清單，目前累積 {len(jobs)} 筆職缺")
            strrec += 30
            time.sleep(0.5) # 友善延遲
        except Exception as e:
            print(f"  ! 抓取列表發生錯誤: {e}")
            break

    # 深度抓取前 35 筆職缺的詳細要求（語文、技能、工具、經歷）
    print(f"\n🔍 [深度解析] 正在抓取前 {min(len(jobs), 35)} 筆職缺的工作內容與技能條件...")
    for idx, job in enumerate(jobs[:35]):
        if not job["p_id"] or not job["job_id"]:
            continue
        detail_url = f"https://www.yes123.com.tw/wk_index/job.asp?p_id={job['p_id']}&job_id={job['job_id']}"
        try:
            req = urllib.request.Request(detail_url, headers=headers)
            with urllib.request.urlopen(req, timeout=6) as resp:
                d_html = resp.read().decode('utf-8', errors='ignore')
                d_soup = BeautifulSoup(d_html, 'html.parser')
                
                # 萃取細部欄位
                job_desc = ""
                skills = []
                tools = []
                edu = "大學以上"
                exp = "不拘"
                
                for tag in d_soup.find_all(['li', 'div', 'p']):
                    t = clean_text(tag.text)
                    if "工作內容：" in t and not job_desc:
                        job_desc = t.replace("工作內容：", "").strip()
                    elif "工作技能：" in t:
                        skills.append(t.replace("工作技能：", "").strip())
                    elif "電腦技能：" in t or "擅長工具：" in t:
                        tools.append(t.replace("電腦技能：", "").replace("擅長工具：", "").strip())
                    elif "學歷要求：" in t:
                        edu = t.replace("學歷要求：", "").strip()
                    elif "工作經驗：" in t:
                        exp = t.replace("工作經驗：", "").strip()
                
                job["detail"] = {
                    "description": job_desc[:250],
                    "skills": " ".join(skills),
                    "tools": " ".join(tools),
                    "education": edu,
                    "experience": exp,
                    "full_text": d_soup.text
                }
            time.sleep(0.3)
        except Exception as e:
            job["detail"] = {"error": str(e)}

    return jobs

def analyze_job_data(jobs):
    """統計分析薪資、技能、學歷、工具分佈"""
    total = len(jobs)
    if total == 0:
        return None

    # 1. 薪資分析
    sal_ranges = {
        "30K~35K": 0,
        "35K~40K": 0,
        "40K~50K": 0,
        "50K以上(高薪)": 0,
        "面議(經常性達4萬以上)": 0,
        "其他/面議": 0
    }
    valid_mins = []
    
    for j in jobs:
        p_min, p_max, p_type = parse_salary(j["pay_raw"])
        if p_min:
            valid_mins.append(p_min)
            if p_type == "面議(4萬以上)":
                sal_ranges["面議(經常性達4萬以上)"] += 1
            elif p_min < 35000:
                sal_ranges["30K~35K"] += 1
            elif 35000 <= p_min < 40000:
                sal_ranges["35K~40K"] += 1
            elif 40000 <= p_min < 50000:
                sal_ranges["40K~50K"] += 1
            else:
                sal_ranges["50K以上(高薪)"] += 1
        else:
            sal_ranges["其他/面議"] += 1

    avg_min_sal = sum(valid_mins) / len(valid_mins) if valid_mins else 0
    median_min_sal = sorted(valid_mins)[len(valid_mins)//2] if valid_mins else 0

    # 2. 地區分佈
    locations = Counter([j["location"] for j in jobs])

    # 3. 技能與關鍵字分析 (從標題、內容、工具、技能中掃描)
    skill_keywords = {
        "英語流利/精通": [r"英[語文]", r"english", r"toeic", r"多益", r"外語"],
        "多益 TOEIC (明確提及)": [r"toeic", r"多益"],
        "第二外語 (日文/越語/西語)": [r"日[語文]", r"japanese", r"越南", r"西班牙", r"德語"],
        "進出口實務 / 報關船務": [r"進出口", r"報關", r"船務", r"貿易實務", r"信用狀", r"l/?c", r"貿易流程"],
        "國外客戶開發 / 參展出差": [r"客戶開發", r"參展", r"海外參展", r"海外出差", r"國外業務開發", r"開發新客戶"],
        "ERP / SAP 企業資源系統": [r"erp", r"sap", r"鼎新", r"oracle", r"進銷存"],
        "辦公室軟體 (Excel/Word/PPT)": [r"excel", r"word", r"powerpoint", r"office"],
        "數據分析 / 商業智慧 (Python/BI)": [r"python", r"bi", r"數據分析", r"商業分析", r"ga4", r"sql"],
        "跨境電商 (Amazon/Alibaba)": [r"電商", r"跨境", r"alibaba", r"amazon", r"蝦皮", r"網路行銷", r"數位行銷"],
        "談判與商務溝通": [r"談判", r"溝通", r"協商", r"議價", r"顧客關係", r"crm"]
    }

    skill_counts = {k: 0 for k in skill_keywords}
    
    # 4. 學歷要求
    edu_counts = Counter()
    # 5. 經歷要求
    exp_counts = Counter()

    for j in jobs:
        detail = j.get("detail", {})
        combined_text = f"{j['title']} {j['company']} {detail.get('description', '')} {detail.get('skills', '')} {detail.get('tools', '')} {detail.get('full_text', '')}".lower()
        
        for skill_name, patterns in skill_keywords.items():
            if any(re.search(pat, combined_text) for pat in patterns):
                skill_counts[skill_name] += 1
                
        edu = detail.get("education", "")
        if "專科" in edu:
            edu_counts["專科以上 (含五專/二專)"] += 1
        elif "大學" in edu:
            edu_counts["大學以上"] += 1
        elif "碩士" in edu:
            edu_counts["碩士以上"] += 1
        elif "高中" in edu or "高職" in edu:
            edu_counts["高中職以上"] += 1
        else:
            edu_counts["不拘/未註明"] += 1

        exp = detail.get("experience", "")
        if "不拘" in exp or "無" in exp:
            exp_counts["無經驗可 / 應屆畢業生友善"] += 1
        elif "1年" in exp:
            exp_counts["1~2 年經驗"] += 1
        elif "2年" in exp or "3年" in exp:
            exp_counts["2~3 年經驗"] += 1
        elif "5年" in exp:
            exp_counts["5 年以上資深主管"] += 1
        else:
            exp_counts["不拘 / 歡迎新鮮人"] += 1

    return {
        "total_jobs": total,
        "avg_min_sal": round(avg_min_sal),
        "median_min_sal": round(median_min_sal),
        "sal_ranges": sal_ranges,
        "locations": dict(locations.most_common(8)),
        "skill_counts": skill_counts,
        "edu_counts": dict(edu_counts),
        "exp_counts": dict(exp_counts),
        "sample_jobs": jobs[:15]
    }

def print_executive_report(result):
    """印出符合學術與系務會議規格的客觀分析摘要"""
    total = result["total_jobs"]
    print("\n" + "="*78)
    print(" 國立臺中科技大學 國際貿易與經營系 (NUTC IB) 就業市場實證雷達")
    print(f" 樣本規模：{total} 筆最新中部/全台外銷經貿職缺 | 分析時間：{time.strftime('%Y-%m-%d %H:%M')}")
    print("="*78)

    print("\n【一、 薪資行情與起薪級距分佈】")
    print(f" • 樣本平均月薪起薪：NT$ {result['avg_min_sal']:,} 元")
    print(f" • 樣本起薪中位數：  NT$ {result['median_min_sal']:,} 元")
    print(" • 薪資結構分佈：")
    for r_name, count in result["sal_ranges"].items():
        pct = (count / total) * 100
        bar = "█" * int(pct / 3)
        print(f"   - {r_name:<20}: {count:>2} 筆 ({pct:>5.1f}%) | {bar}")

    print("\n【二、 企業最渴望的 10 大核心能力與技能排行 (課綱規劃參考)】")
    sorted_skills = sorted(result["skill_counts"].items(), key=lambda x: x[1], reverse=True)
    for rank, (skill, count) in enumerate(sorted_skills, 1):
        pct = (count / total) * 100
        bar = "▓" * int(pct / 4)
        print(f"   {rank:>2}. {skill:<26}: {count:>2} 家企業提及 ({pct:>5.1f}%) | {bar}")

    print("\n【三、 學歷與經歷門檻 (應屆畢業生就業機會)】")
    print(" • 學歷要求：")
    for edu, count in result["edu_counts"].items():
        pct = (count / total) * 100
        print(f"   - {edu:<22}: {count:>2} 筆 ({pct:>5.1f}%)")
    print(" • 經歷要求：")
    for exp, count in result["exp_counts"].items():
        pct = (count / total) * 100
        print(f"   - {exp:<22}: {count:>2} 筆 ({pct:>5.1f}%)")

    print("\n【四、 中部在地外銷熱區分佈】")
    for loc, count in list(result["locations"].items())[:6]:
        pct = (count / total) * 100
        print(f"   - {loc:<16}: {count:>2} 筆 ({pct:>5.1f}%)")

    print("\n【五、 代表性徵才職缺抽樣】")
    for i, j in enumerate(result["sample_jobs"][:5], 1):
        print(f"   {i}. [{j['location']}] {j['company']} - {j['title']} ({j['pay_raw']})")

    print("="*78 + "\n")

if __name__ == "__main__":
    # 爬取國外業務與國貿職缺
    jobs = crawl_jobs(keyword="國外業務", area="04", max_jobs=50)
    
    # 若數量不足可擴充關鍵字
    if len(jobs) < 30:
        more_jobs = crawl_jobs(keyword="國貿業務", area="04", max_jobs=30)
        jobs.extend(more_jobs)

    analysis = analyze_job_data(jobs)
    if analysis:
        print_executive_report(analysis)
        
        # 存檔為 JSON 供後續整合至戰情室
        output_path = "/Users/chenchunchih/Downloads/校務資料/job_market_insights.json"
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(analysis, f, ensure_ascii=False, indent=2)
        print(f"💾 分析結果已結構化儲存至：{output_path}")
