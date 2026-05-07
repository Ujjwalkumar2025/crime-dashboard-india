"""
src/analysis.py
────────────────────────────────────────────────────────────────
All data analysis functions for the dashboard.

Each function is standalone — it takes a DataFrame + filters
and returns a clean DataFrame ready for plotting.
────────────────────────────────────────────────────────────────
"""

import pandas as pd


# ── Helper: apply common filters ─────────────────────────────
def _apply_filters(df: pd.DataFrame, year=None, state=None, crime_type=None) -> pd.DataFrame:
    """Internal helper to apply year / state / crime_type filters."""
    filtered = df.copy()
    if year:
        filtered = filtered[filtered["Year"] == year]
    if state and state != "All India":
        filtered = filtered[filtered["State"] == state]
    if crime_type and crime_type != "All":
        filtered = filtered[filtered["Crime_Type"] == crime_type]
    return filtered


# ── 1. State-wise totals (for heatmap) ───────────────────────
def get_total_crimes_by_state(df, year=None, crime_type=None) -> pd.DataFrame:
    """
    Returns total cases per state.
    Used for the choropleth heatmap.
    """
    filtered = _apply_filters(df, year=year, crime_type=crime_type)

    result = (
        filtered
        .groupby(["State", "State_GeoJSON"], as_index=False)["Cases_Reported"]
        .sum()
        .sort_values("Cases_Reported", ascending=False)
    )
    return result


# ── 2. Top N states by total or per-capita ───────────────────
def get_top_states(df, year=None, crime_type=None, n=10, by="total") -> pd.DataFrame:
    """
    Returns top N states ranked by total crimes or per-capita rate.

    Parameters
    ----------
    by : "total" or "per_capita"
    """
    filtered = _apply_filters(df, year=year, crime_type=crime_type)

    if by == "per_capita" and "Cases_Per_Lakh" in filtered.columns:
        result = (
            filtered
            .groupby("State", as_index=False)["Cases_Per_Lakh"]
            .sum()
            .sort_values("Cases_Per_Lakh", ascending=False)
        )
        result.columns = ["State", "Value"]
        result["Metric"] = "Cases per Lakh Population"
    else:
        result = (
            filtered
            .groupby("State", as_index=False)["Cases_Reported"]
            .sum()
            .sort_values("Cases_Reported", ascending=False)
        )
        result.columns = ["State", "Value"]
        result["Metric"] = "Total Cases"

    return result.head(n).reset_index(drop=True)


# ── 3. Crime trends over years ───────────────────────────────
def get_crime_trends(df, state=None, crime_type=None) -> pd.DataFrame:
    """
    Returns total cases per year (with optional state / crime filter).
    Used for the line chart.
    """
    filtered = _apply_filters(df, state=state, crime_type=crime_type)

    return (
        filtered
        .groupby("Year", as_index=False)["Cases_Reported"]
        .sum()
        .sort_values("Year")
    )


# ── 4. Multi-crime trends (for comparison chart) ─────────────
def get_multi_crime_trends(df, crime_types: list, state=None) -> pd.DataFrame:
    """
    Returns yearly trend for multiple crime types stacked in one DataFrame.
    Used for the multi-line comparison chart.
    """
    frames = []
    for crime in crime_types:
        t = get_crime_trends(df, state=state, crime_type=crime)
        t["Crime_Type"] = crime
        frames.append(t)
    return pd.concat(frames, ignore_index=True)


# ── 5. Crime type breakdown ───────────────────────────────────
def get_crime_type_breakdown(df, year=None, state=None) -> pd.DataFrame:
    """
    Returns total cases per crime type.
    Used for the donut/pie chart.
    """
    filtered = _apply_filters(df, year=year, state=state)

    return (
        filtered
        .groupby("Crime_Type", as_index=False)["Cases_Reported"]
        .sum()
        .sort_values("Cases_Reported", ascending=False)
    )


