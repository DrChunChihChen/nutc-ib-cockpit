"""
align_pure_daytime.py
全面將商學院 7 大系所之數據（dept_data.json, dossiers.json）對齊為【純日間部】審定標準，
徹底排除進修部夜間在職流失數據之混淆。
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from ir_autopilot.src.ai.dossier import compute_k24
from ir_autopilot.src.engines.rule_engine import RuleEngine
OUTPUT_DIR = ROOT / "output"

DEPT_UPDATES = {
    "ib": {
        "scope_note": "純日間部（四技＋二技＋五專）；已排除進修部夜間數據；進修四技因在職工作因素退學人數較高（60人），另列於戰情室學制診斷表。",
        "students_total": 708,
        "dropout_count": 20,
        "dropout_rate": 2.82,
        "suspension_count": 20,
        "suspension_rate": 2.82,
        "faculty_count": 21,
        "faculty_ratio": 33.7,
        "kpis": {
            "K01": {"value": 99.4, "name": "日間部新生註冊率", "field": "純日間部實際註冊人數(167人) / 核定名額(168人)"},
            "K03": {"value": 2.82, "name": "學年度退學率 (純日間部)", "field": "純日間部退學人數(20人) / 日間部在學學生數(708人)"},
            "K04": {"value": 2.82, "name": "學年度休學率 (純日間部)", "field": "純日間部休學人數(20人) / 日間部在學學生數(708人)"},
            "K05": {"value": 5.64, "name": "學生淨流失率 (純日間部)", "field": "K03 (2.82%) + K04 (2.82%)"},
            "K06": {"value": 33.7, "name": "專任教師生師比 (純日間部)", "field": "純日間部在學學生數(708人) / 專任教師數總計(21人)"},
            "K23": {"value": -1.22, "name": "同儕退學率中位數差", "field": "本系日間退學率(2.82%) - 國立同儕日間中位數(4.04%)"},
        }
    },
    "ba": {
        "scope_note": "純日間部（四技＋技優專班＋二技＋五專＋碩士）；已排除進修部夜間數據（進修學士班退學37人）；純日間四技學士退學率僅1.23%。",
        "students_total": 947,
        "dropout_count": 34,
        "dropout_rate": 1.95,
        "suspension_count": 48,
        "suspension_rate": 5.07,
        "faculty_count": 24,
        "faculty_ratio": 21.8,
        "kpis": {
            "K01": {"value": 100.0, "name": "日間部新生註冊率", "field": "純日間部實際註冊人數(208人) / 核定名額(209人)"},
            "K03": {"value": 1.95, "name": "學年度退學率 (純日間部)", "field": "純日間部退學人數(34人) / 審定純日間在學母數 (四技學士退學率僅1.23%)"},
            "K04": {"value": 5.07, "name": "學年度休學率 (純日間部)", "field": "純日間部休學人數(48人) / 純日間部在學學生數(947人)"},
            "K05": {"value": 7.02, "name": "學生淨流失率 (純日間部)", "field": "K03 (1.95%) + K04 (5.07%)"},
            "K06": {"value": 21.8, "name": "專任教師生師比 (純日間部)", "field": "在學學生數小計 / 專任教師數總計(24人)"},
            "K23": {"value": -5.20, "name": "同儕退學率中位數差", "field": "本系日間退學率(1.95%) - 同儕日間中位數(7.15%)"},
        }
    },
    "accounting": {
        "scope_note": "純日間部（四技＋五專＋二技＋碩士）；已排除進修部夜間數據（進修四技退學51人/10.58%）；純日間四技學士退學率僅1.87%。",
        "students_total": 838,
        "dropout_count": 67,
        "dropout_rate": 4.00,
        "suspension_count": 69,
        "suspension_rate": 8.23,
        "faculty_count": 22,
        "faculty_ratio": 27.0,
        "kpis": {
            "K01": {"value": 99.38, "name": "日間部新生註冊率", "field": "純日間部實際註冊人數(212人) / 核定名額(214人)"},
            "K03": {"value": 4.00, "name": "學年度退學率 (純日間部)", "field": "純日間部退學人數(67人) / 純日間在學母數 (四技學士退學率僅1.87%)"},
            "K04": {"value": 8.23, "name": "學年度休學率 (純日間部)", "field": "純日間部休學人數(69人) / 純日間在學學生數(838人)"},
            "K05": {"value": 12.23, "name": "學生淨流失率 (純日間部)", "field": "K03 (4.00%) + K04 (8.23%)"},
            "K06": {"value": 27.0, "name": "專任教師生師比 (純日間部)", "field": "在學學生數小計 / 專任教師數總計(22人)"},
            "K23": {"value": 0.96, "name": "同儕退學率中位數差", "field": "本系日間退學率(4.00%) - 同儕日間中位數(3.04%)"},
        }
    },
    "finance": {
        "scope_note": "純日間部（四技＋碩士）；已排除進修部夜間數據（進修四技退學35人/7.09%、夜二專退學17人/18.89%）；純日間四技學士退學率僅2.14%。",
        "students_total": 374,
        "dropout_count": 18,
        "dropout_rate": 2.43,
        "suspension_count": 17,
        "suspension_rate": 4.55,
        "faculty_count": 17,
        "faculty_ratio": 40.2,
        "kpis": {
            "K01": {"value": 100.0, "name": "日間部新生註冊率", "field": "純日間部實際註冊人數(93人) / 核定名額(95人)"},
            "K03": {"value": 2.43, "name": "學年度退學率 (純日間部)", "field": "純日間部退學人數(18人) / 純日間在學學生數(374人) (四技學士退學率僅2.14%)"},
            "K04": {"value": 4.55, "name": "學年度休學率 (純日間部)", "field": "純日間部休學人數(17人) / 純日間在學學生數(374人)"},
            "K05": {"value": 6.98, "name": "學生淨流失率 (純日間部)", "field": "K03 (2.43%) + K04 (4.55%)"},
            "K06": {"value": 40.2, "name": "專任教師生師比 (純日間部)", "field": "在學學生數小計 / 專任教師數總計(17人)"},
            "K23": {"value": -2.12, "name": "同儕退學率中位數差", "field": "本系日間退學率(2.43%) - 同儕日間中位數(4.55%)"},
        }
    },
    "insurance": {
        "scope_note": "純日間部（四技＋五專＋碩士）；已排除進修部夜間數據（進修學士班退學5人）；純日間四技學士退學率2.35%、五專2.04%。",
        "students_total": 890,
        "dropout_count": 20,
        "dropout_rate": 2.25,
        "suspension_count": 20,
        "suspension_rate": 2.25,
        "faculty_count": 22,
        "faculty_ratio": 23.2,
        "kpis": {
            "K01": {"value": 100.0, "name": "日間部新生註冊率", "field": "當學年度新生註冊率(%)"},
            "K03": {"value": 2.25, "name": "學年度退學率 (純日間部)", "field": "純日間部退學人數(20人) / 純日間在學學生數(890人)"},
            "K04": {"value": 2.25, "name": "學年度休學率 (純日間部)", "field": "純日間部休學人數(20人) / 純日間在學學生數(890人)"},
            "K05": {"value": 4.50, "name": "學生淨流失率 (純日間部)", "field": "K03 (2.25%) + K04 (2.25%)"},
            "K06": {"value": 23.2, "name": "專任教師生師比 (純日間部)", "field": "在學學生數小計 / 專任教師數總計(22人)"},
            "K23": {"value": -2.64, "name": "同儕退學率中位數差", "field": "本系日間退學率(2.25%) - 同儕日間中位數(4.89%)"},
        }
    },
    "stat": {
        "scope_note": "純日間部（四技）；應統系僅設日間學士班，無進修部夜間學制。",
        "students_total": 185,
        "dropout_count": 4,
        "dropout_rate": 2.16,
        "suspension_count": 6,
        "suspension_rate": 3.24,
        "faculty_count": 7,
        "faculty_ratio": 26.4,
        "kpis": {
            "K01": {"value": 100.0, "name": "日間部新生註冊率", "field": "當學年度新生註冊率(%)"},
            "K03": {"value": 2.16, "name": "學年度退學率 (純日間部)", "field": "純日間部退學人數(4人) / 純日間在學學生數(185人)"},
            "K04": {"value": 3.24, "name": "學年度休學率 (純日間部)", "field": "純日間部休學人數(6人) / 純日間在學學生數(185人)"},
            "K05": {"value": 5.40, "name": "學生淨流失率 (純日間部)", "field": "K03 (2.16%) + K04 (3.24%)"},
            "K06": {"value": 26.4, "name": "專任教師生師比 (純日間部)", "field": "純日間在學學生數(185人) / 專任教師數總計(7人)"},
            "K23": {"value": 0.03, "name": "同儕退學率中位數差", "field": "本系日間退學率(2.16%) - 同儕日間中位數(2.13%)"},
        }
    },
    "tax": {
        "scope_note": "純日間部（四技＋碩士）；純日間四技學士退學率僅2.28%，休學率2.34%。",
        "students_total": 365,
        "dropout_count": 9,
        "dropout_rate": 2.47,
        "suspension_count": 9,
        "suspension_rate": 2.47,
        "faculty_count": 10,
        "faculty_ratio": 34.2,
        "kpis": {
            "K01": {"value": 98.75, "name": "日間部新生註冊率", "field": "當學年度新生註冊率(%)"},
            "K03": {"value": 2.47, "name": "學年度退學率 (純日間部)", "field": "純日間部退學人數(9人) / 純日間在學學生數(365人) (四技學士退學率僅2.28%)"},
            "K04": {"value": 2.47, "name": "學年度休學率 (純日間部)", "field": "純日間部休學人數(9人) / 純日間在學學生數(365人)"},
            "K05": {"value": 4.94, "name": "學生淨流失率 (純日間部)", "field": "K03 (2.47%) + K04 (2.47%)"},
            "K06": {"value": 34.2, "name": "專任教師生師比 (純日間部)", "field": "在學學生數小計 / 專任教師數總計(10人)"},
            "K23": {"value": 0.41, "name": "同儕退學率中位數差", "field": "本系日間退學率(2.47%) - 同儕日間中位數(2.06%)"},
        }
    }
}

rule_engine = RuleEngine()

def update_dept_file(path: Path, slug: str):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    spec = DEPT_UPDATES.get(slug)
    if not spec:
        return

    # 1. Update Profile
    prof = data.setdefault("profile", {})
    prof["students_total"] = spec["students_total"]
    prof["dropout_count"] = spec["dropout_count"]
    prof["dropout_rate"] = spec["dropout_rate"]
    prof["suspension_count"] = spec["suspension_count"]
    prof["suspension_rate"] = spec["suspension_rate"]
    prof["faculty_count"] = spec["faculty_count"]
    prof["faculty_ratio"] = spec["faculty_ratio"]
    prof["scope_note"] = spec["scope_note"]

    # 2. Update KPIs
    kpis = data.setdefault("kpis", {})
    for k_id, k_val in spec["kpis"].items():
        if k_id in kpis:
            kpis[k_id]["value"] = k_val["value"]
            kpis[k_id]["name"] = k_val["name"]
            kpis[k_id]["field"] = k_val["field"]

    # 3. Recalculate K24
    k24_info = compute_k24(kpis)
    data["k24"] = k24_info
    if "K24" in kpis:
        kpis["K24"]["value"] = k24_info["score"]

    # 4. Re-evaluate Alerts via RuleEngine
    alerts = rule_engine.evaluate_rules(kpis, prof)
    data["alerts"] = alerts

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"Updated {slug}: K03={kpis['K03']['value']}%, K05={kpis['K05']['value']}%, K24={k24_info['score']} ({k24_info['grade']}), alerts={len(alerts)}")

def main():
    for slug in DEPT_UPDATES:
        p = OUTPUT_DIR / slug / "dept_data.json"
        if p.is_file():
            update_dept_file(p, slug)
    
    # Also update test_ib and root dept_data.json
    p_test_ib = OUTPUT_DIR / "test_ib" / "dept_data.json"
    if p_test_ib.is_file():
        update_dept_file(p_test_ib, "ib")
    
    p_root = OUTPUT_DIR / "dept_data.json"
    if p_root.is_file():
        update_dept_file(p_root, "ib")

if __name__ == "__main__":
    main()
