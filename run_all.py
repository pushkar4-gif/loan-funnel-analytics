"""Rebuild everything:  python run_all.py   (add --llm to let an LLM write the daily digests)"""
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
STEPS = [
    "src/generate_data.py",        # synthetic multi-lender loan funnel (seeded, reproducible)
    "src/run_sql.py",              # BigQuery SQL → DuckDB marts + data-quality checks
    "src/alert_eval.py",           # p-chart alerts scored vs incident log
    "src/call_prioritization.py",  # uplift model for the call-centre queue
    "src/lender_criteria.py",      # lender-criteria negotiation evidence
    "src/daily_digest.py",         # automated morning digest (template, or LLM with --llm)
    "src/build_bi_extracts.py",    # small CSVs for Power BI / Looker
    "src/make_figures.py",         # README charts
]

for s in STEPS:
    print(f"\n=== {s} ===", flush=True)
    extra = sys.argv[1:] if s.endswith("digest.py") else []
    subprocess.run([sys.executable, str(ROOT / s), *extra], check=True, cwd=ROOT)
