"""
setup.py — One-time setup script for the E-Commerce Customer Behavior project.

Run this ONCE after placing the raw CSV in data/online_retail.csv.
It will:
  1. Create required directories
  2. Verify the raw data file exists
  3. Initialize SQLite tables
  4. Run all four pipeline stages in order

Usage:
    python setup.py
"""

import os
import sys

# ---------------------------------------------------------------------------
# Fix Windows console encoding — emojis crash with default cp1252 codec.
# ---------------------------------------------------------------------------
os.environ["PYTHONIOENCODING"] = "utf-8"
if sys.stdout.encoding != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")


# ---------------------------------------------------------------------------
# Anchor all paths to the folder where THIS script lives (project root).
# This means it works correctly no matter what your current working dir is.
# ---------------------------------------------------------------------------
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT)

import database
from modules import alpha_ingest, beta_rfm, gamma_products, delta_regional


def main():
    # -----------------------------------------------------------------------
    # Banner
    # -----------------------------------------------------------------------
    print()
    print("🛒" + "=" * 58 + "🛒")
    print("   E-Commerce Customer Behavior Analysis — Setup")
    print("🛒" + "=" * 58 + "🛒")

    # -----------------------------------------------------------------------
    # Step 1: Create required directories
    # -----------------------------------------------------------------------
    print("\n🔧 [Step 1/6] Creating project directories …")

    db_dir = os.path.join(PROJECT_ROOT, "db")
    data_dir = os.path.join(PROJECT_ROOT, "data")

    os.makedirs(db_dir, exist_ok=True)
    print(f"   ✅ db/   → {db_dir}")

    os.makedirs(data_dir, exist_ok=True)
    print(f"   ✅ data/ → {data_dir}")

    # -----------------------------------------------------------------------
    # Step 2: Check that the raw CSV exists
    #    WHY check early?  No point running the rest of the pipeline
    #    if there's no data to ingest.
    # -----------------------------------------------------------------------
    print("\n📂 [Step 2/6] Checking for raw data file …")

    csv_path = os.path.join(data_dir, "online_retail.csv")
    if not os.path.isfile(csv_path):
        print(f"   ❌ File not found: {csv_path}")
        print()
        print("   To get the data:")
        print("   1. Go to: https://archive.ics.uci.edu/ml/datasets/Online+Retail")
        print("   2. Download 'Online Retail.xlsx'")
        print("   3. Open in Excel and Save As CSV → data/online_retail.csv")
        print("      (Or use Python:  pd.read_excel('Online Retail.xlsx')")
        print("                        .to_csv('data/online_retail.csv', index=False))")
        print()
        print("   Then re-run:  python setup.py")
        sys.exit(1)

    file_size_mb = os.path.getsize(csv_path) / (1024 * 1024)
    print(f"   ✅ Found: {csv_path} ({file_size_mb:.1f} MB)")

    # -----------------------------------------------------------------------
    # Step 3: Initialize SQLite tables
    # -----------------------------------------------------------------------
    print("\n🗄️  [Step 3/6] Initializing SQLite database …")
    database.create_tables()

    # -----------------------------------------------------------------------
    # Step 4: Run Alpha — Data Ingestion
    # -----------------------------------------------------------------------
    print("\n🚀 [Step 4/6] Running Alpha — Data Ingestion …")
    alpha_ingest.run()

    # -----------------------------------------------------------------------
    # Step 5: Run Beta — RFM Segmentation
    # -----------------------------------------------------------------------
    print("\n🚀 [Step 5/6] Running Beta — RFM Segmentation …")
    beta_rfm.run()

    # -----------------------------------------------------------------------
    # Step 6a: Run Gamma — Product Analytics
    # -----------------------------------------------------------------------
    print("\n🚀 [Step 6/6] Running Gamma & Delta — Product + Regional …")
    gamma_products.run()

    # -----------------------------------------------------------------------
    # Step 6b: Run Delta — Regional Analysis
    # -----------------------------------------------------------------------
    delta_regional.run()

    # -----------------------------------------------------------------------
    # Final summary
    # -----------------------------------------------------------------------
    print("\n" + "=" * 60)
    print("🎉  Setup complete!")
    print("=" * 60)

    # Show KPI snapshot so the user knows it worked
    kpi = database.get_kpi_summary()
    print(f"   Customers  : {kpi['total_customers']:,}")
    print(f"   Revenue    : £{kpi['total_revenue']:,.2f}")
    print(f"   Orders     : {kpi['total_orders']:,}")
    print(f"   Countries  : {kpi['countries_covered']}")

    print("\n   👉 Next step:  streamlit run app.py")
    print()


if __name__ == "__main__":
    main()
