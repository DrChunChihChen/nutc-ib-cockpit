"""
Dossier: 代理人唯一的數字來源。
所有數值皆由 output/{slug}/dept_data.json（UDB 計算結果）與 raw_data/01_*交叉查榜*.csv 即時計算，
不存在任何手打常數。每個數字附 source / year，供 LLM 引用與事後接地檢查。
"""
import csv
import glob
import json
import os
from collections import Counter
from datetime import datetime
from typing import Any, Dict, List, Optional

OUTPUT_DIR = os.environ.get("IR_OUTPUT_DIR", os.path.join(os.path.dirname(__file__), "..", "..", "..", "output"))

DEPT_ALIASES = {
    "國際貿易與經營": "ib", "國際貿易": "ib", "國貿": "ib", "國企": "ib", "國際企業": "ib", "國際商務": "ib",
    "企業管理": "ba", "企管": "ba", "工管": "ba", "工業管理": "ba", "工業工程": "ba",
    "會計資訊": "accounting", "會資": "accounting", "會計": "accounting",
    "財務金融": "finance", "財金": "finance", "金融": "finance",
    "保險金融管理": "insurance", "保金": "insurance", "保險": "insurance", "風險管理": "insurance", "風保": "insurance", "風管": "insurance",
    "應用統計": "stat", "應統": "stat", "統計": "stat", "資訊管理": "stat", "資管": "stat",
    "財政稅務": "tax", "財稅": "tax", "財政": "tax", "稅務": "tax",
}
SLUG_TO_NAME = {
    "ib": "國際貿易與經營系", "ba": "企業管理系", "accounting": "會計資訊系", "finance": "財務金融系",
    "insurance": "保險金融管理系", "stat": "應用統計系", "tax": "財政稅務系",
}

# K24 綜合風險分：權重公開、分項全部可由 dossier 重算
K24_WEIGHTS = {"K01": 0.30, "K05": 0.25, "K10": 0.20, "K19": 0.15, "K06": 0.10}


def detect_slug(text: str, default: str = "ib") -> str:
    for alias in sorted(DEPT_ALIASES.keys(), key=lambda x: len(x), reverse=True):
        if alias in text:
            return DEPT_ALIASES[alias]
    return default


def _load_json(path: str) -> Optional[Dict[str, Any]]:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def _clip(x: float, lo: float = 0.0, hi: float = 100.0) -> float:
    return max(lo, min(hi, x))


def compute_k24(kpis: Dict[str, Any]) -> Dict[str, Any]:
    """五維加權。每個分項先換算成 0–100 的子分數，再乘權重。缺任一指標即標示 partial。"""
    def v(k):
        return kpis.get(k, {}).get("value")

    sub, missing = {}, []
    if v("K01") is not None:
        sub["K01"] = _clip(v("K01"))                       # 註冊率本身即 0–100
    else:
        missing.append("K01")
    if v("K05") is not None:
        sub["K05"] = _clip(100 - v("K05"))                 # 留存 = 100 − 淨流失率
    else:
        missing.append("K05")
    if v("K10") is not None:
        sub["K10"] = _clip(50 + v("K10") * 5)              # 與同儕中位數差：每 1pp = 5 分，0pp = 50
    else:
        missing.append("K10")
    if v("K19") is not None:
        sub["K19"] = _clip(100 + v("K19"))                 # 缺口 −19.5% → 80.5
    else:
        missing.append("K19")
    if v("K06") is not None:
        sub["K06"] = _clip(100 - max(0.0, v("K06") - 20) * 2.5)  # 生師比 20 以下滿分，40 = 50 分
    else:
        missing.append("K06")

    total_w = sum(K24_WEIGHTS[k] for k in sub)
    score = sum(sub[k] * K24_WEIGHTS[k] for k in sub) / total_w if total_w else None
    grade = None
    if score is not None:
        grade = "A 穩健" if score >= 80 else ("B 觀察" if score >= 60 else "C 預警")
    return {
        "score": round(score, 1) if score is not None else None,
        "grade": grade,
        "weights": K24_WEIGHTS,
        "subscores": {k: round(s, 1) for k, s in sub.items()},
        "contributions": {k: round(sub[k] * K24_WEIGHTS[k], 2) for k in sub},
        "missing": missing,
        "formula": "K24 = Σ w_k · sub_k；sub_K01=註冊率, sub_K05=100−淨流失率, sub_K10=50+5×同儕差(pp), sub_K19=100+缺口%, sub_K06=100−2.5×max(0,生師比−20)",
    }


