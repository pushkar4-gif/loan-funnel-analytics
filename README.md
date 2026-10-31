# Loan Funnel Analytics

Analytics pipeline for a multi-lender personal loan funnel (lead → application → approval → disbursal) across 4 lending partners. Covers funnel reporting, drop-off alerts, call-centre prioritisation, lender approval analysis and automated reporting.

The data is synthetic (236K leads, Apr–Sep 2026), generated with a fixed seed so every run gives the same results.

![Funnel](docs/figures/funnel.png)

## Results

| Area | Approach | Result |
|---|---|---|
| Funnel | Stage conversion by month, channel and lender (SQL) | 13.9% lead-to-disbursal; largest drop is lead → application start (51%) |
| Alerts | Daily p-chart on stage rates (14-day baseline, 3σ limit) | Caught all 3 test incidents on day 1; 0.12 false alerts/week vs 6.7 for a fixed 10% rule |
| Call prioritisation | T-learner uplift model (gradient boosting) on randomised call data | Ranking by uplift × ticket size gave 3.1× the incremental disbursal of random calling |
| Lender criteria | 90+ DPD comparison with 95% CIs | Segment rejected by Lender B repaid at 1.8% vs 2.1% for its own book |
| Drop-off recovery | Recoverable value by funnel stage | ₹36.5 Cr across the last 30 days of drop-offs |

![Alert](docs/figures/alert_android.png)
![Call policies](docs/figures/call_policies.png)

## Run

```bash
pip install -r requirements.txt
python run_all.py
pytest -q
```

`run_all.py` generates the data, runs the SQL, trains the models and writes outputs and charts. The full data files are not committed; samples are in `data/sample/`.

Optional: `python run_all.py --llm` writes the daily digest with an LLM (needs `anthropic` and `ANTHROPIC_API_KEY`). Any number in the LLM text that isn't in the source data makes it fall back to the template.

## Structure

```
src/            data generation, SQL runner, alert evaluation, uplift model, lender analysis, digest, charts
sql/            8 queries in BigQuery SQL, run locally on DuckDB via sqlglot
apps_script/    Google Sheets script that emails daily alerts
outputs/        query results, model evaluation, CSV extracts for Power BI
docs/           decision memo, metric definitions, charts
tests/          pytest checks
```

## Tech

Python (pandas, scikit-learn, SciPy), SQL (BigQuery dialect, DuckDB), matplotlib, Google Apps Script, GitHub Actions.
