import copy
import csv
import json
import os
from pathlib import Path
import subprocess
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from ir_autopilot.src.ai import dossier, grounding
from ir_autopilot.src.ai.proactive_agent import ProactiveAgent
from ir_autopilot.src.ai.query_responses import school_response, peer_response, scope_response

ROOT = Path(__file__).resolve().parents[1]
DOSSIERS = json.loads((ROOT / 'netlify/functions/dossiers.json').read_text())
CASES = json.loads((ROOT / 'tests/fixtures/eval_cases.json').read_text())


def js(items):
    result = subprocess.run(['node', str(ROOT / 'tests/node_runner.mjs')], input=json.dumps(items), text=True, capture_output=True, check=True)
    return json.loads(result.stdout)


class RegressionTests(unittest.TestCase):
    def setUp(self):
        self.loader = patch('ir_autopilot.src.ai.proactive_agent.build_dossier', side_effect=lambda s: copy.deepcopy(DOSSIERS[s]))
        self.loader.start()
        self.addCleanup(self.loader.stop)
        self.agent = ProactiveAgent(SimpleNamespace(available=False))

    def ask(self, message, context=None):
        return self.agent.process_chat(message, context or {'default_slug': 'ib'})

    def test_shared_numeric_cases(self):
        cases = json.loads((ROOT / 'tests/fixtures/grounding_cases.json').read_text())
        results = js([dict(c, kind='grounding') for c in cases])
        for c, result in zip(cases, results):
            with self.subTest(answer=c['answer']):
                py = grounding.check(c['answer'], c['dossier'], c.get('prompt'))
                self.assertEqual(py, result)
                self.assertEqual(py['ok'], c['ok'])
                self.assertEqual(py['checked'], c['checked'])

    def test_peer_department_not_school_total(self):
        r = self.ask('高科企管最近如何')
        self.assertEqual(r['facts']['flow_records'], 10)
        self.assertEqual(r['facts']['years'], ['113', '114', '115'])
        self.assertIn('10 筆', r['response'])
        self.assertNotIn('37', r['response'])
        self.assertEqual(r['facts'], js([{'message':'高科企管最近如何'}])[0]['facts'])

    def test_full_school_totals(self):
        cases = [('高科',481),('北商',89),('逢甲',107),('勤益',84),('雲科',123)]
        results = js([{'message':f'{s}最近如何'} for s,_ in cases])
        for (name, count), node in zip(cases, results):
            r = self.ask(f'{name}最近如何')
            self.assertEqual(r['facts']['flow_records'], count)
            self.assertEqual(r['facts'], node['facts'])

    def test_college_ranking_and_gap(self):
        top = self.ask('商學院全院哪一個系註冊率最高')
        self.assertEqual(top['dept']['slug'], 'all')
        self.assertEqual(top['facts']['matched_slugs'], ['ba','finance','insurance','stat'])
        self.assertEqual(len(top['table']['rows']), 7)
        gap = self.ask('全院少子化在117年總共會少多少學生')
        self.assertEqual(gap['facts']['total_gap'], -122)
        self.assertEqual(gap['facts']['year'], 117)

    def test_cross_department_and_explicit_context_override(self):
        r = self.ask('國貿系與會資系註冊率比較')
        self.assertEqual(r['facts']['slugs'], ['ib','accounting'])
        self.assertEqual(len(r['table']['rows']), 2)
        self.assertEqual(self.ask('企管系註冊率', {'slug':'ib'})['dept']['slug'], 'ba')

    def test_greetings_and_pure_out_of_scope(self):
        for greeting in ['你好，','您好！','哈囉 ','早安，','嗨，']:
            self.assertEqual(self.ask(greeting+'企管系註冊率多少？')['intent'], 'overview')
        for q in ['你好','你好，明天天氣如何？','講個笑話給我聽']:
            self.assertEqual(self.ask(q)['intent'], 'out_of_scope')

    def test_requested_flow_year(self):
        # Independently count exported year + destination rows (no response helpers).
        rows = DOSSIERS['ba']['module5']['destinations']
        expected = sum(r['count'] for r in rows if r['year']=='114' and r['school']=='國立高雄科技大學' and r['dept']=='國立高雄科技大學企業管理系')
        r = self.ask('高科企管114學年最近如何')
        self.assertEqual(r['facts']['flow_records'], expected)
        self.assertEqual(r['facts']['years'], ['114'])
        self.assertNotEqual(expected, 10)

    def test_missing_year_and_missing_department_are_unknown(self):
        d = copy.deepcopy(DOSSIERS)
        del d['ba']['module5']['destinations']
        r = peer_response('ba','國立高雄科技大學',d,'高科企管最近如何')
        self.assertIsNone(r['facts']['flow_records'])
        self.assertIsNone(r['grounding']['ok'])
        r = self.ask('高科企管112學年最近如何')
        self.assertIsNone(r['facts']['flow_records'])

    def test_partial_college_cannot_publish_total(self):
        d = copy.deepcopy(DOSSIERS)
        d['tax']['demographics']['timeline'] = []
        args = {'message':'全院117年少子化缺口','intent':'demographics','dossiers':d,'slugs':list(dossier.SLUG_TO_NAME)}
        r = scope_response(**args)
        self.assertIsNone(r['facts']['total_gap'])
        self.assertEqual(r['facts']['missing'], ['tax'])
        self.assertIsNone(r['grounding']['ok'])
        self.assertEqual(r, js([dict(args,kind='scope')])[0])

    def test_mixed_indicator_years_no_false_difference(self):
        r = self.ask('北商應統最近如何')
        self.assertEqual(r['facts']['indicator_years'], [114,113])
        self.assertIn('學年不同', r['table']['rows'][0][3])
        node = js([{'message':'北商應統最近如何'}])[0]
        self.assertEqual(r, node)

    def test_threshold_scope(self):
        r = self.ask('哪一個系的生師比超過25警示值')
        self.assertEqual(r['facts']['matched_slugs'], ['ib','accounting','finance','stat','tax'])
        self.assertEqual(r['facts']['threshold'], 25)

    def test_original_50_cases_route_and_parity(self):
        node = js([{'message':c['query']} for c in CASES])
        for c, n in zip(CASES,node):
            with self.subTest(id=c['id'],query=c['query']):
                p = self.ask(c['query'])
                self.assertEqual(p['intent'], n['intent'])
                self.assertEqual(p['dept'], n['dept'])
                self.assertEqual(p['intent'],c['expected_intent'])
                if 'expect_dept' in c:
                    self.assertEqual(p['dept']['slug'],c['expect_dept'])
                if p.get('facts'):
                    self.assertEqual(p, n)

    def test_csv_etl_preserves_non_top5_and_dept_year(self):
        for new in [True,False]:
            with self.subTest(format='new' if new else 'legacy'), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)/'ba/raw_data'; root.mkdir(parents=True)
                cols = ['school_name','dest_school','dest_dept','category','status','year'] if new else ['最終分發學校','最終分發系所','分發去向分類','原系錄取別','學年度']
                records = []
                for i in range(7):
                    row = {'dest_school':f'學校{i}','dest_dept':'管理系','category':'其他學校','status':'正取','year':'114','school_name':'本校'} if new else {'最終分發學校':f'學校{i}','最終分發系所':'管理系','分發去向分類':'其他學校','原系錄取別':'正取','學年度':'114'}
                    records.extend([row]*(8-i))
                with (root/'01_測試流向.csv').open('w') as f:
                    writer=csv.DictWriter(f,fieldnames=cols);writer.writeheader();writer.writerows(records)
                with patch.object(dossier,'OUTPUT_DIR',tmp): m=dossier.compute_module5('ba','本校')
                self.assertEqual(len(m['top_destinations']),5)
                self.assertEqual(len(m['destinations']),7)
                self.assertEqual(sum(r['count'] for r in m['destinations']),len(records))
                self.assertEqual(m['destinations'][-1],{'school':'學校6','dept':'管理系','year':'114','count':2})

    def test_evaluator_does_not_pass_unknown_or_wrong_scope(self):
        from scratch.run_50_evals import evaluate_result
        case = next(c for c in CASES if c['id'] == 44)
        correct = self.ask(case['query'])
        self.assertTrue(evaluate_result(case, correct)['overall_pass'])
        for ground in [None, {}, {'ok': None}, {'ok': False}]:
            result = dict(correct, grounding=ground)
            self.assertFalse(evaluate_result(case, result)['overall_pass'])
        wrong = copy.deepcopy(correct)
        wrong['facts']['total_gap'] = -23
        self.assertFalse(evaluate_result(case, wrong)['overall_pass'])
        wrong = copy.deepcopy(correct)
        wrong['dept']['slug'] = 'ib'
        self.assertFalse(evaluate_result(case, wrong)['overall_pass'])

    def test_numbers_with_sentence_period_and_percentage_not_year(self):
        self.assertFalse(grounding.check('The rate is 9999.', {})['ok'])
        self.assertEqual(self.ask('高科企管註冊率100%嗎')['facts']['years'], ['113','114','115'])
        self.assertEqual(js([{'kind':'grounding','answer':'The rate is 9999.','dossier':{}}])[0],grounding.check('The rate is 9999.', {}))

    def test_export_rejects_missing_input_without_overwriting_bundle(self):
        from scripts.export_dossiers import export
        with tempfile.TemporaryDirectory() as tmp:
            destination=Path(tmp)/'dossiers.json'
            destination.write_text('original')
            with self.assertRaises(ValueError):
                export(Path(tmp)/'absent',destination)
            self.assertEqual(destination.read_text(),'original')

    @unittest.skipUnless(os.environ.get('IR_TEST_OUTPUT_DIR'), 'Set IR_TEST_OUTPUT_DIR to audit original CSV inputs')
    def test_export_matches_source_files(self):
        from scripts.export_dossiers import export
        with tempfile.TemporaryDirectory() as tmp, patch.object(dossier,'OUTPUT_DIR',dossier.OUTPUT_DIR):
            actual=export(Path(os.environ['IR_TEST_OUTPUT_DIR']),Path(tmp)/'bundle.json')
            self.assertEqual(actual,DOSSIERS)


    def test_export_is_aggregate_only(self):
        for d in DOSSIERS.values():
            for r in d['module5']['destinations']:
                self.assertEqual(set(r), {'school','dept','year','count'})
            self.assertEqual(sum(r['count'] for r in d['module5']['destinations']),d['module5']['poached'])


if __name__ == '__main__':
    unittest.main()
