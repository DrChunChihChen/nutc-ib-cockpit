"""Functional IR evaluation, not a load test. Unverified answers never count as PASS.

Default: offline (no API calls). --live enables the configured model explicitly.
Golden assertions are from the audited source snapshot; update them only after a
source audit, never by copying the system's latest answer into expected values.
"""
import argparse
import json
from pathlib import Path
import sys
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
CASES_PATH = ROOT / 'tests/fixtures/eval_cases.json'


def evaluate_result(case, result):
    chart, table = result.get('chart'), result.get('table')
    checks = {'intent': result.get('intent') == case['expected_intent']}
    if case.get('expected_chart') is not None:
        checks['chart'] = bool(chart) == case['expected_chart']
    if 'expect_table' in case:
        checks['table'] = bool(table and table.get('rows')) == case['expect_table']
    if case.get('expect_dept'):
        checks['dept'] = result.get('dept', {}).get('slug') == case['expect_dept']
    if case.get('expect_prompt_disambig'):
        checks['disambiguation'] = '所有的系所' in result.get('response', '')
    expected = case.get('expected_facts')
    ground_ok = (result.get('grounding') or {}).get('ok')
    # A model's own ok flag is not an independent factuality oracle.
    factuality = 'unverified'
    if expected:
        facts = result.get('facts') or {}
        correct = all(facts.get(key) == value for key, value in expected.items())
        factuality = 'verified' if correct and ground_ok is True else 'failed' if not correct or ground_ok is False else 'unverified'
    elif result.get('intent') == 'out_of_scope' and ground_ok is True and not chart and not table:
        factuality = 'not_applicable'
    elif ground_ok is False:
        factuality = 'failed'
    structural_ok = all(checks.values())
    return {'id':case['id'], 'query':case['query'], 'checks':checks, 'structural_ok':structural_ok,
            'factuality':factuality, 'overall_pass':structural_ok and factuality in ('verified','not_applicable'),
            'grounding':result.get('grounding'), 'response_preview':result.get('response','')[:300]}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--live', action='store_true')
    p.add_argument('--report', type=Path, default=ROOT / 'scratch/evaluation_50_report.json')
    args = p.parse_args()
    from ir_autopilot.src.ai.proactive_agent import ProactiveAgent
    agent = ProactiveAgent() if args.live else ProactiveAgent(SimpleNamespace(available=False))
    cases = json.loads(CASES_PATH.read_text())
    results = []
    for case in cases:
        try:
            result = agent.process_chat(case['query'], {'default_slug':'ib'})
            results.append(evaluate_result(case, result))
        except Exception as exc:
            results.append({'id':case['id'],'query':case['query'],'overall_pass':False,'structural_ok':False,'factuality':'failed','error':str(exc)})
    counts = {'total':len(results),'structural_pass':sum(r['structural_ok'] for r in results),
              'verified_pass':sum(r['overall_pass'] for r in results),
              'unverified':sum(r['factuality']=='unverified' for r in results),
              'failed':sum(not r['structural_ok'] or r['factuality']=='failed' for r in results)}
    args.report.parent.mkdir(parents=True,exist_ok=True)
    args.report.write_text(json.dumps({'mode':'live' if args.live else 'offline','summary':counts,'results':results},ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(counts,ensure_ascii=False))
    return 0 if all(r['overall_pass'] for r in results) else 1


if __name__ == '__main__':
    sys.exit(main())
