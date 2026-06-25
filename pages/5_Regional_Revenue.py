"""
5_Regional_Revenue.py — Geographic Performance
===============================================
Breaks down revenue by country with a horizontal bar chart,
a choropleth world map, and a full data table.  Highlights that
the retailer is UK-based, so the United Kingdom naturally
dominates the revenue distribution.
"""

import streamlit as st
import plotly.express as px
import pandas as pd
import sys
import os

# Add project root to path so imports work
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import get_regional_data
from utils import inject_css, CHART_LAYOUT, section_card, render_sidebar

# --- Page Configuration (must be first Streamlit command) ---
st.set_page_config(
    page_title="Regional Revenue",
    page_icon="🌍",
    layout="wide",
)
inject_css()
render_sidebar()

# --- Page Header ---
st.title("🌍 Regional Revenue — Geographic Performance")
st.markdown(
    "Explore how revenue is distributed across the retailer's international "
    "customer base.  Because the company is **UK-based**, the United Kingdom "
    "accounts for the vast majority of sales."
)

st.divider()

# --- Load Data ---
try:
    regional = get_regional_data()
except Exception as e:
    st.error(
        "⚠️ Database not found. Please run `python setup.py` first to "
        "initialize the database and load the data."
    )
    st.exception(e)
    st.stop()

# Sort by revenue descending for consistent presentation
regional = regional.sort_values("TotalRevenue", ascending=False)

# --- Contextual Note ---
st.info(
    "📌 The **United Kingdom** dominates revenue since the retailer is UK-based. "
    "This is expected and shows analytical awareness of the data source."
)

# ------------------------------------------------------------------
# Chart 1 & 2 — Bar chart and Choropleth side by side
# ------------------------------------------------------------------
col_left, col_right = st.columns(2)

# --- Chart 1: Horizontal Bar — Top 15 Countries by Revenue ---
with col_left:
    with st.container(border=True):
        section_card("Revenue by Country (Top 15)")
        top_15 = regional.head(15)

        fig_bar = px.bar(
            top_15,
            x="TotalRevenue",
            y="Country",
            orientation="h",
            title="Revenue by Country (Top 15)",
            color="TotalRevenue",
            color_continuous_scale="Teal",
            template="plotly_white",
        )
        fig_bar.update_layout(
            xaxis_title="Total Revenue (£)",
            yaxis_title="",
            yaxis=dict(autorange="reversed"),  # highest revenue at the top
            coloraxis_showscale=False,
        )
        fig_bar.update_layout(**CHART_LAYOUT)
        st.plotly_chart(fig_bar, use_container_width=True)

# --- Chart 2: Choropleth — Global Revenue Distribution ---
with col_right:
    with st.container(border=True):
        section_card("Global Revenue Distribution")
        fig_map = px.choropleth(
            regional,
            locations="Country",
            locationmode="country names",
            color="TotalRevenue",
            title="Global Revenue Distribution",
            color_continuous_scale="YlOrRd",
            template="plotly_white",
            projection="natural earth",
        )
        fig_map.update_layout(
            coloraxis_colorbar_title="Revenue (£)",
            geo=dict(showframe=False, showcoastlines=True),
        )
        fig_map.update_layout(**CHART_LAYOUT)
        st.plotly_chart(fig_map, use_container_width=True)

st.divider()

# ------------------------------------------------------------------
# Full Country Data Table
# ------------------------------------------------------------------
with st.container(border=True):
    section_card("Full Country Revenue Breakdown")
    st.dataframe(
        regional.sort_values("TotalRevenue", ascending=False),
        use_container_width=True,
    )