# ── 6. Automated insights ─────────────────────────────────────
def get_insights(df) -> list[dict]:
    """
    Generates 5 plain-English insights automatically from the data.
    Returns a list of dicts: {icon, title, text}

    This is the "story" section of your dashboard —
    what separates a student project from a professional one.
    """
    insights = []

    latest_year   = int(df["Year"].max())
    earliest_year = int(df["Year"].min())

    # ── Insight 1: Overall growth ─────────────────────────────
    total_latest   = df[df["Year"] == latest_year]["Cases_Reported"].sum()
    total_earliest = df[df["Year"] == earliest_year]["Cases_Reported"].sum()
    growth_pct = (total_latest - total_earliest) / total_earliest * 100
    direction  = "increased" if growth_pct > 0 else "decreased"

    insights.append({
        "icon": "📈",
        "title": "Overall Crime Trend",
        "text": (
            f"Total reported crimes {direction} by {abs(growth_pct):.1f}% "
            f"from {earliest_year} to {latest_year}."
        )
    })

    # ── Insight 2: Fastest growing crime type ─────────────────
    crime_growth = []
    for crime in df["Crime_Type"].unique():
        c = df[df["Crime_Type"] == crime]
        early = c[c["Year"] == earliest_year]["Cases_Reported"].sum()
        late  = c[c["Year"] == latest_year]["Cases_Reported"].sum()
        if early > 0:
            crime_growth.append((crime, (late - early) / early * 100))

    crime_growth.sort(key=lambda x: x[1], reverse=True)
    top_crime, top_pct = crime_growth[0]

    insights.append({
        "icon": "🚨",
        "title": "Fastest Growing Crime",
        "text": (
            f"{top_crime} saw the highest growth — "
            f"up {top_pct:.0f}% since {earliest_year}. "
            "Requires urgent policy attention."
        )
    })

    # ── Insight 3: Highest risk state (per capita) ────────────
    if "Cases_Per_Lakh" in df.columns:
        latest_df = df[df["Year"] == latest_year]
        top_state_name = (
            latest_df
            .groupby("State")["Cases_Per_Lakh"]
            .sum()
            .idxmax()
        )
        top_state_val = (
            latest_df[latest_df["State"] == top_state_name]["Cases_Per_Lakh"]
            .sum()
        )
        insights.append({
            "icon": "🗺️",
            "title": "Highest Risk State (Per Capita)",
            "text": (
                f"{top_state_name} has the highest crime rate in {latest_year} "
                f"({top_state_val:.0f} cases per lakh). "
                "Law enforcement resources should be prioritised here."
            )
        })

    # ── Insight 4: Top 3 safest states ───────────────────────
    if "Cases_Per_Lakh" in df.columns:
        latest_df = df[df["Year"] == latest_year]
        safest = (
            latest_df
            .groupby("State")["Cases_Per_Lakh"]
            .sum()
            .nsmallest(3)
            .index.tolist()
        )
        insights.append({
            "icon": "✅",
            "title": "Top 3 Safest States",
            "text": (
                f"{', '.join(safest)} reported the lowest crime rates "
                f"per lakh population in {latest_year}. "
                "Their policing models could be studied for replication."
            )
        })

    # ── Insight 5: Most improved state ───────────────────────
    state_growth = []
    for state in df["State"].unique():
        s = df[df["State"] == state]
        early = s[s["Year"] == earliest_year]["Cases_Reported"].sum()
        late  = s[s["Year"] == latest_year]["Cases_Reported"].sum()
        if early > 0:
            state_growth.append((state, (late - early) / early * 100))

    state_growth.sort(key=lambda x: x[1])   # Most negative = most improved
    best_state, best_pct = state_growth[0]

    insights.append({
        "icon": "💪",
        "title": "Most Improved State",
        "text": (
            f"{best_state} showed the biggest improvement — "
            f"crime declined by {abs(best_pct):.1f}% since {earliest_year}. "
            "A potential benchmark for effective governance."
        )
    })

    return insights


# ── 7. Year-over-year change per state ───────────────────────
def get_yoy_change(df, year: int) -> pd.DataFrame | None:
    """
    Returns percentage change in total crimes for each state
    compared to the previous year.
    Returns None if year is the earliest year in the dataset.
    """
    if year <= df["Year"].min():
        return None

    curr = df[df["Year"] == year].groupby("State")["Cases_Reported"].sum()
    prev = df[df["Year"] == year - 1].groupby("State")["Cases_Reported"].sum()

    pct_change = ((curr - prev) / prev * 100).reset_index()
    pct_change.columns = ["State", "YoY_Change_Pct"]
    pct_change["YoY_Change_Pct"] = pct_change["YoY_Change_Pct"].round(1)

    return pct_change