def compute_module5(slug: str, school_name: str) -> Optional[Dict[str, Any]]:
    """由交叉查榜 CSV 即時計算：本校考生數、留任、外流去向 Top5。兩種欄位格式皆支援。"""
    files = glob.glob(os.path.join(OUTPUT_DIR, slug, "raw_data", "01_*流向*.csv"))
    files = [f for f in files if "彙整" not in f]
    if not files:
        return None
    rows: List[Dict[str, str]] = []
    with open(files[0], "r", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        return None

    if "school_name" in rows[0]:   # 新格式（多校母體）
        own = [r for r in rows if school_name in r.get("school_name", "")]
        dest_key, cat_key, status_key, year_key = "dest_school", "category", "status", "year"
        retained = [r for r in own if "留任" in r.get(cat_key, "")]
        poached = [r for r in own if "其他學校" in r.get(cat_key, "")]
        unplaced = [r for r in own if "未分發" in r.get(cat_key, "") or "放棄" in r.get(cat_key, "")]
        population_note = f"交叉查榜母體 {len(rows)} 筆（含競校），其中本校系 {len(own)} 筆"
    else:                          # 舊格式（僅本系）
        own = rows
        dest_key, cat_key, status_key, year_key = "最終分發學校", "分發去向分類", "原系錄取別", "學年度"
        retained = [r for r in own if "本校" in r.get(cat_key, "") or school_name in r.get(dest_key, "")]
        poached = [r for r in own if "其他學校" in r.get(cat_key, "")]
        unplaced = [r for r in own if "未分發" in r.get(cat_key, "") or "放棄" in r.get(cat_key, "")]
        population_note = f"本系交叉查榜母體 {len(own)} 筆"

    years = sorted({r.get(year_key, "") for r in own if r.get(year_key)})
    dest = Counter(r.get(dest_key, "") for r in poached if r.get(dest_key) and r.get(dest_key) != "—")
    top = dest.most_common(5)
    n = len(own)
    return {
        "source": os.path.basename(files[0]),
        "years": years,
        "population_note": population_note,
        "own_candidates": n,
        "retained": len(retained),
        "retention_rate": round(len(retained) / n * 100, 1) if n else None,
        "poached": len(poached),
        "unplaced": len(unplaced),
        "main_admitted": sum(1 for r in own if r.get(status_key, "").startswith("正取")),
        "top_destinations": [{"school": s, "count": c, "share_of_poached": round(c / len(poached) * 100, 1) if poached else None} for s, c in top],
    }


def build_dossier(slug: str) -> Dict[str, Any]:
    data = _load_json(os.path.join(OUTPUT_DIR, slug, "dept_data.json")) or {}
    dept_name = data.get("dept_name") or SLUG_TO_NAME.get(slug, slug)
    school_name = data.get("school_name", "國立臺中科技大學")
    kpis = data.get("kpis", {})
    fetched_at = None
    try:
        fetched_at = datetime.fromtimestamp(os.path.getmtime(os.path.join(OUTPUT_DIR, slug, "dept_data.json"))).strftime("%Y-%m-%d")
    except Exception:
        pass

    demo = data.get("demo", {})
    timeline = demo.get("timeline", [])
    y117 = next((t for t in timeline if t.get("year") == 117), None)
    y128 = next((t for t in timeline if t.get("year") == 128), None)

    peers = []
    for p in (data.get("peers", {}).get("peers", []) if isinstance(data.get("peers"), dict) else []):
        peers.append({
            "school": p.get("school_name"), "dept": p.get("dept_name"), "public": p.get("public"),
            "year": p.get("latest_year"), "enrollment_rate": p.get("enrollment_rate"),
            "dropout_rate": p.get("dropout_rate"), "faculty_ratio": p.get("faculty_ratio"),
            "students_total": p.get("students_total"), "foreign_ratio": p.get("foreign_ratio"),
        })

    partners = data.get("partners") or {}
    verified = _load_json(os.path.join(OUTPUT_DIR, slug, "partners_verified.json")) or {}
    for c in partners.get("clusters", []):
        c["verification"] = [verified.get(name) or {"name": name, "verified": False} for name in c.get("companies", [])]

    return {
        "meta": {"school_name": school_name, "dept_name": dept_name, "slug": slug, "dept_code": data.get("dept_code"),
                 "data_file": f"output/{slug}/dept_data.json", "fetched_at": fetched_at,
                 "latest_year": data.get("profile", {}).get("latest_year")},
        "profile": data.get("profile", {}),
        "kpis": kpis,
        "k24": compute_k24(kpis),
        "alerts": data.get("alerts", []),
        "demographics": {"base_capacity": demo.get("base_capacity"), "y117": y117, "y128": y128, "timeline": timeline,
                          "source": "內政部歷年出生數 × 本系份額推估（dept_data.json demo）"},
        "peers": peers,
        "module5": compute_module5(slug, school_name),
        "partners": partners,
    }


def dossier_to_text(d: Dict[str, Any], sections: Optional[List[str]] = None) -> str:
    """給 LLM 的精簡 JSON（避免 timeline 全量塞入）。"""
    slim = {k: v for k, v in d.items() if (sections is None or k in sections or k == "meta")}
    if "demographics" in slim:
        dm = dict(slim["demographics"])
        dm["timeline"] = [t for t in dm.get("timeline", []) if t.get("year") in (113, 115, 117, 119, 121, 124, 128)]
        slim["demographics"] = dm
    if "partners" in slim:
        slim["partners"] = {"csic_focus": slim["partners"].get("csic_focus"),
                            "clusters": [{"category": c.get("category"), "companies": c.get("companies"),
                                          "verification": c.get("verification")} for c in slim["partners"].get("clusters", [])],
                            "note": "名單為人工整理之候選清單；verified=false 者尚未經商工登記核對，回答時必須說明。"}
    return json.dumps(slim, ensure_ascii=False, indent=1)
