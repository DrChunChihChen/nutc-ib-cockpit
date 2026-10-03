"""Numeric provenance check, not a guarantee of semantic or causal correctness.

Only dossier values are evidence. Prompt numbers and arbitrary array sums are not.
Keep behavior aligned with grounding.mjs, including ASCII token boundaries.
"""
import math
import re
from typing import Any, Dict, Optional

_NUM = re.compile(r'(?<![A-Za-z0-9_.])(-?\d{1,3}(?:,\d{3})+(?:\.\d+)?|-?\d+(?:\.\d+)?)(?!\d|\.\d|[A-Za-z_])')

def _text(text):
    text = re.sub(r'^\s*\d+[.)、]\s+', '', text, flags=re.MULTILINE)
    text = re.sub(r'(?:UDB\s*)?[學教]\d+(?:-\d+)?', '', text)
    # pp is a numeric unit, not an identifier suffix.
    return re.sub(r'(?<=\d)pp\b', ' 個百分點', text)


def _collect_numbers(obj: Any, out: set) -> None:
    if isinstance(obj, bool):
        return
    if isinstance(obj, (int, float)):
        if math.isfinite(obj):
            out.add(float(obj))
    elif isinstance(obj, str):
        out.update(float(m.replace(',', '')) for m in _NUM.findall(_text(obj)))
    elif isinstance(obj, dict):
        for v in obj.values():
            _collect_numbers(v, out)
    elif isinstance(obj, (list, tuple)):
        for v in obj:
            _collect_numbers(v, out)


def check(answer: str, dossier: Dict[str, Any], prompt: Optional[str] = None) -> Dict[str, Any]:
    allowed = set()
    _collect_numbers(dossier, allowed)
    ungrounded, checked = [], 0
    for m in _NUM.finditer(_text(answer)):
        raw = m[1]
        value = float(raw.replace(',', ''))
        precision = len(raw.split('.')[1]) if '.' in raw else 0
        scale = 10 ** min(precision, 8)
        checked += 1
        # Round source values to the precision the answer actually reports.
        # Do not round both sides to integers (99.01 must not validate 99.49).
        if not any(abs(math.floor(a * scale + 0.5 + 1e-8) / scale - value) < 1e-8 for a in allowed):
            ungrounded.append(raw)
    return {'ok': not ungrounded, 'checked': checked, 'ungrounded': ungrounded,
            'method': 'numeric_only', 'note': '僅驗證數值是否存在於來源；不代表指標、系所、學年或語意已核實。'}
