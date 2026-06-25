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
    margin=dict(t=40, b=40, l=50, r=20),
    title=dict(font=dict(size=14)),
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

    /* Sidebar Navigation Links */
    [data-testid="stSidebarNav"] a {
        transition: all 0.2s ease;
    }
    [data-testid="stSidebarNav"] a:hover {
        background: rgba(128,128,128,0.1) !important;
    }
    [data-testid="stSidebarNav"] a[aria-current="page"] {
        font-weight: 500 !important;
        background: rgba(128,128,128,0.15) !important;
        border-left: 3px solid var(--primary-color) !important;
        border-radius: 0 !important;
    }

    /* Main area padding */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 3rem !important;
        max-width: 1200px !important;
    }

    /* Style the Plotly Notifier Box ("Double-click to zoom back out") */
    .plotly-notifier .notifier-note {
        background-color: var(--secondary-background-color) !important;
        color: var(--text-color) !important;
        border-radius: 8px !important;
        border: 1px solid rgba(128, 128, 128, 0.2) !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2) !important;
        font-family: 'Inter', sans-serif !important;
        padding: 8px 14px !important;
        font-size: 13px !important;
        backdrop-filter: blur(8px) !important;
    }
    .plotly-notifier .notifier-close {
        color: var(--text-color) !important;
        opacity: 0.5 !important;
        right: 4px !important;
        top: 4px !important;
        transition: opacity 0.2s ease !important;
    }
    .plotly-notifier .notifier-close:hover {
        opacity: 1 !important;
    }

    /* KPI Cards CSS - Using CSS Variables for automatic Light/Dark mode toggling */
    .kpi-card {
        background: var(--secondary-background-color);
        border: 1px solid rgba(128, 128, 128, 0.2);
        border-radius: 12px;
        padding: 16px 20px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -2px rgba(0, 0, 0, 0.05);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .kpi-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.2), 0 4px 6px -4px rgba(0, 0, 0, 0.1);
    }

    /* Hide default metric borders */
    [data-testid="metric-container"] {
        display: none !important;
    }

    /* Container Card Styling for Charts */
    [data-testid="stVerticalBlockBorderWrapper"] {
        background-color: var(--secondary-background-color) !important;
        border-radius: 12px !important;
        border: 1px solid rgba(128, 128, 128, 0.2) !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1) !important;
    }

    /* Dataframe table styling */
    [data-testid="stDataFrame"] {
        border: 1px solid rgba(128, 128, 128, 0.2) !important;
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
            <span style="font-size: 12px; font-weight: 500; color: var(--text-color); opacity: 0.8;">{title}</span>
        </div>
        <p style="font-size: 28px; font-weight: 700; color: var(--text-color); margin: 0 0 4px; letter-spacing: -0.5px;">{value}</p>
        <p style="font-size: 11px; color: var(--text-color); opacity: 0.6; margin: 0; font-weight: 400;">{subtitle}</p>
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

def section_card(title: str, subtitle: str = "", module: str = "") -> None:
    """Write a styled section header with optional module badge."""
    badge_html = ""
    if module:
        badge_html = _module_badge_html(module)
    header = f"""
    <div style="margin-bottom: 8px;">
        <div style="display: flex; align-items: center; gap: 10px; flex-wrap: wrap;">
            <p style="font-size: 15px; font-weight: 600; color: var(--text-color); margin: 0;">{title}</p>
            {badge_html}
        </div>
        {'<p style="font-size: 12px; color: var(--text-color); opacity: 0.6; margin: 4px 0 0 0;">' + subtitle + '</p>' if subtitle else ''}
    </div>
    """
    st.markdown(header, unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Module badge system — maps PDF module names to styled pill badges
# ---------------------------------------------------------------------------

# Module metadata matching the PDF exactly
MODULE_INFO = {
    "alpha": {
        "label": "Module Alpha",
        "name": "Consumer Log Handler",
        "color": "#F97316",      # Orange
        "bg": "rgba(249,115,22,0.12)",
    },
    "beta": {
        "label": "Module Beta",
        "name": "RFM Segmentation Core",
        "color": "#8B5CF6",      # Purple
        "bg": "rgba(139,92,246,0.12)",
    },
    "gamma": {
        "label": "Module Gamma",
        "name": "Product Purchase Analytics Module",
        "color": "#10B981",      # Emerald
        "bg": "rgba(16,185,129,0.12)",
    },
    "delta": {
        "label": "Module Delta",
        "name": "Regional Revenue Mapping Subsystem",
        "color": "#3B82F6",      # Blue
        "bg": "rgba(59,130,246,0.12)",
    },
}


def _module_badge_html(module_key: str) -> str:
    """Return inline HTML for a small module pill badge."""
    info = MODULE_INFO.get(module_key, {})
    if not info:
        return ""
    return (
        f'<span style="display:inline-flex;align-items:center;gap:5px;'
        f'background:{info["bg"]};border:1px solid {info["color"]}33;'
        f'border-radius:6px;padding:2px 10px;font-size:11px;font-weight:600;'
        f'color:{info["color"]};letter-spacing:0.3px;white-space:nowrap;">'
        f'{info["label"]}'
        f'</span>'
    )


def module_banner(module_key: str) -> None:
    """Render a full-width module attribution banner below the page title."""
    info = MODULE_INFO.get(module_key)
    if not info:
        return
    st.markdown(f"""
    <div style="
        display: flex; align-items: center; gap: 12px;
        background: {info['bg']}; border-left: 4px solid {info['color']};
        border-radius: 0 8px 8px 0; padding: 10px 16px; margin-bottom: 4px;
    ">
        <span style="font-size: 13px; font-weight: 700; color: {info['color']};">{info['label']}</span>
        <span style="font-size: 12px; color: var(--text-color); opacity: 0.75;">·</span>
        <span style="font-size: 12px; color: var(--text-color); opacity: 0.75;">{info['name']}</span>
    </div>
    """, unsafe_allow_html=True)


def module_banner_multi(module_keys: list) -> None:
    """Render a banner showing multiple modules powering a page."""
    badges = ""
    for key in module_keys:
        info = MODULE_INFO.get(key)
        if not info:
            continue
        badges += (
            f'<div style="display:flex;align-items:center;gap:8px;'
            f'background:{info["bg"]};border-left:3px solid {info["color"]};'
            f'border-radius:0 6px 6px 0;padding:7px 14px;">'
            f'<span style="font-size:12px;font-weight:700;color:{info["color"]};">{info["label"]}</span>'
            f'<span style="font-size:11px;color:var(--text-color);opacity:0.7;">{info["name"]}</span>'
            f'</div>'
        )
    st.markdown(f"""
    <div style="display:flex;flex-direction:column;gap:6px;margin-bottom:4px;">
        {badges}
    </div>
    """, unsafe_allow_html=True)

def render_sidebar():
    """Renders the common sidebar elements across all pages."""
    st.sidebar.title("🛒 E-Commerce Dashboard")
    st.sidebar.markdown("Navigate using the sidebar pages above.")
    st.sidebar.divider()
    
    st.sidebar.markdown("💡 **Pro Tip**: Hover over any graph to interact! You can drag to zoom, double-click to reset, and click the arrows icon in the top right to view it in fullscreen.")
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("""
    <div style="font-size: 10px; color: var(--text-color); opacity: 0.6; line-height: 1.6;">
        <strong style="color: var(--text-color); font-size: 10px; opacity: 0.8;">Dataset</strong><br>
        UCI Online Retail<br>
        Dec 2010 – Dec 2011<br><br>
        <strong style="color: var(--text-color); font-size: 10px; opacity: 0.8;">Project 05</strong><br>
        Data Analytics Capstone
    </div>
    """, unsafe_allow_html=True)
