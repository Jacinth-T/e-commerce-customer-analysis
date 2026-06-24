"""
delta_regional.py — Step 4 of the pipeline: Regional revenue analysis.

Groups transactions by Country to show where the money is coming from.
Spoiler: the UK dominates because the dataset is from a UK retailer,
but the international breakdown is still useful for targeting strategy.
"""

import os
import sys

import pandas as pd

# ---------------------------------------------------------------------------
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

import database  # noqa: E402


def run():
    """Build country-level summary and store in SQLite."""
    print("\n🌍  DELTA — Regional Analysis")
    print("=" * 50)

    # -----------------------------------------------------------------------
    # 1. Pull transactions
    # -----------------------------------------------------------------------
    print("   [1/3] Loading transactions from SQLite …")
    df = database.get_transactions()

    # -----------------------------------------------------------------------
    # 2. Aggregate by Country
    # -----------------------------------------------------------------------
    print("   [2/3] Aggregating by country …")
    regional = df.groupby("Country").agg(
        TotalRevenue=("TotalPrice", "sum"),
        OrderCount=("InvoiceNo", "nunique"),
        CustomerCount=("CustomerID", "nunique"),
    ).reset_index()

    # Sort by revenue — biggest markets first
    regional = regional.sort_values("TotalRevenue", ascending=False).reset_index(drop=True)

    # -----------------------------------------------------------------------
    # 3. Store in SQLite
    # -----------------------------------------------------------------------
    print("   [3/3] Writing to SQLite 'regional_summary' table …")
    conn = database.get_connection()
    regional.to_sql("regional_summary", conn, if_exists="replace", index=False)
    conn.close()

    # -----------------------------------------------------------------------
    # Summary
    # -----------------------------------------------------------------------
    print(f"\n   ✅ Regional summary complete — {len(regional)} countries.")
    print("\n   Top 5 countries by revenue:")
    for i, row in regional.head(5).iterrows():
        country = row["Country"]
        rev = row["TotalRevenue"]
        print(f"      {i+1}. {country:<25s} £{rev:>12,.2f}")

    # Note about UK dominance (this is a UK-based retailer)
    uk_row = regional[regional["Country"] == "United Kingdom"]
    if not uk_row.empty:
        uk_pct = uk_row.iloc[0]["TotalRevenue"] / regional["TotalRevenue"].sum() * 100
        print(f"\n   📌 Note: United Kingdom accounts for {uk_pct:.1f}% of total revenue.")
        print("      This is expected — the retailer is UK-based.")

    return regional


# ---------------------------------------------------------------------------
if __name__ == "__main__":
    run()
