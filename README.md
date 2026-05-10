# India Crime Intelligence Dashboard — ECO6810

An interactive dashboard analysing crime patterns across India using NCRB data (2001–2012).

## Run Commands

**Step 1 — Install dependencies and run analysis:**
```bash
uv sync
uv run main.py
```

**Step 2 — Launch interactive dashboard:**
```bash
uv run streamlit run app.py
```
Opens at http://localhost:8501

## Expected Output Files

| File | Description |
|------|-------------|
| `outputs/baseline_metric.json` | National avg crime rate per lakh in 2001 (65.63) |
| `outputs/primary_metric.json` | % change in IPC crimes 2001→2012 (+27.5%) |
| `outputs/supporting_analysis.json` | Top states, crime shares, growth rates |
| `outputs/milestone_manifest.json` | Project status and data source details |

## Data Source

- **Name:** NCRB District-wise IPC Crimes 2001–2012
- **File:** `data/crime_data.csv` (committed, 4,896 rows)
- **Origin:** https://www.kaggle.com/datasets/rajanand/crime-in-india
- **Licence:** Government of India Open Data (public domain)
- **Probe:** `uv run artifacts/probes/probe_ncrb.py`

## Project Structure

```
├── main.py                        ← Reproducible run entry point
├── app.py                         ← Streamlit dashboard
├── project_code/
│   ├── data_cleaning.py           ← Data loading and cleaning
│   ├── analysis.py                ← Analysis functions
│   └── prediction.py             ← Linear regression forecast model
├── data/
│   └── crime_data.csv            ← Cleaned NCRB data (2001–2012)
├── outputs/                       ← All JSON outputs
├── artifacts/probes/              ← Data source probe
│   └── probe_ncrb.py
├── CHARTER.md                     ← Project plan
├── report.md                      ← Final written report
└── AI_USAGE_LOG.md               ← AI usage declaration
```

## Team

| Name | GitHub | Role |
|------|--------|------|
| Ujjwal Kumar | Ujjwalkumar2025 | Data cleaning, analysis, main.py, dashboard |
| Piyush | piyush17-ux | Visualisation, report, testing, GitHub |
