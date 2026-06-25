"""
2_Customer_Segments.py — Customer Segment Analysis (RFM)
========================================================
Visualises customer segments derived from Recency, Frequency,
and Monetary (RFM) scoring.  Includes a scatter/bubble chart,
a segment distribution bar chart, and a summary statistics table.
"""

import streamlit as st
import plotly.express as px
import pandas as pd
import sys
import os

# Add project root to path so imports work
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import get_rfm_scores
from utils import inject_css, SEGMENT_COLORS, CHART_LAYOUT, section_card, render_sidebar, module_banner

# --- Page Configuration (must be first Streamlit command) ---
st.set_page_config(
    page_title="Customer Segments",
    page_icon="👥",
    layout="wide",
)
inject_css()
render_sidebar()

# --- Page Header ---
st.title("👥 Customer Segments — RFM Analysis")
module_banner("beta")
st.markdown(
    "**RFM Analysis** segments customers based on three behavioural dimensions: "
    "**Recency** (how recently they purchased), **Frequency** (how often they buy), "
    "and **Monetary** (how much they spend).  Together these metrics identify your "
    "most valuable customers, at-risk accounts, and new shoppers."
)

st.divider()

# --- Load Data ---
try:
    rfm = get_rfm_scores()
except Exception as e:
    st.error(
        "⚠️ Database not found. Please run `python setup.py` first to "
        "initialize the database and load the data."
    )
    st.exception(e)
    st.stop()

# ------------------------------------------------------------------
# Chart 1 & 2 — Side-by-side: Scatter plot & Segment distribution
# ------------------------------------------------------------------
col_left, col_right = st.columns(2)

# --- Chart 1: Scatter / Bubble — Frequency vs Monetary ---
with col_left:
    with st.container(border=True):
        section_card("RFM Segmentation — Frequency vs. Monetary Value", 
                     "Each dot represents one customer · colored by RFM segment", module="beta")
        
        fig_scatter = px.scatter(
            rfm,
            x="Frequency",
            y="Monetary",
            color="Segment",
            color_discrete_map=SEGMENT_COLORS,
            opacity=0.65,
            log_x=True,
            log_y=True,
            template="plotly_white",
            labels={
                "Frequency": "Order frequency (# invoices)",
                "Monetary": "Total spend (£)",
                "Segment": "Segment"
            },
            title="RFM Segmentation — Frequency vs. Monetary Value"
        )
        
        fig_scatter.update_traces(marker=dict(size=5))  # Small, uniform dots — NOT bubbles
        
        fig_scatter.update_layout(**CHART_LAYOUT)
        fig_scatter.update_layout(
            legend=dict(
                orientation="v",
                yanchor="top",
                y=1,
                xanchor="left",
                x=1.01,
                font=dict(size=11)
            )
        )
        
        st.plotly_chart(fig_scatter, use_container_width=True)

with col_right:
    with st.container(border=True):
        section_card("RFM Segment Distribution", module="beta")
        # Count customers in each segment
        segment_counts = (
            rfm["Segment"]
            .value_counts()
            .reset_index()
            .rename(columns={"index": "Segment", "Segment": "Segment", "count": "Count"})
        )
        # Handle both pandas naming conventions
        if "Count" not in segment_counts.columns:
            segment_counts.columns = ["Segment", "Count"]

        fig_bar = px.bar(
            segment_counts,
            x="Segment",
            y="Count",
            color="Segment",
            color_discrete_map=SEGMENT_COLORS,
            title="RFM Segment Distribution",
            template="plotly_white",
            text_auto=True,
        )
        fig_bar.update_layout(
            xaxis_title="Customer Segment",
            yaxis_title="Number of Customers",
            showlegend=False,
        )
        fig_bar.update_layout(**CHART_LAYOUT)
        st.plotly_chart(fig_bar, use_container_width=True)

st.divider()

# ------------------------------------------------------------------
# Summary Table — Segment-level aggregated statistics
# ------------------------------------------------------------------
with st.container(border=True):
    section_card("RFM Customer Segment Data", "Full RFM scores and segment classifications", module="beta")
    
    # Color mapping for badges
    badge_colors = {
        "Champions": "blue",
        "Loyal Customers": "green",
        "Potential Loyalists": "orange",
        "At Risk": "red",
        "Lost": "gray",
        "New Customers": "violet",
        "Others": "violet",
    }

    st.dataframe(
        rfm[["CustomerID", "Country", "Recency", "Frequency", "Monetary", "Segment"]],
        column_config={
            "CustomerID": st.column_config.TextColumn("Customer ID", width="small"),
            "Recency": st.column_config.NumberColumn("Recency (days)", format="%d days"),
            "Frequency": st.column_config.NumberColumn("Orders", format="%d"),
            "Monetary": st.column_config.NumberColumn("Total spend", format="£%.2f"),
            "Segment": st.column_config.TextColumn("Segment"),
        },
        hide_index=True,
        use_container_width=True,
        height=340,
    )
