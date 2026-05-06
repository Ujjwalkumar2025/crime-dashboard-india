"""
artifacts/probes/probe_ncrb.py
────────────────────────────────────────────────────────────────
Proof that the NCRB data source is accessible and valid.

Run:
    uv run artifacts/probes/probe_ncrb.py
────────────────────────────────────────────────────────────────
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import pandas as pd

DATA_FILE = Path("data/crime_data.csv")

print("🔍  NCRB Data Probe")
print("-" * 40)

if not DATA_FILE.exists():
    print(f"❌  {DATA_FILE} not found.")
    print("    Run: python data/load_real_ncrb.py")
    sys.exit(1)

df = pd.read_csv(DATA_FILE)

# Basic checks
assert len(df) > 1000,            "❌ Too few rows"
assert "State" in df.columns,     "❌ Missing State column"
assert "Year" in df.columns,      "❌ Missing Year column"
assert "Crime_Type" in df.columns,"❌ Missing Crime_Type column"
assert "Cases_Reported" in df.columns, "❌ Missing Cases_Reported column"
assert df["Cases_Reported"].sum() > 0, "❌ No cases reported"

print(f"✅  File found: {DATA_FILE}")
print(f"    Rows      : {len(df):,}")
print(f"    States    : {df['State'].nunique()}")
print(f"    Years     : {df['Year'].min()} – {df['Year'].max()}")
print(f"    Crimes    : {df['Crime_Type'].nunique()}")
print(f"    Total cases: {df['Cases_Reported'].sum():,}")
print(f"\n    Crime types: {sorted(df['Crime_Type'].unique())}")
print(f"\n✅  All checks passed. Data source is valid.")
