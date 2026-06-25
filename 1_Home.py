"""
app.py — Streamlit Entry Point (Home / Overview Page)
=====================================================
Main landing page for the E-Commerce Customer Behavior Analysis dashboard.
Displays KPI summary cards and a brief project overview.
"""

import streamlit as st
import plotly.express as px
import sys
import os

# Add project root to path so imports work
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import get_kpi_summary, get_transactions, query_to_df
from utils import inject_css, render_kpi_row, render_sidebar

# --- Page Configuration (must be first Streamlit command) ---
st.set_page_config(
    page_title="E-Commerce Dashboard",
    page_icon="🛒",
    layout="wide",
)
inject_css()

# --- Sidebar ---
render_sidebar()

# --- Main Page Title ---
st.title("🛒 E-Commerce Customer Behavior Analysis")
st.markdown(
    "Welcome to the **E-Commerce Customer Behavior Analysis** dashboard. "
    "This project explores transactional data from a UK-based online retailer "
    "to uncover purchasing patterns, customer segments, product performance, "
    "and regional revenue insights."
)

st.divider()

# --- KPI Summary Cards ---
try:
    # Fetch high-level metrics from the database
    kpi = get_kpi_summary()

    # Display four metric cards side-by-side
    render_kpi_row(
        kpi['total_customers'],
        kpi['total_revenue'],
        kpi['total_orders'],
        kpi['countries_covered']
    )

except Exception as e:
    st.error(
        "⚠️ Database not found. Please run `python setup.py` first to "
        "initialize the database and load the data."
    )
    st.exception(e)
    st.stop()

st.divider()

# --- Quick Summary Section ---
st.subheader("📋 About the Dataset")
st.markdown(
    """
    This dashboard analyses the **UCI Online Retail** dataset, which contains
    all transactions occurring between **December 2010** and **December 2011**
    for a **UK-based and registered non-store online retailer**.

    The company mainly sells unique all-occasion gifts, and many of its
    customers are wholesalers. Key highlights of the dataset:

    - **Transactional data** with invoice-level detail (products, quantities, prices)
    - **Customer identifiers** enabling behavioural segmentation (RFM analysis)
    - **International reach** spanning multiple countries across Europe and beyond

    Use the **sidebar pages** to explore:
    - 👥 **Customer Segments** — RFM-based behavioural clustering
    - 📦 **Product Analytics** — Catalog revenue matrix & top sellers
    - 📈 **Purchase Timeline** — Monthly trends & seasonal patterns
    - 🌍 **Regional Revenue** — Geographic performance breakdown
    """
)
