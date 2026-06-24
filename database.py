"""
database.py — Central database access layer for the e-commerce project.

WHY a separate database module?
  → Keeps all SQL logic in one place so the pipeline scripts
    (alpha, beta, gamma, delta) never write raw SQL themselves.
  → If we ever swap SQLite for Postgres, we only change THIS file.
"""

import os
import sqlite3
import pandas as pd

# ---------------------------------------------------------------------------
# Path setup — we anchor everything to the folder where THIS file lives,
# so it works whether you run from the project root, from modules/, or
# from anywhere else on the system.
# ---------------------------------------------------------------------------
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
DB_DIR = os.path.join(PROJECT_ROOT, "db")
DB_PATH = os.path.join(DB_DIR, "ecommerce.db")


# ---------------------------------------------------------------------------
# Connection helper
# ---------------------------------------------------------------------------
def get_connection():
    """Return a sqlite3 connection to the project database.
    
    Creates the db/ folder if it doesn't exist yet — handy for first-time
    setup so callers don't have to worry about directory creation.
    """
    # Make sure the db/ directory is there before we try to open a file in it
    os.makedirs(DB_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    return conn


# ---------------------------------------------------------------------------
# Table creation
# ---------------------------------------------------------------------------
def create_tables():
    """Run all CREATE TABLE IF NOT EXISTS statements.
    
    We use IF NOT EXISTS so this function is safe to call repeatedly —
    it won't blow away data that's already loaded.
    """
    conn = get_connection()
    cursor = conn.cursor()

    # -- 1. Raw cleaned transactions ------------------------------------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            InvoiceNo     TEXT,
            StockCode     TEXT,
            Description   TEXT,
            Quantity      INTEGER,
            InvoiceDate   TEXT,
            UnitPrice     REAL,
            CustomerID    TEXT,
            Country       TEXT,
            TotalPrice    REAL
        );
    """)

    # -- 2. RFM scores per customer -------------------------------------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS rfm_scores (
            CustomerID   TEXT,
            Country      TEXT,
            Recency      INTEGER,
            Frequency    INTEGER,
            Monetary     REAL,
            R_Score      INTEGER,
            F_Score      INTEGER,
            M_Score      INTEGER,
            RFM_Score    TEXT,
            Segment      TEXT
        );
    """)

    # -- 3. Product-level aggregation -----------------------------------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS product_summary (
            Description        TEXT,
            TotalQuantitySold  INTEGER,
            TotalRevenue       REAL,
            OrderCount         INTEGER
        );
    """)

    # -- 4. Country-level aggregation -----------------------------------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS regional_summary (
            Country         TEXT,
            TotalRevenue    REAL,
            OrderCount      INTEGER,
            CustomerCount   INTEGER
        );
    """)

    conn.commit()
    conn.close()
    print("   ✅ All four tables created / verified in SQLite.")


# ---------------------------------------------------------------------------
# Generic query helper
# ---------------------------------------------------------------------------
def query_to_df(sql):
    """Run any SQL query against the database, return a Pandas DataFrame.
    
    WHY a generic helper?  
      → Many parts of the dashboard need ad-hoc queries; writing
        boilerplate connection code each time is tedious and error-prone.
    """
    conn = get_connection()
    df = pd.read_sql_query(sql, conn)
    conn.close()
    return df


# ---------------------------------------------------------------------------
# Convenience accessors — one function per common data pull
# ---------------------------------------------------------------------------
def get_rfm_scores():
    """Return the entire rfm_scores table as a DataFrame."""
    return query_to_df("SELECT * FROM rfm_scores")


def get_top_products(n=10):
    """Return the top n products ranked by TotalRevenue (descending)."""
    return query_to_df(
        f"SELECT * FROM product_summary ORDER BY TotalRevenue DESC LIMIT {n}"
    )


def get_regional_data():
    """Return the full regional_summary table as a DataFrame."""
    return query_to_df("SELECT * FROM regional_summary")


def get_transactions():
    """Return the entire cleaned transactions table as a DataFrame."""
    return query_to_df("SELECT * FROM transactions")


def get_monthly_revenue():
    """Group transactions by month and return monthly revenue + order count.
    
    We use strftime('%Y-%m', InvoiceDate) inside SQL so the heavy lifting
    happens in the database, not in Python.
    """
    sql = """
        SELECT
            strftime('%Y-%m', InvoiceDate) AS Month,
            SUM(TotalPrice)               AS Revenue,
            COUNT(DISTINCT InvoiceNo)      AS OrderCount
        FROM transactions
        GROUP BY Month
        ORDER BY Month
    """
    return query_to_df(sql)


def get_kpi_summary():
    """Return a dict with top-level business KPIs.
    
    This powers the big number cards at the top of the dashboard.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(DISTINCT CustomerID) FROM transactions")
    total_customers = cursor.fetchone()[0]

    cursor.execute("SELECT SUM(TotalPrice) FROM transactions")
    total_revenue = cursor.fetchone()[0] or 0.0  # guard against empty table

    cursor.execute("SELECT COUNT(DISTINCT InvoiceNo) FROM transactions")
    total_orders = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(DISTINCT Country) FROM transactions")
    countries_covered = cursor.fetchone()[0]

    conn.close()

    return {
        "total_customers": total_customers,
        "total_revenue": round(total_revenue, 2),
        "total_orders": total_orders,
        "countries_covered": countries_covered,
    }


# ---------------------------------------------------------------------------
# Quick self-test
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("🔧 Running database.py self-test …")
    create_tables()
    print("   KPI summary:", get_kpi_summary())
    print("   Done.")
