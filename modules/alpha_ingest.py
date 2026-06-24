"""
alpha_ingest.py — Step 1 of the pipeline: Load & clean the raw CSV.

WHY "alpha"?
  → We prefix modules with Greek letters so the pipeline runs in
    alphabetical order: alpha → beta → gamma → delta.

This module reads the UCI Online Retail dataset, cleans it up, and
pushes the result into the SQLite `transactions` table.
"""

import os
import sys
import pandas as pd

# ---------------------------------------------------------------------------
# We need to import from the project root, so add it to sys.path.
# This lets us do `import database` even when this file is inside modules/.
# ---------------------------------------------------------------------------
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

import database  # noqa: E402  (import not at top — needed after path fix)


def run():
    """Load raw CSV, clean it, and store in SQLite."""
    print("\n📥  ALPHA — Data Ingestion")
    print("=" * 50)

    # -----------------------------------------------------------------------
    # 1. Read the raw CSV
    # -----------------------------------------------------------------------
    csv_path = os.path.join(PROJECT_ROOT, "data", "online_retail.csv")
    print(f"   [1/9] Reading CSV from: {csv_path}")

    # encoding='latin1' because the UCI dataset has special chars (£, accents)
    df = pd.read_csv(csv_path, encoding="latin1")
    original_count = len(df)
    print(f"         → Original rows: {original_count:,}")

    # -----------------------------------------------------------------------
    # 2. Drop rows where CustomerID is null
    #    WHY? We can't do RFM analysis without knowing WHO the customer is.
    # -----------------------------------------------------------------------
    print("   [2/9] Dropping rows with missing CustomerID …")
    df = df.dropna(subset=["CustomerID"])

    # -----------------------------------------------------------------------
    # 3. Remove cancelled orders (InvoiceNo starts with 'C')
    #    WHY? Cancellations would distort revenue and frequency counts.
    # -----------------------------------------------------------------------
    print("   [3/9] Removing cancelled orders (InvoiceNo starts with 'C') …")
    df = df[~df["InvoiceNo"].astype(str).str.startswith("C")]

    # -----------------------------------------------------------------------
    # 4. Remove rows with non-positive Quantity or UnitPrice
    #    WHY? Negative quantities are returns; zero prices are freebies —
    #         neither should count toward revenue.
    # -----------------------------------------------------------------------
    print("   [4/9] Filtering out Quantity <= 0 and UnitPrice <= 0 …")
    df = df[df["Quantity"] > 0]
    df = df[df["UnitPrice"] > 0]

    # -----------------------------------------------------------------------
    # 5. Convert InvoiceDate to datetime
    # -----------------------------------------------------------------------
    print("   [5/9] Converting InvoiceDate to datetime …")
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

    # -----------------------------------------------------------------------
    # 6. Add TotalPrice column
    #    WHY? We need a revenue figure per line item for aggregation.
    # -----------------------------------------------------------------------
    print("   [6/9] Calculating TotalPrice = Quantity × UnitPrice …")
    df["TotalPrice"] = df["Quantity"] * df["UnitPrice"]

    # -----------------------------------------------------------------------
    # 7. Convert CustomerID to clean string
    #    WHY? Pandas reads it as float (e.g. 17850.0); we want '17850'.
    # -----------------------------------------------------------------------
    print("   [7/9] Converting CustomerID to string …")
    df["CustomerID"] = df["CustomerID"].astype(int).astype(str)

    # -----------------------------------------------------------------------
    # 8. Keep only the columns our schema expects
    # -----------------------------------------------------------------------
    print("   [8/9] Selecting final columns …")
    columns_to_keep = [
        "InvoiceNo", "StockCode", "Description", "Quantity",
        "InvoiceDate", "UnitPrice", "CustomerID", "Country", "TotalPrice",
    ]
    df = df[columns_to_keep]

    # -----------------------------------------------------------------------
    # 9. Write to SQLite
    # -----------------------------------------------------------------------
    print("   [9/9] Writing to SQLite 'transactions' table …")
    conn = database.get_connection()
    # 'replace' drops and recreates — safe for re-runs during development
    df.to_sql("transactions", conn, if_exists="replace", index=False)
    conn.close()

    # -----------------------------------------------------------------------
    # Summary
    # -----------------------------------------------------------------------
    rows_dropped = original_count - len(df)
    print(f"\n   ✅ Ingestion complete!")
    print(f"      Rows dropped : {rows_dropped:,}")
    print(f"      Rows loaded  : {len(df):,}")
    return df


# ---------------------------------------------------------------------------
# Allow running this module standalone for quick testing
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    database.create_tables()
    run()
