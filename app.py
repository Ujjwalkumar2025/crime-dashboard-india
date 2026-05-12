"""
app.py  — India Crime Intelligence Dashboard
────────────────────────────────────────────────────────────────
Run with:
    streamlit run app.py

Make sure you've already run:
    python data/generate_sample_data.py
────────────────────────────────────────────────────────────────
"""

import sys, os, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests

from data_cleaning import load_and_clean_data, get_filter_options
from analysis import (
    get_total_crimes_by_state,
    get_top_states,
    get_crime_trends,
    get_multi_crime_trends,
    get_crime_type_breakdown,
    get_insights,
    get_yoy_change,
)
from prediction import (
    predict_crime_trend,
    get_state_forecasts,
    get_crime_type_forecasts,
)

# ═══════════════════════════════════════════════════════════════
# PAGE CONFIG
# ═══════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="India Crime Intelligence Dashboard",
    page_icon="🚔",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ═══════════════════════════════════════════════════════════════
# CUSTOM CSS  (dark-theme polish)
# ═══════════════════════════════════════════════════════════════
st.markdown("""
<style>
/* KPI metric cards */
.metric-card {
    background: linear-gradient(135deg, #1a2332, #1e2d40);
    border-left: 4px solid #4fc3f7;
    border-radius: 10px;
    padding: 20px 22px;
    margin: 4px 0;
    box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    transition: transform 0.2s;
}
.metric-card:hover { transform: translateY(-2px); }
.metric-value {
    font-size: 2.1rem;
    font-weight: 800;
    color: #4fc3f7;
    margin: 0;
    letter-spacing: -1px;
}
.metric-label {
    font-size: 0.82rem;
    color: #7a8898;
    margin-top: 6px;
    font-weight: 500;
}

/* Section headers */
.section-header {
    font-size: 1.2rem;
    font-weight: 700;
    color: #dce8f5;
    padding-bottom: 8px;
    border-bottom: 2px solid #4fc3f7;
    margin: 28px 0 14px 0;
}

/* Insight cards */
.insight-card {
    background: linear-gradient(135deg, #1a2332, #1e2d40);
    border-radius: 10px;
    padding: 16px 18px;
    margin: 6px 0;
    border: 1px solid #2b3d52;
    height: 100%;
}
.insight-icon  { font-size: 1.6rem; }
.insight-title { font-weight: 600; color: #dce8f5; margin-top: 6px; font-size: 0.95rem; }
.insight-text  { color: #7a8898; font-size: 0.85rem; margin-top: 6px; line-height: 1.5; }

/* Caption style override */
.caption-note {
    color: #556070;
    font-size: 0.78rem;
    margin-top: -8px;
    margin-bottom: 12px;
}
</style>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# DATA LOADING  (cached so it only runs once)
# ═══════════════════════════════════════════════════════════════
@st.cache_data
def load_data():
    return load_and_clean_data()

@st.cache_data(ttl=3600)
def load_india_geojson():
    """
    Loads India state boundaries GeoJSON.
    Priority: local file (data/india_states.geojson) → remote URL fallback.
    Run data/download_geojson.py once to get the version with Ladakh.
    """
    # ── Try local file first (has Ladakh if you ran download_geojson.py) ──
    local_path = "data/india_states.geojson"
    if os.path.exists(local_path):
        with open(local_path, "r", encoding="utf-8") as f:
            return json.load(f)

    # ── Fall back to remote URL ───────────────────────────────────────────
    url = (
        "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112"
        "/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    )
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        return resp.json()
    except Exception:
        return None


try:
    df       = load_data()
    geojson  = load_india_geojson()
    FILTERS  = get_filter_options(df)
except FileNotFoundError as err:
    st.error(str(err))
    st.stop()


# ═══════════════════════════════════════════════════════════════
# SIDEBAR — FILTERS
# ═══════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div style="background:linear-gradient(135deg,#1a3a5c,#0d2137);
         border-radius:10px;padding:16px 14px;margin-bottom:8px;
         border-left:4px solid #4fc3f7;">
        <div style="font-size:1.6rem">🚔</div>
        <div style="font-size:1.1rem;font-weight:700;color:#dce8f5;margin-top:4px">
            Crime Intelligence
        </div>
        <div style="font-size:0.75rem;color:#4fc3f7;margin-top:2px">
            India · NCRB Data · 2001–2012
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.divider()

    selected_year  = st.selectbox("📅 Year",       ["All Years"]  + FILTERS["years"])
    selected_state = st.selectbox("🗺️ State",       ["All India"]  + FILTERS["states"])
    selected_crime = st.selectbox("🚨 Crime Type",  ["All"]        + FILTERS["crime_types"])

    st.divider()
    st.markdown(
        "<small>Data: NCRB (National Crime Records Bureau)</small><br>"
        "<small>Built with Python · Streamlit · Plotly</small>",
        unsafe_allow_html=True,
    )

# Convenience variables
year_val  = None if selected_year  == "All Years" else int(selected_year)
state_val = None if selected_state == "All India"  else selected_state
crime_val = None if selected_crime == "All"        else selected_crime


# ═══════════════════════════════════════════════════════════════
# TITLE BAR
# ═══════════════════════════════════════════════════════════════
st.markdown("""
<div style="background:linear-gradient(135deg,#0d2137,#1a3a5c,#0d2137);
     border-radius:12px;padding:28px 32px;margin-bottom:20px;
     border:1px solid #1e3a5f;">
    <div style="display:flex;align-items:center;gap:16px">
        <div style="font-size:3rem">🚔</div>
        <div>
            <h1 style="margin:0;color:#dce8f5;font-size:2rem;font-weight:800">
                India Crime Intelligence Dashboard
            </h1>
            <p style="margin:4px 0 0 0;color:#4fc3f7;font-size:0.9rem">
                National Crime Records Bureau · 34 States & UTs · 2001–2012 · 12 Crime Categories
            </p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)
