# Project Charter — ECO 6810 Final Project

## Header

| Field | Value |
|-------|-------|
| Team members | Ujjwal Kumar, Piyush Pushpad
| Project type | Descriptive |
| Estimated hours per person | 45–50 hours |
| Charter version | v1 |
| Date | 2026-05-06 |

---

## 1. Problem and stakeholder

The Ministry of Home Affairs (MHA), Government of India, needs a data-driven summary of state-wise crime patterns to decide where to allocate central police modernisation funds under the Modernisation of Police Forces (MPF) scheme for FY 2026-27. Currently, allocation decisions rely on raw crime counts, which systematically over-fund large states and under-fund high-risk smaller ones. This project provides a per-capita crime rate analysis across 34 states and UTs (2001–2012) that gives the MHA a fairer basis for resource allocation decisions.

---

## 2. Main outcome variable

- **Name:** State-level IPC crime rate
- **Unit:** Reported IPC cases per lakh population, per year
- **Source:** NCRB — `01_District_wise_crimes_committed_IPC_2001_2012.csv`, column `TOTAL IPC CRIMES`, rows where `DISTRICT = "TOTAL"`, normalised by state population
- **Population / panel:** 34 Indian states and UTs, years 2001–2012, aggregated to state level

---

## 3. Main quantitative success threshold

**Descriptive:** Produce stratified estimates of IPC crime rate (cases per lakh) across N ≥ 30 state/UT strata, for each of 12 years (2001–2012), with documented percentage change from baseline year (2001) to end year (2012) for each stratum.

The project is a success if:
- Crime rate estimates are produced for ≥ 30 states
- At least 10 crime categories are stratified separately
- The nationwide percentage change 2001→2012 is computed and reported with the exact case counts used

Current preliminary value: **+27.48%** (total IPC crimes, 2001→2012)

---

## 4. Baseline to beat

**National average IPC crime rate in 2001: 65.63 cases per lakh population.**

This is computed directly from the NCRB data:
- Total IPC cases in 2001 across all states: 928,060
- Total population covered: ~1,414 million
- Baseline rate = 928,060 / (1,414M / 100,000) = 65.63

All trend analysis and state comparisons are measured against this baseline. States above 65.63 in any given year are flagged as high-risk. This was computed before any modelling using `main.py`.

---

## 5. Falsifiable hypothesis

States with higher population density (proxied by total population) will **not** necessarily have higher per-capita crime rates — at least 5 of the top 10 highest per-capita crime states in 2012 will be mid-sized states (population < 50 million), not the largest states (UP, Maharashtra, Bihar).

---

## 6. Data sources and access plan

**Source 1 — NCRB District-wise IPC Crimes 2001–2012**
- URL: https://www.kaggle.com/datasets/rajanand/crime-in-india
- Licence: Government of India Open Data (public domain)
- Access: Direct CSV download from Kaggle (free account required)
- File: `01_District_wise_crimes_committed_IPC_2001_2012.csv`
- Size: ~9,000 rows, 33 columns

Probe (10-line access check):
```python
import pandas as pd
df = pd.read_csv("data/01_District_wise_crimes_committed_IPC_2001_2012.csv")
state_totals = df[df["DISTRICT"] == "TOTAL"]
print(state_totals[["STATE/UT","YEAR","TOTAL IPC CRIMES"]].head(1))
# Expected output: ANDHRA PRADESH | 2001 | 130089
```

Full probe: `uv run artifacts/probes/probe_ncrb.py`

No login walls, no scraping, no authentication beyond a free Kaggle account. Data is committed under `data/crime_data.csv` (cleaned version).

---

## 7. Scope limits

- We will not estimate any causal effect of policing policy on crime rates.
- We will not harmonise district boundaries across years; analysis is at state level only.
- We will not cover years beyond 2012 (data availability limit of this NCRB file).
- We will not model socioeconomic drivers of crime (poverty, unemployment, etc.).
- We will not produce confidence intervals or standard errors — this is a descriptive census of reported crimes, not a sample survey.
- We will not cover unreported crimes or dark figures.
- Secondary outcomes (crime type breakdowns, safest states, fastest-growing crime) will be reported in the dashboard but are not the primary graded metric.

---

## 8. Risks and fallback

**Risk:** The NCRB 2001–2012 dataset covers only reported IPC crimes. If the instructor determines this time range is too narrow for meaningful trend analysis, we will supplement with the NCRB 2013–2014 files from the same Kaggle dataset (already downloaded) to extend coverage to 2014, and document the join methodology.

**Fallback:** If population data introduces normalisation errors (population estimates are static 2021 Census figures, not year-specific), we will fall back to reporting absolute IPC crime counts alongside per-capita rates and clearly note the limitation in the report.

---

## 9. Reproducibility checklist

- [x] `uv run main.py` runs end-to-end in under 10 minutes on a clean machine with no manual intervention.
- [x] It writes `outputs/primary_metric.json` containing `{"metric_name": "pct_change_total_ipc_crimes_2001_to_2012", "value": 27.48, "threshold": 0, "passed": true}`.
- [x] It writes `outputs/baseline_metric.json` containing `{"metric_name": "national_avg_crime_rate_per_lakh_2001", "value": 65.63, "threshold": null, "passed": null}`.
- [x] `README.md` documents the commands and expected outputs in ≤ 20 lines.
- [x] Data is committed under `data/crime_data.csv` with licence note (Government of India Open Data).

---

## Sign-off

By submitting this charter, the team agrees that this is the plan the project will be graded against.

Signed: Ujjwal Kumar, Piyush Pushpad
