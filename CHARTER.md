# Project Charter — ECO 6810 Final Project

## Header

| Field | Value |
|-------|-------|
| Team members | Ujjwal Kumar (ujjwal.kumar_ma2024@ashoka.edu.in), Piyush Pushpad (piyush.pushpad_ma2025@ashoka.edu.in) |
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
- **Source:** NCRB — `01_District_wise_crimes_committed_IPC_2001_2012.csv`, rows where `DISTRICT = "TOTAL"`, normalised by state population
- **Population / panel:** 34 Indian states and UTs, years 2001–2012, aggregated to state level

---

## 3. Main quantitative success threshold

**Descriptive:** Produce stratified estimates of IPC crime rate (cases per lakh) across N ≥ 30 state/UT strata, for each of 12 years (2001–2012), with documented percentage change from baseline year (2001) to end year (2012) for each stratum.

The project is a success if:
- Crime rate estimates are produced for ≥ 30 states
- At least 10 crime categories are stratified separately
- The nationwide % change 2001→2012 is computed with exact case counts

**Current value: +27.48%** (total IPC crimes, 2001→2012)

---

## 4. Baseline to beat

**National average IPC crime rate in 2001: 65.63 cases per lakh population.**

- Total IPC cases in 2001: 864,197
- Total population covered: ~1,317 million
- Baseline rate = 864,197 / (1,317 × 10) = 65.63

Computed directly from NCRB data before any modelling. See `outputs/baseline_metric.json`.

---

## 5. Falsifiable hypothesis

At least 5 of the top 10 highest per-capita crime states in 2012 will be mid-sized states (population < 50 million), not the largest states (UP, Maharashtra, Bihar) — showing that absolute crime counts mislead resource allocation.

---

## 6. Data sources and access plan

**Source 1 — NCRB District-wise IPC Crimes 2001–2012**
- URL: https://www.kaggle.com/datasets/rajanand/crime-in-india
- Licence: Government of India Open Data (public domain)
- Access: Direct CSV download from Kaggle (free account)
- File committed: `data/crime_data.csv` (cleaned, 4,896 rows)

Probe:
```python
# artifacts/probes/probe_ncrb.py
import pandas as pd
df = pd.read_csv("data/crime_data.csv")
state_totals = df[df["Year"] == 2001]
print(state_totals[["State","Year","Cases_Reported"]].head(1))
# Expected: Andhra Pradesh | 2001 | some positive integer
```

Run: `uv run artifacts/probes/probe_ncrb.py`

---

## 7. Scope limits

- We will not estimate causal effects of policing policy on crime rates
- We will not harmonise district boundaries; analysis is at state level only
- We will not cover years beyond 2012 (data file limit)
- We will not model socioeconomic drivers of crime
- We will not produce confidence intervals — this is a descriptive census
- Secondary outcomes (crime type breakdowns, forecasts) are reported but not the primary graded metric

---

## 8. Risks and fallback

**Risk:** NCRB 2001–2012 covers only reported IPC crimes; unreported crimes are excluded.

**Fallback:** If population data introduces normalisation errors, we fall back to absolute IPC crime counts and clearly note the limitation in the report.

---

## 9. Reproducibility checklist

- [x] `uv run main.py` runs end-to-end in under 10 minutes on a clean machine
- [x] Writes `outputs/primary_metric.json` with `metric_name`, `value`, `threshold`, `passed`
- [x] Writes `outputs/baseline_metric.json` with same schema
- [x] `README.md` documents run command and expected outputs in ≤ 20 lines
- [x] Data committed under `data/crime_data.csv` with licence note

---

## Team Roles

| Member | GitHub | Responsibility |
|--------|--------|----------------|
| Ujjwal Kumar | Ujjwalkumar2025 | ujjwal.kumar_msc2024@ashoka.edu.in | Data cleaning, analysis, main.py, dashboard |
| Piyush Pushpad | piyush17-ux | piyush.pushpad_ma2025@ashoka.edu.in |Visualization, report, testing, GitHub |

---

## Sign-off

