"""Deterministic, source-scoped responses. Keep parity with netlify/functions/lib/query-responses.mjs."""
import re
from .dossier import DEPT_ALIASES, SLUG_TO_NAME


def number(value):
    return '—' if value is None else f'{value:g}' if isinstance(value, (float, int)) else str(value)


def normalize(text):
    return (text or '').replace('台', '臺').removeprefix('國立').strip()


def same_school(a, b):
    return normalize(a) == normalize(b)


def same_dept(dept, school, target):
    value = normalize(dept)
    prefix = normalize(school)
    if value.startswith(prefix):
        value = value[len(prefix):]
    return value == normalize(target)


def selected_slugs(message):
    remaining = message
    selected = set()
    for alias in sorted(DEPT_ALIASES, key=len, reverse=True):
        if alias in remaining:
            selected.add(DEPT_ALIASES[alias])
            remaining = remaining.replace(alias, '')
    if re.search(r'全院|商學院|全校|各系|哪(?:一)?個系|哪些系|院長', message):
        return list(SLUG_TO_NAME)
    return [s for s in SLUG_TO_NAME if s in selected]


def requested_year(message):
    match = re.search(r'(?<!\d)(1\d{2})\s*(?:學年度|學年|年度|年)', message)
    return int(match[1]) if match else None


def flow(d, school, dept=None, year=None):
    m = d.get('module5') or {}
    years = [str(year)] if year is not None else [str(y) for y in m.get('years', [])]
    available = 'destinations' in m and bool(years) and all(y in [str(v) for v in m.get('years', [])] for y in years)
    rows = [r for r in m.get('destinations', []) if same_school(r['school'], school) and str(r['year']) in years]
    # An unknown destination department must not silently become zero for a named department.
    if dept is not None and any(not r.get('dept') or r['dept'] == '—' for r in rows):
        available = False
    count = sum(r['count'] for r in rows if dept is None or same_dept(r['dept'], r['school'], dept)) if available else None
    return {'count': count, 'years': years, 'unit': 'records', 'source': m.get('source')}


def period(years):
    return '、'.join(map(str, years)) + ' 學年' if years else '期間未知'


def response(intent, text, table, facts, slugs, data_time):
    all_scope = len(slugs) > 1
    complete = facts.get('complete', True)
    return {
        'intent': intent,
        'dept': {'slug': 'all' if all_scope else slugs[0], 'name': '商學院全院' if len(slugs) == len(SLUG_TO_NAME) else '跨系比較' if all_scope else SLUG_TO_NAME[slugs[0]], 'school': '國立臺中科技大學'},
        'response': text, 'table': table, 'chart': None, 'facts': facts,
        'model': 'rule-based-ir-engine', 'reasoning': '按查詢範圍與資料期間直接計算。',
        'grounding': {'ok': True if complete else None, 'method': 'structured_sources', 'checked': len(table['rows']), 'ungrounded': [], 'note': '數值由來源欄位計算；缺少資料時不宣稱完整。'},
        'source': 'UDB 系所指標／交叉查榜／出生數推估（各列標示期間）',
        'drilldown_link': 'heatmap.html' if all_scope else f'{slugs[0]}/index.html', 'data_time': data_time,
    }


