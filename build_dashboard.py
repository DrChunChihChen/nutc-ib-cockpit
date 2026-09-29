# -*- coding: utf-8 -*-
"""
build_dashboard.py
國立臺中科技大學 國際貿易與經營系 (NUTC ITM)
系務策略發展與生源海嘯動態決策戰情室 (Executive Strategic Intelligence Cockpit)
編譯器與資料自動整合建置腳本 (升級強化版)
主持人：陳俊智 副教授 (Dr. Elvis Chen)
"""

import os
import json

def generate_dashboard():
    # 1. 完整資料庫結構 (整合四支實證腳本與教育部、技專招聯會官方實證硬數據)
    raw_data = {
        "metadata": {
            "title": "國立臺中科技大學 國際貿易與經營系",
            "subtitle": "系務策略發展與生源海嘯動態決策戰情室",
            "english_title": "NUTC ITM Executive Strategic Intelligence Cockpit",
            "principal_investigator": "陳俊智 副教授 (Dr. Elvis Chen)",
            "academic_year": "114學年度 (2025/2026 最新官方資料庫)",
            "data_sources": [
                "教育部大專校院校務資訊公開平台 (UDB)",
                "技專校院招生委員會聯合會 (JCTV)",
                "教育部統計處《113至128學年度各教育階段學生數預測報告》",
                "內政部戶政司歷年出生人口統計"
            ]
        },
        # 六強國立科大比較
        "regional_six": [
            {
                "code": "北商-國商",
                "school": "臺北商業大學",
                "dept": "國際商務系/科",
                "region": "北部",
                "total_stu": 919,
                "five_year": 266,
                "undergrad_day": 439,
                "undergrad_eve": 160,
                "grad": 54,
                "faculty_total": 21,
                "faculty_prof": 6,
                "faculty_assoc": 11,
                "faculty_asst": 2,
                "oversea_stu": 68,
                "oversea_pct": 7.4,
                "reg_114_rate": 100.0,
                "reg_114_quota": 58,
                "reg_114_act": 58,
                "score_113": 80.93,
                "score_114": 79.86,
                "score_delta": -1.07,
                "drop_cnt_113": 49,
                "drop_rate_113": 2.71,
                "type": "都會菁英旗艦",
                "radar": [88, 75, 68, 100, 73]
            },
            {
                "code": "中科-國貿",
                "school": "臺中科技大學",
                "dept": "國際貿易與經營系/科",
                "region": "中部",
                "total_stu": 1044,
                "five_year": 248,
                "undergrad_day": 482,
                "undergrad_eve": 314,
                "grad": 0,
                "faculty_total": 21,
                "faculty_prof": 4,
                "faculty_assoc": 14,
                "faculty_asst": 3,
                "oversea_stu": 58,
                "oversea_pct": 5.6,
                "reg_114_rate": 99.06,
                "reg_114_quota": 80,
                "reg_114_act": 79,
                "score_113": 75.56,
                "score_114": 71.78,
                "score_delta": -3.78,
                "drop_cnt_113": 80,
                "drop_rate_113": 3.73,
                "type": "中部旗艦大系",
                "radar": [78, 95, 56, 99, 63]
            },
            {
                "code": "雲科-國管",
                "school": "雲林科技大學",
                "dept": "國際管理學士學位學程",
                "region": "中部",
                "total_stu": 104,
                "five_year": 0,
                "undergrad_day": 104,
                "undergrad_eve": 0,
                "grad": 0,
                "faculty_total": 3,
                "faculty_prof": 1,
                "faculty_assoc": 1,
                "faculty_asst": 1,
                "oversea_stu": 20,
                "oversea_pct": 19.2,
                "reg_114_rate": 100.0,
                "reg_114_quota": 17,
                "reg_114_act": 17,
                "score_113": 81.33,
                "score_114": 79.78,
                "score_delta": -1.55,
                "drop_cnt_113": 4,
                "drop_rate_113": 2.20,
                "type": "精緻國際小學程",
                "radar": [87, 20, 95, 100, 78]
            },
            {
                "code": "高科-航管",
                "school": "高雄科技大學",
                "dept": "航運管理系",
                "region": "南部",
                "total_stu": 595,
                "five_year": 0,
                "undergrad_day": 415,
                "undergrad_eve": 101,
                "grad": 79,
                "faculty_total": 14,
                "faculty_prof": 8,
                "faculty_assoc": 4,
                "faculty_asst": 2,
                "oversea_stu": 13,
                "oversea_pct": 2.2,
                "reg_114_rate": 98.86,
                "reg_114_quota": 86,
                "reg_114_act": 85,
                "score_113": 73.56,
                "score_114": 73.89,
                "score_delta": 0.33,
                "drop_cnt_113": 30,
                "drop_rate_113": 2.52,
                "type": "海運物流利基型",
                "radar": [80, 60, 25, 99, 75]
            },
            {
                "code": "高科-國企",
                "school": "高雄科技大學",
                "dept": "國際企業系",
                "region": "南部",
                "total_stu": 554,
                "five_year": 0,
                "undergrad_day": 251,
                "undergrad_eve": 190,
                "grad": 113,
                "faculty_total": 13,
                "faculty_prof": 8,
                "faculty_assoc": 2,
                "faculty_asst": 3,
                "oversea_stu": 40,
                "oversea_pct": 7.2,
                "reg_114_rate": 100.0,
                "reg_114_quota": 45,
                "reg_114_act": 45,
                "score_113": 76.44,
                "score_114": 67.50,
                "score_delta": -8.94,
                "drop_cnt_113": 36,
                "drop_rate_113": 3.21,
                "type": "南部綜合型研發",
                "radar": [70, 58, 65, 100, 68]
            },
            {
                "code": "高科-供應鏈",
                "school": "高雄科技大學",
                "dept": "供應鏈管理系",
                "region": "南部",
                "total_stu": 306,
                "five_year": 0,
                "undergrad_day": 240,
                "undergrad_eve": 40,
                "grad": 26,
                "faculty_total": 9,
                "faculty_prof": 2,
                "faculty_assoc": 6,
                "faculty_asst": 1,
                "oversea_stu": 4,
                "oversea_pct": 1.3,
                "reg_114_rate": 96.15,
                "reg_114_quota": 52,
                "reg_114_act": 50,
                "score_113": 71.85,
                "score_114": 65.70,
                "score_delta": -6.15,
                "drop_cnt_113": 20,
                "drop_rate_113": 3.07,
                "type": "專精新興領域型",
                "radar": [68, 35, 15, 96, 69]
            }
        ],

        # 中部商管競爭陣列 (Module 2)
        "central_competitors": [
            {
                "school": "中科大國貿",
                "type": "國立科大龍頭",
                "quota_status": "四技核定 80 (維持)",
                "reg_114_day": 99.06,
                "reg_114_eve": 50.91,
                "score_cutoff": 71.78,
                "students_total": 1044,
                "drop_rate": 3.73,
                "cash_reserve": "國立公庫 (極高安全)",
                "tuition_per_sem": "約 2.7 萬 (公立優勢)",
                "source_mix": "統測技職 85% / 繁星技優 15%",
                "strategy_label": "規模旗艦・但進修部與退學面臨逆風",
                "threat_level": "基準主戰系",
                "features": "一中商圈核心、五專+四技+二技完整縱深、免學費優勢大，但缺碩士班、進修部招生急墜"
            },
            {
                "school": "逢甲國貿",
                "type": "私立頂尖普大",
                "quota_status": "年招約 200 (3班日間155+全英38)",
                "reg_114_day": 97.50,
                "reg_114_eve": 78.20,
                "score_cutoff": 74.50,
                "students_total": 1180,
                "drop_rate": 2.45,
                "cash_reserve": "約 45.8 億 (私校財務頂尖)",
                "tuition_per_sem": "約 5.5 萬 (私立標準)",
                "source_mix": "普通高中學測 90% / 技職 10%",
                "strategy_label": "普高生源虹吸・全英與商圈強勢",
                "threat_level": "極高 (學測生源主戰場)",
                "features": "逢甲西屯商圈品牌、全英語學程吸引台商子弟、商學院 AACSB 認證、產學資源龐大"
            },
            {
                "school": "東海國貿",
                "type": "老牌私立普大",
                "quota_status": "斷腕減招 30% (150人砍至106人)",
                "reg_114_day": 96.80,
                "reg_114_eve": 0.0,
                "score_cutoff": 69.20,
                "students_total": 520,
                "drop_rate": 3.10,
                "cash_reserve": "約 28.5 億 (財務穩健)",
                "tuition_per_sem": "約 5.6 萬",
                "source_mix": "普通高中學測 92% / 分科分發 8%",
                "strategy_label": "戰略減招保率・博雅與跨國雙聯",
                "threat_level": "中高 (品牌生源爭奪)",
                "features": "大砍三成名額使註冊率一舉重回 96.8%、美國天普雙聯 2+2、博雅書院品牌"
            },
            {
                "school": "朝陽科大商管",
                "type": "私立技職龍頭",
                "quota_status": "商管核定維持規模",
                "reg_114_day": 89.20,
                "reg_114_eve": 65.40,
                "score_cutoff": 63.40,
                "students_total": 2100,
                "drop_rate": 4.15,
                "cash_reserve": "25.5 億 (私校第二高)",
                "tuition_per_sem": "約 5.3 萬",
                "source_mix": "統測高職 75% / 境外生 25%",
                "strategy_label": "高額現金堡壘・航空院帶動與南向招募",
                "threat_level": "中等 (技職生源防禦)",
                "features": "25.5億現金安全線、航空學院吸睛效應、深耕東南亞國際外加專班填補生源缺口"
            },
            {
                "school": "嶺東國企",
                "type": "私立科大",
                "quota_status": "核定名額微幅縮減",
                "reg_114_day": 51.40,
                "reg_114_eve": 38.60,
                "score_cutoff": 52.10,
                "students_total": 410,
                "drop_rate": 7.22,
                "cash_reserve": "31.2 億 (全台私校第三高)",
                "tuition_per_sem": "約 5.2 萬",
                "source_mix": "統測高職 90% / 其他 10%",
                "strategy_label": "超高資金存量・但生源面臨斷崖雪崩",
                "threat_level": "警訊警示案例",
                "features": "31.2億現金充裕保證不倒，但日間註冊暴跌至51.4%、退學率7.22%極度危險"
            },
            {
                "school": "虎科財金",
                "type": "國立科大",
                "quota_status": "小系編制 (436人, 10師)",
                "reg_114_day": 98.00,
                "reg_114_eve": 39.29,
                "score_cutoff": 65.64,
                "students_total": 436,
                "drop_rate": 2.80,
                "cash_reserve": "國立公庫",
                "tuition_per_sem": "約 2.6 萬",
                "source_mix": "統測商管群 85% / 技優 15%",
                "strategy_label": "公立日間滿招・但進修部與分數失守",
                "threat_level": "警訊借鏡對象",
                "features": "日間維持98%，但錄取分暴跌至65.64分（被中科遠拋），二技進修部重挫至39.29%"
            }
        ],

        # 6年統測商管最低錄取折合單科均分走勢 (Module 3)
        "score_trends": {
            "years": ["109", "110", "111", "112", "113", "114"],
            "departments": {
                "中科大國貿": [75.44, 76.89, 68.33, 68.44, 75.56, 71.78],
                "中科大企管": [76.71, 77.86, 70.00, 68.77, 75.95, 71.73],
                "雲科大企管": [83.11, 83.44, 78.44, 73.44, 81.56, 78.56],
                "北商大國商": [84.71, 84.07, 80.14, 74.43, 80.93, 79.86],
                "北商大企管": [83.71, 83.86, 79.00, 74.18, 82.06, 79.58],
                "勤益企管":   [70.79, 73.18, 61.86, 61.36, 68.14, 63.78],
                "虎科財金":   [72.50, 74.10, 65.80, 64.20, 71.30, 65.64]
            }
        },

        # 中科國貿 vs 企管深度體質 (Module 3)
        "itm_vs_ba_deep": {
            "faculty": {
                "itm": {"total": 21, "male": 10, "female": 11, "prof": 4, "assoc": 14, "asst": 3, "lect": 0},
                "ba": {"total": 24, "male": 13, "female": 11, "prof": 5, "assoc": 12, "asst": 7, "lect": 0}
            },
            "students": {
                "itm": {"total": 1044, "five_year": 248, "day_ug": 482, "star": 0, "eve_ug": 314, "day_ma": 0, "emba": 0, "ssr": 49.7},
                "ba": {"total": 1165, "five_year": 438, "day_ug": 295, "star": 103, "eve_ug": 227, "day_ma": 35, "emba": 67, "ssr": 48.5}
            },
            "registration_matrix": [
                {"prog": "日間學士班(含四技)", "itm_113": "100.00% (80/80)", "itm_114": "99.06% (79/80, 境+26)", "ba_113": "100.00% (40/40)", "ba_114": "100.00% (40/40, 境+14)", "diff": "國貿核定為企管2倍"},
                {"prog": "日間二年制(二技)", "itm_113": "97.37% (37/38)", "itm_114": "100.00% (38/38, 境+1)", "ba_113": "100.00% (38/38)", "ba_114": "100.00% (38/38)", "diff": "兩系日間二技均滿額"},
                {"prog": "進修學士班(含四技)", "itm_113": "53.75% (43/80)", "itm_114": "50.91% (28/55)", "ba_113": "85.00% (34/40)", "ba_114": "70.00% (28/40)", "diff": "國貿減招25名仍跌至50.91% (警戒)"},
                {"prog": "進修二年制(二技)", "itm_113": "62.67% (47/75)", "itm_114": "89.09% (49/55)", "ba_113": "97.14% (34/35)", "ba_114": "100.00% (35/35)", "diff": "國貿二技進修減招20名強彈+26.4%"},
                {"prog": "日間五專", "itm_113": "100.00% (50/50)", "itm_114": "100.00% (50/50)", "ba_113": "100.00% (90/90)", "ba_114": "98.89% (89/90)", "diff": "國貿1班 (50人) vs 企管2班 (90人)"},
                {"prog": "碩士在職專班 (EMBA)", "itm_113": "無此學制 (0人)", "itm_114": "無此學制 (0人)", "ba_113": "100.00% (33/33)", "ba_114": "100.00% (33/33)", "diff": "企管高額產官學收入護城河"},
                {"prog": "日間碩士班", "itm_113": "無此學制 (0人)", "itm_114": "無此學制 (0人)", "ba_113": "100.00% (16/16)", "ba_114": "100.00% (16/16, 境+2)", "diff": "企管具備學術研究傳承梯隊"}
            ],
            "attrition": {
                "base_students": {"itm": 2142, "ba": 2440},
                "drop_total": {"itm": 80, "ba": 72},
                "drop_rate": {"itm": 3.73, "ba": 2.95},
                "self_drop": {"itm": 33, "ba": 25},
                "mismatch_drop": {"itm": 24, "ba": 20},
                "work_drop": {"itm": 8, "ba": 3},
                "forced_drop": {"itm": 47, "ba": 47},
                "sus_students": {"itm": 1071, "ba": 1220},
                "sus_count": {"itm": 73, "ba": 73},
                "sus_rate": {"itm": 6.82, "ba": 5.98}
            }
        },

        # 少子化預測基礎數據 (Module 4)
        "fertility_timeline": [
            {"yr": 113, "fresh": 18.8, "tcte": 7.52, "biz": 1.43, "pool": 3146, "day_score": 72.04, "eve_rate": 52.9, "five_def": "極穩 (98~100%)"},
            {"yr": 114, "fresh": 18.4, "tcte": 7.36, "biz": 1.40, "pool": 3080, "day_score": 71.78, "eve_rate": 50.9, "five_def": "極穩 (98~100%)"},
            {"yr": 115, "fresh": 17.9, "tcte": 7.16, "biz": 1.36, "pool": 2992, "day_score": 71.44, "eve_rate": 48.3, "five_def": "極穩 (98~100%)"},
            {"yr": 116, "fresh": 16.8, "tcte": 6.72, "biz": 1.28, "pool": 2816, "day_score": 70.75, "eve_rate": 43.3, "five_def": "良好 (92~95%)"},
            {"yr": 117, "fresh": 15.6, "tcte": 6.24, "biz": 1.19, "pool": 2618, "day_score": 69.98, "eve_rate": 38.0, "five_def": "良好 (92~95%) [虎年海嘯谷底]"},
            {"yr": 118, "fresh": 16.1, "tcte": 6.44, "biz": 1.22, "pool": 2684, "day_score": 70.24, "eve_rate": 39.7, "five_def": "極穩 (98~100%)"},
            {"yr": 119, "fresh": 16.5, "tcte": 6.60, "biz": 1.25, "pool": 2750, "day_score": 70.49, "eve_rate": 41.5, "five_def": "極穩 (98~100%)"},
            {"yr": 120, "fresh": 16.4, "tcte": 6.56, "biz": 1.25, "pool": 2750, "day_score": 70.49, "eve_rate": 41.5, "five_def": "極穩 (98~100%)"},
            {"yr": 121, "fresh": 16.0, "tcte": 6.40, "biz": 1.22, "pool": 2684, "day_score": 70.24, "eve_rate": 39.7, "five_def": "極穩 (98~100%)"},
            {"yr": 122, "fresh": 15.6, "tcte": 6.24, "biz": 1.19, "pool": 2618, "day_score": 69.98, "eve_rate": 38.0, "five_def": "良好 (92~95%) [進修部瀕臨停招]"},
            {"yr": 123, "fresh": 15.3, "tcte": 6.12, "biz": 1.16, "pool": 2552, "day_score": 69.72, "eve_rate": 36.3, "five_def": "極穩 (98~100%)"},
            {"yr": 124, "fresh": 15.1, "tcte": 6.04, "biz": 1.15, "pool": 2530, "day_score": 69.64, "eve_rate": 35.7, "five_def": "極穩 (98~100%)"},
            {"yr": 125, "fresh": 14.9, "tcte": 5.96, "biz": 1.13, "pool": 2485, "day_score": 69.46, "eve_rate": 34.6, "five_def": "極穩 (98~100%)"},
            {"yr": 126, "fresh": 14.8, "tcte": 5.92, "biz": 1.12, "pool": 2464, "day_score": 69.38, "eve_rate": 34.1, "five_def": "極穩 (98~100%)"},
            {"yr": 127, "fresh": 14.8, "tcte": 5.92, "biz": 1.12, "pool": 2464, "day_score": 69.38, "eve_rate": 34.1, "five_def": "極穩 (98~100%)"},
            {"yr": 128, "fresh": 14.8, "tcte": 5.92, "biz": 1.12, "pool": 2464, "day_score": 69.38, "eve_rate": 34.1, "five_def": "極穩 (98~100%)"}
        ],

        # 師資換血與五年轉型戰情 (Module 5)
        "faculty_strategy": {
            "retire_schedule": [
                {"yr": 115, "count": 1, "domain": "傳統商事法規", "detail": "專任副教授屆齡，釋出 1 個助理教授員額"},
                {"yr": 116, "count": 1, "domain": "國際貿易實務與信用狀", "detail": "專任正教授屆齡，可招募新一代 AI 跨境電商師資"},
                {"yr": 117, "count": 2, "domain": "關稅海關實務 / 國際行銷", "detail": "虎年海嘯波谷！釋出 2 個員額對接歐盟 CBAM 碳關稅與 ESG"},
                {"yr": 118, "count": 1, "domain": "商務貿易英文", "detail": "專任副教授屆齡，改聘全英語 (EMI) 國際經貿談判新血"},
                {"yr": 119, "count": 2, "domain": "國際金融 / 企業經營", "detail": "釋出 2 個員額對接經貿巨量資料與 Python 商務智慧"},
                {"yr": 120, "count": 1, "domain": "國際貿易法", "detail": "專任教授屆齡，完成 5 年期 8 名師資全面年輕化換血"}
            ],
            "hiring_matrix": [
                {"domain": "AI 跨境電商與智慧數位行銷", "priority": "緊急 (5/5)", "urgency": "High", "desc": "生成式AI文案、TikTok/亞馬遜實戰、跨境金流與SEO", "headcount": "2~3名"},
                {"domain": "ESG 永續貿易與歐盟碳關稅 (CBAM)", "priority": "緊急 (5/5)", "urgency": "High", "desc": "碳足跡申報、綠色供應鏈審查、國際ESG貿易壁壘認證", "headcount": "1~2名"},
                {"domain": "商管經貿巨量資料與 Python 分析", "priority": "高度 (4/5)", "urgency": "Medium-High", "desc": "全球海關提單大數據、供應鏈預測、商務商業智慧 (BI)", "headcount": "1名"},
                {"domain": "全英語授課 (EMI) 國際經貿法與地緣談判", "priority": "必要 (5/5)", "urgency": "High", "desc": "台美21世紀貿易倡議、CPTPP規範、全英教學認證", "headcount": "現有師資升級+新聘"}
            ],
            "curriculum_rebalance": {
                "categories": ["傳統國貿法規實務", "跨境電商與數位行銷", "ESG永續與綠色供應鏈", "經貿科技與商務數據", "商務外語與國際談判"],
                "current_114": [45, 15, 10, 10, 20],
                "target_119": [20, 35, 20, 15, 10]
            },
            "radar_kpi": {
                "dimensions": ["招生競爭力", "學生留存度", "產學研發力", "國際化深度", "課程跨域數位度", "畢業起薪競爭力"],
                "itm_now": [85, 62, 70, 75, 60, 80],
                "itm_target": [95, 88, 88, 92, 90, 92]
            }
        }
    }

    json_str = json.dumps(raw_data, ensure_ascii=False)

    # 組合完整的 HTML 戰情室檔案
    html_content = f"""<!DOCTYPE html>
<html lang="zh-Hant" class="scroll-smooth">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>國立臺中科技大學 國際貿易與經營系 | 系務策略發展與生源海嘯動態決策戰情室</title>
    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- Chart.js CDN -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <!-- Lucide Icons CDN -->
    <script src="https://unpkg.com/lucide@latest"></script>
    <script>
        tailwind.config = {{
            darkMode: 'class',
            theme: {{
                extend: {{
                    colors: {{
                        brand: {{
                            50: '#ecfdf5',
                            100: '#d1fae5',
                            500: '#10b981',
                            600: '#059669',
                            700: '#047857',
                            800: '#065f46',
                            900: '#064e3b',
                            gold: '#f59e0b'
                        }}
                    }}
                }}
            }}
        }}
    </script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Noto+Sans+TC:wght@300;400;500;700;900&display=swap');
        body {{
            font-family: 'Inter', 'Noto Sans TC', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        }}
        .custom-scrollbar::-webkit-scrollbar {{
            width: 6px;
            height: 6px;
        }}
        .custom-scrollbar::-webkit-scrollbar-track {{
            background: #0f172a;
        }}
        .custom-scrollbar::-webkit-scrollbar-thumb {{
            background: #334155;
            border-radius: 4px;
        }}
        .custom-scrollbar::-webkit-scrollbar-thumb:hover {{
            background: #475569;
        }}
        @media print {{
            .no-print {{ display: none !important; }}
            .page-break {{ page-break-before: always; }}
            body {{ background: white !important; color: black !important; }}
        }}
    </style>
</head>
<body class="bg-slate-900 text-slate-100 min-h-screen custom-scrollbar antialiased">

    <!-- 離線降級防護提示條 (當 CDN 異常時自動觸發) -->
    <div id="offline-notice-banner" class="hidden bg-amber-500/20 border-b border-amber-500/40 text-amber-300 text-xs px-4 py-2 text-center flex items-center justify-center gap-2">
        <i data-lucide="shield-alert" class="w-4 h-4 text-amber-400"></i>
        <span>離線相容防護模式已啟用：外部圖表 CDN 未載入，戰情室已切換至本機數據表格與動態試算防護模式。所有數據、指標卡片、明細表與 CSV 匯出功能均正常運作。</span>
    </div>

    <!-- 頂部高管戰情室全域 Header -->
    <header class="sticky top-0 z-50 bg-slate-900/95 backdrop-blur-md border-b border-slate-800 shadow-xl">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex items-center justify-between h-20">
                <!-- 標題與所屬單位 -->
                <div class="flex items-center space-x-4">
                    <div class="w-12 h-12 rounded-xl bg-gradient-to-tr from-emerald-600 to-teal-400 flex items-center justify-center shadow-lg shadow-emerald-500/20 text-white font-bold text-xl">
                        NUTC
                    </div>
                    <div>
                        <div class="flex items-center space-x-2">
                            <h1 class="text-xl font-bold tracking-tight text-white flex items-center gap-2">
                                國立臺中科技大學 國際貿易與經營系
                                <span class="bg-emerald-500/20 text-emerald-300 text-xs px-2.5 py-0.5 rounded-full border border-emerald-500/30 font-semibold">114 最新決策戰情室</span>
                            </h1>
                        </div>
                        <p class="text-xs text-slate-400 tracking-wide mt-0.5 flex items-center gap-2">
                            <span>系務策略發展與生源海嘯動態決策戰情室</span>
                            <span class="text-slate-600">|</span>
                            <span class="text-emerald-400 font-medium">主持人：陳俊智 副教授 (Dr. Elvis Chen)</span>
                            <span class="text-slate-600">|</span>
                            <span class="text-slate-500">UDB & 技專招聯會官方實證硬數據連線</span>
                        </p>
                    </div>
                </div>

                <!-- 頂部功能區 -->
                <div class="flex items-center space-x-3 no-print">
                    <button onclick="openSpecModal()" class="px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 text-xs font-medium flex items-center gap-1.5 transition">
                        <i data-lucide="info" class="w-4 h-4 text-cyan-400"></i>
                        <span>架構設計規格書</span>
                    </button>
                    <button onclick="window.print()" class="px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 text-xs font-medium flex items-center gap-1.5 transition">
                        <i data-lucide="printer" class="w-4 h-4 text-emerald-400"></i>
                        <span>列印/匯出PDF</span>
                    </button>
                    <button onclick="exportAllCSV()" class="px-3.5 py-1.5 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-medium flex items-center gap-1.5 shadow-lg shadow-emerald-600/30 transition">
                        <i data-lucide="download" class="w-4 h-4"></i>
                        <span>下載實證數據集 (CSV)</span>
                    </button>
                </div>
            </div>

            <!-- 5 大核心功能模組導航切換 Tabs -->
            <div class="flex space-x-1 border-t border-slate-800/80 pt-1 overflow-x-auto no-print">
                <button onclick="switchTab('module1')" id="tab-btn-module1" class="tab-btn px-4 py-3 text-xs sm:text-sm font-semibold border-b-2 border-emerald-500 text-emerald-400 flex items-center gap-2 whitespace-nowrap transition">
                    <i data-lucide="compass" class="w-4 h-4"></i>
                    <span>模組 1：北中南國立商管六強旗盤</span>
                </button>
                <button onclick="switchTab('module2')" id="tab-btn-module2" class="tab-btn px-4 py-3 text-xs sm:text-sm font-semibold border-b-2 border-transparent text-slate-400 hover:text-slate-200 flex items-center gap-2 whitespace-nowrap transition">
                    <i data-lucide="swords" class="w-4 h-4"></i>
                    <span>模組 2：中部大專商管大亂鬥</span>
                </button>
                <button onclick="switchTab('module3')" id="tab-btn-module3" class="tab-btn px-4 py-3 text-xs sm:text-sm font-semibold border-b-2 border-transparent text-slate-400 hover:text-slate-200 flex items-center gap-2 whitespace-nowrap transition">
                    <i data-lucide="stethoscope" class="w-4 h-4"></i>
                    <span>模組 3：系所體質深度診斷 (vs企管/虎科)</span>
                </button>
                <button onclick="switchTab('module4')" id="tab-btn-module4" class="tab-btn px-4 py-3 text-xs sm:text-sm font-semibold border-b-2 border-transparent text-slate-400 hover:text-slate-200 flex items-center gap-2 whitespace-nowrap transition">
                    <i data-lucide="waves" class="w-4 h-4"></i>
                    <span>模組 4：113~128 少子化海嘯動態模擬器</span>
                </button>
                <button onclick="switchTab('module5')" id="tab-btn-module5" class="tab-btn px-4 py-3 text-xs sm:text-sm font-semibold border-b-2 border-transparent text-slate-400 hover:text-slate-200 flex items-center gap-2 whitespace-nowrap transition">
                    <i data-lucide="users-round" class="w-4 h-4"></i>
                    <span>模組 5：師資換血與五年轉型決策</span>
                </button>
            </div>
        </div>
    </header>

    <!-- 全域頂部 6 大關鍵 KPI 摘要橫幅卡片 -->
    <section class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-6 pb-2">
        <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
            <!-- KPI 1 -->
            <div class="bg-slate-800/80 border border-slate-700/80 rounded-xl p-3.5 shadow-sm hover:border-emerald-500/50 transition relative overflow-hidden group">
                <div class="text-[11px] text-slate-400 font-medium flex items-center justify-between">
                    <span>114日間四技註冊率</span>
                    <i data-lucide="badge-check" class="w-3.5 h-3.5 text-emerald-400"></i>
                </div>
                <div class="text-xl font-black text-white mt-1 flex items-baseline gap-1">
                    99.06%
                    <span class="text-[10px] text-emerald-400 font-normal">(79/80人)</span>
                </div>
                <div class="text-[10px] text-slate-400 mt-1 flex items-center gap-1">
                    <span class="text-cyan-400">境外外加 +26人</span>
                </div>
                <div class="absolute -right-2 -bottom-2 w-10 h-10 bg-emerald-500/5 rounded-full group-hover:scale-150 transition"></div>
            </div>

            <!-- KPI 2 -->
            <div class="bg-slate-800/80 border border-slate-700/80 rounded-xl p-3.5 shadow-sm hover:border-cyan-500/50 transition relative overflow-hidden group">
                <div class="text-[11px] text-slate-400 font-medium flex items-center justify-between">
                    <span>114統測單科均分</span>
                    <i data-lucide="trophy" class="w-3.5 h-3.5 text-cyan-400"></i>
                </div>
                <div class="text-xl font-black text-white mt-1 flex items-baseline gap-1">
                    71.78<span class="text-xs font-medium text-slate-300">分</span>
                    <span class="text-[10px] text-emerald-400 font-bold bg-emerald-500/10 px-1 rounded">首度逆轉</span>
                </div>
                <div class="text-[10px] text-slate-400 mt-1 flex items-center gap-1">
                    <span>反超中科企管 <span class="text-emerald-400 font-bold">+0.05分</span></span>
                </div>
                <div class="absolute -right-2 -bottom-2 w-10 h-10 bg-cyan-500/5 rounded-full group-hover:scale-150 transition"></div>
            </div>

            <!-- KPI 3 -->
            <div class="bg-slate-800/80 border border-slate-700/80 rounded-xl p-3.5 shadow-sm hover:border-indigo-500/50 transition relative overflow-hidden group">
                <div class="text-[11px] text-slate-400 font-medium flex items-center justify-between">
                    <span>全系在學總人數</span>
                    <i data-lucide="users" class="w-3.5 h-3.5 text-indigo-400"></i>
                </div>
                <div class="text-xl font-black text-white mt-1 flex items-baseline gap-1">
                    1,044<span class="text-xs font-medium text-slate-300">人</span>
                </div>
                <div class="text-[10px] text-slate-400 mt-1 flex items-center gap-1 truncate">
                    <span>五專248 | 四技482 | 進修314</span>
                </div>
                <div class="absolute -right-2 -bottom-2 w-10 h-10 bg-indigo-500/5 rounded-full group-hover:scale-150 transition"></div>
            </div>

            <!-- KPI 4 -->
            <div class="bg-slate-800/80 border border-slate-700/80 rounded-xl p-3.5 shadow-sm hover:border-amber-500/50 transition relative overflow-hidden group">
                <div class="text-[11px] text-slate-400 font-medium flex items-center justify-between">
                    <span>113退學流失率</span>
                    <i data-lucide="alert-triangle" class="w-3.5 h-3.5 text-amber-400"></i>
                </div>
                <div class="text-xl font-black text-amber-400 mt-1 flex items-baseline gap-1">
                    3.73%
                    <span class="text-[10px] text-slate-400 font-normal">(80人)</span>
                </div>
                <div class="text-[10px] text-rose-400 mt-1 flex items-center gap-1 font-medium">
                    <span>六強最高！科系不符24人</span>
                </div>
                <div class="absolute -right-2 -bottom-2 w-10 h-10 bg-amber-500/5 rounded-full group-hover:scale-150 transition"></div>
            </div>

            <!-- KPI 5 -->
            <div class="bg-slate-800/80 border border-slate-700/80 rounded-xl p-3.5 shadow-sm hover:border-rose-500/50 transition relative overflow-hidden group">
                <div class="text-[11px] text-slate-400 font-medium flex items-center justify-between">
                    <span>114進修四技註冊</span>
                    <i data-lucide="trending-down" class="w-3.5 h-3.5 text-rose-400"></i>
                </div>
                <div class="text-xl font-black text-rose-400 mt-1 flex items-baseline gap-1">
                    50.91%
                    <span class="text-[10px] text-slate-400 font-normal">(28/55人)</span>
                </div>
                <div class="text-[10px] text-rose-400/90 mt-1 flex items-center gap-1">
                    <span>深水警戒區 (核定已砍25)</span>
                </div>
                <div class="absolute -right-2 -bottom-2 w-10 h-10 bg-rose-500/5 rounded-full group-hover:scale-150 transition"></div>
            </div>

            <!-- KPI 6 -->
            <div class="bg-slate-800/80 border border-slate-700/80 rounded-xl p-3.5 shadow-sm hover:border-purple-500/50 transition relative overflow-hidden group">
                <div class="text-[11px] text-slate-400 font-medium flex items-center justify-between">
                    <span>師資副教授佔比</span>
                    <i data-lucide="graduation-cap" class="w-3.5 h-3.5 text-purple-400"></i>
                </div>
                <div class="text-xl font-black text-purple-300 mt-1 flex items-baseline gap-1">
                    66.7%
                    <span class="text-[10px] text-slate-400 font-normal">(14/21人)</span>
                </div>
                <div class="text-[10px] text-slate-400 mt-1 flex items-center gap-1">
                    <span class="text-purple-400">未來5~8年迎黃金退休潮</span>
                </div>
                <div class="absolute -right-2 -bottom-2 w-10 h-10 bg-purple-500/5 rounded-full group-hover:scale-150 transition"></div>
            </div>
        </div>
    </section>

    <!-- 模組主要呈現內容容器 -->
    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">

        <!-- =============================================================== -->
        <!-- 模組 1：北中南國立商管/國貿六強戰略旗盤 -->
        <!-- =============================================================== -->
        <section id="module1" class="tab-content block space-y-6">
            <div class="bg-slate-800/60 border border-slate-700/70 rounded-2xl p-5 shadow-lg">
                <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
                    <div>
                        <div class="flex items-center gap-2">
                            <span class="px-2.5 py-0.5 rounded text-xs font-bold bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">MODULE 1</span>
                            <h2 class="text-lg font-bold text-white">北中南國立商管/國貿六強戰略旗盤 (Regional Radar & Benchmarking)</h2>
                        </div>
                        <p class="text-xs text-slate-400 mt-1">
                            以教育部 UDB 校務資訊與技專招聯會官方數據為底層，深度橫向對比「北商國商、中科國貿、雲科國管、高科航管、高科國企、高科供應鏈」全方位戰力指標。
                        </p>
                    </div>
                    <!-- 篩選與排序控制項 -->
                    <div class="flex flex-wrap items-center gap-3 self-start md:self-auto">
                        <div class="flex items-center gap-1.5">
                            <label class="text-xs text-slate-400">區域：</label>
                            <select id="m1-region-filter" onchange="applyRegionalFilters()" class="bg-slate-900 border border-slate-700 text-xs text-slate-200 rounded-lg px-2.5 py-1.5 focus:outline-none focus:border-emerald-500">
                                <option value="ALL">全台六強 (全部)</option>
                                <option value="北部">北部 (北商大)</option>
                                <option value="中部">中部 (中科大/雲科大)</option>
                                <option value="南部">南部 (高科大三大系)</option>
                            </select>
                        </div>
                        <div class="flex items-center gap-1.5">
                            <label class="text-xs text-slate-400">排序：</label>
                            <select id="m1-sort-by" onchange="applyRegionalFilters()" class="bg-slate-900 border border-slate-700 text-xs text-slate-200 rounded-lg px-2.5 py-1.5 focus:outline-none focus:border-emerald-500">
                                <option value="default">預設排序</option>
                                <option value="total_stu_desc">在學人數 (由大到小)</option>
                                <option value="score_114_desc">114統測均分 (由高到低)</option>
                                <option value="drop_rate_asc">退學流失率 (由低到高)</option>
                                <option value="oversea_pct_desc">國際化境外佔比 (由高到低)</option>
                            </select>
                        </div>
                    </div>
                </div>

                <!-- 戰略六強橫向真實數據比對表 -->
                <div class="overflow-x-auto mt-4 rounded-xl border border-slate-700/80">
                    <table class="w-full text-left text-xs border-collapse">
                        <thead class="bg-slate-900/80 text-slate-400 uppercase tracking-wider font-semibold border-b border-slate-700">
                            <tr>
                                <th class="p-3">代號 / 系所全名</th>
                                <th class="p-3">區域</th>
                                <th class="p-3 text-right">在學總人數</th>
                                <th class="p-3 text-right">五專部</th>
                                <th class="p-3 text-right">日間學士</th>
                                <th class="p-3 text-right">進修學士</th>
                                <th class="p-3 text-right">碩博生</th>
                                <th class="p-3">師資結構 (正/副/助)</th>
                                <th class="p-3 text-right">境外生 (佔比)</th>
                                <th class="p-3 text-right">114日間註冊率</th>
                                <th class="p-3 text-right">114統測單科均分</th>
                                <th class="p-3 text-right">113退學率</th>
                            </tr>
                        </thead>
                        <tbody id="regional-table-body" class="divide-y divide-slate-800 bg-slate-850">
                            <!-- 動態生成在下方 -->
                        </tbody>
                    </table>
                </div>
            </div>

            <!-- 兩大核心視覺化：多維雷達圖 + 四象限戰略定位圖 -->
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <!-- 圖 1：全方位戰力多維雷達圖 -->
                <div class="bg-slate-800/70 border border-slate-700/70 rounded-2xl p-5 shadow-lg flex flex-col">
                    <div class="flex items-center justify-between mb-3">
                        <div class="flex items-center gap-2">
                            <i data-lucide="radar" class="w-4 h-4 text-emerald-400"></i>
                            <h3 class="text-sm font-bold text-white">六強系所綜合戰力雷達 (Radar Benchmarking)</h3>
                        </div>
                        <span class="text-[11px] text-slate-400">5 維度標準化得分 (滿分100)</span>
                    </div>
                    <div class="text-xs text-slate-400 mb-2">
                        評估維度：生源吸附力 (統測均分)、規模抗震度 (在學生)、國際化深度 (境外生比)、註冊穩定度 (日間註冊率)、留存防禦力 (100 - 退學率)。
                    </div>
                    <div class="relative flex-1 min-h-[340px] flex items-center justify-center">
                        <canvas id="chart-m1-radar"></canvas>
                    </div>
                </div>

                <!-- 圖 2：戰略四象限定位散佈氣泡圖 -->
                <div class="bg-slate-800/70 border border-slate-700/70 rounded-2xl p-5 shadow-lg flex flex-col">
                    <div class="flex items-center justify-between mb-3">
                        <div class="flex items-center gap-2">
                            <i data-lucide="layout-grid" class="w-4 h-4 text-cyan-400"></i>
                            <h3 class="text-sm font-bold text-white">戰略定位四象限矩陣 (Strategic Positioning Matrix)</h3>
                        </div>
                        <span class="text-[11px] text-slate-400">X: 114統測均分 | Y: 114日間註冊率 | 圓半徑: 在學規模</span>
                    </div>
                    <div class="text-xs text-slate-400 mb-2">
                        中科國貿座落於「規模旗艦堡壘」象限，維持 1,044 人大系規模與 99% 註冊率，但錄取分面臨北商國商與雲科國管的拉扯。
                    </div>
                    <div class="relative flex-1 min-h-[340px]">
                        <canvas id="chart-m1-scatter"></canvas>
                    </div>
                </div>
            </div>

            <!-- 六強深層戰略洞察卡片 -->
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div class="bg-slate-800/50 border border-slate-700/60 rounded-xl p-4">
                    <div class="flex items-center gap-2 text-emerald-400 text-xs font-bold mb-1">
                        <i data-lucide="check-circle-2" class="w-4 h-4"></i>
                        <span>中科國貿優勢 (Strategic Strength)</span>
                    </div>
                    <p class="text-xs text-slate-300 leading-relaxed">
                        在中部技職體系擁有無可撼動的<strong class="text-white">旗艦規模 (1,044人)</strong>，五專 (248人) 滿招防禦度極高，日間四技註冊率高達 99.06%，114 學年錄取分首度反超中科企管。
                    </p>
                </div>
                <div class="bg-slate-800/50 border border-slate-700/60 rounded-xl p-4">
                    <div class="flex items-center gap-2 text-rose-400 text-xs font-bold mb-1">
                        <i data-lucide="alert-circle" class="w-4 h-4"></i>
                        <span>中科國貿隱憂 (Strategic Vulnerability)</span>
                    </div>
                    <p class="text-xs text-slate-300 leading-relaxed">
                        <strong class="text-rose-300">退學率 3.73% (80人) 為六強之冠</strong>（北商僅2.71%、雲科2.20%）；且六強中唯一<strong class="text-rose-300">完全缺乏碩士與碩專班</strong>（高科國企研發碩博達113人、北商54人）。
                    </p>
                </div>
                <div class="bg-slate-800/50 border border-slate-700/60 rounded-xl p-4">
                    <div class="flex items-center gap-2 text-cyan-400 text-xs font-bold mb-1">
                        <i data-lucide="sparkles" class="w-4 h-4"></i>
                        <span>同儕借鏡策略 (Benchmark Action)</span>
                    </div>
                    <p class="text-xs text-slate-300 leading-relaxed">
                        借鏡<strong class="text-white">高科航管</strong>專精供應鏈物流逆勢微揚 (+0.33分)；以及<strong class="text-white">雲科國管</strong>高達 19.2% 境外生與全英語國際化策略，突破少子化在地生源瓶頸。
                    </p>
                </div>
            </div>
        </section>

        <!-- =============================================================== -->
        <!-- 模組 2：中部大專商管大亂鬥 (中科 vs 逢甲 vs 東海 vs 嶺東/朝陽 vs 虎科) -->
        <!-- =============================================================== -->
        <section id="module2" class="tab-content hidden space-y-6">
            <div class="bg-slate-800/60 border border-slate-700/70 rounded-2xl p-5 shadow-lg">
                <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
                    <div>
                        <div class="flex items-center gap-2">
                            <span class="px-2.5 py-0.5 rounded text-xs font-bold bg-amber-500/20 text-amber-300 border border-amber-500/30">MODULE 2</span>
                            <h2 class="text-lg font-bold text-white">中部大專商管大亂鬥 (Central Taiwan Competitive Landscape)</h2>
                        </div>
                        <p class="text-xs text-slate-400 mt-1">
                            剖析中台灣跨學制、跨體系商管群生存戰：國立技職 (中科/虎科) vs 私立老牌普大 (逢甲/東海) vs 私立資金巨頭 (朝陽/嶺東)。
                        </p>
                    </div>
                </div>

                <!-- 中部競合全景矩陣卡片 -->
                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mt-5">
                    <!-- 中科大國貿 -->
                    <div class="bg-slate-900/90 border-2 border-emerald-500/50 rounded-xl p-4 relative shadow-lg">
                        <div class="flex items-center justify-between">
                            <span class="text-xs font-bold px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300">國立科大龍頭</span>
                            <span class="text-[11px] text-emerald-400 font-semibold">基準主戰系</span>
                        </div>
                        <h4 class="text-base font-bold text-white mt-2 flex items-center justify-between">
                            中科大 國際貿易與經營系
                            <span class="text-xs font-normal text-slate-400">1,044人</span>
                        </h4>
                        <div class="grid grid-cols-2 gap-2 mt-3 pt-3 border-t border-slate-800 text-xs">
                            <div><span class="text-slate-400">日間註冊：</span><span class="text-white font-bold">99.06%</span></div>
                            <div><span class="text-slate-400">統測均分：</span><span class="text-emerald-400 font-bold">71.78分</span></div>
                            <div><span class="text-slate-400">進修註冊：</span><span class="text-rose-400 font-bold">50.91%</span></div>
                            <div><span class="text-slate-400">退學率：</span><span class="text-amber-400 font-bold">3.73%</span></div>
                        </div>
                        <p class="text-[11px] text-slate-300 mt-2.5 bg-slate-800/60 p-2 rounded border border-slate-700/50">
                            <strong>核心策略：</strong>公立低學費 (2.7萬/期) 與一中商圈優勢強大；但進修四技腰斬面臨危機，且無研究所承接高階生源。
                        </p>
                    </div>

                    <!-- 逢甲國貿 -->
                    <div class="bg-slate-900/90 border border-slate-700/80 rounded-xl p-4 relative hover:border-indigo-500/50 transition">
                        <div class="flex items-center justify-between">
                            <span class="text-xs font-bold px-2 py-0.5 rounded bg-indigo-500/20 text-indigo-300">私立頂尖普大</span>
                            <span class="text-[11px] text-rose-400 font-semibold flex items-center gap-1"><i data-lucide="flame" class="w-3 h-3"></i>最大生源勁敵</span>
                        </div>
                        <h4 class="text-base font-bold text-white mt-2 flex items-center justify-between">
                            逢甲大學 國際經營與貿易學系
                            <span class="text-xs font-normal text-slate-400">~1,180人</span>
                        </h4>
                        <div class="grid grid-cols-2 gap-2 mt-3 pt-3 border-t border-slate-800 text-xs">
                            <div><span class="text-slate-400">年招生量：</span><span class="text-white font-bold">~200人</span></div>
                            <div><span class="text-slate-400">學測生源：</span><span class="text-indigo-300 font-bold">90%普高</span></div>
                            <div><span class="text-slate-400">全英專班：</span><span class="text-cyan-300 font-bold">38人/年</span></div>
                            <div><span class="text-slate-400">學校資金：</span><span class="text-emerald-400 font-bold">45.8億</span></div>
                        </div>
                        <p class="text-[11px] text-slate-300 mt-2.5 bg-slate-800/60 p-2 rounded border border-slate-700/50">
                            <strong>核心威脅：</strong>每年日間3班(155人)+全英專班(38人)，以西屯商圈品牌、全英語學程、普高學測吸磁，吸走大量原本可能報考科大的菁英生源。
                        </p>
                    </div>

                    <!-- 東海國貿 -->
                    <div class="bg-slate-900/90 border border-slate-700/80 rounded-xl p-4 relative hover:border-cyan-500/50 transition">
                        <div class="flex items-center justify-between">
                            <span class="text-xs font-bold px-2 py-0.5 rounded bg-cyan-500/20 text-cyan-300">私立老牌普大</span>
                            <span class="text-[11px] text-cyan-400 font-semibold">減招轉型典範</span>
                        </div>
                        <h4 class="text-base font-bold text-white mt-2 flex items-center justify-between">
                            東海大學 國際經營與貿易學系
                            <span class="text-xs font-normal text-slate-400">~520人</span>
                        </h4>
                        <div class="grid grid-cols-2 gap-2 mt-3 pt-3 border-t border-slate-800 text-xs">
                            <div><span class="text-slate-400">戰略減招：</span><span class="text-amber-400 font-bold">-30% (150→106)</span></div>
                            <div><span class="text-slate-400">114註冊率：</span><span class="text-emerald-400 font-bold">96.80% (強彈)</span></div>
                            <div><span class="text-slate-400">雙聯學位：</span><span class="text-white font-medium">美國天普2+2</span></div>
                            <div><span class="text-slate-400">學校資金：</span><span class="text-slate-300 font-bold">28.5億</span></div>
                        </div>
                        <p class="text-[11px] text-slate-300 mt-2.5 bg-slate-800/60 p-2 rounded border border-slate-700/50">
                            <strong>戰術啟示：</strong>主動壯士斷腕砍掉3成名額，註冊率立即由谷底強彈至 96.8%，搭配博雅書院與海外雙聯，成功築起精緻化護城河。
                        </p>
                    </div>

                    <!-- 嶺東國企 (警訊案例) -->
                    <div class="bg-slate-900/90 border border-rose-500/40 rounded-xl p-4 relative hover:border-rose-500 transition">
                        <div class="flex items-center justify-between">
                            <span class="text-xs font-bold px-2 py-0.5 rounded bg-rose-500/20 text-rose-300">私立科大警戒</span>
                            <span class="text-[11px] text-rose-400 font-semibold flex items-center gap-1"><i data-lucide="alert-octagon" class="w-3 h-3"></i>生源斷層深水區</span>
                        </div>
                        <h4 class="text-base font-bold text-white mt-2 flex items-center justify-between">
                            嶺東科大 國際企業系
                            <span class="text-xs font-normal text-slate-400">410人</span>
                        </h4>
                        <div class="grid grid-cols-2 gap-2 mt-3 pt-3 border-t border-slate-800 text-xs">
                            <div><span class="text-slate-400">日間註冊：</span><span class="text-rose-400 font-black text-sm">51.40%</span></div>
                            <div><span class="text-slate-400">退學率：</span><span class="text-rose-400 font-black text-sm">7.22%</span></div>
                            <div><span class="text-slate-400">學校現金：</span><span class="text-emerald-400 font-bold">31.2億 (超富)</span></div>
                            <div><span class="text-slate-400">進修註冊：</span><span class="text-rose-400 font-bold">38.60%</span></div>
                        </div>
                        <p class="text-[11px] text-slate-300 mt-2.5 bg-slate-800/60 p-2 rounded border border-slate-700/50">
                            <strong>重大警示：</strong>「學校極有錢 (31.2億現金) 卻無法阻止系所生源崩潰」！日間註冊腰斬至 51.4%、退學率高達 7.22%，印證傳統私立國貿系所生源斷崖已至。
                        </p>
                    </div>

                    <!-- 朝陽科大 -->
                    <div class="bg-slate-900/90 border border-slate-700/80 rounded-xl p-4 relative hover:border-purple-500/50 transition">
                        <div class="flex items-center justify-between">
                            <span class="text-xs font-bold px-2 py-0.5 rounded bg-purple-500/20 text-purple-300">私立技職龍頭</span>
                            <span class="text-[11px] text-purple-300 font-semibold">外展南向防衛</span>
                        </div>
                        <h4 class="text-base font-bold text-white mt-2 flex items-center justify-between">
                            朝陽科大 財務金融/商管群
                            <span class="text-xs font-normal text-slate-400">~2,100人</span>
                        </h4>
                        <div class="grid grid-cols-2 gap-2 mt-3 pt-3 border-t border-slate-800 text-xs">
                            <div><span class="text-slate-400">日間註冊：</span><span class="text-white font-bold">89.20%</span></div>
                            <div><span class="text-slate-400">學校現金：</span><span class="text-emerald-400 font-bold">25.5億 (厚實)</span></div>
                            <div><span class="text-slate-400">境外佔比：</span><span class="text-cyan-300 font-bold">~25%</span></div>
                            <div><span class="text-slate-400">特色學院：</span><span class="text-purple-300 font-medium">航空學院帶動</span></div>
                        </div>
                        <p class="text-[11px] text-slate-300 mt-2.5 bg-slate-800/60 p-2 rounded border border-slate-700/50">
                            <strong>防禦模型：</strong>坐擁 25.5 億現金，藉由航空學院打響知名度，並大舉招收東南亞外加專班填補本地生缺口，私立科大中防禦力最強。
                        </p>
                    </div>

                    <!-- 虎科財金 (借鏡案例) -->
                    <div class="bg-slate-900/90 border border-amber-500/40 rounded-xl p-4 relative hover:border-amber-500 transition">
                        <div class="flex items-center justify-between">
                            <span class="text-xs font-bold px-2 py-0.5 rounded bg-amber-500/20 text-amber-300">國立科大借鏡</span>
                            <span class="text-[11px] text-amber-400 font-semibold flex items-center gap-1"><i data-lucide="alert-triangle" class="w-3 h-3"></i>分數跳水警報</span>
                        </div>
                        <h4 class="text-base font-bold text-white mt-2 flex items-center justify-between">
                            虎尾科大 財務金融系
                            <span class="text-xs font-normal text-slate-400">436人 / 10師</span>
                        </h4>
                        <div class="grid grid-cols-2 gap-2 mt-3 pt-3 border-t border-slate-800 text-xs">
                            <div><span class="text-slate-400">日間註冊：</span><span class="text-white font-bold">98.00%</span></div>
                            <div><span class="text-slate-400">統測均分：</span><span class="text-rose-400 font-black">65.64分 (暴跌)</span></div>
                            <div><span class="text-slate-400">進修二技：</span><span class="text-rose-400 font-black">39.29% (崩盤)</span></div>
                            <div><span class="text-slate-400">生師比：</span><span class="text-emerald-400 font-bold">43.6 (小系)</span></div>
                        </div>
                        <p class="text-[11px] text-slate-300 mt-2.5 bg-slate-800/60 p-2 rounded border border-slate-700/50">
                            <strong>直接借鏡：</strong>國立公立光環無法掩蓋「生源質量滑落」——114 統測錄取分大跌至 65.64 分，且進修二技跌破 40% 停招線，中科國貿須高度警惕進修部。
                        </p>
                    </div>
                </div>
            </div>

            <!-- 中部商管競合格局對比圖表 -->
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <!-- 圖 1：註冊率 vs 退學率 風險對照長條圖 -->
                <div class="bg-slate-800/70 border border-slate-700/70 rounded-2xl p-5 shadow-lg">
                    <div class="flex items-center justify-between mb-3">
                        <div class="flex items-center gap-2">
                            <i data-lucide="bar-chart-3" class="w-4 h-4 text-emerald-400"></i>
                            <h3 class="text-sm font-bold text-white">中部各大專商管註冊率與退學率對比</h3>
                        </div>
                        <span class="text-[11px] text-slate-400">114 新生註冊 vs 113 學年退學</span>
                    </div>
                    <div class="relative min-h-[300px]">
                        <canvas id="chart-m2-bars"></canvas>
                    </div>
                </div>

                <!-- 圖 2：生源爭奪與財務防禦矩陣散佈圖 -->
                <div class="bg-slate-800/70 border border-slate-700/70 rounded-2xl p-5 shadow-lg">
                    <div class="flex items-center justify-between mb-3">
                        <div class="flex items-center gap-2">
                            <i data-lucide="shield-alert" class="w-4 h-4 text-amber-400"></i>
                            <h3 class="text-sm font-bold text-white">財務護城河 vs 招生生源健康度矩陣</h3>
                        </div>
                        <span class="text-[11px] text-slate-400">X: 錄取門檻估值 | Y: 日間註冊率</span>
                    </div>
                    <div class="relative min-h-[300px]">
                        <canvas id="chart-m2-finance"></canvas>
                    </div>
                </div>
            </div>
        </section>

        <!-- =============================================================== -->
        <!-- 模組 3：系所體質深度診斷 (中科國貿 vs 企管 & 虎科財金) -->
        <!-- =============================================================== -->
        <section id="module3" class="tab-content hidden space-y-6">
            <!-- 歷史反超快報 Banner -->
            <div class="bg-gradient-to-r from-emerald-900/60 via-slate-800/80 to-cyan-900/60 border border-emerald-500/40 rounded-2xl p-5 shadow-xl relative overflow-hidden">
                <div class="flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
                    <div>
                        <div class="flex items-center gap-2">
                            <span class="bg-emerald-500 text-slate-950 font-black text-xs px-2.5 py-0.5 rounded uppercase tracking-wider">Historical Milestone</span>
                            <span class="text-xs font-semibold text-emerald-300">114學年度 統測 09商管群最低單科錄取均分</span>
                        </div>
                        <h2 class="text-xl font-extrabold text-white mt-1 flex items-baseline gap-2">
                            中科國貿 <span class="text-emerald-400 text-2xl">71.78分</span> 首度反超 中科企管 <span class="text-slate-300 text-2xl">71.73分</span> (+0.05分)！
                        </h2>
                        <p class="text-xs text-slate-300 mt-1 max-w-3xl leading-relaxed">
                            連續 5 年（109~113）中科企管最低錄取分均領先中科國貿（111年曾落後達 1.67分），於 114 學年度國貿系展現韌性首度實現歷史性黃金交叉反超！
                        </p>
                    </div>
                    <div class="bg-slate-900/90 border border-emerald-500/40 rounded-xl p-3 text-center self-stretch md:self-auto min-w-[160px]">
                        <div class="text-[11px] text-slate-400 font-medium">6年錄取分差消長</div>
                        <div class="text-lg font-black text-emerald-400 mt-0.5">+0.05分</div>
                        <div class="text-[10px] text-slate-400">109年 -1.27 → 114年 +0.05</div>
                    </div>
                </div>
            </div>

            <!-- 6年統測商管最低錄取折合單科均分走勢圖 (互動折線圖) -->
            <div class="bg-slate-800/70 border border-slate-700/70 rounded-2xl p-5 shadow-lg">
                <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 mb-4">
                    <div>
                        <h3 class="text-base font-bold text-white flex items-center gap-2">
                            <i data-lucide="trending-up" class="w-5 h-5 text-emerald-400"></i>
                            近 6 年（109~114學年度）統測商管群最低錄取單科均分趨勢
                        </h3>
                        <p class="text-xs text-slate-400 mt-0.5">
                            官方技專招聯會登記分發最低總分折合單科權重平均（點擊下方按鈕可自訂顯示/隱藏特定校系）
                        </p>
                    </div>
                    <!-- 折線切換按鈕區 -->
                    <div class="flex flex-wrap gap-1.5" id="score-trend-toggles">
                        <!-- 動態生成按鈕 -->
                    </div>
                </div>
                <div class="relative min-h-[380px]">
                    <canvas id="chart-m3-score-trend"></canvas>
                </div>
            </div>

            <!-- 雙雄硬核體質對照表：中科國貿 vs 中科企管 -->
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <!-- 國貿 vs 企管 師資與學制結構 -->
                <div class="bg-slate-800/70 border border-slate-700/70 rounded-2xl p-5 shadow-lg flex flex-col justify-between">
                    <div>
                        <div class="flex items-center justify-between mb-4 border-b border-slate-700 pb-3">
                            <h3 class="text-sm font-bold text-white flex items-center gap-2">
                                <i data-lucide="split" class="w-4 h-4 text-cyan-400"></i>
                                師資與學制梯隊深度解剖 (114學年)
                            </h3>
                            <span class="text-xs text-slate-400">中科國貿 vs 中科企管</span>
                        </div>
                        <div class="space-y-4 text-xs">
                            <!-- 師資總覽 -->
                            <div>
                                <div class="text-slate-400 font-semibold mb-1 flex justify-between">
                                    <span>專任師資規模與結構</span>
                                    <span>國貿 21人 vs 企管 24人</span>
                                </div>
                                <div class="grid grid-cols-2 gap-3 bg-slate-900/60 p-3 rounded-xl border border-slate-700/60">
                                    <div>
                                        <div class="font-bold text-emerald-400">國際貿易與經營系 (21人)</div>
                                        <div class="text-slate-300 mt-1">正教授：4人 (19.0%)</div>
                                        <div class="text-slate-300">副教授：<strong class="text-purple-300">14人 (66.7%)</strong></div>
                                        <div class="text-slate-300">助理教授：3人 (14.3%)</div>
                                        <div class="text-slate-400 text-[10px] mt-1">結構偏向資深副教授卡栓</div>
                                    </div>
                                    <div>
                                        <div class="font-bold text-cyan-400">企業管理系 (24人)</div>
                                        <div class="text-slate-300 mt-1">正教授：5人 (20.8%)</div>
                                        <div class="text-slate-300">副教授：12人 (50.0%)</div>
                                        <div class="text-slate-300">助理教授：<strong class="text-cyan-300">7人 (29.2%)</strong></div>
                                        <div class="text-slate-400 text-[10px] mt-1">年輕新血助理教授充沛</div>
                                    </div>
                                </div>
                            </div>

                            <!-- 學制結構重大痛點 -->
                            <div>
                                <div class="text-slate-400 font-semibold mb-1 flex justify-between">
                                    <span>學制縱深與在學生分佈</span>
                                    <span>國貿 1,044人 vs 企管 1,165人</span>
                                </div>
                                <div class="bg-slate-900/60 p-3 rounded-xl border border-slate-700/60 space-y-2">
                                    <div class="flex justify-between items-center pb-1 border-b border-slate-800">
                                        <span class="text-slate-400">五專部規模</span>
                                        <span class="text-white font-medium">國貿 248人 (1班) vs <strong class="text-cyan-300">企管 438人 (2班)</strong></span>
                                    </div>
                                    <div class="flex justify-between items-center pb-1 border-b border-slate-800">
                                        <span class="text-slate-400">日間學士班 (四技/二技)</span>
                                        <span class="text-emerald-400 font-bold">國貿 482人 vs 企管 295人</span>
                                    </div>
                                    <div class="flex justify-between items-center pb-1 border-b border-slate-800">
                                        <span class="text-slate-400">技優專班</span>
                                        <span class="text-white">國貿 0人 vs <strong class="text-cyan-300">企管 103人</strong></span>
                                    </div>
                                    <div class="flex justify-between items-center pb-1 border-b border-slate-800">
                                        <span class="text-slate-400">進修學士班 (四技/二技)</span>
                                        <span class="text-white">國貿 314人 vs 企管 227人</span>
                                    </div>
                                    <div class="flex justify-between items-center">
                                        <span class="text-rose-400 font-bold">研究所 (日碩+碩專)</span>
                                        <span class="text-rose-400 font-black">國貿 0人 (無) vs 企管 102人 (滿招)</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="text-[11px] text-amber-300/90 bg-amber-500/10 p-3 rounded-xl border border-amber-500/30 mt-3">
                        <strong>關鍵診斷：</strong>企管系擁有完整的「五專2班 + 技優領航 + 日間碩士 + EMBA碩專」多元護城河，抗少子化彈性極高；國貿系欠缺研究所與技優班，日間四技規模龐大，但進修部負擔沉重。
                    </div>
                </div>

                <!-- 退學與休學深水區剖析 (113學年度教育部正式退學報表) -->
                <div class="bg-slate-800/70 border border-slate-700/70 rounded-2xl p-5 shadow-lg flex flex-col justify-between">
                    <div>
                        <div class="flex items-center justify-between mb-4 border-b border-slate-700 pb-3">
                            <h3 class="text-sm font-bold text-white flex items-center gap-2">
                                <i data-lucide="user-x" class="w-4 h-4 text-rose-400"></i>
                                退學與休學深水區流失率分析 (113學年官方退學報表)
                            </h3>
                            <span class="text-xs text-rose-400 font-semibold">流失痛點深度診斷</span>
                        </div>
                        <div class="space-y-3 text-xs">
                            <div class="grid grid-cols-2 gap-3 text-center">
                                <div class="bg-slate-900/80 p-3 rounded-xl border border-rose-500/30">
                                    <div class="text-slate-400 text-[11px]">國貿系 整體退學率</div>
                                    <div class="text-2xl font-black text-rose-400 mt-1">3.73%</div>
                                    <div class="text-slate-400 text-[10px] mt-0.5">退學 80人 / 母數 2,142人次</div>
                                </div>
                                <div class="bg-slate-900/80 p-3 rounded-xl border border-slate-700">
                                    <div class="text-slate-400 text-[11px]">企管系 整體退學率</div>
                                    <div class="text-2xl font-black text-slate-200 mt-1">2.95%</div>
                                    <div class="text-slate-400 text-[10px] mt-0.5">退學 72人 / 母數 2,440人次</div>
                                </div>
                            </div>

                            <!-- 自請退學原因細分長條對比 -->
                            <div class="bg-slate-900/60 p-3.5 rounded-xl border border-slate-700/60 space-y-2">
                                <div class="text-slate-300 font-semibold mb-2">學生自請退學原因細分：</div>
                                <div>
                                    <div class="flex justify-between text-[11px] mb-1">
                                        <span class="text-slate-400">因「科系不符期待」自退</span>
                                        <span class="text-rose-400 font-bold">國貿 24人 (佔自退 72.7%) vs 企管 20人</span>
                                    </div>
                                    <div class="w-full bg-slate-800 h-2 rounded-full overflow-hidden flex">
                                        <div class="bg-rose-500 h-full" style="width: 72.7%"></div>
                                        <div class="bg-slate-600 h-full" style="width: 27.3%"></div>
                                    </div>
                                </div>
                                <div>
                                    <div class="flex justify-between text-[11px] mb-1">
                                        <span class="text-slate-400">因「工作需求」自退</span>
                                        <span class="text-amber-400 font-bold">國貿 8人 vs 企管 3人</span>
                                    </div>
                                    <div class="w-full bg-slate-800 h-2 rounded-full overflow-hidden flex">
                                        <div class="bg-amber-500 h-full" style="width: 72.7%"></div>
                                    </div>
                                </div>
                                <div class="pt-2 border-t border-slate-800 flex justify-between text-[11px]">
                                    <span class="text-slate-400">學年底休學人數 (休學率)</span>
                                    <span class="text-slate-300">國貿 73人 (<strong class="text-amber-400">6.82%</strong>) vs 企管 73人 (5.98%)</span>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="text-[11px] text-slate-300 bg-slate-800/80 p-3 rounded-xl border border-slate-700 mt-3 leading-relaxed">
                        <strong class="text-white">處方對策：</strong>國貿系高達 24 人因「科系不符期待」退學，反映大一新生對傳統「國貿實務/報關信用狀」感到陳舊與落差。必須在大一導入「AI 跨境行銷與全球品牌實戰」，並加強導師預警挽留。
                    </div>
                </div>
            </div>

            <!-- 113 vs 114 學制新生註冊率詳細矩陣對比表 -->
            <div class="bg-slate-800/70 border border-slate-700/70 rounded-2xl p-5 shadow-lg">
                <h3 class="text-sm font-bold text-white flex items-center gap-2 mb-3">
                    <i data-lucide="table" class="w-4 h-4 text-emerald-400"></i>
                    國貿系 vs 企管系 113~114學年度 各學制新生註冊率完整消長矩陣
                </h3>
                <div class="overflow-x-auto rounded-xl border border-slate-700/80">
                    <table class="w-full text-left text-xs border-collapse">
                        <thead class="bg-slate-900/80 text-slate-400 uppercase font-semibold border-b border-slate-700">
                            <tr>
                                <th class="p-3">學制班別</th>
                                <th class="p-3">國貿系 (113學年)</th>
                                <th class="p-3">國貿系 (114學年)</th>
                                <th class="p-3">企管系 (113學年)</th>
                                <th class="p-3">企管系 (114學年)</th>
                                <th class="p-3">體質差異分析</th>
                            </tr>
                        </thead>
                        <tbody id="m3-reg-matrix-body" class="divide-y divide-slate-800 bg-slate-850">
                            <!-- 動態填入 -->
                        </tbody>
                    </table>
                </div>
            </div>
        </section>

        <!-- =============================================================== -->
        <!-- 模組 4：113~128 少子化海嘯動態模擬器 -->
        <!-- =============================================================== -->
        <section id="module4" class="tab-content hidden space-y-6">
            <div class="bg-slate-800/60 border border-slate-700/70 rounded-2xl p-5 shadow-lg">
                <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
                    <div>
                        <div class="flex items-center gap-2">
                            <span class="px-2.5 py-0.5 rounded text-xs font-bold bg-rose-500/20 text-rose-300 border border-rose-500/30">MODULE 4</span>
                            <h2 class="text-lg font-bold text-white">113~128 少子化海嘯動態模擬器 (Dynamic Fertility & Policy Simulator)</h2>
                        </div>
                        <p class="text-xs text-slate-400 mt-1">
                            以教育部統計處《113至128學年度各教育階段學生數預測報告》為基準母體，透過動態互動滑桿即時模擬：少子化劇烈度、技職普高分流、考生池縮水對錄取分與進修部存活年限的連動衝擊。
                        </p>
                    </div>
                    <div class="flex items-center gap-2">
                        <button onclick="resetSimulator()" class="text-xs px-3 py-1.5 rounded-lg bg-slate-700 hover:bg-slate-600 text-slate-200 transition flex items-center gap-1">
                            <i data-lucide="rotate-ccw" class="w-3.5 h-3.5"></i>
                            重設基準參數
                        </button>
                        <button onclick="exportSimCSV()" class="text-xs px-3 py-1.5 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white font-medium transition flex items-center gap-1 shadow-sm">
                            <i data-lucide="download" class="w-3.5 h-3.5"></i>
                            匯出當前動態模擬試算表 (CSV)
                        </button>
                    </div>
                </div>

                <!-- 4 大互動控制滑桿面板 -->
                <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mt-5 p-4 rounded-xl bg-slate-900/80 border border-slate-700/70">
                    <!-- 滑桿 1：少子化衝擊係數 -->
                    <div>
                        <div class="flex justify-between items-center text-xs mb-1.5">
                            <label class="text-slate-300 font-medium">少子化劇烈度乘數</label>
                            <span id="label-slider-severity" class="text-emerald-400 font-bold font-mono">1.00x (教育部標準)</span>
                        </div>
                        <input type="range" id="slider-severity" min="0.75" max="1.25" step="0.05" value="1.00" oninput="updateSimulation()" class="w-full h-1.5 bg-slate-700 rounded-lg appearance-none cursor-pointer accent-emerald-500">
                        <div class="flex justify-between text-[10px] text-slate-500 mt-1">
                            <span>0.75x 溫和</span>
                            <span>1.00x 基準</span>
                            <span>1.25x 嚴峻海嘯</span>
                        </div>
                    </div>

                    <!-- 滑桿 2：技職考生佔比 -->
                    <div>
                        <div class="flex justify-between items-center text-xs mb-1.5">
                            <label class="text-slate-300 font-medium">技職 vs 普高分流比</label>
                            <span id="label-slider-tcte-share" class="text-cyan-400 font-bold font-mono">40.0% (逐年降至35%)</span>
                        </div>
                        <input type="range" id="slider-tcte-share" min="30" max="45" step="1" value="40" oninput="updateSimulation()" class="w-full h-1.5 bg-slate-700 rounded-lg appearance-none cursor-pointer accent-cyan-500">
                        <div class="flex justify-between text-[10px] text-slate-500 mt-1">
                            <span>30% 技職萎縮</span>
                            <span>40% 現狀</span>
                            <span>45% 技職復興</span>
                        </div>
                    </div>

                    <!-- 滑桿 3：中科商管吸附力漂移 -->
                    <div>
                        <div class="flex justify-between items-center text-xs mb-1.5">
                            <label class="text-slate-300 font-medium">中科品牌吸附力漂移</label>
                            <span id="label-slider-attraction" class="text-indigo-400 font-bold font-mono">0.0% (持平)</span>
                        </div>
                        <input type="range" id="slider-attraction" min="-15" max="15" step="1" value="0" oninput="updateSimulation()" class="w-full h-1.5 bg-slate-700 rounded-lg appearance-none cursor-pointer accent-indigo-500">
                        <div class="flex justify-between text-[10px] text-slate-500 mt-1">
                            <span>-15% 流向逢甲/北部</span>
                            <span>0% 基準</span>
                            <span>+15% 品牌擴散</span>
                        </div>
                    </div>

                    <!-- 滑桿 4：進修部衝擊彈性 -->
                    <div>
                        <div class="flex justify-between items-center text-xs mb-1.5">
                            <label class="text-slate-300 font-medium">進修部敏感彈性係數</label>
                            <span id="label-slider-eve-elasticity" class="text-rose-400 font-bold font-mono">1.80 (加速萎縮)</span>
                        </div>
                        <input type="range" id="slider-eve-elasticity" min="1.0" max="2.5" step="0.1" value="1.8" oninput="updateSimulation()" class="w-full h-1.5 bg-slate-700 rounded-lg appearance-none cursor-pointer accent-rose-500">
                        <div class="flex justify-between text-[10px] text-slate-500 mt-1">
                            <span>1.0 線性</span>
                            <span>1.8 基準加速</span>
                            <span>2.5 斷崖崩塌</span>
                        </div>
                    </div>
                </div>

                <!-- 動態模擬儀表板關鍵警報卡片 -->
                <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mt-4">
                    <div class="bg-slate-900/80 border border-slate-700 p-3.5 rounded-xl">
                        <div class="text-[11px] text-slate-400">虎年海嘯波谷 (谷底年份)</div>
                        <div class="text-lg font-black text-amber-400 mt-1 flex items-baseline gap-1">
                            117 學年度
                            <span class="text-xs font-normal text-slate-400">(2028年)</span>
                        </div>
                        <div class="text-[10px] text-slate-400 mt-0.5">大一新生全國僅 15.6 萬人 (首波大坎)</div>
                    </div>

                    <div class="bg-slate-900/80 border border-rose-500/40 p-3.5 rounded-xl">
                        <div class="text-[11px] text-rose-300 font-medium">進修四技存活倒數鐘 (跌破35%)</div>
                        <div id="sim-eve-countdown" class="text-lg font-black text-rose-400 mt-1">
                            122 學年度 (瀕危)
                        </div>
                        <div class="text-[10px] text-slate-400 mt-0.5">預估註冊率將下探至 30% 停招邊緣</div>
                    </div>

                    <div class="bg-slate-900/80 border border-slate-700 p-3.5 rounded-xl">
                        <div class="text-[11px] text-slate-400">128學年 日間錄取分預估</div>
                        <div id="sim-day-score-128" class="text-lg font-black text-emerald-400 mt-1">
                            69.38 分
                        </div>
                        <div class="text-[10px] text-slate-400 mt-0.5">守穩 60分 國立科大安全防線</div>
                    </div>

                    <div class="bg-slate-900/80 border border-slate-700 p-3.5 rounded-xl">
                        <div class="text-[11px] text-slate-400">五專部防護力狀態</div>
                        <div class="text-lg font-black text-cyan-300 mt-1">
                            極穩 (98~100%)
                        </div>
                        <div class="text-[10px] text-slate-400 mt-0.5">公立免學費+就業接軌成為防空洞</div>
                    </div>
                </div>

                <!-- 模擬動態連動折線圖 -->
                <div class="mt-6 grid grid-cols-1 lg:grid-cols-2 gap-6">
                    <!-- 圖 1：生源池與報考總數動態走勢 -->
                    <div class="bg-slate-900/80 border border-slate-700/80 rounded-xl p-4">
                        <div class="flex items-center justify-between mb-2">
                            <h4 class="text-xs font-bold text-white flex items-center gap-1.5">
                                <i data-lucide="line-chart" class="w-4 h-4 text-cyan-400"></i>
                                全國新生 vs 統測商管群 vs 中部生源池預測
                            </h4>
                            <span class="text-[10px] text-slate-400">單位：萬人 / 人</span>
                        </div>
                        <div class="relative min-h-[300px]">
                            <canvas id="chart-m4-pools"></canvas>
                        </div>
                    </div>

                    <!-- 圖 2：日間錄取分數 vs 進修部註冊率走勢 -->
                    <div class="bg-slate-900/80 border border-slate-700/80 rounded-xl p-4">
                        <div class="flex items-center justify-between mb-2">
                            <h4 class="text-xs font-bold text-white flex items-center gap-1.5">
                                <i data-lucide="trending-down" class="w-4 h-4 text-rose-400"></i>
                                日間四技錄取分 (分) vs 進修四技註冊率 (%)
                            </h4>
                            <span class="text-[10px] text-slate-400">雙軸預警模擬</span>
                        </div>
                        <div class="relative min-h-[300px]">
                            <canvas id="chart-m4-outcomes"></canvas>
                        </div>
                    </div>
                </div>

                <!-- 動態模擬即時數據明細表 (隨滑桿連動) -->
                <div class="mt-6 bg-slate-900/80 border border-slate-700/80 rounded-xl p-4">
                    <h4 class="text-xs font-bold text-white flex items-center gap-1.5 mb-3">
                        <i data-lucide="calendar" class="w-4 h-4 text-emerald-400"></i>
                        113~128 學年度少子化預測與模擬明細表 (隨滑桿即時連動)
                    </h4>
                    <div class="overflow-x-auto max-h-[360px] custom-scrollbar border border-slate-800 rounded-lg">
                        <table class="w-full text-left text-xs border-collapse">
                            <thead class="bg-slate-950 text-slate-400 sticky top-0 border-b border-slate-800 font-semibold">
                                <tr>
                                    <th class="p-2.5">學年度</th>
                                    <th class="p-2.5 text-right">大一新生總數</th>
                                    <th class="p-2.5 text-right">統測報考總數</th>
                                    <th class="p-2.5 text-right">商管群考生池</th>
                                    <th class="p-2.5 text-right">中部生源池</th>
                                    <th class="p-2.5 text-right">日間錄取均分</th>
                                    <th class="p-2.5 text-right">進修四技註冊率</th>
                                    <th class="p-2.5">五專部防護力</th>
                                </tr>
                            </thead>
                            <tbody id="m4-sim-table-body" class="divide-y divide-slate-800/80">
                                <!-- 動態填入 -->
                            </tbody>
                        </table>
                    </div>
                </div>

                <!-- 動態決策建議行動方案 -->
                <div class="mt-4 p-4 rounded-xl bg-slate-900/60 border border-slate-800 text-xs text-slate-300 space-y-2">
                    <div class="font-bold text-white flex items-center gap-2">
                        <i data-lucide="shield-check" class="w-4 h-4 text-emerald-400"></i>
                        少子化防禦工程決策推演：
                    </div>
                    <ul class="list-disc pl-5 space-y-1 text-slate-300">
                        <li><strong class="text-white">進修四技退場/轉型倒數：</strong>進修四技註冊率預估在 120~122 年跌入 35% 停招深水區。建議於 116 年前主動將進修部員額轉化為「產學攜手專班 2.0」或「東南亞高階外加專班」，避免註冊率拉低全校評鑑。</li>
                        <li><strong class="text-white">擴大五專部護城河：</strong>中科大五專部防護力維持 98~100%，建議向教育部申請增設「五專國際雙語商務專班」，鎖定國中前 15% 優秀生源，提早綁定 5 年穩定在學生源。</li>
                        <li><strong class="text-white">守衛日間 70 分門檻：</strong>當中部生源池從 3,080 人萎縮至 2,464 人時，日間部需主動強化高中生申請入學管道名額，擴大學測生源搶奪。</li>
                    </ul>
                </div>
            </div>
        </section>

        <!-- =============================================================== -->
        <!-- 模組 5：師資換血與五年轉型決策戰情室 -->
        <!-- =============================================================== -->
        <section id="module5" class="tab-content hidden space-y-6">
            <div class="bg-slate-800/60 border border-slate-700/70 rounded-2xl p-5 shadow-lg">
                <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
                    <div>
                        <div class="flex items-center gap-2">
                            <span class="px-2.5 py-0.5 rounded text-xs font-bold bg-purple-500/20 text-purple-300 border border-purple-500/30">MODULE 5</span>
                            <h2 class="text-lg font-bold text-white">師資換血與五年轉型決策戰情室 (Faculty & Strategic Transformation)</h2>
                        </div>
                        <p class="text-xs text-slate-400 mt-1">
                            針對中科國貿 21 位專任師資（4位正教授、14位副教授、3位助理教授）進行高齡換血模擬，推演 115~120 年退休時程、新聘專長缺口矩陣與五年課程轉型配比。
                        </p>
                    </div>
                </div>

                <!-- 師資梯隊與未來 6 年退休潮時程表 -->
                <div class="mt-5 grid grid-cols-1 lg:grid-cols-3 gap-6">
                    <!-- 師資年齡與職級現況 -->
                    <div class="bg-slate-900/80 border border-slate-700/80 rounded-xl p-4 flex flex-col justify-between">
                        <div>
                            <h4 class="text-xs font-bold text-white flex items-center gap-1.5 mb-2">
                                <i data-lucide="pie-chart" class="w-4 h-4 text-purple-400"></i>
                                專任師資職級階梯 (現有 21 人)
                            </h4>
                            <div class="relative min-h-[220px]">
                                <canvas id="chart-m5-faculty"></canvas>
                            </div>
                        </div>
                        <div class="text-[11px] text-purple-300/90 bg-purple-500/10 p-2.5 rounded-lg border border-purple-500/20 mt-2">
                            副教授佔比高達 66.7% (14人)，為歷史高位。未來數年應鼓勵副教授加速升等，同時預備屆齡退休員額之遞補。
                        </div>
                    </div>

                    <!-- 115~120 年預估退休名額時程甘特表 -->
                    <div class="lg:col-span-2 bg-slate-900/80 border border-slate-700/80 rounded-xl p-4">
                        <h4 class="text-xs font-bold text-white flex items-center gap-1.5 mb-2">
                            <i data-lucide="calendar" class="w-4 h-4 text-amber-400"></i>
                            未來 6 年（115~120學年度）師資退休換血時程預估 (共釋出約 8 名額)
                        </h4>
                        <div class="space-y-2 mt-3" id="m5-retire-list">
                            <!-- 動態填入 -->
                        </div>
                    </div>
                </div>

                <!-- 新聘師資專長缺口矩陣表 -->
                <div class="mt-6 bg-slate-900/80 border border-slate-700/80 rounded-xl p-4">
                    <h4 class="text-xs font-bold text-white flex items-center gap-1.5 mb-3">
                        <i data-lucide="user-plus" class="w-4 h-4 text-emerald-400"></i>
                        新聘師資專長需求矩陣 (Faculty Recruitment Skill Matrix)
                    </h4>
                    <div class="overflow-x-auto">
                        <table class="w-full text-left text-xs">
                            <thead class="bg-slate-800/90 text-slate-300 font-semibold border-b border-slate-700">
                                <tr>
                                    <th class="p-3">領域方向</th>
                                    <th class="p-3">急迫性</th>
                                    <th class="p-3">核心關鍵專長需求</th>
                                    <th class="p-3">建議名額</th>
                                    <th class="p-3">評估效應</th>
                                </tr>
                            </thead>
                            <tbody class="divide-y divide-slate-800 text-slate-300">
                                <tr class="hover:bg-slate-800/40">
                                    <td class="p-3 font-bold text-emerald-400">AI 跨境電商與智慧數位行銷</td>
                                    <td class="p-3"><span class="px-2 py-0.5 rounded bg-rose-500/20 text-rose-300 font-bold">極高急迫 (★★★★★)</span></td>
                                    <td class="p-3">生成式 AI 跨境營銷、Amazon/TikTok Shop 運營、SEO 與跨境金流</td>
                                    <td class="p-3 font-bold text-white">2~3 名</td>
                                    <td class="p-3 text-slate-400">挽救大一休退學率，打造就業護城河</td>
                                </tr>
                                <tr class="hover:bg-slate-800/40">
                                    <td class="p-3 font-bold text-cyan-400">ESG 永續貿易與歐盟碳關稅 (CBAM)</td>
                                    <td class="p-3"><span class="px-2 py-0.5 rounded bg-rose-500/20 text-rose-300 font-bold">極高急迫 (★★★★★)</span></td>
                                    <td class="p-3">歐盟 CBAM 申報、供應鏈碳盤查、綠色物流與國際 ESG 貿易法規</td>
                                    <td class="p-3 font-bold text-white">1~2 名</td>
                                    <td class="p-3 text-slate-400">拓展高額產學合作案與企業顧問</td>
                                </tr>
                                <tr class="hover:bg-slate-800/40">
                                    <td class="p-3 font-bold text-indigo-400">經貿巨量資料與 Python 商業智慧</td>
                                    <td class="p-3"><span class="px-2 py-0.5 rounded bg-amber-500/20 text-amber-300 font-bold">高度急迫 (★★★★☆)</span></td>
                                    <td class="p-3">全球海關提單大數據分析、進出口預測模型、Tableau / Power BI</td>
                                    <td class="p-3 font-bold text-white">1 名</td>
                                    <td class="p-3 text-slate-400">銜接高科技業經貿分析師人才缺口</td>
                                </tr>
                                <tr class="hover:bg-slate-800/40">
                                    <td class="p-3 font-bold text-purple-400">全英語 (EMI) 國際談判與地緣政治</td>
                                    <td class="p-3"><span class="px-2 py-0.5 rounded bg-purple-500/20 text-purple-300 font-bold">必備基礎 (★★★★★)</span></td>
                                    <td class="p-3">美中地緣經貿脫鉤談判、CPTPP 與印太架構、全英專業講授</td>
                                    <td class="p-3 font-bold text-white">既有升級+新聘</td>
                                    <td class="p-3 text-slate-400">吸引外籍生、提升國際化指標</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>

                <!-- 課程五年配比重組路徑 + 評鑑戰力雷達 -->
                <div class="mt-6 grid grid-cols-1 lg:grid-cols-2 gap-6">
                    <!-- 課程轉型配比長條圖 (114現況 vs 119目標) -->
                    <div class="bg-slate-900/80 border border-slate-700/80 rounded-xl p-4">
                        <div class="flex items-center justify-between mb-3">
                            <h4 class="text-xs font-bold text-white flex items-center gap-1.5">
                                <i data-lucide="book-open" class="w-4 h-4 text-emerald-400"></i>
                                五年課程架構重組配比 (114現況 vs 119目標)
                            </h4>
                            <span class="text-[10px] text-slate-400">學分佔比 (%)</span>
                        </div>
                        <div class="relative min-h-[300px]">
                            <canvas id="chart-m5-curriculum"></canvas>
                        </div>
                    </div>

                    <!-- 評鑑與轉型 KPI 雷達 -->
                    <div class="bg-slate-900/80 border border-slate-700/80 rounded-xl p-4">
                        <div class="flex items-center justify-between mb-3">
                            <h4 class="text-xs font-bold text-white flex items-center gap-1.5">
                                <i data-lucide="award" class="w-4 h-4 text-cyan-400"></i>
                                系所評鑑與永續戰力雷達 (現況 vs 五年願景)
                            </h4>
                            <span class="text-[10px] text-slate-400">目標得分 (滿分100)</span>
                        </div>
                        <div class="relative min-h-[300px]">
                            <canvas id="chart-m5-radar"></canvas>
                        </div>
                    </div>
                </div>
            </div>
        </section>

    </main>

    <!-- 架構設計規格書 Modal (Specification Drawer) -->
    <div id="spec-modal" class="fixed inset-0 bg-slate-950/80 backdrop-blur-sm z-50 hidden flex items-center justify-center p-4 no-print">
        <div class="bg-slate-900 border border-slate-700 rounded-2xl max-w-4xl w-full max-h-[90vh] flex flex-col shadow-2xl overflow-hidden">
            <div class="p-5 border-b border-slate-800 flex items-center justify-between bg-slate-850">
                <div class="flex items-center gap-2">
                    <div class="p-2 rounded-lg bg-emerald-500/10 text-emerald-400">
                        <i data-lucide="file-text" class="w-5 h-5"></i>
                    </div>
                    <div>
                        <h3 class="text-base font-bold text-white">戰情室架構設計與人物誌規格書 (Architecture Specification)</h3>
                        <p class="text-xs text-slate-400">中科大國貿系「少子化海嘯」系務策略發展與動態決策戰情室</p>
                    </div>
                </div>
                <button onclick="closeSpecModal()" class="text-slate-400 hover:text-white p-1 rounded-lg hover:bg-slate-800 transition">
                    <i data-lucide="x" class="w-5 h-5"></i>
                </button>
            </div>
            <div class="p-6 overflow-y-auto space-y-5 text-xs text-slate-300 custom-scrollbar leading-relaxed">
                <div>
                    <h4 class="text-sm font-bold text-emerald-400 mb-1.5">一、目標使用者人物誌分析 (Target Persona Analysis)</h4>
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
                        <div class="p-3 rounded-xl bg-slate-800/80 border border-slate-700">
                            <strong class="text-white">主責使用者：Dr. Elvis Chen (陳俊智副教授)</strong>
                            <p class="text-slate-400 mt-1">國立臺中科技大學 國際貿易與經營系 資深學者，主持系務策略發展、校務研究 (IR) 及少子化避險轉型工程。需具備精確數值佐證之動態模型以說服系所同仁與校級決策層。</p>
                        </div>
                        <div class="p-3 rounded-xl bg-slate-800/80 border border-slate-700">
                            <strong class="text-white">次要利害關係人：系主任、課程委員會、教評會委員</strong>
                            <p class="text-slate-400 mt-1">需於系務會議中快速調閱全台競合雷達、掌握退學流失深水區原因，並在教評會新聘師資審查時確認專長與未來 5 年退休潮無縫對接。</p>
                        </div>
                    </div>
                </div>

                <div>
                    <h4 class="text-sm font-bold text-cyan-400 mb-1.5">二、5 大核心互動駕駛艙模組設計 (5 Cockpit Modules)</h4>
                    <ol class="list-decimal pl-5 space-y-1.5 text-slate-300">
                        <li><strong>模組 1（北中南六強旗盤）：</strong>北商國商、中科國貿、雲科國管、高科航管/國企/供應鏈，橫向對比 12 項官方硬指標，揭示中科規模第一但退學率居冠之體質特徵。</li>
                        <li><strong>模組 2（中部大專商管大亂鬥）：</strong>對壘逢甲、東海、嶺東、朝陽、虎科，比較公私立定價優勢、普高學測吸磁、主動減招防禦、現金存量與進修部存亡戰。</li>
                        <li><strong>模組 3（系所體質深度診斷）：</strong>中科國貿 vs 中科企管 6年統測走勢（114年國貿以 71.78分首度反超企管 71.73分），並切入 80人退學深水區（24人因科系不符期待）。</li>
                        <li><strong>模組 4（少子化海嘯動態模擬器）：</strong>113~128 年教育部預測連動 4 支動態滑桿，即時推演 117 虎年波谷、進修四技 122 年瀕臨停招與日間錄取分底線。</li>
                        <li><strong>模組 5（師資換血與五年轉型）：</strong>21 位專任師資（副教授 66.7%）未來 6 年 8 名退休潮排程、AI跨境電商/ESG/Python 數據新聘矩陣與課程五大配比改革。</li>
                    </ol>
                </div>

                <div>
                    <h4 class="text-sm font-bold text-indigo-400 mb-1.5">三、數據管線與零依賴離線部署 (Data Pipeline & Zero-Dependency)</h4>
                    <p>
                        本戰情室採用完全自包含（Self-contained）單一檔案架構，所有實證數據直接編譯入內建 JSON 結構中。可直接雙擊開啟用任何現代瀏覽器執行，零後端伺服器依賴、零資料庫組建成本，隨附 <code class="text-emerald-300 bg-slate-800 px-1 py-0.5 rounded">build_dashboard.py</code> 支援一鍵重編與延伸更新。
                    </p>
                </div>
            </div>
            <div class="p-4 border-t border-slate-800 bg-slate-850 flex justify-end">
                <button onclick="closeSpecModal()" class="px-4 py-2 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white font-medium text-xs transition">
                    關閉規格書
                </button>
            </div>
        </div>
    </div>

    <!-- 底部 Footer -->
    <footer class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 border-t border-slate-800/80 text-xs text-slate-500 flex flex-col sm:flex-row items-center justify-between gap-3 no-print">
        <div>
            國立臺中科技大學 國際貿易與經營系 (NUTC ITM) 策略研究室 © 2026
        </div>
        <div class="flex items-center space-x-4">
            <span>資料校對：114 學年度</span>
            <span>系統版本：v3.2.0 Executive Edition</span>
            <span class="text-emerald-400 font-semibold">Dr. Elvis Chen</span>
        </div>
    </footer>

    <!-- 內嵌全域實證資料庫與戰情室交互運算邏輯 -->
    <script>
        const DB = {json_str};

        // 全域圖表物件快取
        let charts = {{}};

        // 初始化戰情室
        document.addEventListener('DOMContentLoaded', () => {{
            if (window.lucide && typeof lucide.createIcons === 'function') {{
                lucide.createIcons();
            }}
            applyRegionalFilters();
            renderModule3Matrix();
            renderModule5Retire();
            
            if (typeof Chart !== 'undefined') {{
                initModule1Charts();
                initModule2Charts();
                initModule3Charts();
                initModule4Charts();
                initModule5Charts();
            }} else {{
                console.warn('Chart.js CDN unavailable. Running in data tables/cards fallback mode.');
                const banner = document.getElementById('offline-notice-banner');
                if (banner) banner.classList.remove('hidden');
            }}
            updateSimulation();
        }});

        // Tab 切換邏輯
        function switchTab(moduleId) {{
            document.querySelectorAll('.tab-content').forEach(el => {{
                el.classList.add('hidden');
                el.classList.remove('block');
            }});
            
            document.querySelectorAll('.tab-btn').forEach(btn => {{
                btn.classList.remove('border-emerald-500', 'text-emerald-400');
                btn.classList.add('border-transparent', 'text-slate-400');
            }});

            const targetContent = document.getElementById(moduleId);
            if (targetContent) {{
                targetContent.classList.remove('hidden');
                targetContent.classList.add('block');
            }}

            const targetBtn = document.getElementById('tab-btn-' + moduleId);
            if (targetBtn) {{
                targetBtn.classList.remove('border-transparent', 'text-slate-400');
                targetBtn.classList.add('border-emerald-500', 'text-emerald-400');
            }}

            requestAnimationFrame(() => {{
                if (typeof Chart !== 'undefined') {{
                    const activeCanvases = document.querySelectorAll('#' + moduleId + ' canvas');
                    activeCanvases.forEach(canvas => {{
                        const chartInstance = Chart.getChart(canvas);
                        if (chartInstance) chartInstance.resize();
                    }});
                }}
            }});
        }}

        // Modal 控制
        function openSpecModal() {{
            document.getElementById('spec-modal').classList.remove('hidden');
        }}
        function closeSpecModal() {{
            document.getElementById('spec-modal').classList.add('hidden');
        }}

        // ==========================================
        // 模組 1 繪製邏輯 (支援篩選與多維度排序)
        // ==========================================
        function applyRegionalFilters() {{
            const regionVal = document.getElementById('m1-region-filter').value;
            const sortVal = document.getElementById('m1-sort-by').value;

            let list = [...DB.regional_six];
            if (regionVal !== 'ALL') {{
                list = list.filter(x => x.region === regionVal);
            }}

            if (sortVal === 'total_stu_desc') {{
                list.sort((a, b) => b.total_stu - a.total_stu);
            }} else if (sortVal === 'score_114_desc') {{
                list.sort((a, b) => b.score_114 - a.score_114);
            }} else if (sortVal === 'drop_rate_asc') {{
                list.sort((a, b) => a.drop_rate_113 - b.drop_rate_113);
            }} else if (sortVal === 'oversea_pct_desc') {{
                list.sort((a, b) => b.oversea_pct - a.oversea_pct);
            }}

            renderRegionalTable(list);
        }}

        function renderRegionalTable(dataList) {{
            const tbody = document.getElementById('regional-table-body');
            tbody.innerHTML = '';

            dataList.forEach(item => {{
                const isNUTC = item.code.includes('中科');
                const row = document.createElement('tr');
                row.className = isNUTC 
                    ? "bg-emerald-950/30 font-semibold border-l-4 border-emerald-500 hover:bg-emerald-900/40 transition" 
                    : "hover:bg-slate-800/40 transition";
                
                const deltaClass = item.score_delta >= 0 ? "text-emerald-400" : "text-rose-400";
                const deltaSign = item.score_delta > 0 ? "+" : "";

                row.innerHTML = `
                    <td class="p-3">
                        <div class="font-bold text-white flex items-center gap-1.5">
                            ${{item.code}}
                            ${{isNUTC ? '<span class="px-1.5 py-0.5 rounded text-[10px] bg-emerald-500/20 text-emerald-300 font-bold">本系</span>' : ''}}
                        </div>
                        <div class="text-[11px] text-slate-400 mt-0.5">${{item.school}} ${{item.dept}}</div>
                    </td>
                    <td class="p-3"><span class="px-2 py-0.5 rounded text-[10px] bg-slate-800 text-slate-300">${{item.region}}</span></td>
                    <td class="p-3 text-right font-mono font-bold text-white">${{item.total_stu.toLocaleString()}}</td>
                    <td class="p-3 text-right font-mono text-slate-300">${{item.five_year > 0 ? item.five_year : '--'}}</td>
                    <td class="p-3 text-right font-mono text-slate-300">${{item.undergrad_day}}</td>
                    <td class="p-3 text-right font-mono text-slate-300">${{item.undergrad_eve}}</td>
                    <td class="p-3 text-right font-mono text-slate-300">${{item.grad > 0 ? item.grad : '0'}}</td>
                    <td class="p-3 text-slate-300">${{item.faculty_total}}人 (${{item.faculty_prof}}/${{item.faculty_assoc}}/${{item.faculty_asst}})</td>
                    <td class="p-3 text-right text-slate-300">${{item.oversea_stu}}人 <span class="text-[10px] text-slate-400">(${{item.oversea_pct.toFixed(1)}}%)</span></td>
                    <td class="p-3 text-right font-mono font-bold ${{item.reg_114_rate >= 99.0 ? 'text-emerald-400' : 'text-amber-400'}}">${{item.reg_114_rate.toFixed(2)}}%</td>
                    <td class="p-3 text-right font-mono font-bold text-cyan-300">
                        ${{item.score_114.toFixed(2)}}分
                        <span class="text-[10px] block ${{deltaClass}} font-normal">${{deltaSign}}${{item.score_delta.toFixed(2)}}</span>
                    </td>
                    <td class="p-3 text-right font-mono font-bold ${{item.drop_rate_113 >= 3.5 ? 'text-rose-400' : 'text-slate-300'}}">
                        ${{item.drop_rate_113.toFixed(2)}}%
                        <span class="text-[10px] block text-slate-400 font-normal">(${{item.drop_cnt_113}}人)</span>
                    </td>
                `;
                tbody.appendChild(row);
            }});
        }}

        function initModule1Charts() {{
            const ctxRadar = document.getElementById('chart-m1-radar').getContext('2d');
            charts.m1Radar = new Chart(ctxRadar, {{
                type: 'radar',
                data: {{
                    labels: ['生源吸附力 (錄取分)', '規模抗震度 (在學生)', '國際化深度 (境外生)', '註冊穩定度 (日間註冊)', '留存防禦力 (100-退學)'],
                    datasets: [
                        {{
                            label: '中科-國貿 (本系)',
                            data: DB.regional_six.find(x => x.code === '中科-國貿').radar,
                            borderColor: '#10b981',
                            backgroundColor: 'rgba(16, 185, 129, 0.25)',
                            borderWidth: 2.5,
                            pointBackgroundColor: '#10b981'
                        }},
                        {{
                            label: '北商-國商',
                            data: DB.regional_six.find(x => x.code === '北商-國商').radar,
                            borderColor: '#6366f1',
                            backgroundColor: 'rgba(99, 102, 241, 0.15)',
                            borderWidth: 1.5,
                            borderDash: [4, 4]
                        }},
                        {{
                            label: '雲科-國管',
                            data: DB.regional_six.find(x => x.code === '雲科-國管').radar,
                            borderColor: '#f59e0b',
                            backgroundColor: 'rgba(245, 158, 11, 0.15)',
                            borderWidth: 1.5,
                            borderDash: [2, 2]
                        }},
                        {{
                            label: '高科-航管',
                            data: DB.regional_six.find(x => x.code === '高科-航管').radar,
                            borderColor: '#06b6d4',
                            backgroundColor: 'rgba(6, 182, 212, 0.12)',
                            borderWidth: 1.5
                        }}
                    ]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {{
                        r: {{
                            angleLines: {{ color: 'rgba(255, 255, 255, 0.1)' }},
                            grid: {{ color: 'rgba(255, 255, 255, 0.08)' }},
                            pointLabels: {{ color: '#cbd5e1', font: {{ size: 11 }} }},
                            suggestedMin: 0,
                            suggestedMax: 100,
                            ticks: {{ display: false }}
                        }}
                    }},
                    plugins: {{
                        legend: {{
                            position: 'bottom',
                            labels: {{ color: '#cbd5e1', font: {{ size: 11 }}, boxWidth: 12 }}
                        }}
                    }}
                }}
            }});

            const ctxScatter = document.getElementById('chart-m1-scatter').getContext('2d');
            const scatterPoints = DB.regional_six.map(x => ({{
                x: x.score_114,
                y: x.reg_114_rate,
                r: Math.sqrt(x.total_stu) * 0.9,
                label: x.code,
                total: x.total_stu
            }}));

            charts.m1Scatter = new Chart(ctxScatter, {{
                type: 'bubble',
                data: {{
                    datasets: scatterPoints.map(p => ({{
                        label: p.label,
                        data: [p],
                        backgroundColor: p.label.includes('中科') ? 'rgba(16, 185, 129, 0.75)' : 'rgba(99, 102, 241, 0.5)',
                        borderColor: p.label.includes('中科') ? '#10b981' : '#818cf8',
                        borderWidth: p.label.includes('中科') ? 3 : 1.5
                    }}))
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {{
                        x: {{
                            title: {{ display: true, text: '114學年 統測商管最低錄取單科均分 (分)', color: '#94a3b8', font: {{ size: 11 }} }},
                            grid: {{ color: 'rgba(255, 255, 255, 0.08)' }},
                            ticks: {{ color: '#cbd5e1' }},
                            min: 64,
                            max: 82
                        }},
                        y: {{
                            title: {{ display: true, text: '114學年 日間四技註冊率 (%)', color: '#94a3b8', font: {{ size: 11 }} }},
                            grid: {{ color: 'rgba(255, 255, 255, 0.08)' }},
                            ticks: {{ color: '#cbd5e1' }},
                            min: 94,
                            max: 101
                        }}
                    }},
                    plugins: {{
                        legend: {{
                            position: 'bottom',
                            labels: {{ color: '#cbd5e1', font: {{ size: 11 }}, boxWidth: 10 }}
                        }},
                        tooltip: {{
                            callbacks: {{
                                label: function(context) {{
                                    const raw = context.raw;
                                    return `${{raw.label}}: 均分 ${{raw.x.toFixed(2)}}分 | 註冊率 ${{raw.y.toFixed(2)}}% | 在學生 ${{raw.total}}人`;
                                }}
                            }}
                        }}
                    }}
                }}
            }});
        }}

        // ==========================================
        // 模組 2 繪製邏輯
        // ==========================================
        function initModule2Charts() {{
            const comps = DB.central_competitors;
            const labels = comps.map(c => c.school);

            const ctxBars = document.getElementById('chart-m2-bars').getContext('2d');
            charts.m2Bars = new Chart(ctxBars, {{
                type: 'bar',
                data: {{
                    labels: labels,
                    datasets: [
                        {{
                            label: '114 日間四技註冊率 (%)',
                            data: comps.map(c => c.reg_114_day),
                            backgroundColor: comps.map(c => c.school.includes('中科') ? '#10b981' : (c.reg_114_day < 60 ? '#f43f5e' : '#38bdf8')),
                            borderRadius: 6
                        }},
                        {{
                            label: '113 退學流失率 (%)',
                            data: comps.map(c => c.drop_rate),
                            backgroundColor: 'rgba(251, 146, 60, 0.8)',
                            borderRadius: 6
                        }}
                    ]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {{
                        x: {{ ticks: {{ color: '#cbd5e1', font: {{ size: 11 }} }}, grid: {{ display: false }} }},
                        y: {{ ticks: {{ color: '#cbd5e1' }}, grid: {{ color: 'rgba(255, 255, 255, 0.08)' }}, max: 105 }}
                    }},
                    plugins: {{
                        legend: {{ position: 'bottom', labels: {{ color: '#cbd5e1', font: {{ size: 11 }} }} }}
                    }}
                }}
            }});

            const ctxFin = document.getElementById('chart-m2-finance').getContext('2d');
            charts.m2Finance = new Chart(ctxFin, {{
                type: 'scatter',
                data: {{
                    datasets: comps.map(c => ({{
                        label: c.school,
                        data: [{{
                            x: c.score_cutoff,
                            y: c.reg_114_day,
                            reserve: c.cash_reserve,
                            tuition: c.tuition_per_sem,
                            mix: c.source_mix,
                            note: c.strategy_label
                        }}],
                        backgroundColor: c.school.includes('中科') ? '#10b981' : (c.reg_114_day < 60 ? '#f43f5e' : '#a855f7'),
                        pointRadius: c.school.includes('中科') ? 11 : 8,
                        pointHoverRadius: 13
                    }}))
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {{
                        x: {{
                            title: {{ display: true, text: '錄取門檻折合分數估值 (分)', color: '#94a3b8' }},
                            ticks: {{ color: '#cbd5e1' }},
                            grid: {{ color: 'rgba(255, 255, 255, 0.08)' }},
                            suggestedMin: 48,
                            suggestedMax: 78
                        }},
                        y: {{
                            title: {{ display: true, text: '114 日間部註冊率 (%)', color: '#94a3b8' }},
                            ticks: {{ color: '#cbd5e1' }},
                            grid: {{ color: 'rgba(255, 255, 255, 0.08)' }},
                            suggestedMin: 45,
                            suggestedMax: 105
                        }}
                    }},
                    plugins: {{
                        legend: {{ position: 'bottom', labels: {{ color: '#cbd5e1', font: {{ size: 10 }} }} }},
                        tooltip: {{
                            callbacks: {{
                                label: function(context) {{
                                    const raw = context.raw;
                                    return [
                                        `${{context.dataset.label}} (門檻均分: ${{raw.x}}分 | 日間註冊率: ${{raw.y}}%)`,
                                        `資金護城河: ${{raw.reserve}}`,
                                        `每期學費: ${{raw.tuition}}`,
                                        `生源結構: ${{raw.mix}}`,
                                        `戰略特徵: ${{raw.note}}`
                                    ];
                                }}
                            }}
                        }}
                    }}
                }}
            }});
        }}

        // ==========================================
        // 模組 3 繪製邏輯 (支援動態顯隱按鈕)
        // ==========================================
        function initModule3Charts() {{
            const trends = DB.score_trends;
            const ctxTrend = document.getElementById('chart-m3-score-trend').getContext('2d');

            const colors = {{
                '中科大國貿': '#10b981',
                '中科大企管': '#06b6d4',
                '雲科大企管': '#f59e0b',
                '北商大國商': '#6366f1',
                '北商大企管': '#a855f7',
                '勤益企管':   '#64748b',
                '虎科財金':   '#f43f5e'
            }};

            const datasets = Object.keys(trends.departments).map((dept, idx) => {{
                const isITM = dept === '中科大國貿';
                const isBA = dept === '中科大企管';
                return {{
                    label: dept,
                    data: trends.departments[dept],
                    borderColor: colors[dept] || '#cbd5e1',
                    backgroundColor: colors[dept] || '#cbd5e1',
                    borderWidth: isITM ? 3.5 : (isBA ? 2.5 : 1.5),
                    pointRadius: isITM ? 6 : 4,
                    pointHoverRadius: 8,
                    borderDash: (isITM || isBA) ? [] : [4, 4],
                    tension: 0.25,
                    hidden: false
                }};
            }});

            charts.m3Trend = new Chart(ctxTrend, {{
                type: 'line',
                data: {{
                    labels: trends.years.map(y => y + '學年度'),
                    datasets: datasets
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {{
                        x: {{ ticks: {{ color: '#cbd5e1', font: {{ size: 12 }} }}, grid: {{ color: 'rgba(255, 255, 255, 0.05)' }} }},
                        y: {{
                            title: {{ display: true, text: '最低錄取折合單科均分 (分)', color: '#94a3b8' }},
                            ticks: {{ color: '#cbd5e1' }},
                            grid: {{ color: 'rgba(255, 255, 255, 0.08)' }},
                            min: 60,
                            max: 88
                        }}
                    }},
                    plugins: {{
                        legend: {{
                            position: 'bottom',
                            labels: {{ color: '#cbd5e1', font: {{ size: 11 }}, boxWidth: 14 }}
                        }},
                        tooltip: {{
                            mode: 'index',
                            intersect: false
                        }}
                    }}
                }}
            }});

            // 建立動態切換按鈕
            const toggleContainer = document.getElementById('score-trend-toggles');
            toggleContainer.innerHTML = '';
            datasets.forEach((ds, i) => {{
                const btn = document.createElement('button');
                btn.className = 'px-2 py-1 rounded text-[11px] font-medium border border-slate-700 bg-slate-800 text-slate-300 hover:text-white transition flex items-center gap-1';
                btn.innerHTML = `<span class="w-2 h-2 rounded-full" style="background-color: ${{ds.borderColor}}"></span> ${{ds.label}}`;
                btn.onclick = () => {{
                    const meta = charts.m3Trend.getDatasetMeta(i);
                    meta.hidden = meta.hidden === null ? !charts.m3Trend.data.datasets[i].hidden : null;
                    btn.classList.toggle('opacity-40');
                    charts.m3Trend.update();
                }};
                toggleContainer.appendChild(btn);
            }});
        }}

        function renderModule3Matrix() {{
            const tbody = document.getElementById('m3-reg-matrix-body');
            if (!tbody) return;
            tbody.innerHTML = '';

            DB.itm_vs_ba_deep.registration_matrix.forEach(r => {{
                const tr = document.createElement('tr');
                tr.className = 'hover:bg-slate-800/40 transition';
                tr.innerHTML = `
                    <td class="p-3 font-bold text-white">${{r.prog}}</td>
                    <td class="p-3 text-slate-300 font-mono">${{r.itm_113}}</td>
                    <td class="p-3 font-mono font-bold ${{r.itm_114.includes('50.91') ? 'text-rose-400' : 'text-emerald-400'}}">${{r.itm_114}}</td>
                    <td class="p-3 text-slate-300 font-mono">${{r.ba_113}}</td>
                    <td class="p-3 font-mono font-bold text-cyan-300">${{r.ba_114}}</td>
                    <td class="p-3 text-[11px] text-slate-400">${{r.diff}}</td>
                `;
                tbody.appendChild(tr);
            }});
        }}

        // ==========================================
        // 模組 4 模擬器動態連動
        // ==========================================
        function initModule4Charts() {{
            const ctxPools = document.getElementById('chart-m4-pools').getContext('2d');
            charts.m4Pools = new Chart(ctxPools, {{
                type: 'line',
                data: {{
                    labels: DB.fertility_timeline.map(x => x.yr + '年'),
                    datasets: [
                        {{
                            label: '大一新生總數 (萬人)',
                            data: DB.fertility_timeline.map(x => x.fresh),
                            borderColor: '#38bdf8',
                            yAxisID: 'yLeft',
                            tension: 0.2
                        }},
                        {{
                            label: '統測報考總數 (萬人)',
                            data: DB.fertility_timeline.map(x => x.tcte),
                            borderColor: '#818cf8',
                            yAxisID: 'yLeft',
                            borderDash: [3, 3],
                            tension: 0.2
                        }},
                        {{
                            label: '中部商管生源池 (人)',
                            data: DB.fertility_timeline.map(x => x.pool),
                            borderColor: '#10b981',
                            backgroundColor: 'rgba(16, 185, 129, 0.15)',
                            fill: true,
                            yAxisID: 'yRight',
                            tension: 0.2
                        }}
                    ]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {{
                        x: {{ ticks: {{ color: '#cbd5e1' }}, grid: {{ display: false }} }},
                        yLeft: {{
                            type: 'linear',
                            position: 'left',
                            title: {{ display: true, text: '萬人', color: '#94a3b8' }},
                            ticks: {{ color: '#cbd5e1' }},
                            grid: {{ color: 'rgba(255, 255, 255, 0.05)' }}
                        }},
                        yRight: {{
                            type: 'linear',
                            position: 'right',
                            title: {{ display: true, text: '中部生源人數', color: '#94a3b8' }},
                            ticks: {{ color: '#cbd5e1' }},
                            grid: {{ display: false }}
                        }}
                    }},
                    plugins: {{
                        legend: {{ position: 'bottom', labels: {{ color: '#cbd5e1', font: {{ size: 10 }} }} }}
                    }}
                }}
            }});

            const ctxOutcomes = document.getElementById('chart-m4-outcomes').getContext('2d');
            charts.m4Outcomes = new Chart(ctxOutcomes, {{
                type: 'line',
                data: {{
                    labels: DB.fertility_timeline.map(x => x.yr + '年'),
                    datasets: [
                        {{
                            label: '日間四技錄取單科均分 (分)',
                            data: DB.fertility_timeline.map(x => x.day_score),
                            borderColor: '#10b981',
                            borderWidth: 2.5,
                            yAxisID: 'yScore',
                            tension: 0.2
                        }},
                        {{
                            label: '進修四技新生註冊率 (%)',
                            data: DB.fertility_timeline.map(x => x.eve_rate),
                            borderColor: '#f43f5e',
                            borderWidth: 2.5,
                            borderDash: [4, 4],
                            yAxisID: 'yRate',
                            tension: 0.2
                        }}
                    ]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {{
                        x: {{ ticks: {{ color: '#cbd5e1' }}, grid: {{ display: false }} }},
                        yScore: {{
                            type: 'linear',
                            position: 'left',
                            title: {{ display: true, text: '錄取均分 (分)', color: '#10b981' }},
                            ticks: {{ color: '#10b981' }},
                            suggestedMin: 55,
                            suggestedMax: 78,
                            grid: {{ color: 'rgba(255, 255, 255, 0.05)' }}
                        }},
                        yRate: {{
                            type: 'linear',
                            position: 'right',
                            title: {{ display: true, text: '進修註冊率 (%)', color: '#f43f5e' }},
                            ticks: {{ color: '#f43f5e' }},
                            suggestedMin: 0,
                            suggestedMax: 85,
                            grid: {{ display: false }}
                        }}
                    }},
                    plugins: {{
                        legend: {{ position: 'bottom', labels: {{ color: '#cbd5e1', font: {{ size: 10 }} }} }}
                    }}
                }}
            }});
        }}

        function updateSimulation() {{
            const severity = parseFloat(document.getElementById('slider-severity').value);
            const tcteShare = parseFloat(document.getElementById('slider-tcte-share').value) / 100.0;
            const attraction = parseFloat(document.getElementById('slider-attraction').value) / 100.0;
            const eveElast = parseFloat(document.getElementById('slider-eve-elasticity').value);

            document.getElementById('label-slider-severity').innerText = `${{severity.toFixed(2)}}x ${{severity > 1.05 ? '(劇烈衝擊)' : (severity < 0.95 ? '(溫和政策)' : '(教育部標準)')}}`;
            document.getElementById('label-slider-tcte-share').innerText = `${{(tcteShare * 100).toFixed(1)}}%`;
            document.getElementById('label-slider-attraction').innerText = `${{attraction >= 0 ? '+' : ''}}${{(attraction * 100).toFixed(1)}}%`;
            document.getElementById('label-slider-eve-elasticity').innerText = `${{eveElast.toFixed(1)}}`;

            const baseFresh = [18.8, 18.4, 17.9, 16.8, 15.6, 16.1, 16.5, 16.4, 16.0, 15.6, 15.3, 15.1, 14.9, 14.8, 14.8, 14.8];
            // 依據少子化劇烈度乘數精準放大或縮小各年度自113年基準之新生減幅
            const simFresh = baseFresh.map((f, i) => i === 0 ? f : +(18.8 - (18.8 - f) * severity).toFixed(2));
            const simTCTE = simFresh.map(f => +(f * tcteShare).toFixed(2));
            const simBiz = simTCTE.map(t => +(t * 0.19).toFixed(2));
            const simPool = simBiz.map(b => Math.round(b * 10000 * 0.22 * (1 + attraction)));

            // 基準114年中部商管生源池母體 (依據 simulate_fertility_impact.py 官方基準 3,080 人)
            const baseRefPool114 = 3080;
            const simDayScores = simPool.map(p => {{
                const ratio = p / baseRefPool114;
                let s = +(71.78 - (1.0 - ratio) * 12.0).toFixed(2);
                return s < 60.0 ? 60.0 : s;
            }});

            const simEveRates = simPool.map(p => {{
                const ratio = p / baseRefPool114;
                let r = +(50.91 * Math.pow(Math.max(ratio, 0.35), eveElast)).toFixed(1);
                return r < 10.0 ? 10.0 : r;
            }});

            let dangerYear = '128 學年度前安全';
            for (let i = 0; i < simEveRates.length; i++) {{
                if (simEveRates[i] <= 35.0) {{
                    dangerYear = (113 + i) + ' 學年度 (瀕危停招)';
                    break;
                }}
            }}
            document.getElementById('sim-eve-countdown').innerText = dangerYear;
            document.getElementById('sim-day-score-128').innerText = simDayScores[simDayScores.length - 1].toFixed(2) + ' 分';

            if (typeof Chart !== 'undefined') {{
                if (charts.m4Pools) {{
                    charts.m4Pools.data.datasets[0].data = simFresh;
                    charts.m4Pools.data.datasets[1].data = simTCTE;
                    charts.m4Pools.data.datasets[2].data = simPool;
                    charts.m4Pools.update('none');
                }}

                if (charts.m4Outcomes) {{
                    charts.m4Outcomes.data.datasets[0].data = simDayScores;
                    charts.m4Outcomes.data.datasets[1].data = simEveRates;
                    charts.m4Outcomes.update('none');
                }}
            }}

            renderSimTable(simFresh, simTCTE, simBiz, simPool, simDayScores, simEveRates);
        }}

        function renderSimTable(fresh, tcte, biz, pool, dayScore, eveRate) {{
            const tbody = document.getElementById('m4-sim-table-body');
            if (!tbody) return;
            tbody.innerHTML = '';

            for (let i = 0; i < 16; i++) {{
                const yr = 113 + i;
                const tr = document.createElement('tr');
                tr.className = yr === 117 ? 'bg-amber-950/30 font-bold' : (eveRate[i] < 35.0 ? 'bg-rose-950/20' : 'hover:bg-slate-800/40');
                
                let eveBadge = '';
                if (eveRate[i] < 35.0) {{
                    eveBadge = `<span class="px-1.5 py-0.5 rounded text-[10px] bg-rose-500/20 text-rose-300">極度危險</span>`;
                }} else if (eveRate[i] < 45.0) {{
                    eveBadge = `<span class="px-1.5 py-0.5 rounded text-[10px] bg-amber-500/20 text-amber-300">嚴峻警戒</span>`;
                }} else {{
                    eveBadge = `<span class="px-1.5 py-0.5 rounded text-[10px] bg-emerald-500/20 text-emerald-300">防守線</span>`;
                }}

                let fiveDef = (yr === 116 || yr === 117) ? '<span class="text-amber-400">良好 (92~95%)</span>' : '<span class="text-emerald-400">極穩 (98~100%)</span>';

                tr.innerHTML = `
                    <td class="p-2.5 font-bold text-white">${{yr}}學年 ${{yr === 117 ? '<span class="text-rose-400 text-[10px]">[虎年谷底]</span>' : ''}}</td>
                    <td class="p-2.5 text-right font-mono text-slate-300">${{fresh[i].toFixed(1)}}萬</td>
                    <td class="p-2.5 text-right font-mono text-slate-300">${{tcte[i].toFixed(2)}}萬</td>
                    <td class="p-2.5 text-right font-mono text-slate-300">${{biz[i].toFixed(2)}}萬</td>
                    <td class="p-2.5 text-right font-mono font-bold text-cyan-300">${{pool[i].toLocaleString()}}人</td>
                    <td class="p-2.5 text-right font-mono font-bold text-emerald-400">${{dayScore[i].toFixed(2)}}分</td>
                    <td class="p-2.5 text-right font-mono font-bold">${{eveRate[i].toFixed(1)}}% ${{eveBadge}}</td>
                    <td class="p-2.5">${{fiveDef}}</td>
                `;
                tbody.appendChild(tr);
            }}
        }}

        function resetSimulator() {{
            document.getElementById('slider-severity').value = 1.00;
            document.getElementById('slider-tcte-share').value = 40;
            document.getElementById('slider-attraction').value = 0;
            document.getElementById('slider-eve-elasticity').value = 1.8;
            updateSimulation();
        }}

        // ==========================================
        // 模組 5 繪製邏輯
        // ==========================================
        function initModule5Charts() {{
            const ctxFac = document.getElementById('chart-m5-faculty').getContext('2d');
            charts.m5Faculty = new Chart(ctxFac, {{
                type: 'doughnut',
                data: {{
                    labels: ['正教授 (4人 / 19.0%)', '副教授 (14人 / 66.7%)', '助理教授 (3人 / 14.3%)'],
                    datasets: [{{
                        data: [4, 14, 3],
                        backgroundColor: ['#10b981', '#a855f7', '#38bdf8'],
                        borderWidth: 2,
                        borderColor: '#0f172a'
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{
                        legend: {{ position: 'bottom', labels: {{ color: '#cbd5e1', font: {{ size: 11 }} }} }}
                    }}
                }}
            }});

            const ctxCurr = document.getElementById('chart-m5-curriculum').getContext('2d');
            charts.m5Curr = new Chart(ctxCurr, {{
                type: 'bar',
                data: {{
                    labels: DB.faculty_strategy.curriculum_rebalance.categories,
                    datasets: [
                        {{
                            label: '114 現況配比 (%)',
                            data: DB.faculty_strategy.curriculum_rebalance.current_114,
                            backgroundColor: '#64748b',
                            borderRadius: 4
                        }},
                        {{
                            label: '119 目標配比 (%)',
                            data: DB.faculty_strategy.curriculum_rebalance.target_119,
                            backgroundColor: '#10b981',
                            borderRadius: 4
                        }}
                    ]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {{
                        x: {{ ticks: {{ color: '#cbd5e1', font: {{ size: 10 }} }}, grid: {{ display: false }} }},
                        y: {{ ticks: {{ color: '#cbd5e1' }}, grid: {{ color: 'rgba(255, 255, 255, 0.08)' }}, max: 50 }}
                    }},
                    plugins: {{
                        legend: {{ position: 'bottom', labels: {{ color: '#cbd5e1', font: {{ size: 11 }} }} }}
                    }}
                }}
            }});

            const ctxM5Radar = document.getElementById('chart-m5-radar').getContext('2d');
            charts.m5Radar = new Chart(ctxM5Radar, {{
                type: 'radar',
                data: {{
                    labels: DB.faculty_strategy.radar_kpi.dimensions,
                    datasets: [
                        {{
                            label: '114 現況評估',
                            data: DB.faculty_strategy.radar_kpi.itm_now,
                            borderColor: '#64748b',
                            backgroundColor: 'rgba(100, 116, 139, 0.2)',
                            borderWidth: 2
                        }},
                        {{
                            label: '119 轉型五年願景',
                            data: DB.faculty_strategy.radar_kpi.itm_target,
                            borderColor: '#06b6d4',
                            backgroundColor: 'rgba(6, 182, 212, 0.25)',
                            borderWidth: 2.5
                        }}
                    ]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {{
                        r: {{
                            angleLines: {{ color: 'rgba(255, 255, 255, 0.1)' }},
                            grid: {{ color: 'rgba(255, 255, 255, 0.08)' }},
                            pointLabels: {{ color: '#cbd5e1', font: {{ size: 10 }} }},
                            suggestedMin: 50,
                            suggestedMax: 100,
                            ticks: {{ display: false }}
                        }}
                    }},
                    plugins: {{
                        legend: {{ position: 'bottom', labels: {{ color: '#cbd5e1', font: {{ size: 11 }} }} }}
                    }}
                }}
            }});
        }}

        function renderModule5Retire() {{
            const container = document.getElementById('m5-retire-list');
            if (!container) return;
            container.innerHTML = '';

            DB.faculty_strategy.retire_schedule.forEach(item => {{
                const div = document.createElement('div');
                div.className = item.count >= 2 
                    ? "flex flex-col sm:flex-row sm:items-center justify-between p-2.5 rounded-lg bg-slate-800/90 border border-amber-500/40 text-xs gap-2" 
                    : "flex flex-col sm:flex-row sm:items-center justify-between p-2.5 rounded-lg bg-slate-800/70 border border-slate-700/60 text-xs gap-2";

                div.innerHTML = `
                    <div class="flex items-center gap-2">
                        <span class="font-bold ${{item.count >= 2 ? 'text-rose-400' : 'text-amber-400'}}">${{item.yr}} 學年度</span>
                        <span class="text-white font-medium">預估退休：<strong class="${{item.count >= 2 ? 'text-rose-400 font-bold' : 'text-emerald-400'}}">${{item.count}} 名</strong> (${{item.domain}})</span>
                    </div>
                    <div class="text-[11px] text-slate-400">${{item.detail}}</div>
                `;
                container.appendChild(div);
            }});
        }}

        // CSV 全域綜合資料庫下載功能
        function exportAllCSV() {{
            const lines = [
                '# 國立臺中科技大學 國際貿易與經營系 (NUTC ITM) 校務研究策略分析實證數據集 (114學年度)',
                '# 資料來源：教育部大專校院校務資訊公開平台 (UDB)、技專校院招聯會 (JCTV)、教育部少子化預測報告',
                '',
                '=== 表一：全台國立科大 國貿/商務/航管/供應鏈 六強旗艦指標 ===',
                '代號,學校名稱,系所名稱,區域,在學總人數,五專部人數,日間學士人數,進修學士人數,碩博生人數,專任師資總數,正教授,副教授,助理教授,境外生人數,境外生比率(%),114日間四技註冊率(%),114統測單科均分(分),113退學人數,113退學率(%)',
                ...DB.regional_six.map(x => [
                    x.code, x.school, x.dept, x.region, x.total_stu, x.five_year, x.undergrad_day, x.undergrad_eve, x.grad, x.faculty_total, x.faculty_prof, x.faculty_assoc, x.faculty_asst, x.oversea_stu, x.oversea_pct, x.reg_114_rate, x.score_114, x.drop_cnt_113, x.drop_rate_113
                ].join(',')),
                '',
                '=== 表二：中部大專商管競爭系所綜合情報比對 ===',
                '學校系所,定位類型,核定名額現況,114日間註冊率(%),114進修註冊率(%),門檻均分估值(分),在學總人數,退學流失率(%),財務現金存量,每學期學費,生源管道分流,戰略威脅等級',
                ...DB.central_competitors.map(c => [
                    c.school, c.type, `"${{c.quota_status}}"`, c.reg_114_day, c.reg_114_eve, c.score_cutoff, c.students_total, c.drop_rate, `"${{c.cash_reserve}}"`, `"${{c.tuition_per_sem}}"`, `"${{c.source_mix}}"`, `"${{c.threat_level}}"`
                ].join(',')),
                '',
                '=== 表三：近6年 (109~114學年度) 統測 09商管群最低單科錄取均分走勢 ===',
                '學年度,中科大國貿,中科大企管,(國貿-企管差距),雲科大企管,北商大國商,北商大企管,勤益企管,虎科財金',
                ...DB.score_trends.years.map((y, i) => {{
                    const itm = DB.score_trends.departments['中科大國貿'][i];
                    const ba = DB.score_trends.departments['中科大企管'][i];
                    const diff = +(itm - ba).toFixed(2);
                    const diffStr = diff > 0 ? `+${{diff}}` : `${{diff}}`;
                    const yun = DB.score_trends.departments['雲科大企管'][i];
                    const ntub_ib = DB.score_trends.departments['北商大國商'][i];
                    const ntub_ba = DB.score_trends.departments['北商大企管'][i];
                    const ncut = DB.score_trends.departments['勤益企管'][i];
                    const nfu = DB.score_trends.departments['虎科財金'][i];
                    return `${{y}}學年,${{itm}},${{ba}},${{diffStr}},${{yun}},${{ntub_ib}},${{ntub_ba}},${{ncut}},${{nfu}}`;
                }}),
                '',
                '=== 表四：中科國貿 vs 企管 各學制註冊率詳細消長矩陣 ===',
                '學制班別,國貿系113註冊率,國貿系114註冊率,企管系113註冊率,企管系114註冊率,體質差異分析',
                ...DB.itm_vs_ba_deep.registration_matrix.map(r => [
                    `"${{r.prog}}"`, `"${{r.itm_113}}"`, `"${{r.itm_114}}"`, `"${{r.ba_113}}"`, `"${{r.ba_114}}"`, `"${{r.diff}}"`
                ].join(',')),
                '',
                '=== 表五：教育部 113~128 學年度少子化預測基準模型 ===',
                '學年度,全國大一新生總數(萬人),統測報考總數(萬人),商管群人數(萬人),中部商管生源池(人),中科日間錄取均分推估(分),中科進修部註冊率推估(%),五專部防護力',
                ...DB.fertility_timeline.map(f => [
                    `${{f.yr}}學年`, f.fresh, f.tcte, f.biz, f.pool, f.day_score, f.eve_rate, `"${{f.five_def}}"`
                ].join(',')),
                '',
                '=== 表六：中科國貿 115~120學年度 專任師資退休換血與轉型排程 ===',
                '學年度,預估退休人數,專長領域,員額釋出與轉型對策',
                ...DB.faculty_strategy.retire_schedule.map(s => [
                    `${{s.yr}}學年`, s.count, `"${{s.domain}}"`, `"${{s.detail}}"`
                ].join(','))
            ];

            let csvContent = "\\uFEFF" + lines.join("\\n");
            const blob = new Blob([csvContent], {{ type: 'text/csv;charset=utf-8;' }});
            const url = URL.createObjectURL(blob);
            const link = document.createElement("a");
            link.setAttribute("href", url);
            link.setAttribute("download", "NUTC_ITM_Comprehensive_Master_Dataset_114.csv");
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        }}

        // Module 4 當前動態模擬試算表專屬匯出功能
        function exportSimCSV() {{
            const severity = parseFloat(document.getElementById('slider-severity').value);
            const tcteShare = parseFloat(document.getElementById('slider-tcte-share').value);
            const attraction = parseFloat(document.getElementById('slider-attraction').value);
            const eveElast = parseFloat(document.getElementById('slider-eve-elasticity').value);

            const baseFresh = [18.8, 18.4, 17.9, 16.8, 15.6, 16.1, 16.5, 16.4, 16.0, 15.6, 15.3, 15.1, 14.9, 14.8, 14.8, 14.8];
            const simFresh = baseFresh.map((f, i) => i === 0 ? f : +(18.8 - (18.8 - f) * severity).toFixed(2));
            const simTCTE = simFresh.map(f => +(f * (tcteShare / 100.0)).toFixed(2));
            const simBiz = simTCTE.map(t => +(t * 0.19).toFixed(2));
            const simPool = simBiz.map(b => Math.round(b * 10000 * 0.22 * (1 + attraction / 100.0)));
            const baseRefPool114 = 3080;
            const simDayScores = simPool.map(p => {{
                const ratio = p / baseRefPool114;
                let s = +(71.78 - (1.0 - ratio) * 12.0).toFixed(2);
                return s < 60.0 ? 60.0 : s;
            }});
            const simEveRates = simPool.map(p => {{
                const ratio = p / baseRefPool114;
                let r = +(50.91 * Math.pow(Math.max(ratio, 0.35), eveElast)).toFixed(1);
                return r < 10.0 ? 10.0 : r;
            }});

            const rows = [
                ['# 國立臺中科技大學 國際貿易與經營系 113~128學年度少子化海嘯動態推估試算表'],
                [`# 模擬參數: 少子化乘數=${{severity}}x, 技職分流比=${{tcteShare}}%, 品牌吸附力=${{attraction}}%, 進修部彈性=${{eveElast}}`],
                ['學年度', '全國大一新生總數(萬人)', '統測報考總數(萬人)', '統測商管群人數(萬人)', '中部商管生源池(人)', '日間四技錄取單科均分預測(分)', '進修四技註冊率預測(%)', '五專部防護力', '進修部存續警戒狀態'],
                ...simFresh.map((fresh, i) => {{
                    const yr = 113 + i;
                    const pool = simPool[i];
                    const day = simDayScores[i];
                    const eve = simEveRates[i];
                    const five = (yr === 116 || yr === 117) ? '良好 (約92~95%)' : '極穩 (98~100%)';
                    const level = eve <= 35.0 ? '極度危險 (瀕臨停招)' : (eve < 45.0 ? '嚴峻警戒' : '正常防守線');
                    return [yr + '學年度', fresh, simTCTE[i], simBiz[i], pool, day, eve, five, level];
                }})
            ];

            let csvContent = "\\uFEFF" + rows.map(e => e.join(",")).join("\\n");
            const blob = new Blob([csvContent], {{ type: 'text/csv;charset=utf-8;' }});
            const url = URL.createObjectURL(blob);
            const link = document.createElement("a");
            link.setAttribute("href", url);
            link.setAttribute("download", `NUTC_ITM_Simulated_Projection_113_128_S${{severity}}_T${{tcteShare}}.csv`);
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        }}
    </script>
</body>
</html>
"""

    output_path = "/Users/chenchunchih/Downloads/校務資料/interactive_dashboard.html"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"[SUCCESS] Base dashboard built successfully: {output_path} ({len(html_content)} bytes)")
    
    # 自動調用 Module 6 注入模組
    import subprocess
    mod6_script = "/Users/chenchunchih/Downloads/校務資料/update_dashboard_with_module6.py"
    if os.path.exists(mod6_script):
        subprocess.run(["python3", mod6_script])

if __name__ == "__main__":
    generate_dashboard()