st.caption(
    f"Analysing crime patterns across India  ·  "
    f"{'All Years' if not year_val else year_val}  ·  "
    f"{selected_state}  ·  {selected_crime}"
)
st.divider()


# ═══════════════════════════════════════════════════════════════
# KPI CARDS
# ═══════════════════════════════════════════════════════════════
# Apply all filters to get the numbers shown in the cards
fdf = df.copy()
if year_val:   fdf = fdf[fdf["Year"]       == year_val]
if state_val:  fdf = fdf[fdf["State"]      == state_val]
if crime_val:  fdf = fdf[fdf["Crime_Type"] == crime_val]

total_cases  = int(fdf["Cases_Reported"].sum())
num_states   = fdf["State"].nunique()
num_crimes   = fdf["Crime_Type"].nunique()
avg_per_state = int(total_cases / num_states) if num_states else 0

# Year-over-year delta for the card
if year_val and year_val > df["Year"].min():
    prev_fdf = df[df["Year"] == year_val - 1]
    if state_val: prev_fdf = prev_fdf[prev_fdf["State"]      == state_val]
    if crime_val: prev_fdf = prev_fdf[prev_fdf["Crime_Type"] == crime_val]
    prev_total = int(prev_fdf["Cases_Reported"].sum())
    yoy_pct = (total_cases - prev_total) / prev_total * 100 if prev_total else 0
    delta_html = (
        f'<div class="metric-delta delta-{"up" if yoy_pct > 0 else "down"}">'
        f'{"▲" if yoy_pct > 0 else "▼"} {abs(yoy_pct):.1f}% vs {year_val-1}</div>'
    )
else:
    delta_html = ""

c1, c2, c3, c4 = st.columns(4)

CARD = """
<div style="background:linear-gradient(135deg,#1a2332,#1e2d40);
     border-left:4px solid {color};border-radius:10px;
     padding:20px 22px;margin:4px 0;
     box-shadow:0 4px 15px rgba(0,0,0,0.3);">
  <div style="font-size:2rem;font-weight:800;color:{color};
       letter-spacing:-1px;margin:0">{value}</div>
  <div style="font-size:0.82rem;color:#7a8898;margin-top:6px;
       font-weight:500">{label}</div>
</div>"""

with c1:
    st.markdown(CARD.format(color="#4fc3f7", value=f"{total_cases:,}",
        label="📋 Total Cases Reported"), unsafe_allow_html=True)
with c2:
    st.markdown(CARD.format(color="#81c784", value=num_states,
        label="🗺️ States Analysed"), unsafe_allow_html=True)
with c3:
    st.markdown(CARD.format(color="#ffb74d", value=num_crimes,
        label="🚨 Crime Categories"), unsafe_allow_html=True)