def school_response(school, dossiers, message):
    year = requested_year(message)
    rows, flows, years = [], {}, set()
    for slug in SLUG_TO_NAME:
        d = dossiers.get(slug, {})
        f = flow(d, school, year=year)
        flows[slug] = f
        for p in d.get('peers', []):
            if not same_school(p.get('school'), school):
                continue
            py = p.get('year')
            visible = year is None or str(py) == str(year)
            years.add(str(py) if py is not None else '未知')
            rows.append([SLUG_TO_NAME[slug], p['dept'], f'{py} 學年' if visible else f'缺 {year} 學年（收錄 {py}）',
                         number(p.get('enrollment_rate')) + '%' if visible else '—',
                         number(p.get('dropout_rate')) + '%' if visible else '—',
                         number(p.get('faculty_ratio')) if visible else '—',
                         number(p.get('students_total')) if visible else '—',
                         number(f['count']), period(f['years'])])
    available = [f['count'] for f in flows.values() if f['count'] is not None]
    complete = len(available) == len(SLUG_TO_NAME)
    total = sum(available) if complete else None
    flow_years = sorted({y for f in flows.values() for y in f['years']})
    text = f'{school}：本院資料庫收錄 {len(rows)} 組系所對接；指標學年逐列標示。\n\n'
    text += f'交叉查榜（{period(flow_years)}）向該校外流共 **{total} 筆**。' if complete else '交叉查榜資料不完整，無法提供全院外流總數。'
    text += '跨系紀錄未去重，不代表不重複人數；表內外流為流向該校所有系所的紀錄。\n\n'
    text += '請問您詢問的是上述哪一個特定系所？還是系統中該校所有的系所？'
    facts = {'complete': complete, 'school': school, 'flow_records': total, 'flows': flows, 'years': flow_years}
    return response('school_intelligence', text, {'title': f'{school} 對接清冊',
                    'headers': ['本院系所', '同儕系所', '指標學年', '註冊率', '退學率', '生師比', '在學人數', '流向整校紀錄（筆）', '查榜期間'], 'rows': rows}, facts, list(SLUG_TO_NAME), f'指標：{period(sorted(years))}；查榜：{period(flow_years)}')


def peer_response(slug, school, dossiers, message):
    d = dossiers[slug]
    p = next((p for p in d.get('peers', []) if same_school(p.get('school'), school)), None)
    if p is None:
        return None
    year = requested_year(message)
    own_year, peer_year = d['meta'].get('latest_year'), p.get('year')
    f = flow(d, school, p['dept'], year)
    rows = []
    metrics = [('新生註冊率', 'K01', 'enrollment_rate', '%', 'UDB 學12-1'), ('學年度退學率', 'K03', 'dropout_rate', '%', 'UDB 學14-1'), ('專任生師比', 'K06', 'faculty_ratio', '', 'UDB 教1-1')]
    for label, key, field, unit, source in metrics:
        own = d.get('kpis', {}).get(key, {}).get('value') if year is None or str(own_year) == str(year) else None
        other = p.get(field) if year is None or str(peer_year) == str(year) else None
        comparable = own is not None and other is not None and own_year is not None and str(own_year) == str(peer_year)
        diff = number(round(own - other, 2)) + (' 個百分點' if unit == '%' else '') if comparable else '學年不同或資料不足，不計差距'
        rows.append([label, number(own) + unit, number(other) + unit, diff, source])
    rows.append(['流向該校該系紀錄', '—', number(f['count']) + ' 筆', period(f['years']), f['source'] or '資料缺失'])
    text = f"{SLUG_TO_NAME[slug]}（{own_year} 學年）與{school}{p['dept']}（{peer_year} 學年）指標如下。"
    text += f"\n交叉查榜（{period(f['years'])}）：流向{school}{p['dept']}共 **{f['count']} 筆**。" if f['count'] is not None else '\n缺少指定期間或目的系所資料，無法計算流向該系的紀錄。'
    text += '紀錄未跨年度去重，不代表不重複人數。'
    complete = f['count'] is not None and (year is None or (str(own_year) == str(year) and str(peer_year) == str(year)))
    return response('peer_comparison', text, {'title': '系所實證對比', 'headers': ['指標', f'本系（{own_year}）', f"{p['dept']}（{peer_year}）", '本系減同儕／期間', '來源'], 'rows': rows},
                    {'complete': complete, 'school': school, 'peer_dept': p['dept'], 'flow_records': f['count'], 'years': f['years'], 'indicator_years': [own_year, peer_year]}, [slug], f'指標：{own_year}／{peer_year} 學年；查榜：{period(f["years"])}')


