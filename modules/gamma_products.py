"""
gamma_products.py — Step 3 of the pipeline: Product-level analytics.

Aggregates transaction data by product Description to find:
  - Which products sell the most units?
  - Which products generate the most revenue?
  - Which products appear in the most orders?
"""

import os
import sys

import pandas as pd

# ---------------------------------------------------------------------------
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

import database  # noqa: E402


def run():
    """Build product-level summary and store top 50 in SQLite."""
    print("\n📦  GAMMA — Product Analytics")
    print("=" * 50)

    # -----------------------------------------------------------------------
    # 1. Pull transactions
    # -----------------------------------------------------------------------
    print("   [1/4] Loading transactions from SQLite …")
    df = database.get_transactions()

    # -----------------------------------------------------------------------
    # 2. Aggregate by product Description
    #    WHY group by Description (not StockCode)?
    #      → Descriptions are human-readable — better for dashboards.
    #      → Some StockCodes share the same Description; grouping by
    #        Description gives us the business-level view.
    # -----------------------------------------------------------------------
    print("   [2/4] Aggregating by product description …")
    product = df.groupby("Description").agg(
        TotalQuantitySold=("Quantity", "sum"),
        TotalRevenue=("TotalPrice", "sum"),
        OrderCount=("InvoiceNo", "nunique"),
    ).reset_index()

    # Sort by revenue — the metric that matters most to the business
    product = product.sort_values("TotalRevenue", ascending=False)

    # -----------------------------------------------------------------------
    # 3. Keep top 50
    #    WHY only 50?  The long tail is noisy and clutters the dashboard.
    # -----------------------------------------------------------------------
    print("   [3/4] Keeping top 50 products by revenue …")
    product_top = product.head(50).reset_index(drop=True)

    # -----------------------------------------------------------------------
    # 4. Store in SQLite
    # -----------------------------------------------------------------------
    print("   [4/4] Writing to SQLite 'product_summary' table …")
    conn = database.get_connection()
    product_top.to_sql("product_summary", conn, if_exists="replace", index=False)
    conn.close()

    # -----------------------------------------------------------------------
    # Preview
    # -----------------------------------------------------------------------
    print(f"\n   ✅ Product summary complete — {len(product_top)} products stored.")
    print("\n   Top 5 products by revenue:")
    for i, row in product_top.head(5).iterrows():
        desc = row["Description"][:40]  # truncate long names
        rev = row["TotalRevenue"]
        print(f"      {i+1}. {desc:<42s} £{rev:>10,.2f}")

    return product_top


# ---------------------------------------------------------------------------
if __name__ == "__main__":
    run()
