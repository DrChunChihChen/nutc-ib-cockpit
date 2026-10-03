"""
GCIS client：經濟部商工行政資料開放平臺 API（2026-10-02 實測）
用法：
    python3 -m ir_autopilot.src.ai.gcis_client verify ib        # 核對國貿系候選廠商
    python3 -m ir_autopilot.src.ai.gcis_client lookup 鑫德信不動產仲介經紀有限公司
規則：日期民國 7 碼；$top≤1000；回應錯誤藏在 200 內文（中文），需比對字串。
"""
import json
import os
import re
import sys
import time
from typing import Any, Dict, List, Optional

import requests

BASE = "https://data.gcis.nat.gov.tw/od/data/api/"
API = {
    "keyword":   "6BBA2268-1367-4B42-9CCA-BC17499EBE8C",  # Company_Name like X and Company_Status eq S
    "basic":     "5F64D864-61CB-4D0D-8AD9-492047CC1EA6",  # Business_Accounting_NO eq
    "directors": "4E5F7653-1B91-4DDC-99D5-468530FAE396",
    "branches":  "FDB8D2C8-573D-4276-BFA4-8D3925ABE1CB",
    "changes":   "4347A009-6489-4F19-AC79-78F366BE7976",  # Change_Of_Approval_Data eq 民國日期
    "dissolved": "561D23B6-5EA7-4FF4-A78D-A617ED64BC64",
    "setup":     "467E8A3A-72C6-4663-9557-D9D74C597E14",
}
STATUS_CODES = ["01", "04", "03", "02", "05"]   # 01 核准設立, 04 解散（其餘依平台狀態代碼表）
ERR_PAT = re.compile(r"超出|維護中|非授權|參數有誤|不開放|不存在")
OUTPUT_DIR = os.environ.get("IR_OUTPUT_DIR", os.path.join(os.path.dirname(__file__), "..", "..", "..", "output"))


class GcisError(RuntimeError):
    pass


def _get(api: str, flt: str, top: int = 50, skip: int = 0) -> List[Dict[str, Any]]:
    url = f"{BASE}{API[api]}"
    r = requests.get(url, params={"$format": "json", "$filter": flt, "$skip": skip, "$top": top},
                     headers={"User-Agent": "Mozilla/5.0 NUTC-IR"}, timeout=30)
    txt = r.text.strip()
    if not txt:
        return []
    if ERR_PAT.search(txt[:200]) and not txt.startswith("["):
        raise GcisError(txt[:120])
    return r.json()


def normalize(name: str) -> str:
    n = re.sub(r"\s", "", name)
    n = re.sub(r"^.*[)）＿_]", "", n)
    parts = re.split(r"[_\-（(｜|]", n)
    cand = [p for p in parts if "公司" in p]
    n = cand[-1] if cand else parts[0]
    return re.sub(r"(分公司|門市|加盟店|營業所|.{1,3}廠)$", "", n)


def lookup(name: str) -> Dict[str, Any]:
    q = normalize(name)
    if "公司" not in q:
        return {"name": name, "verified": False, "reason": "非公司型態（可能為商業登記）"}
    best = None
    for s in STATUS_CODES:
        rows = _get("keyword", f"Company_Name like {q[:6]} and Company_Status eq {s}", top=30)
        exact = next((r for r in rows if r.get("Company_Name") == q), None)
        if exact:
            best = exact
            break
        if best is None and rows:
            best = {**rows[0], "_fuzzy": True}
        time.sleep(0.2)
    if not best:
        return {"name": name, "verified": False, "reason": "商工登記查無"}
    return {
        "name": name, "query": q, "verified": not best.get("_fuzzy"), "fuzzy": bool(best.get("_fuzzy")),
        "matched_name": best.get("Company_Name"), "tax_id": best.get("Business_Accounting_NO"),
        "status": best.get("Company_Status_Desc"), "capital": best.get("Capital_Stock_Amount"),
        "paid_in": best.get("Paid_In_Capital_Amount"), "setup_date": best.get("Company_Setup_Date"),
        "last_change": best.get("Change_Of_Approval_Data"), "location": best.get("Company_Location"),
        "source": "GCIS 公司登記關鍵字查詢", "fetched_at": time.strftime("%Y-%m-%d"),
    }


def verify_partners(slug: str) -> Dict[str, Any]:
    path = os.path.join(OUTPUT_DIR, slug, "dept_data.json")
    data = json.load(open(path, encoding="utf-8"))
    names = [n for c in data.get("partners", {}).get("clusters", []) for n in c.get("companies", [])]
    out_path = os.path.join(OUTPUT_DIR, slug, "partners_verified.json")
    out = json.load(open(out_path, encoding="utf-8")) if os.path.exists(out_path) else {}
    for n in names:
        if n in out and out[n].get("verified"):
            continue
        try:
            out[n] = lookup(n)
        except GcisError as e:
            print(f"[GCIS] 停止：{e}")
            break
        print(f"{n} -> {out[n].get('tax_id')} {out[n].get('status')} verified={out[n]['verified']}")
        time.sleep(0.3)
    json.dump(out, open(out_path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"寫入 {out_path}：{sum(1 for v in out.values() if v.get('verified'))}/{len(names)} 已核對")
    return out


if __name__ == "__main__":
    if len(sys.argv) >= 3 and sys.argv[1] == "verify":
        verify_partners(sys.argv[2])
    elif len(sys.argv) >= 3 and sys.argv[1] == "lookup":
        print(json.dumps(lookup(sys.argv[2]), ensure_ascii=False, indent=1))
    else:
        print(__doc__)
