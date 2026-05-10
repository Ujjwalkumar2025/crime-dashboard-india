# Crime Patterns Across India: A State-Level Analysis Using NCRB Data (2001–2012)

**Course:** ECO6810  
**Team:** Ujjwal Kumar, Piyush  
**Repo:** Ujjwalkumar2025/crime-dashboard-india  
**Data:** National Crime Records Bureau — District-wise IPC Crimes, 2001–2012

---

## 1. Introduction

When policymakers talk about crime in India, the conversation almost always gravitates toward states like Uttar Pradesh or Bihar — partly because they make headlines, and partly because they genuinely report large absolute numbers. What gets lost in that framing is the size of these states. Uttar Pradesh has over 230 million people. Comparing its raw crime count to a state like Mizoram with two million people and calling one "more dangerous" than the other does not really tell us anything useful.

This project started from that frustration. We wanted to look at crime across Indian states not just in terms of total reported cases, but in terms of what an average resident actually faces — crimes per lakh population. The data comes from the National Crime Records Bureau (NCRB), specifically the district-wise IPC crimes dataset covering 2001 to 2012. After cleaning and aggregating to the state level, we had 4,896 observations across 34 states and union territories, covering 12 major crime categories.

The stakeholder we had in mind was the Ministry of Home Affairs, which periodically allocates police modernisation funds across states. Our argument — and we think the data supports it — is that allocation based on absolute crime counts systematically over-resources already large states and under-resources smaller, high-risk ones.

---

## 2. Data and Methods

The raw NCRB file contains district-level entries. For each state and year, NCRB includes a "TOTAL" row that aggregates all districts — we used only those rows. This avoids double-counting and gives us a clean state-year panel.

We retained 12 crime categories: Murder, Rape, Kidnapping & Abduction, Robbery, Burglary, Theft, Riots, Dacoity, Assault, Cruelty by Husband or Relatives, Dowry Deaths, and Assault on Women. These span both violent and property crime and give a reasonable cross-section of the IPC framework.

For normalisation, we divided case counts by state population (in lakhs) using 2021 Census estimates. This is a limitation worth flagging upfront — the population figures do not change year by year in our dataset, which slightly overstates per-capita crime rates in the earlier years when populations were smaller. A more careful analysis would interpolate population between Census rounds, but for the purposes of this descriptive project, the approximation is acceptable.

The main output is a Streamlit-based interactive dashboard, complemented by this report. All outputs, including baseline and primary metric JSON files, are reproducible by running `uv run main.py` from the repo root.

---

## 3. Baseline

Our baseline metric is the **national average IPC crime rate in 2001: 65.63 cases per lakh population.** Total reported IPC crimes that year were 864,197 across all 34 states and UTs. This number serves as the reference point for all trend analysis. States above this threshold in any given year are flagged as high-risk; states below it are treated as comparatively safer, though "safe" is always relative.

---

## 4. Findings

### 4.1 The Trend Is Upward, But Not Uniformly So

Nationwide, total IPC crimes rose from 864,197 in 2001 to 1,101,721 in 2012 — a **27.5% increase** over eleven years. On a per-capita basis, the rate climbed from 65.63 to roughly 83.6 cases per lakh. That is a meaningful rise, but it is worth interpreting carefully. Some of this increase likely reflects better reporting rather than more crime — particularly for categories like rape and cruelty by husband, where social and legal changes in the 2000s made victims more willing to file complaints. We cannot cleanly separate these effects from the data alone.

What we can say is that the trend is real and consistent across most states. There is no year in this period where national totals dropped significantly.

### 4.2 Absolute Numbers Mislead

The five states with the highest total IPC crimes in 2012 were Maharashtra, Andhra Pradesh, Bihar, Uttar Pradesh, and Madhya Pradesh. This is not particularly surprising — these are among India's most populous states.

The picture changes substantially when we switch to per-capita rates. In 2012, **Andhra Pradesh** had the highest crime rate at **222.2 cases per lakh** — nearly three times the national baseline. Chandigarh, Kerala, Mizoram, and Haryana rounded out the top five. Bihar, despite its reputation and large absolute numbers, does not appear in the top five per-capita. This is the central finding of the project: the states that need the most policy attention are not necessarily the ones that look worst in newspaper headlines.