with c4:
    st.markdown(CARD.format(color="#f06292", value=f"{avg_per_state:,}",
        label="📊 Avg Cases / State"), unsafe_allow_html=True)

st.markdown("---")


# ═══════════════════════════════════════════════════════════════
# ROW 1 — HEATMAP  +  CRIME TYPE DONUT
# ═══════════════════════════════════════════════════════════════
col_map, col_donut = st.columns([3, 2])

# ── Heatmap ───────────────────────────────────────────────────
with col_map:
    st.markdown('<div class="section-header">🗺️ State-wise Crime Intensity</div>', unsafe_allow_html=True)

    state_totals = get_total_crimes_by_state(df, year=year_val, crime_type=crime_val)

    # Ladakh has no NCRB data (became UT in 2019) but we add it
    # with 0 cases so it renders on the map rather than going blank
    import pandas as pd
    if "Ladakh" not in state_totals["State"].values:
        ladakh_row = pd.DataFrame([{
            "State": "Ladakh",
            "State_GeoJSON": "Ladakh",
            "Cases_Reported": 0
        }])
        state_totals = pd.concat([state_totals, ladakh_row], ignore_index=True)

    if geojson:
        fig_map = px.choropleth(
            state_totals,
            geojson=geojson,
            featureidkey="properties.ST_NM",
            locations="State_GeoJSON",           # Normalised names column
            color="Cases_Reported",
            color_continuous_scale="Reds",
            hover_name="State",
            hover_data={"Cases_Reported": ":,", "State_GeoJSON": False},
            labels={"Cases_Reported": "Cases"},
        )
        fig_map.update_geos(fitbounds="locations", visible=False)
        fig_map.update_layout(
            margin=dict(l=0, r=0, t=0, b=0),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            coloraxis_colorbar=dict(
                title=dict(text="Cases", font=dict(color="#7a8898")),
                tickfont=dict(color="#7a8898"),
            ),
            height=420,
        )
        st.markdown('<div style="background:#0e1117;border-radius:10px;padding:4px">',
            unsafe_allow_html=True)
        st.plotly_chart(fig_map, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        # Fallback when offline: simple horizontal bar chart
        fig_map = px.bar(
            state_totals.head(15),
            x="Cases_Reported", y="State",
            orientation="h",
            color="Cases_Reported",
            color_continuous_scale="Reds",
            title="Top 15 States by Crime Count",
        )
        fig_map.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(26,35,50,0.8)",
            font=dict(color="#dce8f5"),
            height=420,
        )
        st.plotly_chart(fig_map, use_container_width=True)

    st.markdown(
        '<p class="caption-note">💡 Darker red = higher crime intensity. '
        'Hover over a state to see exact numbers.</p>',
        unsafe_allow_html=True,
    )

# ── Crime Type Donut ──────────────────────────────────────────
with col_donut:
    st.markdown('<div class="section-header">🧠 Crime Type Breakdown</div>', unsafe_allow_html=True)

    crime_breakdown = get_crime_type_breakdown(df, year=year_val, state=state_val)

    fig_donut = px.pie(
        crime_breakdown,
        values="Cases_Reported",
        names="Crime_Type",
        hole=0.45,
        color_discrete_sequence=px.colors.qualitative.Bold,
    )
    fig_donut.update_traces(
        textposition="inside",
        textinfo="percent",
        hovertemplate="<b>%{label}</b><br>Cases: %{value:,}<br>Share: %{percent}",
    )
    fig_donut.update_layout(
        margin=dict(l=10, r=10, t=20, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#dce8f5"),
        legend=dict(font=dict(size=10), bgcolor="rgba(0,0,0,0)"),
        height=420,
        showlegend=True,
    )
    st.plotly_chart(fig_donut, use_container_width=True)
    st.markdown(
        '<p class="caption-note">💡 Hover over each slice for exact counts. '
        'Use the sidebar to filter by year / state.</p>',
        unsafe_allow_html=True,
    )


# ═══════════════════════════════════════════════════════════════
# ROW 2 — CRIME TRENDS
# ═══════════════════════════════════════════════════════════════
st.markdown('<div class="section-header">📈 Crime Trends Over Time</div>', unsafe_allow_html=True)

col_trend1, col_trend2 = st.columns(2)

# ── Single crime / overall trend ─────────────────────────────
with col_trend1:
    title = f"{selected_state}  —  {selected_crime}"
    trends = get_crime_trends(df, state=state_val, crime_type=crime_val)

    fig_line = px.line(
        trends,
        x="Year", y="Cases_Reported",
        markers=True,
        labels={"Cases_Reported": "Cases"},
        title=title,
    )
    fig_line.update_traces(
        line=dict(color="#4fc3f7", width=2.5),
        marker=dict(size=9, color="#4fc3f7"),
    )
    fig_line.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(26,35,50,0.6)",
        font=dict(color="#dce8f5"),
        title_font_size=13,
        xaxis=dict(showgrid=False, tickmode="linear", dtick=1),
        yaxis=dict(showgrid=True, gridcolor="#1e2d40"),
        height=320,
        margin=dict(t=40),
    )
    st.plotly_chart(fig_line, use_container_width=True)

