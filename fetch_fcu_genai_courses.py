import subprocess
import json
import concurrent.futures
import pandas as pd
import time

SEMESTERS = [
    (113, 2, '113-2'),
    (113, 1, '113-1'),
    (112, 2, '112-2'),
    (112, 1, '112-1'),
]

# Task list
TASKS = []

# 1. GenAI direct keywords
GENAI_KEYWORDS = [
    '生成式',
    'ChatGPT',
    'LLM',
    '大型語言模型',
    '大語言模型',
    '語言模型',
    'AIGC',
    'AI Agent',
    '提示語',
    '提示詞',
    'Prompt',
    'Midjourney',
    'Stable Diffusion',
]

for y, s, label in SEMESTERS:
    for kw in GENAI_KEYWORDS:
        TASKS.append((y, s, label, kw, 'genai'))

# 2. Broad AI keywords for business and cross-disciplinary
for y, s, label in SEMESTERS:
    TASKS.append((y, s, label, '人工智慧', 'broad'))

def query_single(task):
    y, s, label, kw, mode = task
    payload = {
        'baseOptions': {'lang': 'cht', 'year': y, 'sms': s},
        'typeOptions': {
            'code': {'enabled': False, 'value': ''},
            'weekPeriod': {'enabled': False, 'week': '*', 'period': '*'},
            'course': {'enabled': True, 'value': kw},
            'teacher': {'enabled': False, 'value': ''},
            'useEnglish': {'enabled': False},
            'useLanguage': {'enabled': False, 'value': '01'},
            'specificSubject': {'enabled': False, 'value': '1'},
            'courseDescription': {'enabled': False, 'value': ''}
        }
    }
    cmd = [
        'curl', '-s', '-k', '-X', 'POST',
        'https://coursesearch04.fcu.edu.tw/Service/Search.asmx/GetType2Result',
        '-H', 'Content-Type: application/json; charset=utf-8',
        '--max-time', '8',
        '-d', json.dumps(payload)
    ]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        if res.returncode == 0 and res.stdout:
            data = json.loads(res.stdout)
            items = data.get('items', [])
            for it in items:
                it['query_year'] = y
                it['query_sms'] = s
                it['query_label'] = label
                it['query_kw'] = kw
                it['query_mode'] = mode
            return items
    except Exception as e:
        pass
    return []

def main():
    print(f"Starting search across {len(TASKS)} queries with 8 worker threads...")
    start_time = time.time()
    raw_results = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        futures = {executor.submit(query_single, t): t for t in TASKS}
        for future in concurrent.futures.as_completed(futures):
            res = future.result()
            if res:
                raw_results.extend(res)

    print(f"Fetch completed in {time.time() - start_time:.2f}s. Raw hits: {len(raw_results)}")

    # Deduplicate and categorize
    genai_dict = {}
    business_ai_dict = {}

    biz_humanities_depts = ['國貿', '商', '企管', '創能', '人社', '人文', '建築', '設計', '藝術', '金融', '行銷', '外文', '中文', '通識', '智慧城市', '倫理', '案例']

    for it in raw_results:
        y = it['query_year']
        s = it['query_sms']
        label = it['query_label']
        selcode = it.get('scr_selcode', '')
        cls_name = it.get('cls_name', '').strip()
        sub_name = it.get('sub_name', '').strip()
        key = f"{label}_{selcode}_{cls_name}"

        outline_url = f"https://coursesearch04.fcu.edu.tw/CourseOutline.aspx?lang=cht&courseid={y}{s}{selcode}"

        course_obj = {
            '學年期': label,
            '選課代號': selcode,
            '課程代碼': it.get('sub_id3', ''),
            '課程名稱': sub_name,
            '開課單位': cls_name,
            '授課教師': it.get('scr_teacher', '').strip(),
            '學分': it.get('scr_credit', 0),
            '修別': it.get('scj_scr_mso', '').strip(),
            '上課時間地點': it.get('scr_period', '').strip(),
            '全英語': it.get('scr_english', 'N'),
            '限修人數': it.get('scr_precnt', 0),
            '已選人數': it.get('scr_acptcnt', 0),
            '檢索關鍵字': it['query_kw'],
            '課程大綱連結': outline_url
        }

        # Check GenAI vs Broad
        is_genai = any(g in sub_name for g in ['生成式', 'ChatGPT', 'AI agent', 'AI Agent', '提示語', '提示詞', 'Prompt', 'LLM', '語言模型'])
        
        if is_genai:
            course_obj['分類'] = '生成式AI與提示語核心專門課程'
            if key not in genai_dict:
                genai_dict[key] = course_obj
        else:
            # Broad AI: check if in business, humanities, management, interdisciplinary
            if any(b in cls_name or b in sub_name for b in biz_humanities_depts):
                course_obj['分類'] = '商管/人文/跨領域AI實務應用課程'
                if key not in business_ai_dict and key not in genai_dict:
                    business_ai_dict[key] = course_obj

    final_courses = list(genai_dict.values()) + list(business_ai_dict.values())
    print(f"GenAI Core Courses: {len(genai_dict)}")
    print(f"Business/Humanities/Interdisciplinary AI Courses: {len(business_ai_dict)}")
    print(f"Total Unique Filtered Courses: {len(final_courses)}")

    # Sort
    df = pd.DataFrame(final_courses)
    df.sort_values(by=['分類', '學年期', '選課代號'], ascending=[True, False, True], inplace=True)

    df.to_csv('逢甲大學生成式AI與跨域課程清單.csv', index=False, encoding='utf-8-sig')
    with open('逢甲大學生成式AI與跨域課程清單.json', 'w', encoding='utf-8') as f:
        json.dump(final_courses, f, ensure_ascii=False, indent=2)

    print("\n=== 清單匯出成功！===")
    for c in sorted(final_courses, key=lambda x: (x['分類'], x['學年期'], x['選課代號']), reverse=True):
        print(f"[{c['分類']}] [{c['學年期']}] 代號:{c['選課代號']} | {c['課程名稱']} | {c['開課單位']} | 教師:{c['授課教師']} | {c['修別']} {c['學分']}學分 | {c['上課時間地點']}")

if __name__ == '__main__':
    main()