### 4.3 Crime Categories Tell Different Stories

Assault (30.1% of all cases) and Theft (29.3%) together account for nearly 60% of all reported IPC crimes in this period. But the more interesting story is in the growth rates.

**Cruelty by Husband or Relatives** grew by **113.2%** between 2001 and 2012 — the fastest of any category. Kidnapping and Abduction was close behind at **109.1%**. Rape increased by **54.3%**. These are not small movements at the margins.

On the other side, Dacoity declined by **29.8%** and Burglary by **7.1%**. The pattern suggests a shift in the nature of crime — away from property offences and toward crimes against persons, particularly women. This has obvious implications for the kind of policing investment that would be most effective.

### 4.4 States Getting Worse vs. States Improving

West Bengal showed the largest increase in total IPC crimes over the period at **+162.3%**, followed by Tripura (+129.5%) and Bihar (+123.2%). These are striking numbers. Some of this is likely explained by population growth and improved reporting infrastructure, but the scale of the increase in West Bengal in particular warrants closer examination.

On the positive side, Tamil Nadu reduced its crime count by **17.6%** over this period, and Mizoram by **17.5%**. Both states maintained relatively low per-capita rates as well. Tamil Nadu in particular is an interesting case — it is a large, urbanised state, which makes its sustained decline harder to explain by simple demographic factors alone. We flag it here as a candidate for further study.

### 4.5 Trend Projection

We fitted a simple linear regression on the national yearly totals and projected forward to 2016. The model carries an R² of 0.863, which means the linear trend explains about 86% of the year-to-year variance — reasonable for a twelve-year panel. The forecast suggests total IPC crimes will reach approximately 1.15 million by 2016, a further increase of about 4.7% from the 2012 level. We are cautious about over-interpreting this; linear projections do not account for policy changes, economic shocks, or demographic shifts that could alter the trajectory.

---

## 5. Limitations

A few things we would do differently with more time and better data.

First, the population normalisation issue mentioned earlier. Using static 2021 Census estimates for all years between 2001 and 2012 introduces measurement error, especially in the early years.

Second, this dataset ends in 2012. A lot has changed since then — the 2013 amendments to rape laws, the rise of cybercrime, significant urbanisation — and the trends we identify may not hold in more recent data.

Third, we are looking only at reported crimes. Under-reporting is a serious and well-documented problem in Indian crime statistics, and it is not uniform across states or crime types. States with more active police forces or more accessible complaint mechanisms will tend to show higher reported crime, which can create a misleading picture.

Finally, we have not controlled for any socioeconomic variables — income levels, urbanisation, unemployment — that are known to correlate with crime. Our analysis is purely descriptive, not causal.

---

## 6. Conclusion

The main takeaway from this project is simple: **absolute crime counts are a poor basis for policy decisions about police resource allocation.** When you adjust for population, the ranking of states changes substantially. Andhra Pradesh, Chandigarh, and Mizoram emerge as high-risk in per-capita terms, even though they do not dominate news coverage. Bihar and Uttar Pradesh, conversely, look less alarming on a per-person basis than their raw numbers suggest.

The rise in crimes against women — particularly cruelty by husband (+113%) and rape (+54%) — is the most important trend in this data, and probably deserves a dedicated analysis beyond what we have done here.

For the Ministry of Home Affairs, the practical implication is to weight per-capita crime rates more heavily in fund allocation, alongside some measure of improvement or deterioration over time. States that are worsening fast — West Bengal, Tripura, Bihar — need investment. States showing sustained improvement — Tamil Nadu, Mizoram — might offer models worth studying.

---

## 7. Reproducibility

All results in this report are derived from `data/crime_data.csv` committed in the repo. To reproduce:

```bash
uv sync
uv run main.py
```

This writes all metric JSON files to `outputs/`. The interactive dashboard can be run with:

```bash
uv run streamlit run app.py
```

---

## 8. AI Usage

AI assistance (Claude) was used to generate code scaffolding, debug errors, and structure the project. All metric values in this report were verified against the actual dataset. The analysis, interpretation of findings, and conclusions are our own. See `AI_USAGE_LOG.md` for a detailed breakdown.
