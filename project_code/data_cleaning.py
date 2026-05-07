"""
src/data_cleaning.py
────────────────────────────────────────────────────────────────
Loads and cleans the crime dataset.

Works with:
  • Our generated sample data (data/crime_data.csv)
  • Real NCRB data from Kaggle (adjust column names in the
    COLUMN_MAP dictionary below if needed)
────────────────────────────────────────────────────────────────
"""

import pandas as pd
import os

# ── If your real NCRB file has different column names, map them here ──
# Keys   = what's in your CSV
# Values = what our code expects
COLUMN_MAP = {
    # Example: "state_name": "State",
    #          "year":       "Year",
    # (Leave empty if using our generated sample data)
}

# GeoJSON uses these exact state names — we normalise our data to match
GEOJSON_NAME_FIX = {
    "Arunachal Pradesh": "Arunanchal Pradesh",   # GeoJSON has a typo
    "Jammu & Kashmir":   "Jammu & Kashmir",       # Explicit match
    "Andaman And Nicobar Islands": "Andaman & Nicobar Island",
    "Dadra And Nagar Haveli": "Dadra and Nagar Haveli",
    "Daman And Diu": "Daman & Diu",
}


def load_and_clean_data(filepath: str = "data/crime_data.csv") -> pd.DataFrame:
    """
    Loads the CSV, cleans it, and adds a 'Cases_Per_Lakh' column.

    Parameters
    ----------
    filepath : path to the CSV file

    Returns
    -------
    Clean pandas DataFrame ready for analysis
    """
    # ── Check file exists ─────────────────────────────────────
    if not os.path.exists(filepath):
        raise FileNotFoundError(
            f"\n❌ Dataset not found at '{filepath}'.\n"
            "   Please run:  python data/generate_sample_data.py\n"
            "   Then restart the Streamlit app."
        )

    df = pd.read_csv(filepath)

    # ── Rename columns if real NCRB data has different names ──
    if COLUMN_MAP:
        df = df.rename(columns=COLUMN_MAP)

    # ── Standardise column names ──────────────────────────────
    # Strips spaces, replaces spaces with underscores
    df.columns = df.columns.str.strip().str.replace(r"\s+", "_", regex=True)

    # ── Drop rows where essential columns are missing ─────────
    essential = ["State", "Year", "Crime_Type", "Cases_Reported"]
    df = df.dropna(subset=essential)

    # ── Fix data types ────────────────────────────────────────
    df["Year"]          = df["Year"].astype(int)
    df["Cases_Reported"] = (
        pd.to_numeric(df["Cases_Reported"], errors="coerce")
        .fillna(0)
        .astype(int)
    )

    if "Population_Millions" in df.columns:
        df["Population_Millions"] = pd.to_numeric(
            df["Population_Millions"], errors="coerce"
        )

    # ── Clean text columns ────────────────────────────────────
    df["State"]      = df["State"].str.strip().str.title()
    df["Crime_Type"] = df["Crime_Type"].str.strip()

    # ── Fix state names to match GeoJSON ─────────────────────
    df["State_GeoJSON"] = df["State"].replace(GEOJSON_NAME_FIX)

    # ── Add crime rate per lakh population ────────────────────
    # This is the IMPORTANT metric — absolute numbers are misleading
    # because larger states will always show more total crimes
    if "Population_Millions" in df.columns:
        # 1 million = 10 lakh, so: cases / (pop_millions * 10) = cases per lakh
        df["Cases_Per_Lakh"] = (
            df["Cases_Reported"] / (df["Population_Millions"] * 10)
        ).round(2)

    return df


def get_filter_options(df: pd.DataFrame) -> dict:
    """
    Returns sorted lists of unique values for Streamlit sidebar filters.
    """
    return {
        "years":       sorted(df["Year"].unique().tolist()),
        "states":      sorted(df["State"].unique().tolist()),
        "crime_types": sorted(df["Crime_Type"].unique().tolist()),
    }
