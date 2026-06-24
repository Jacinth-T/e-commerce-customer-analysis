"""
3_Product_Analytics.py — Catalog Revenue Matrix
================================================
Explores product-level performance with Top-10 charts for revenue
and units sold, plus a searchable product summary table.
"""

import streamlit as st
import plotly.express as px
import pandas as pd
import sys
import os

# Add project root to path so imports work
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import get_top_products, query_to_df
from utils import inject_css, CHART_LAYOUT, section_card

# --- Page Configuration (must be first Streamlit command) ---
st.set_page_config(
    page_title="Product Analytics",
    page_icon="📦",
    layout="wide",
)
inject_css()

# --- Page Header ---
st.title("📦 Product Analytics — Catalog Revenue Matrix")
st.markdown(
    "Explore which products drive the most revenue and which move the highest "
    "volume of units.  Use the search box below to look up any product in the "
    "catalog."
)

st.divider()

# --- Load Data ---
try:
    product_summary = get_top_products(50)
except Exception as e:
    st.error(
        "⚠️ Database not found. Please run `python setup.py` first to "
        "initialize the database and load the data."
    )
    st.exception(e)
    st.stop()

# ------------------------------------------------------------------
# Charts — Top 10 by Revenue & Top 10 by Quantity (side by side)
# ------------------------------------------------------------------
col_left, col_right = st.columns(2)

# --- Chart 1: Top 10 by Revenue (horizontal bar) ---
with col_left:
    with st.container(border=True):
        section_card("Top 10 Products by Revenue")
        top_revenue = product_summary.nlargest(10, "TotalRevenue")

        fig_rev = px.bar(
            top_revenue,
            x="TotalRevenue",
            y="Description",
            orientation="h",
            title="Top 10 Products by Revenue",
            color="TotalRevenue",
            color_continuous_scale="Viridis",
            template="plotly_white",
        )
        fig_rev.update_layout(
            xaxis_title="Total Revenue (£)",
            yaxis_title="",
            yaxis=dict(autorange="reversed"),  # highest at top
            coloraxis_showscale=False,
        )
        fig_rev.update_layout(**CHART_LAYOUT)
        st.plotly_chart(fig_rev, use_container_width=True)

# --- Chart 2: Top 10 by Quantity Sold (horizontal bar) ---
with col_right:
    with st.container(border=True):
        section_card("Top 10 Products by Units Sold")
        top_qty = product_summary.nlargest(10, "TotalQuantitySold")

        fig_qty = px.bar(
            top_qty,
            x="TotalQuantitySold",
            y="Description",
            orientation="h",
            title="Top 10 Products by Units Sold",
            color="TotalQuantitySold",
            color_continuous_scale="Plasma",
            template="plotly_white",
        )
        fig_qty.update_layout(
            xaxis_title="Total Units Sold",
            yaxis_title="",
            yaxis=dict(autorange="reversed"),  # highest at top
            coloraxis_showscale=False,
        )
        fig_qty.update_layout(**CHART_LAYOUT)
        st.plotly_chart(fig_qty, use_container_width=True)

st.divider()

# ------------------------------------------------------------------
# Searchable Product Table
# ------------------------------------------------------------------
with st.container(border=True):
    section_card("Product Catalog Search")

    search_term = st.text_input(
        "Search products by description",
        placeholder="e.g. LUNCH BAG, CANDLE, MUG ...",
    )

    # Apply case-insensitive filter if user has typed something
    if search_term:
        filtered = product_summary[
            product_summary["Description"]
            .str.contains(search_term, case=False, na=False)
        ]
    else:
        filtered = product_summary

    st.caption(f"Showing **{len(filtered)}** of {len(product_summary)} products")
    st.dataframe(
        filtered.sort_values("TotalRevenue", ascending=False),
        use_container_width=True,
    )
