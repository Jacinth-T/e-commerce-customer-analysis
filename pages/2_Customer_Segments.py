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
from utils import inject_css, SEGMENT_COLORS, CHART_LAYOUT, section_card

# --- Page Configuration (must be first Streamlit command) ---
st.set_page_config(
    page_title="Customer Segments",
    page_icon="👥",
    layout="wide",
)
inject_css()

# --- Page Header ---
st.title("👥 Customer Segments — RFM Analysis")
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
        section_card("Customer segments by frequency & monetary value", 
                     "Each dot represents one customer · colored by RFM segment")
        
        fig_scatter = px.scatter(
            rfm,
            x="Frequency",
            y="Monetary",
            color="Segment",
            color_discrete_map=SEGMENT_COLORS,
            opacity=0.65,
            template="plotly_white",
            labels={
                "Frequency": "Order frequency (# invoices)",
                "Monetary": "Total spend (£)",
                "Segment": "Segment"
            },
            title="Customer segments — frequency vs. monetary value"
        )
        
        fig_scatter.update_traces(marker=dict(size=5))  # Small, uniform dots — NOT bubbles
        
        fig_scatter.update_layout(
            plot_bgcolor="#FFFFFF",
            paper_bgcolor="#FFFFFF",
            font=dict(family="sans-serif", color="#1E293B"),
            title=dict(font=dict(size=14, weight="normal")),
            margin=dict(t=40, b=40, l=50, r=20),
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
        section_card("Number of customers per segment")
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
            title="Number of Customers per Segment",
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
    section_card("Customer Segment Data", "Full RFM scores and segment classifications")
    
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