# ── Top 5 crime types comparison ─────────────────────────────
with col_trend2:
    top5_crimes = crime_breakdown.head(5)["Crime_Type"].tolist()
    multi_trend = get_multi_crime_trends(df, top5_crimes, state=state_val)

    fig_multi = px.line(
        multi_trend,
        x="Year", y="Cases_Reported",
        color="Crime_Type",
        markers=True,
        labels={"Cases_Reported": "Cases"},
        title="Top 5 Crime Types — Year-on-Year Comparison",
    )
    fig_multi.update_traces(line_width=2, marker_size=7)
    fig_multi.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(26,35,50,0.6)",
        font=dict(color="#dce8f5"),
        title_font_size=13,
        xaxis=dict(showgrid=False, tickmode="linear", dtick=1),
        yaxis=dict(showgrid=True, gridcolor="#1e2d40"),
        legend=dict(font=dict(size=10), bgcolor="rgba(0,0,0,0)"),
        height=320,
        margin=dict(t=40),
    )
    st.plotly_chart(fig_multi, use_container_width=True)

st.markdown(
    '<p class="caption-note">💡 Look for inflection points — a sudden spike often '
    'correlates with new reporting laws, social events, or policy changes.</p>',
    unsafe_allow_html=True,
)


# ═══════════════════════════════════════════════════════════════
# ROW 3 — STATE RISK RANKINGS
# ═══════════════════════════════════════════════════════════════
st.markdown('<div class="section-header">🚨 State Risk Rankings</div>', unsafe_allow_html=True)

col_rank1, col_rank2 = st.columns(2)

# ── By total count ────────────────────────────────────────────
with col_rank1:
    st.write("**By Total Cases Reported**")
    top_total = get_top_states(df, year=year_val, crime_type=crime_val, by="total")

    fig_bar1 = px.bar(
        top_total,
        x="Value", y="State",
        orientation="h",
        color="Value",
        color_continuous_scale="Reds",
        text="Value",
        labels={"Value": "Total Cases", "State": ""},
    )
    fig_bar1.update_traces(
        texttemplate="%{text:,}",
        textposition="outside",
        textfont_size=10,
    )
    fig_bar1.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(26,35,50,0.6)",
        font=dict(color="#dce8f5"),
        showlegend=False,
        coloraxis_showscale=False,
        yaxis=dict(categoryorder="total ascending"),
        xaxis=dict(showgrid=False),
        height=400,
        margin=dict(l=0, r=60),
    )
    st.plotly_chart(fig_bar1, use_container_width=True)

# ── By per-capita rate ────────────────────────────────────────
with col_rank2:
    st.write("**By Crime Rate — Cases per Lakh Population** ← *The smarter metric*")
    top_percap = get_top_states(df, year=year_val, crime_type=crime_val, by="per_capita")

    fig_bar2 = px.bar(
        top_percap,
        x="Value", y="State",
        orientation="h",
        color="Value",
        color_continuous_scale="Oranges",
        text="Value",
        labels={"Value": "Cases / Lakh Pop.", "State": ""},
    )
    fig_bar2.update_traces(
        texttemplate="%{text:.0f}",
        textposition="outside",
        textfont_size=10,
    )
    fig_bar2.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(26,35,50,0.6)",
        font=dict(color="#dce8f5"),
        showlegend=False,
        coloraxis_showscale=False,
        yaxis=dict(categoryorder="total ascending"),
        xaxis=dict(showgrid=False),
        height=400,
        margin=dict(l=0, r=60),
    )
    st.plotly_chart(fig_bar2, use_container_width=True)

