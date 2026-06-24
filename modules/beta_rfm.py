"""
beta_rfm.py — Step 2 of the pipeline: RFM Segmentation.

RFM = Recency, Frequency, Monetary
  - Recency   : How recently did the customer purchase? (lower = better)
  - Frequency  : How often do they purchase? (higher = better)
  - Monetary   : How much do they spend? (higher = better)

Each metric is scored 1-4 via quartiles, then combined into a segment
label like 'Champions', 'At Risk', etc.
"""

import os
import sys
from datetime import timedelta

import pandas as pd

# ---------------------------------------------------------------------------
# Path fix — same pattern as alpha_ingest.py
# ---------------------------------------------------------------------------
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

import database  # noqa: E402


# ---------------------------------------------------------------------------
# Segment assignment logic
# ---------------------------------------------------------------------------
def assign_segment(row):
    """Map R/F/M scores to a human-readable segment name.
    
    WHY check conditions in this specific order?
      → Champions are the most valuable, so we identify them first.
      → The remaining conditions cascade from most to least engaged.
      → 'Others' is the catch-all fallback at the end.
    """
    r, f = row["R_Score"], row["F_Score"]

    if r >= 4 and f >= 4:
        return "Champions"
    elif f >= 3:
        # High frequency but NOT champion → loyal but maybe not recent
        if r <= 2:
            return "At Risk"           # still buying often, but slipping away
        return "Loyal Customers"
    elif r >= 4 and f == 1:
        return "New Customers"         # just showed up, bought once
    elif r >= 3 and f <= 2:
        return "Potential Loyalists"   # recent-ish, low frequency — nurture them
    elif r == 1 and f == 1:
        return "Lost"                  # haven't been back, only came once
    else:
        return "Others"


def run():
    """Build RFM scores for every customer and store in SQLite."""
    print("\n📊  BETA — RFM Segmentation")
    print("=" * 50)

    # -----------------------------------------------------------------------
    # 1. Pull cleaned transactions
    # -----------------------------------------------------------------------
    print("   [1/7] Loading transactions from SQLite …")
    df = database.get_transactions()
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

    # -----------------------------------------------------------------------
    # 2. Determine the snapshot date
    #    WHY +1 day? So that the most-recent purchase has Recency = 1,
    #    not 0 — avoids division-by-zero issues downstream.
    # -----------------------------------------------------------------------
    snapshot_date = df["InvoiceDate"].max() + timedelta(days=1)
    print(f"   [2/7] Snapshot date: {snapshot_date.date()}")

    # -----------------------------------------------------------------------
    # 3. Aggregate per customer
    # -----------------------------------------------------------------------
    print("   [3/7] Computing Recency, Frequency, Monetary per customer …")
    rfm = df.groupby("CustomerID").agg(
        Recency=("InvoiceDate", lambda x: (snapshot_date - x.max()).days),
        Frequency=("InvoiceNo", "nunique"),
        Monetary=("TotalPrice", "sum"),
    ).reset_index()

    # -----------------------------------------------------------------------
    # 4. Score each metric into quartiles (1-4)
    #    WHY duplicates='drop'?  Some metrics have lots of ties at the
    #    boundaries, which would make qcut fail without this flag.
    # -----------------------------------------------------------------------
    print("   [4/7] Scoring into quartiles (1-4) …")

    # Recency is REVERSED — lower days = higher score (more recent = better)
    rfm["R_Score"] = pd.qcut(
        rfm["Recency"],
        q=4,
        labels=False,
        duplicates="drop",
    )
    # Invert: qcut gives 0=lowest → 3=highest; for Recency, low value = good
    rfm["R_Score"] = rfm["R_Score"].max() - rfm["R_Score"] + 1

    rfm["F_Score"] = pd.qcut(
        rfm["Frequency"],
        q=4,
        labels=False,
        duplicates="drop",
    ) + 1  # shift from 0-based to 1-based

    rfm["M_Score"] = pd.qcut(
        rfm["Monetary"],
        q=4,
        labels=False,
        duplicates="drop",
    ) + 1

    # -----------------------------------------------------------------------
    # 5. Create composite RFM_Score string
    # -----------------------------------------------------------------------
    print("   [5/7] Building RFM_Score string …")
    rfm["RFM_Score"] = (
        rfm["R_Score"].astype(str)
        + rfm["F_Score"].astype(str)
        + rfm["M_Score"].astype(str)
    )

    # -----------------------------------------------------------------------
    # 6. Assign segments
    # -----------------------------------------------------------------------
    print("   [6/7] Assigning customer segments …")
    rfm["Segment"] = rfm.apply(assign_segment, axis=1)

    # -----------------------------------------------------------------------
    # 6b. Merge Country info
    #     WHY mode?  A customer may have ordered from multiple countries
    #     (rare, but possible). We take the most common one.
    # -----------------------------------------------------------------------
    country_map = (
        df.groupby("CustomerID")["Country"]
        .agg(lambda x: x.mode().iloc[0])
        .reset_index()
    )
    rfm = rfm.merge(country_map, on="CustomerID", how="left")

    # -----------------------------------------------------------------------
    # 7. Store in SQLite
    # -----------------------------------------------------------------------
    print("   [7/7] Writing to SQLite 'rfm_scores' table …")
    # Reorder columns to match the schema
    rfm = rfm[[
        "CustomerID", "Country", "Recency", "Frequency", "Monetary",
        "R_Score", "F_Score", "M_Score", "RFM_Score", "Segment",
    ]]
    conn = database.get_connection()
    rfm.to_sql("rfm_scores", conn, if_exists="replace", index=False)
    conn.close()

    # -----------------------------------------------------------------------
    # Summary
    # -----------------------------------------------------------------------
    print(f"\n   ✅ RFM complete — {len(rfm):,} customers scored.")
    print("\n   Segment distribution:")
    seg_counts = rfm["Segment"].value_counts()
    for seg, cnt in seg_counts.items():
        pct = cnt / len(rfm) * 100
        print(f"      {seg:<22s} {cnt:>5,}  ({pct:.1f}%)")

    return rfm


# ---------------------------------------------------------------------------
if __name__ == "__main__":
    run()
