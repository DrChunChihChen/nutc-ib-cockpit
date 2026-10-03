"""
Grounding check: 回答中的每個數字都必須能在 dossier 中找到（容忍四捨五入）。
回傳 {"ok": bool, "checked": n, "ungrounded": [...]}，供 UI 顯示警告。
"""
import json
import re
from typing import Any, Dict, List, Set

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
        for v in obj:
            _collect_numbers(v, out)


def check(answer: str, dossier: Dict[str, Any]) -> Dict[str, Any]:
    allowed: Set[float] = set()
    _collect_numbers(dossier, allowed)
    # 常見衍生：百分比 ↔ 比例、四捨五入到整數
    derived = set()
    for a in allowed:
        derived.add(round(a))
        derived.add(round(a, 1))
    allowed |= derived
    allowed |= {float(y) for y in range(100, 131)}   # 民國學年
    allowed |= {float(y) for y in range(2010, 2031)}

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