st.markdown(
    '<p class="caption-note">💡 <b>Why per capita matters:</b> '
    'UP will always have more absolute crimes than Goa — it has 100× the population. '
    'Per-lakh numbers reveal the true risk level a citizen faces.</p>',
    unsafe_allow_html=True,
)


# ═══════════════════════════════════════════════════════════════
# ROW 4 — AUTOMATED INSIGHTS  (the storytelling section)
# ═══════════════════════════════════════════════════════════════
st.markdown('<div class="section-header">🧠 Key Insights</div>', unsafe_allow_html=True)
st.caption("Automatically derived from the data — the 'so what?' section that sets your project apart.")

insights = get_insights(df)
insight_cols = st.columns(len(insights))

for col, insight in zip(insight_cols, insights):
    with col:
        st.markdown(f"""<div class="insight-card">
            <div class="insight-icon">{insight['icon']}</div>
            <div class="insight-title">{insight['title']}</div>
            <div class="insight-text">{insight['text']}</div>
        </div>""", unsafe_allow_html=True)




# ═══════════════════════════════════════════════════════════════
# ROW 5 — PREDICTION MODEL
# ═══════════════════════════════════════════════════════════════
st.markdown('<div class="section-header">🔮 Crime Trend Prediction (2013–2016)</div>', unsafe_allow_html=True)
st.caption("Linear regression model trained on 2001–2012 NCRB data. Forecasts 4 years ahead.")

# ── Forecast chart ────────────────────────────────────────────
pred_col1, pred_col2 = st.columns([3, 2])

with pred_col1:
    result = predict_crime_trend(df, state=state_val, crime_type=crime_val)

    if result:
        stats = result["model_stats"]
        full  = result["full_df"]

        # Actual line
        actual  = full[full["Type"] == "Actual"]
        fitted  = full[full["Type"] == "Trend Line"]
        forecast = full[full["Type"] == "Forecast"]

        fig_pred = go.Figure()

        # Confidence band
        fig_pred.add_trace(go.Scatter(
            x=list(forecast["Year"]) + list(forecast["Year"])[::-1],
            y=list(forecast["Upper"]) + list(forecast["Lower"])[::-1],
            fill="toself",
            fillcolor="rgba(255,165,0,0.15)",
            line=dict(color="rgba(255,255,255,0)"),
            name="Confidence Band",
            showlegend=True,
        ))

        # Fitted trend line (historical)
        fig_pred.add_trace(go.Scatter(
            x=fitted["Year"], y=fitted["Cases_Reported"],
            mode="lines",
            line=dict(color="#ffffff", width=1, dash="dot"),
            name="Trend Line",
        ))

        # Actual data
        fig_pred.add_trace(go.Scatter(
            x=actual["Year"], y=actual["Cases_Reported"],
            mode="lines+markers",
            line=dict(color="#4fc3f7", width=2.5),
            marker=dict(size=8, color="#4fc3f7"),
            name="Actual (2001–2012)",
        ))

        # Forecast
        fig_pred.add_trace(go.Scatter(
            x=forecast["Year"], y=forecast["Cases_Reported"],
            mode="lines+markers",
            line=dict(color="#ff9800", width=2.5, dash="dash"),
            marker=dict(size=9, color="#ff9800", symbol="diamond"),
            name="Forecast (2013–2016)",
        ))

        # Vertical line at forecast start
        fig_pred.add_vline(
            x=2012.5,
            line_dash="dash",
            line_color="rgba(255,255,255,0.3)",
            annotation_text="Forecast →",
            annotation_font_color="#7a8898",
        )

        fig_pred.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(26,35,50,0.6)",
            font=dict(color="#dce8f5"),
            xaxis=dict(showgrid=False, tickmode="linear", dtick=1),
            yaxis=dict(showgrid=True, gridcolor="#1e2d40", title="Cases Reported"),
            legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=11)),
            height=380,
            margin=dict(t=20),
        )
        st.plotly_chart(fig_pred, use_container_width=True)
        st.markdown(
            f'<p class="caption-note">💡 R² = {stats["r_squared"]} — '
            f'model explains {stats["r_squared"]*100:.1f}% of variance. '
            f'Slope: {stats["slope_per_year"]:+,.0f} cases/year.</p>',
            unsafe_allow_html=True,
        )

