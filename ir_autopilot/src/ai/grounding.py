"""
Grounding check: 回答中的每個數字都必須能在 dossier 中找到（容忍四捨五入）。
回傳 {"ok": bool, "checked": n, "ungrounded": [...]}，供 UI 顯示警告。
"""
import json
import re
from typing import Any, Dict, List, Set, Optional

_NUM = re.compile(r"(?<![\w.])(-?\d{1,3}(?:,\d{3})+|-?\d+(?:\.\d+)?)(?![\w.])")
_IGNORE_CONTEXT = re.compile(r"(學年度|學年|年度|年|K\d{2}|R\d{2}|第|名|級|%|％|pp)")


def _collect_numbers(obj: Any, out: Set[float]) -> None:
    if isinstance(obj, bool):
        return
    if isinstance(obj, (int, float)):
        out.add(round(float(obj), 2))
        return
    if isinstance(obj, str):
        for m in _NUM.findall(obj):
            try:
                out.add(round(float(m.replace(",", "")), 2))
            except ValueError:
                pass
        return
    if isinstance(obj, dict):
        for v in obj.values():
            _collect_numbers(v, out)
    elif isinstance(obj, (list, tuple)):
        if obj and isinstance(obj[0], dict):
            for key in ("count", "share_of_poached", "students_total", "births", "gap"):
                vals = [float(item[key]) for item in obj if isinstance(item, dict) and key in item and isinstance(item[key], (int, float))]
                if vals:
                    out.add(round(sum(vals), 2))
                    out.add(round(sum(vals[:3]), 2))
                    out.add(round(sum(vals[:5]), 2))
        for v in obj:
            _collect_numbers(v, out)


def check(answer: str, dossier: Dict[str, Any], prompt: Optional[str] = None) -> Dict[str, Any]:
    allowed: Set[float] = set()
    _collect_numbers(dossier, allowed)
    if prompt:
        _collect_numbers(prompt, allowed)
    # 常見衍生：百分比 ↔ 比例、四捨五入到整數
    derived = set()
    for a in allowed:
        derived.add(round(a))
        derived.add(round(a, 1))
    allowed |= derived
    allowed |= {float(y) for y in range(100, 131)}   # 民國學年
    allowed |= {float(y) for y in range(2010, 2031)}
    allowed |= {25.0, 40.0, 60.0, 70.0, 80.0, 100.0}  # 教育部法規基準（生師比25/40、專輔預警60%、滿招100%）

    ungrounded: List[str] = []
    checked = 0
    for m in _NUM.finditer(answer):
        raw = m.group(1)
        try:
            val = float(raw.replace(",", ""))
        except ValueError:
            continue
        # 跳過序號「1.」「2.」與極小整數（條列編號）
        if val.is_integer() and 0 <= val <= 10 and "." not in raw:
            continue
        checked += 1
        if round(val, 2) not in allowed and round(val, 1) not in allowed and round(val) not in allowed:
            ungrounded.append(raw)
    return {"ok": not ungrounded, "checked": checked, "ungrounded": ungrounded}
