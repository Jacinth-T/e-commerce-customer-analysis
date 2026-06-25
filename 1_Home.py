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
from utils import inject_css, render_kpi_row, render_sidebar, MODULE_INFO

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

st.divider()

# --- System Modules Section ---
st.subheader("🧩 System Modules")
st.markdown(
    "The data pipeline is composed of four discrete modules, each responsible "
    "for a specific stage of the analysis. The graphs and tables on each page "
    "are powered by these modules."
)

# Render module cards in a 2x2 grid
module_page_map = {
    "alpha": {
        "desc": "Standardizes transaction receipt rows, invoice tables, and website order data.",
        "pages": "📊 Home (KPI Cards) · 📈 Purchase Timeline",
        "icon": "📥",
    },
    "beta": {
        "desc": "Measures customer value boundaries using Recency, Frequency, and Monetary metrics.",
        "pages": "👥 Customer Segments",
        "icon": "📊",
    },
    "gamma": {
        "desc": "Tally order totals across the catalog to trace product performance trends.",
        "pages": "📦 Product Analytics",
        "icon": "📦",
    },
    "delta": {
        "desc": "Tracks customer orders by country to monitor geographic growth.",
        "pages": "🌍 Regional Revenue",
        "icon": "🌍",
    },
}

col_a, col_b = st.columns(2)
for idx, (key, extra) in enumerate(module_page_map.items()):
    info = MODULE_INFO[key]
    card_html = f"""
    <div style="
        background: {info['bg']};
        border-left: 4px solid {info['color']};
        border-radius: 0 10px 10px 0;
        padding: 14px 18px;
        margin-bottom: 2px;
    ">
        <div style="display:flex;align-items:center;gap:8px;margin-bottom:6px;">
            <span style="font-size:15px;">{extra['icon']}</span>
            <span style="font-size:14px;font-weight:700;color:{info['color']};">{info['label']}</span>
            <span style="font-size:12px;color:var(--text-color);opacity:0.6;">·</span>
            <span style="font-size:12px;font-weight:500;color:var(--text-color);opacity:0.8;">{info['name']}</span>
        </div>
        <p style="font-size:12px;color:var(--text-color);opacity:0.7;margin:0 0 8px;line-height:1.5;">{extra['desc']}</p>
        <p style="font-size:11px;font-weight:600;color:var(--text-color);opacity:0.55;margin:0;letter-spacing:0.3px;">USED IN → {extra['pages']}</p>
    </div>
    """
    with (col_a if idx % 2 == 0 else col_b):
        st.markdown(card_html, unsafe_allow_html=True)