with pred_col2:
    if result:
        st.markdown("**Model Summary**")
        s = result["model_stats"]

        st.markdown(f"""<div class="insight-card">
            <div class="insight-icon">📐</div>
            <div class="insight-title">Model Fit (R²)</div>
            <div class="insight-text">{s['r_squared']} — {'Strong fit ✅' if s['r_squared'] > 0.75 else 'Moderate fit ⚠️'}</div>
        </div>""", unsafe_allow_html=True)

        st.markdown(f"""<div class="insight-card">
            <div class="insight-icon">📈</div>
            <div class="insight-title">Trend Direction</div>
            <div class="insight-text">{s['trend_direction']} · {abs(s['slope_per_year']):,.0f} cases/year</div>
        </div>""", unsafe_allow_html=True)

        st.markdown(f"""<div class="insight-card">
            <div class="insight-icon">🔮</div>
            <div class="insight-title">2016 Forecast</div>
            <div class="insight-text">{s['forecast_end_value']:,} cases · {s['forecast_pct_change']:+.1f}% vs 2012</div>
        </div>""", unsafe_allow_html=True)

        st.markdown(f"""<div class="insight-card">
            <div class="insight-icon">📏</div>
            <div class="insight-title">Avg Error (MAE)</div>
            <div class="insight-text">±{s['mae']:,} cases per year</div>
        </div>""", unsafe_allow_html=True)

# ── State forecast rankings ───────────────────────────────────
st.markdown("**🗺️ Which States Are Getting Riskier? (Projected to 2016)**")

rank_col1, rank_col2 = st.columns(2)

state_fc = get_state_forecasts(df, crime_type=crime_val)

with rank_col1:
    st.write("🔴 **Top 8 States Getting Worse**")
    worst = state_fc.head(8)[["State", "Pct_Change", "Forecast_Cases"]].copy()
    worst.columns = ["State", "% Change", "Forecast 2016"]
    worst["% Change"] = worst["% Change"].apply(lambda x: f"+{x:.1f}%")
    worst["Forecast 2016"] = worst["Forecast 2016"].apply(lambda x: f"{x:,}")
    st.dataframe(worst, use_container_width=True, hide_index=True)

with rank_col2:
    st.write("🟢 **Top 8 States Improving**")
    best = state_fc.tail(8).iloc[::-1][["State", "Pct_Change", "Forecast_Cases"]].copy()
    best.columns = ["State", "% Change", "Forecast 2016"]
    best["% Change"] = best["% Change"].apply(lambda x: f"{x:.1f}%")
    best["Forecast 2016"] = best["Forecast 2016"].apply(lambda x: f"{x:,}")
    st.dataframe(best, use_container_width=True, hide_index=True)

# ── Crime type forecast ───────────────────────────────────────
st.markdown("**📊 Crime Type Projections to 2016**")
crime_fc = get_crime_type_forecasts(df, state=state_val)

fig_crime_fc = px.bar(
    crime_fc.sort_values("Pct_Change"),
    x="Pct_Change", y="Crime_Type",
    orientation="h",
    color="Pct_Change",
    color_continuous_scale=["#4caf50", "#ffeb3b", "#f44336"],
    color_continuous_midpoint=0,
    text="Pct_Change",
    labels={"Pct_Change": "Projected % Change", "Crime_Type": ""},
)
fig_crime_fc.update_traces(
    texttemplate="%{text:+.1f}%",
    textposition="outside",
    textfont_size=11,
)
fig_crime_fc.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(26,35,50,0.6)",
    font=dict(color="#dce8f5"),
    coloraxis_showscale=False,
    xaxis=dict(showgrid=False, zeroline=True, zerolinecolor="#4a5568"),
    yaxis=dict(showgrid=False),
    height=380,
    margin=dict(l=0, r=80),
)
st.plotly_chart(fig_crime_fc, use_container_width=True)
st.markdown(
    '<p class="caption-note">💡 Green = projected decrease · Red = projected increase · '
    'Based on linear trend from 2001–2012 NCRB data.</p>',
    unsafe_allow_html=True,
)


# ═══════════════════════════════════════════════════════════════
# FOOTER
# ═══════════════════════════════════════════════════════════════
st.divider()
st.markdown(
    "<center><small>🚔 India Crime Intelligence Dashboard  ·  "
    "Data: NCRB  ·  Built with Python, Streamlit & Plotly</small></center>",
    unsafe_allow_html=True,
)
