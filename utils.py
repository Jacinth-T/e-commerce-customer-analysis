# utils.py
import streamlit as st

SEGMENT_COLORS = {
    "Champions":          "#F97316",   # Orange 500
    "Loyal Customers":    "#f59e0b",   # Amber 500
    "Potential Loyalists":"#fbbf24",   # Amber 400
    "At Risk":            "#ef4444",   # Red 500
    "Lost":               "#9ca3af",   # Gray 400
    "New Customers":      "#34d399",   # Emerald 400
    "Others":             "#a78bfa",   # Purple 400
}

CHART_LAYOUT = dict(
    template="plotly_white",
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    font=dict(family="'Inter', sans-serif", size=12, color="#431407"),
    margin=dict(t=40, b=40, l=50, r=20),
    title=dict(font=dict(size=14)),
    hoverlabel=dict(
        bgcolor="#431407",
        font_color="#FFFFFF",
        font_size=12,
    ),
)

def inject_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    /* Global Typography */
    .stApp {
        font-family: 'Inter', sans-serif !important;
    }
    
    /* Protect Material Icons */
    .material-symbols-rounded, .material-symbols-outlined, [class*="Icon"], [data-testid*="stIcon"] {
        font-family: 'Material Symbols Rounded', 'Material Icons', sans-serif !important;
    }

    /* Sidebar — dark rich orange/brown gradient */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #431407 0%, #7c2d12 100%) !important;
    }
    [data-testid="stSidebar"] .stMarkdown p,
    [data-testid="stSidebar"] .stMarkdown a,
    [data-testid="stSidebar"] label {
        color: rgba(255, 255, 255, 0.75) !important;
        font-size: 13px !important;
    }
    [data-testid="stSidebarNav"] a {
        color: rgba(255, 255, 255, 0.65) !important;
        font-size: 13px !important;
        transition: all 0.2s ease;
    }
    [data-testid="stSidebarNav"] a:hover {
        background: rgba(255,255,255,0.05) !important;
        color: #fff !important;
    }
    [data-testid="stSidebarNav"] a[aria-current="page"] {
        color: #fff !important;
        font-weight: 500 !important;
        background: rgba(255,255,255,0.1) !important;
        border-left: 3px solid #F97316 !important;
        border-radius: 0 !important;
    }

    /* Main area padding */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 3rem !important;
        max-width: 1200px !important;
    }

    /* KPI Cards CSS */
    .kpi-card {
        background: #ffffff;
        border: 1px solid #ffedd5;
        border-radius: 12px;
        padding: 16px 20px;
        box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.05), 0 2px 4px -2px rgb(0 0 0 / 0.05);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .kpi-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1);
    }

    /* Hide default metric borders */
    [data-testid="metric-container"] {
        display: none !important;
    }

    /* Container Card Styling for Charts */
    [data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #ffffff;
        border-radius: 12px !important;
        border: 1px solid #ffedd5 !important;
        box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.03) !important;
    }

    /* Dataframe table styling */
    [data-testid="stDataFrame"] {
        border: 1px solid #ffedd5 !important;
        border-radius: 8px !important;
    }
    </style>
    """, unsafe_allow_html=True)

def format_currency(value: float) -> str:
    """Format a number as £XM or £XK for display."""
    if value >= 1_000_000:
        return f"£{value / 1_000_000:.2f}M"
    elif value >= 1_000:
        return f"£{value / 1_000:.1f}K"
    return f"£{value:,.2f}"

def kpi_card(title: str, value: str, subtitle: str, icon: str, accent_color: str) -> str:
    """Returns an HTML string for a styled KPI card with hover effects."""
    return f"""
    <div class="kpi-card" style="border-top: 3px solid {accent_color};">
        <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 8px;">
            <span style="font-size: 16px;">{icon}</span>
            <span style="font-size: 12px; font-weight: 500; color: #7c2d12;">{title}</span>
        </div>
        <p style="font-size: 28px; font-weight: 700; color: #431407; margin: 0 0 4px; letter-spacing: -0.5px;">{value}</p>
        <p style="font-size: 11px; color: #9a3412; margin: 0; font-weight: 400;">{subtitle}</p>
    </div>
    """

def render_kpi_row(total_customers, total_revenue, total_orders, countries):
    """Render the 4 KPI cards in a 4-column row."""
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(kpi_card(
            "Total customers", f"{total_customers:,}", "unique buyers",
            "👤", "#F97316"
        ), unsafe_allow_html=True)
    with c2:
        st.markdown(kpi_card(
            "Total revenue", format_currency(total_revenue), "gross sales",
            "💷", "#ea580c"
        ), unsafe_allow_html=True)
    with c3:
        st.markdown(kpi_card(
            "Total orders", f"{total_orders:,}", "unique invoices",
            "🧾", "#f59e0b"
        ), unsafe_allow_html=True)
    with c4:
        st.markdown(kpi_card(
            "Countries", f"{countries}", "regions covered",
            "🌍", "#c2410c"
        ), unsafe_allow_html=True)

def section_card(title: str, subtitle: str = "") -> None:
    """Write a styled section header."""
    header = f"""
    <div style="margin-bottom: 8px;">
        <p style="font-size: 15px; font-weight: 600; color: #431407; margin: 0 0 2px;">{title}</p>
        {'<p style="font-size: 12px; color: #9a3412; margin: 0;">' + subtitle + '</p>' if subtitle else ''}
    </div>
    """
    st.markdown(header, unsafe_allow_html=True)