def scope_response(message, intent, dossiers, slugs):
    """Aggregate only matching years. Missing rows remain visible and prevent full totals."""
    year = requested_year(message)
    rows, missing, values = [], [], []
    demo = intent == 'demographics'
    key, label, unit = ('K06', '生師比', '') if '生師比' in message else ('K03', '退學率', '%') if '退學' in message else ('K05', '淨流失率', '%') if '淨流失' in message else ('K01', '新生註冊率', '%')
    if demo:
        year = year or 117
    else:
        known_years = {dossiers.get(s, {}).get('meta', {}).get('latest_year') for s in slugs} - {None}
        year = year or (max(known_years) if known_years else None)
    for slug in slugs:
        d = dossiers.get(slug, {})
        if demo:
            t = next((t for t in d.get('demographics', {}).get('timeline', []) if str(t.get('year')) == str(year)), {})
            val = t.get('gap')
            valid = all(t.get(k) is not None for k in ['gap', 'capacity', 'est_baseline'])
            rows.append([SLUG_TO_NAME[slug], year, t.get('capacity'), t.get('est_baseline'), val, d.get('demographics', {}).get('source', '缺少資料')])
        else:
            k = d.get('kpis', {}).get(key, {})
            valid = year is not None and str(d.get('meta', {}).get('latest_year')) == str(year) and k.get('value') is not None
            val = k.get('value') if valid else None
            rows.append([SLUG_TO_NAME[slug], year, val, unit, k.get('source_id', '缺少資料')])
        if not valid:
            missing.append(slug)
        else:
            values.append((slug, val))
    complete = not missing
    facts = {'complete': complete, 'slugs': slugs, 'year': year, 'missing': missing, 'metric': 'gap' if demo else key,
             'values': dict(values)}
    scope = '全院' if len(slugs) == len(SLUG_TO_NAME) else '所選系所'
    if demo:
        total = sum(v for _, v in values) if complete else None
        facts['total_gap'] = total
        text = f'{scope} {year} 學年基準推估缺口合計 {number(total)} 人（推估入學數減核定名額）。' if complete else f'{year} 學年有系所缺少推估，無法提供{scope}總缺口。'
        headers = ['系所', '學年', '名額', '基準推估', '缺口（人）', '來源']
    else:
        text = f'{scope} {year} 學年{label}比較如下。'
        threshold = re.search(r'(?:超過|大於|高於)\s*(\d+(?:\.\d+)?)', message)
        if threshold:
            cutoff = float(threshold[1])
            matched = [s for s, v in values if v > cutoff]
            facts.update({'threshold': cutoff, 'matched_slugs': matched})
            text += '已收錄資料中超過提問門檻的系所：' + ('、'.join(SLUG_TO_NAME[s] for s in matched) or '無') + '。'
        elif values and ('最高' in message or '最低' in message):
            best = (min if '最低' in message else max)(v for _, v in values)
            matched = [s for s, v in values if v == best]
            facts['matched_slugs'] = matched
            text += '已收錄資料中' + ('最低' if '最低' in message else '最高') + '為' + '、'.join(SLUG_TO_NAME[s] for s in matched) + f'（{number(best)}{unit}）。'
        headers = ['系所', '學年', label, '單位', '來源']
    if missing:
        text += '缺少同年資料：' + '、'.join(SLUG_TO_NAME[s] for s in missing) + '。'
    result = response('demographics' if demo else 'overview', text, {'title': f'{scope}同年比較', 'headers': headers, 'rows': rows}, facts, slugs, f'{year} 學年')
    result['chart'] = {'type': 'bar', 'title': f'{scope}{"推估缺口" if demo else label}', 'labels': [SLUG_TO_NAME[s] for s in slugs], 'datasets': [{'label': '缺口（人）' if demo else label, 'data': [dict(values).get(s) for s in slugs]}]}
    return result