Signed: Ujjwal Kumar, Piyush Pushpad
# Project Charter — ECO 6810 Final Project

## Header

| Field | Value |
|-------|-------|
| Team members | Ujjwal Kumar (ujjwal.kumar_ma2024@ashoka.edu.in), Piyush Pushpad (piyush.pushpad_ma2025@ashoka.edu.in) |
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
- **Source:** NCRB — `01_District_wise_crimes_committed_IPC_2001_2012.csv`, rows where `DISTRICT = "TOTAL"`, normalised by state population
- **Population / panel:** 34 Indian states and UTs, years 2001–2012, aggregated to state level

---

## 3. Main quantitative success threshold

**Descriptive:** Produce stratified estimates of IPC crime rate (cases per lakh) across N ≥ 30 state/UT strata, for each of 12 years (2001–2012), with documented percentage change from baseline year (2001) to end year (2012) for each stratum.

The project is a success if:
- Crime rate estimates are produced for ≥ 30 states
- At least 10 crime categories are stratified separately
- The nationwide % change 2001→2012 is computed with exact case counts

**Current value: +27.48%** (total IPC crimes, 2001→2012)

---

## 4. Baseline to beat

**National average IPC crime rate in 2001: 65.63 cases per lakh population.**

- Total IPC cases in 2001: 864,197
- Total population covered: ~1,317 million
- Baseline rate = 864,197 / (1,317 × 10) = 65.63

Computed directly from NCRB data before any modelling. See `outputs/baseline_metric.json`.

---

## 5. Falsifiable hypothesis

At least 5 of the top 10 highest per-capita crime states in 2012 will be mid-sized states (population < 50 million), not the largest states (UP, Maharashtra, Bihar) — showing that absolute crime counts mislead resource allocation.

---

## 6. Data sources and access plan

**Source 1 — NCRB District-wise IPC Crimes 2001–2012**
- URL: https://www.kaggle.com/datasets/rajanand/crime-in-india
- Licence: Government of India Open Data (public domain)
- Access: Direct CSV download from Kaggle (free account)
- File committed: `data/crime_data.csv` (cleaned, 4,896 rows)

Probe:
```python
# artifacts/probes/probe_ncrb.py
import pandas as pd
df = pd.read_csv("data/crime_data.csv")
state_totals = df[df["Year"] == 2001]
print(state_totals[["State","Year","Cases_Reported"]].head(1))
# Expected: Andhra Pradesh | 2001 | some positive integer
```

Run: `uv run artifacts/probes/probe_ncrb.py`

---

## 7. Scope limits

- We will not estimate causal effects of policing policy on crime rates
- We will not harmonise district boundaries; analysis is at state level only
- We will not cover years beyond 2012 (data file limit)
- We will not model socioeconomic drivers of crime
- We will not produce confidence intervals — this is a descriptive census
- Secondary outcomes (crime type breakdowns, forecasts) are reported but not the primary graded metric

---

## 8. Risks and fallback

**Risk:** NCRB 2001–2012 covers only reported IPC crimes; unreported crimes are excluded.

**Fallback:** If population data introduces normalisation errors, we fall back to absolute IPC crime counts and clearly note the limitation in the report.

---

## 9. Reproducibility checklist

- [x] `uv run main.py` runs end-to-end in under 10 minutes on a clean machine
- [x] Writes `outputs/primary_metric.json` with `metric_name`, `value`, `threshold`, `passed`
- [x] Writes `outputs/baseline_metric.json` with same schema
- [x] `README.md` documents run command and expected outputs in ≤ 20 lines
- [x] Data committed under `data/crime_data.csv` with licence note

---

## Team Roles

| Member | GitHub | Responsibility |
|--------|--------|----------------|
| Ujjwal Kumar | Ujjwalkumar2025 | ujjwal.kumar_msc2024@ashoka.edu.in | Data cleaning, analysis, main.py, dashboard |
| Piyush Pushpad | piyush17-ux | piyush.pushpad_ma2025@ashoka.edu.in |Visualization, report, testing, GitHub |

---

## Sign-off

Signed: Ujjwal Kumar, Piyush Pushpad
