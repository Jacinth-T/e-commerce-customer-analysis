"""
4_Purchase_Timeline.py — Purchase Ingestion Timeline
=====================================================
Visualises monthly revenue and order volume trends across the
Dec 2010 – Dec 2011 dataset period.  Highlights seasonal spikes
such as the pre-Christmas shopping rush.
"""

import streamlit as st
import plotly.express as px
import pandas as pd
import sys
import os

# Add project root to path so imports work
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import get_monthly_revenue
from utils import inject_css, CHART_LAYOUT, section_card

# --- Page Configuration (must be first Streamlit command) ---
st.set_page_config(
    page_title="Purchase Timeline",
    page_icon="📈",
    layout="wide",
)
inject_css()

# --- Page Header ---
st.title("📈 Purchase Timeline — Monthly Trends")
st.markdown(
    "This page tracks **temporal purchasing patterns** across the dataset period. "
    "Monthly aggregations reveal seasonal trends, growth trajectories, and "
    "anomalies that inform inventory and marketing decisions."
)

st.divider()

# --- Load Data ---
try:
    monthly = get_monthly_revenue()
except Exception as e:
    st.error(
        "⚠️ Database not found. Please run `python setup.py` first to "
        "initialize the database and load the data."
    )
    st.exception(e)
    st.stop()

# ------------------------------------------------------------------
# Chart 1: Monthly Revenue — Line Chart
# ------------------------------------------------------------------
with st.container(border=True):
    section_card("Monthly Revenue Over Time")

    fig_line = px.line(
        monthly,
        x="Month",
        y="Revenue",
        title="Monthly Revenue Over Time",
        template="plotly_white",
        markers=True,
    )
    fig_line.update_layout(
        xaxis_title="Month",
        yaxis_title="Total Revenue (£)",
    )

    # Add annotation for the Nov-Dec Christmas spike
    fig_line.add_annotation(
        x=monthly["Month"].iloc[-2] if len(monthly) >= 2 else monthly["Month"].iloc[-1],
        y=monthly["Revenue"].max(),
        text="🎄 Christmas Rush",
        showarrow=True,
        arrowhead=2,
        ax=-60,
        ay=-40,
        font=dict(size=12, color="crimson"),
    )

    fig_line.update_layout(**CHART_LAYOUT)
    st.plotly_chart(fig_line, use_container_width=True)

st.divider()

# ------------------------------------------------------------------
# Chart 2: Monthly Order Volume — Bar Chart
# ------------------------------------------------------------------
with st.container(border=True):
    section_card("Monthly Order Volume")

    fig_bar = px.bar(
        monthly,
        x="Month",
        y="OrderCount",
        title="Monthly Order Volume",
        color="OrderCount",
        color_continuous_scale="Blues",
        template="plotly_white",
        text_auto=True,
    )
    fig_bar.update_layout(
        xaxis_title="Month",
        yaxis_title="Number of Orders",
        coloraxis_showscale=False,
    )

    fig_bar.update_layout(**CHART_LAYOUT)
    st.plotly_chart(fig_bar, use_container_width=True)

# --- Insight Box ---
st.info(
    "📌 **Seasonal Insight:** A clear spike in both revenue and order volume is "
    "visible in **November 2011**, driven by the pre-Christmas shopping rush. "
    "This is typical for online gift retailers and aligns with Black Friday / "
    "holiday season demand.  December shows a slight dip as order cut-off dates "
    "for holiday delivery pass."
)
