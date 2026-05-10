"""
src/prediction.py
────────────────────────────────────────────────────────────────
Crime trend prediction using Linear Regression.

For each state + crime type combination, we:
1. Fit a linear regression on historical yearly data (2001–2012)
2. Forecast 4 years ahead (2013–2016)
3. Return actual + predicted data for plotting
4. Rank states by projected increase/decrease
────────────────────────────────────────────────────────────────
"""

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_absolute_error


def predict_crime_trend(
    df: pd.DataFrame,
    state: str = None,
    crime_type: str = None,
    forecast_years: int = 4,
) -> dict:
    """
    Fits a linear regression on historical crime data and forecasts ahead.

    Parameters
    ----------
    df           : cleaned crime DataFrame
    state        : filter to one state (None = All India)
    crime_type   : filter to one crime type (None = all crimes combined)
    forecast_years : how many years to predict beyond the data

    Returns
    -------
    dict with keys:
        historical_df  : actual data points
        forecast_df    : predicted future points
        full_df        : historical + forecast combined (for plotting)
        model_stats    : R², MAE, slope, trend direction
    """
    # ── Filter data ───────────────────────────────────────────
    filtered = df.copy()
    if state and state != "All India":
        filtered = filtered[filtered["State"] == state]
    if crime_type and crime_type != "All":
        filtered = filtered[filtered["Crime_Type"] == crime_type]

    # Aggregate by year
    yearly = (
        filtered
        .groupby("Year", as_index=False)["Cases_Reported"]
        .sum()
        .sort_values("Year")
    )

    if len(yearly) < 3:
        return None  # Not enough data to fit

    # ── Fit linear regression ─────────────────────────────────
    X = yearly["Year"].values.reshape(-1, 1)
    y = yearly["Cases_Reported"].values

    model = LinearRegression()
    model.fit(X, y)

    # Model stats
    y_pred_hist = model.predict(X)
    r2  = round(r2_score(y, y_pred_hist), 3)
    mae = round(mean_absolute_error(y, y_pred_hist), 0)
    slope = round(float(model.coef_[0]), 1)

    # ── Forecast future years ─────────────────────────────────
    last_year    = int(yearly["Year"].max())
    future_years = list(range(last_year + 1, last_year + forecast_years + 1))
    X_future     = np.array(future_years).reshape(-1, 1)
    y_future     = model.predict(X_future)
    y_future     = np.maximum(y_future, 0)  # No negative crime counts

    # ── Build DataFrames ──────────────────────────────────────
    historical_df = yearly.copy()
    historical_df["Type"] = "Actual"
    historical_df["Lower"] = None
    historical_df["Upper"] = None

    # Simple confidence band: ±1.5 × MAE
    band = mae * 1.5
    forecast_df = pd.DataFrame({
        "Year":           future_years,
        "Cases_Reported": y_future.astype(int),
        "Type":           "Forecast",
        "Lower":          (y_future - band).astype(int),
        "Upper":          (y_future + band).astype(int),
    })

    # Fitted line over historical period (for the trend line)
    fitted_df = pd.DataFrame({
        "Year":           yearly["Year"].tolist(),
        "Cases_Reported": y_pred_hist.astype(int),
        "Type":           "Trend Line",
        "Lower":          None,
        "Upper":          None,
    })

    full_df = pd.concat([historical_df, fitted_df, forecast_df], ignore_index=True)

    # ── Trend summary ─────────────────────────────────────────
    pct_change_forecast = round(
        (float(y_future[-1]) - float(y[-1])) / float(y[-1]) * 100, 1
    ) if y[-1] > 0 else 0

    model_stats = {
        "r_squared":           r2,
        "mae":                 int(mae),
        "slope_per_year":      slope,
        "trend_direction":     "Increasing ↑" if slope > 0 else "Decreasing ↓",
        "forecast_pct_change": pct_change_forecast,
        "last_actual_year":    last_year,
        "last_actual_value":   int(y[-1]),
        "forecast_end_year":   future_years[-1],
        "forecast_end_value":  int(y_future[-1]),
    }

    return {
        "historical_df": historical_df,
        "forecast_df":   forecast_df,
        "fitted_df":     fitted_df,
        "full_df":       full_df,
        "model_stats":   model_stats,
    }


def get_state_forecasts(
    df: pd.DataFrame,
    crime_type: str = None,
    forecast_years: int = 4,
    top_n: int = 10,
) -> pd.DataFrame:
    """
    Runs prediction for ALL states and ranks them by projected
    % change — tells you which states are getting safer/riskier.

    Returns a DataFrame sorted by forecast_pct_change descending.
    """
    results = []

    for state in df["State"].unique():
        result = predict_crime_trend(
            df,
            state=state,
            crime_type=crime_type,
            forecast_years=forecast_years,
        )
        if result is None:
            continue

        stats = result["model_stats"]
        results.append({
            "State":              state,
            "Current_Cases":      stats["last_actual_value"],
            "Forecast_Cases":     stats["forecast_end_value"],
            "Pct_Change":         stats["forecast_pct_change"],
            "Trend":              stats["trend_direction"],
            "R_Squared":          stats["r_squared"],
            "Slope_Per_Year":     stats["slope_per_year"],
            "Forecast_Year":      stats["forecast_end_year"],
        })

    return (
        pd.DataFrame(results)
        .sort_values("Pct_Change", ascending=False)
        .reset_index(drop=True)
    )


def get_crime_type_forecasts(
    df: pd.DataFrame,
    state: str = None,
    forecast_years: int = 4,
) -> pd.DataFrame:
    """
    Runs prediction for ALL crime types and ranks by projected % change.
    Useful for: "which crime is growing fastest?"
    """
    results = []

    for crime in df["Crime_Type"].unique():
        result = predict_crime_trend(
            df,
            state=state,
            crime_type=crime,
            forecast_years=forecast_years,
        )
        if result is None:
            continue

        stats = result["model_stats"]
        results.append({
            "Crime_Type":     crime,
            "Current_Cases":  stats["last_actual_value"],
            "Forecast_Cases": stats["forecast_end_value"],
            "Pct_Change":     stats["forecast_pct_change"],
            "Trend":          stats["trend_direction"],
            "R_Squared":      stats["r_squared"],
        })

    return (
        pd.DataFrame(results)
        .sort_values("Pct_Change", ascending=False)
        .reset_index(drop=True)
    )
