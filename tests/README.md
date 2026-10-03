# IR correctness regression checks

Run from the repository root (Python 3.10+ and Node required):

```sh
uv run --with requests python -m unittest discover -s tests -v
```

The suite exercises the actual Python agent and Netlify handler offline against the same
aggregate dossier bundle. It includes the original 50 routing cases, audited numeric
expectations, Chinese numeric tokenization, precise destination departments, selected
years, complete school totals, all-college ranking/projection, missing data, greetings,
new/legacy CSV formats, and evaluator false-positive regressions. No model API is called.

To also compare the committed bundle with original local source files:

```sh
IR_TEST_OUTPUT_DIR=/absolute/path/to/output uv run --with requests python -m unittest discover -s tests -v
```

Export a new aggregate bundle without deploying:

```sh
python3 scripts/export_dossiers.py --output-dir /absolute/path/to/output
```

Every department must contain `dept_data.json` and an `01_*流向*.csv` in `raw_data/`.
The export preserves school, destination department, year, and record counts. It exports
no candidate names or identifiers. Missing required data fails before replacing the
previous bundle. Top 5 is only for display; queries use the complete aggregates.

Run the 50-case evaluator separately:

```sh
IR_OUTPUT_DIR=/absolute/path/to/output uv run --with requests python scratch/run_50_evals.py
```

It defaults to offline operation. `--live` explicitly enables the configured model.
The report separates structural checks, verified assertions, unverified answers, and
failures. Unverified answers do not count as PASS and cause a nonzero exit code.
Current offline snapshot: 50 structural passes, 24 verified/not-applicable passes,
26 unverified, 0 failures. This is a functional evaluation, not a load test or an
end-to-end model accuracy measurement.

Golden expectations in `fixtures/eval_cases.json` were checked against the reviewed
source snapshot: school totals NKUST 481, NTUB 89, FCU 107, NCUT 84, YunTech 123 records;
NKUST business administration destination 10 records across 113–115; college 117 gap
-122; 114 enrollment leaders BA/finance/insurance/stat at 100%. Re-audit expectations
when source data changes rather than copying current responses into the fixture.

`grounding.method = numeric_only` checks numeric provenance at reported precision.
It deliberately does not claim to validate prose semantics or causality. Prompt values,
unrelated years, regulatory constants, and arbitrary array sums are not evidence.
Structured responses and independent scope/value/year assertions cover the reviewed
aggregation bugs. Free-form model prose still requires semantic evaluation.
