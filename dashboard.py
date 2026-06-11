import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import warnings, os

warnings.filterwarnings("ignore")

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="FMCG Sales Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
)



# ── Design tokens ─────────────────────────────────────────────────────────────
# Primary accent: fresh green  #2D6A4F  (FMCG / consumer goods feel)
# Surface:        white        #FFFFFF
# Background:     off-white    #F7F8FA
# Border:         subtle grey  #E4E7EC
# Text primary:   near-black   #111827
# Text secondary: medium grey  #6B7280
# Text muted:     light grey   #9CA3AF

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

:root {
    --green:        #2D6A4F;
    --green-mid:    #40916C;
    --green-light:  #74C69D;
    --green-dim:    rgba(45,106,79,0.08);
    --amber:        #D97706;
    --red:          #C0392B;
    --bg:           #F7F8FA;
    --surface:      #FFFFFF;
    --border:       #E4E7EC;
    --border-strong:#C9D0D9;
    --text-primary: #111827;
    --text-secondary:#6B7280;
    --text-muted:   #9CA3AF;
    --radius:       8px;
    --radius-lg:    12px;
}

html, body, [class*="css"], [class*="st-"] {
    font-family: 'Inter', -apple-system, sans-serif !important;
}

.stApp {
    background: var(--bg) !important;
}

/* ── Sidebar ─────────────────────────────────────── */
[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] * {
    color: var(--text-primary) !important;
}
[data-testid="stSidebar"] .stRadio label,
[data-testid="stSidebar"] .stMultiSelect label,
[data-testid="stSidebar"] .stSelectbox label {
    font-size: 0.7rem !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.1em !important;
    color: var(--text-muted) !important;
}
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label {
    font-size: 0.875rem !important;
    font-weight: 500 !important;
    text-transform: none !important;
    letter-spacing: 0 !important;
    color: var(--text-secondary) !important;
    padding: 0.4rem 0.6rem !important;
    border-radius: var(--radius) !important;
}
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:hover {
    background: var(--green-dim) !important;
    color: var(--green) !important;
}
[data-testid="stSidebar"] hr {
    border-color: var(--border) !important;
    margin: 1rem 0 !important;
}

/* ── Page Header ─────────────────────────────────── */
.page-header {
    border-left: 3px solid var(--green);
    padding: 0.35rem 0 0.35rem 1rem;
    margin-bottom: 1.5rem;
}
.page-header h1 {
    font-size: 1.375rem;
    font-weight: 700;
    color: var(--text-primary);
    margin: 0 0 0.2rem 0;
    letter-spacing: -0.02em;
    line-height: 1.3;
}
.page-header p {
    font-size: 0.8rem;
    color: var(--text-secondary);
    margin: 0;
}

/* ── KPI Cards ───────────────────────────────────── */
.kpi-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    padding: 1.1rem 1.25rem 1rem 1.25rem;
    position: relative;
    overflow: hidden;
}
.kpi-card::after {
    content: '';
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 2px;
    background: var(--green);
    border-radius: 0 0 var(--radius-lg) var(--radius-lg);
    opacity: 0;
    transition: opacity 0.2s;
}
.kpi-card:hover::after { opacity: 1; }
.kpi-label {
    font-size: 0.68rem;
    font-weight: 700;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-bottom: 0.35rem;
}
.kpi-value {
    font-size: 1.65rem;
    font-weight: 700;
    color: var(--text-primary);
    line-height: 1.1;
    letter-spacing: -0.03em;
}
.kpi-delta {
    display: inline-block;
    font-size: 0.72rem;
    font-weight: 600;
    margin-top: 0.4rem;
    padding: 0.2rem 0.55rem;
    border-radius: 20px;
}
.kpi-delta.up   { color:#166534; background:rgba(22,101,52,0.09); }
.kpi-delta.down { color:#991B1B; background:rgba(153,27,27,0.09); }
.kpi-delta.neu  { color:var(--text-muted); background:rgba(156,163,175,0.12); }

/* ── Section Label ───────────────────────────────── */
.section-label {
    font-size: 0.68rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: var(--text-muted);
    margin: 0 0 0.6rem 0;
}

/* ── Chart Title ─────────────────────────────────── */
.chart-title {
    font-size: 0.875rem;
    font-weight: 600;
    color: var(--text-primary);
    margin-bottom: 0.15rem;
    letter-spacing: -0.01em;
}
.chart-sub {
    font-size: 0.75rem;
    color: var(--text-muted);
    margin-bottom: 0.5rem;
}

/* ── Divider ─────────────────────────────────────── */
.rule {
    height: 1px;
    background: var(--border);
    margin: 1.5rem 0;
    border: none;
}

/* ── Footer ──────────────────────────────────────── */
.dash-footer {
    margin-top: 2.5rem;
    padding-top: 1rem;
    border-top: 1px solid var(--border);
    font-size: 0.72rem;
    color: var(--text-muted);
    display: flex;
    justify-content: space-between;
}

/* ── Global tweaks ───────────────────────────────── */
#MainMenu, footer { visibility: hidden; }
[data-testid="stPlotlyChart"] { border-radius: var(--radius); }
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--border-strong); border-radius: 3px; }

/* ── Streamlit header — styled as navbar ─────────── */
header[data-testid="stHeader"] {
    background: var(--surface) !important;
    border-bottom: 1px solid var(--border) !important;
}

/* Keep decoration and toolbar hidden but NOT the sidebar button */
[data-testid="stDecoration"] { display: none !important; }

/* Sidebar collapse/expand button — always visible */
[data-testid="stSidebarCollapseButton"],
[data-testid="stSidebarExpandButton"],
[data-testid="collapsedControl"] {
    display: flex !important;
    visibility: visible !important;
    opacity: 1 !important;
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    color: var(--text-primary) !important;
}
[data-testid="stSidebarCollapseButton"]:hover,
[data-testid="stSidebarExpandButton"]:hover,
[data-testid="collapsedControl"]:hover {
    background: var(--green-dim) !important;
    border-color: var(--green) !important;
    color: var(--green) !important;
}

/* Content padding */
.main .block-container {
    padding: 1.75rem 2rem 3rem 2rem;
    max-width: 1360px;
}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)


# ── Plotly base theme ─────────────────────────────────────────────────────────
BG     = "#FFFFFF"
GRID   = "#F3F4F6"
TICK   = "#9CA3AF"
FONT   = "Inter, -apple-system, sans-serif"

GREEN      = "#2D6A4F"
GREEN_MID  = "#40916C"
GREEN_LT   = "#74C69D"
AMBER      = "#D97706"
RED_SOFT   = "#C0392B"
BLUE_SOFT  = "#2563EB"
INDIGO     = "#4F46E5"
ROSE       = "#DB2777"

# Per-dimension color palettes
CAT_PAL = {
    "Milk"     : GREEN,
    "Yogurt"   : GREEN_MID,
    "ReadyMeal": AMBER,
    "SnackBar" : INDIGO,
    "Juice"    : ROSE,
}
CH_PAL = {
    "Retail"    : GREEN,
    "Discount"  : AMBER,
    "E-commerce": BLUE_SOFT,
}
REG_PAL = {
    "PL-North"  : GREEN,
    "PL-South"  : GREEN_MID,
    "PL-Central": AMBER,
}
PROMO_PAL = {
    "Promoted"    : GREEN,
    "Non-Promoted": "#9CA3AF",
}

def base_layout(height=320, **kwargs):
    return dict(
        paper_bgcolor=BG, plot_bgcolor=BG,
        height=height,
        font=dict(family=FONT, color=TICK, size=12),
        margin=dict(t=28, b=16, l=12, r=72),
        hoverlabel=dict(
            bgcolor="#111827",
            font_size=12,
            font_family=FONT,
            font_color="#F9FAFB",
            bordercolor="#111827",
        ),
        **kwargs
    )

def axis_x(**kw):
    return dict(gridcolor=GRID, linecolor=GRID, zerolinecolor=GRID,
                tickfont=dict(size=11, color=TICK),
                title_font=dict(size=11, color="#6B7280"),
                zeroline=False, **kw)

def axis_y(**kw):
    return dict(gridcolor=GRID, linecolor="rgba(0,0,0,0)", zerolinecolor=GRID,
                tickfont=dict(size=11, color=TICK),
                title_font=dict(size=11, color="#6B7280"),
                zeroline=False, **kw)


# ── Load data ─────────────────────────────────────────────────────────────────
@st.cache_data
def load_data(path):
    df = pd.read_csv(path)
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    for col in ["price_unit","stock_available","delivered_qty","units_sold","delivery_days"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    for col in ["stock_available","delivered_qty","units_sold"]:
        df[col] = df[col].clip(lower=0)
    for col in ["price_unit","units_sold","delivered_qty","stock_available","delivery_days"]:
        Q1, Q3 = df[col].quantile(0.25), df[col].quantile(0.75)
        df[col] = df[col].clip(Q1 - 3*(Q3-Q1), Q3 + 3*(Q3-Q1))
    if "revenue" not in df.columns:
        df["revenue"] = (df["price_unit"] * df["units_sold"]).round(2)
    if "sell_through_rate" not in df.columns:
        df["sell_through_rate"] = np.where(
            df["delivered_qty"] > 0,
            (df["units_sold"] / df["delivered_qty"] * 100).round(2), 0
        ).clip(0, 100)
    if "stock_adequate" not in df.columns:
        df["stock_adequate"] = (df["stock_available"] >= df["delivered_qty"]).astype(int)
    if "is_promoted" not in df.columns:
        df["is_promoted"] = df["promotion_flag"].map({1: "Promoted", 0: "Non-Promoted"})
    if "year" not in df.columns:
        df["year"]       = df["date"].dt.year
        df["month"]      = df["date"].dt.month
        df["month_name"] = df["date"].dt.strftime("%b")
        df["quarter"]    = df["date"].dt.quarter.map({1:"Q1",2:"Q2",3:"Q3",4:"Q4"})
        df["yearmonth"]  = df["date"].dt.to_period("M").astype(str)
    if "delivery_tier" not in df.columns:
        bins   = [0, 1, 2, 3, 5.01]
        labels = ["Same Day", "Fast (2d)", "Standard (3d)", "Slow (4-5d)"]
        df["delivery_tier"] = pd.cut(df["delivery_days"], bins=bins, labels=labels, include_lowest=True)
    return df


PATHS = [
    "cleaned_FMCG_data.csv",
    "FMCG_2022_2024.csv",
    "data/cleaned_FMCG_data.csv",
    "data/FMCG_2022_2024.csv",
]
df_full = None
for p in PATHS:
    if os.path.exists(p):
        df_full = load_data(p)
        break

if df_full is None:
    st.markdown("### Upload Dataset")
    uploaded = st.file_uploader("Upload cleaned_FMCG_data.csv", type="csv")
    if uploaded:
        df_full = load_data(uploaded)
        st.rerun()
    else:
        st.info("Place the CSV file in the same folder as `dashboard.py`, or upload directly above.")
        st.stop()


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding:0.75rem 0 0.5rem 0'>
        <div style='font-size:0.62rem;font-weight:700;color:#9CA3AF;
                    text-transform:uppercase;letter-spacing:0.12em;margin-bottom:0.2rem'>
            Dashboard
        </div>
        <div style='font-size:1rem;font-weight:700;color:#111827;letter-spacing:-0.01em'>
            FMCG Sales 2022–2024
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)

    page = st.radio(
        "nav",
        ["Executive Overview", "Product & Channel", "Operations & Promotion"],
        label_visibility="collapsed"
    )

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown('<div style="font-size:0.68rem;font-weight:700;color:#9CA3AF;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:0.5rem">Filters</div>', unsafe_allow_html=True)

    sel_year = st.multiselect(
        "Year", sorted(df_full["year"].unique()),
        default=sorted(df_full["year"].unique())
    )
    sel_cat = st.multiselect(
        "Category", sorted(df_full["category"].unique()),
        default=sorted(df_full["category"].unique())
    )
    sel_channel = st.multiselect(
        "Channel", sorted(df_full["channel"].unique()),
        default=sorted(df_full["channel"].unique())
    )
    sel_region = st.multiselect(
        "Region", sorted(df_full["region"].unique()),
        default=sorted(df_full["region"].unique())
    )

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style='font-size:0.72rem;color:#9CA3AF;line-height:2'>
        <span style='color:#6B7280;font-weight:500'>{len(df_full):,}</span> transactions<br>
        Jan 2022 – Dec 2024
    </div>
    """, unsafe_allow_html=True)


# ── Apply filters ─────────────────────────────────────────────────────────────
df = df_full[
    df_full["year"].isin(sel_year) &
    df_full["category"].isin(sel_cat) &
    df_full["channel"].isin(sel_channel) &
    df_full["region"].isin(sel_region)
].copy()

if df.empty:
    st.warning("No data matches the selected filters.")
    st.stop()


# ── Helpers ───────────────────────────────────────────────────────────────────
def header(title, subtitle=""):
    sub = f"<p>{subtitle}</p>" if subtitle else ""
    st.markdown(f'<div class="page-header"><h1>{title}</h1>{sub}</div>', unsafe_allow_html=True)

def kpi(label, value, delta=None, dtype="neu"):
    d_html = ""
    if delta:
        arrow = "▲" if dtype=="up" else ("▼" if dtype=="down" else "·")
        d_html = f'<div class="kpi-delta {dtype}">{arrow} {delta}</div>'
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
        {d_html}
    </div>""", unsafe_allow_html=True)

def ctitle(title, sub=""):
    s = f'<div class="chart-sub">{sub}</div>' if sub else ""
    st.markdown(f'<div class="chart-title">{title}</div>{s}', unsafe_allow_html=True)

def rule():
    st.markdown('<div class="rule"></div>', unsafe_allow_html=True)

def fmt_rev(v):
    if v >= 1e9: return f"${v/1e9:.2f}B"
    if v >= 1e6: return f"${v/1e6:.1f}M"
    if v >= 1e3: return f"${v/1e3:.1f}K"
    return f"${v:.0f}"


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 1 — EXECUTIVE OVERVIEW
# ═══════════════════════════════════════════════════════════════════════════════

if page == "Executive Overview":
    header("Executive Overview", "FMCG sales performance summary 2022 to 2024")

    total_rev   = df["revenue"].sum()
    total_units = df["units_sold"].sum()
    total_tx    = len(df)
    avg_str     = df["sell_through_rate"].mean()
    avg_del     = df["delivery_days"].mean()
    rev_23      = df[df["year"] == 2023]["revenue"].sum()
    rev_24      = df[df["year"] == 2024]["revenue"].sum()
    yoy         = ((rev_24 / rev_23) - 1) * 100 if rev_23 > 0 else 0
    yoy_type    = "up" if yoy >= 0 else "down"

    c1, c2, c3, c4, c5 = st.columns(5)
    with c1: kpi("Total Revenue",      fmt_rev(total_rev), f"YoY 23→24: {yoy:+.1f}%", yoy_type)
    with c2: kpi("Total Units Sold",   f"{total_units/1e6:.2f}M")
    with c3: kpi("Total Transactions", f"{total_tx:,}")
    with c4: kpi("Avg Sell-Through",   f"{avg_str:.2f}%")
    with c5: kpi("Avg Delivery Days",  f"{avg_del:.1f}d")

    rule()

    # Monthly trend + Revenue by category
    c1, c2 = st.columns([2, 1], gap="medium")

    with c1:
        monthly = df.groupby("yearmonth")["revenue"].sum().reset_index().sort_values("yearmonth")
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=monthly["yearmonth"], y=monthly["revenue"],
            mode="lines",
            line=dict(color=GREEN, width=2, shape="spline"),
            fill="tozeroy",
            fillcolor="rgba(45,106,79,0.07)",
            hovertemplate="<b>%{x}</b><br>Revenue: $%{y:,.0f}<extra></extra>",
        ))
        for yr in ["2023-01", "2024-01"]:
            if yr in monthly["yearmonth"].values:
                fig.add_vline(x=yr, line_dash="dot", line_color=GRID, line_width=1.5)
        fig.update_layout(
            **base_layout(height=300),
            xaxis=axis_x(tickangle=-45, tickvals=monthly["yearmonth"].iloc[::4].tolist()),
            yaxis=axis_y(tickformat="$.2s"),
            showlegend=False,
        )
        ctitle("Monthly Revenue Trend", "Dotted lines mark year boundaries")
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    with c2:
        cat_rev = df.groupby("category")["revenue"].sum().reset_index().sort_values("revenue")
        fig = go.Figure(go.Bar(
            x=cat_rev["revenue"], y=cat_rev["category"],
            orientation="h",
            marker_color=[CAT_PAL.get(c, TICK) for c in cat_rev["category"]],
            marker_line_width=0,
            text=cat_rev["revenue"].apply(lambda x: f"${x/1e6:.1f}M"),
            textposition="outside",
            textfont=dict(size=11, color=TICK, family=FONT),
            hovertemplate="<b>%{y}</b><br>$%{x:,.0f}<extra></extra>",
        ))
        fig.update_layout(
            **base_layout(height=300),
            xaxis=axis_x(tickformat="$.2s"),
            yaxis=axis_y(),
            showlegend=False,
        )
        ctitle("Revenue by Category")
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    rule()

    # Donut channel + Heatmap quarter × year
    c1, c2 = st.columns([1, 2], gap="medium")

    with c1:
        ch_rev = df.groupby("channel")["revenue"].sum().reset_index()
        fig = go.Figure(go.Pie(
            labels=ch_rev["channel"],
            values=ch_rev["revenue"],
            hole=0.62,
            marker_colors=[CH_PAL.get(c, TICK) for c in ch_rev["channel"]],
            textinfo="percent+label",
            textposition="outside",
            textfont=dict(size=12, family=FONT),
            hovertemplate="<b>%{label}</b><br>$%{value:,.0f} — %{percent}<extra></extra>",
            pull=[0.02] * len(ch_rev),
        ))
        total_center = fmt_rev(ch_rev["revenue"].sum())
        fig.update_layout(
            **base_layout(height=300),
            showlegend=False,
            annotations=[dict(
                text=f"<b>{total_center}</b>",
                x=0.5, y=0.5,
                font=dict(size=15, color="#111827", family=FONT),
                showarrow=False
            )]
        )
        ctitle("Revenue by Channel")
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    with c2:
        pivot = df.pivot_table(values="revenue", index="year", columns="quarter", aggfunc="sum").fillna(0)
        text_vals = [[f"${v/1e6:.1f}M" for v in row] for row in pivot.values]
        fig = go.Figure(go.Heatmap(
            z=pivot.values,
            x=pivot.columns.tolist(),
            y=[str(y) for y in pivot.index.tolist()],
            colorscale=[[0, "#F0FDF4"], [0.5, "#86EFAC"], [1, GREEN]],
            text=text_vals,
            texttemplate="%{text}",
            textfont={"size": 13, "family": FONT, "color": "#111827"},
            showscale=False,
            hovertemplate="Year %{y} · %{x}: %{text}<extra></extra>",
            xgap=4, ygap=4,
        ))
        fig.update_layout(
            **base_layout(height=300),
            xaxis=dict(side="top", **axis_x()),
            yaxis=axis_y(),
        )
        ctitle("Quarterly Revenue Heatmap", "Darker = higher revenue")
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    # Region bar
    rule()
    reg_rev = df.groupby("region")["revenue"].sum().reset_index().sort_values("revenue", ascending=True)
    fig = go.Figure(go.Bar(
        x=reg_rev["revenue"], y=reg_rev["region"],
        orientation="h",
        marker_color=[REG_PAL.get(r, TICK) for r in reg_rev["region"]],
        marker_line_width=0,
        text=reg_rev["revenue"].apply(lambda x: fmt_rev(x)),
        textposition="outside",
        textfont=dict(size=12, color=TICK, family=FONT),
        hovertemplate="<b>%{y}</b><br>$%{x:,.0f}<extra></extra>",
    ))
    fig.update_layout(
        **base_layout(height=220),
        xaxis=axis_x(tickformat="$.2s"),
        yaxis=axis_y(),
        showlegend=False,
    )
    ctitle("Revenue by Region")
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 2 — PRODUCT & CHANNEL
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "Product & Channel":
    header("Product & Channel Performance", "Brand, category, and distribution channel breakdown")

    best_cat   = df.groupby("category")["revenue"].sum().idxmax()
    best_ch    = df.groupby("channel")["revenue"].sum().idxmax()
    best_brand = df.groupby("brand")["revenue"].sum().idxmax()
    avg_price  = df["price_unit"].mean()

    c1, c2, c3, c4 = st.columns(4)
    with c1: kpi("Top Category",   best_cat)
    with c2: kpi("Top Channel",    best_ch)
    with c3: kpi("Top Brand",      best_brand)
    with c4: kpi("Avg Price/Unit", f"${avg_price:.2f}")

    rule()

    # Top 10 brands + Category × Channel stacked
    c1, c2 = st.columns(2, gap="medium")

    with c1:
        top10 = (df.groupby("brand")["revenue"].sum().reset_index()
                   .sort_values("revenue", ascending=False).head(10)
                   .sort_values("revenue", ascending=True))
        n = len(top10)
        greens = [f"rgba(45,106,79,{0.35 + 0.65 * i / max(n-1,1)})" for i in range(n)]
        fig = go.Figure(go.Bar(
            x=top10["revenue"], y=top10["brand"],
            orientation="h",
            marker_color=greens,
            marker_line_width=0,
            text=top10["revenue"].apply(lambda x: f"${x/1e6:.2f}M"),
            textposition="outside",
            textfont=dict(size=11, color=TICK, family=FONT),
            hovertemplate="<b>%{y}</b><br>$%{x:,.0f}<extra></extra>",
        ))
        fig.update_layout(
            **base_layout(height=360),
            xaxis=axis_x(tickformat="$.2s"),
            yaxis=axis_y(),
            showlegend=False,
        )
        ctitle("Top 10 Brands by Revenue")
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    with c2:
        cat_ch = df.groupby(["category", "channel"])["units_sold"].sum().reset_index()
        fig = go.Figure()
        for ch, color in CH_PAL.items():
            sub = cat_ch[cat_ch["channel"] == ch]
            fig.add_trace(go.Bar(
                x=sub["category"], y=sub["units_sold"],
                name=ch, marker_color=color, marker_line_width=0,
                hovertemplate=f"<b>%{{x}}</b><br>{ch}: %{{y:,.0f}} units<extra></extra>",
            ))
        fig.update_layout(
            **base_layout(height=360), barmode="stack",
            yaxis=axis_y(tickformat=".2s"),
            xaxis=axis_x(),
            legend=dict(orientation="h", y=-0.18, font=dict(size=11),
                        bgcolor="rgba(0,0,0,0)", borderwidth=0),
        )
        ctitle("Units Sold — Category × Channel")
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    rule()

    # Channel monthly trend + Avg price per category
    c1, c2 = st.columns([2, 1], gap="medium")

    with c1:
        ch_monthly = (df.groupby(["yearmonth", "channel"])["revenue"].sum()
                        .reset_index().sort_values("yearmonth"))
        fig = go.Figure()
        for ch, color in CH_PAL.items():
            sub = ch_monthly[ch_monthly["channel"] == ch]
            fig.add_trace(go.Scatter(
                x=sub["yearmonth"], y=sub["revenue"],
                name=ch, line=dict(color=color, width=2),
                mode="lines+markers", marker_size=3,
                hovertemplate=f"<b>{ch}</b><br>%{{x}}<br>$%{{y:,.0f}}<extra></extra>",
            ))
        fig.update_layout(
            **base_layout(height=320),
            xaxis=axis_x(tickangle=-45,
                         tickvals=ch_monthly["yearmonth"].unique()[::4].tolist()),
            yaxis=axis_y(tickformat="$.2s"),
            legend=dict(orientation="h", y=-0.24, font=dict(size=11),
                        bgcolor="rgba(0,0,0,0)", borderwidth=0),
        )
        ctitle("Monthly Revenue Trend by Channel")
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    with c2:
        apc = (df.groupby("category")["price_unit"].mean().reset_index()
                 .sort_values("price_unit", ascending=True))
        fig = go.Figure(go.Bar(
            x=apc["price_unit"], y=apc["category"],
            orientation="h",
            marker_color=[CAT_PAL.get(c, TICK) for c in apc["category"]],
            marker_line_width=0,
            text=apc["price_unit"].apply(lambda x: f"${x:.2f}"),
            textposition="outside",
            textfont=dict(size=11, color=TICK, family=FONT),
            hovertemplate="<b>%{y}</b><br>Avg Price: $%{x:.2f}<extra></extra>",
        ))
        fig.update_layout(
            **base_layout(height=320),
            xaxis=axis_x(tickformat="$.2f"),
            yaxis=axis_y(),
            showlegend=False,
        )
        ctitle("Avg Price/Unit by Category")
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    rule()

    # Pack type × Category
    pack_data = df.groupby(["pack_type", "category"])["revenue"].sum().reset_index()
    fig = go.Figure()
    for cat, color in CAT_PAL.items():
        sub = pack_data[pack_data["category"] == cat]
        fig.add_trace(go.Bar(
            x=sub["pack_type"], y=sub["revenue"],
            name=cat, marker_color=color, marker_line_width=0,
            hovertemplate=f"<b>%{{x}}</b><br>{cat}: $%{{y:,.0f}}<extra></extra>",
        ))
    fig.update_layout(
        **base_layout(height=300), barmode="group",
        yaxis=axis_y(tickformat="$.2s"),
        xaxis=axis_x(),
        legend=dict(orientation="h", y=-0.22, font=dict(size=11),
                    bgcolor="rgba(0,0,0,0)", borderwidth=0),
    )
    ctitle("Revenue by Pack Type × Category")
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 3 — OPERATIONS & PROMOTION
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "Operations & Promotion":
    header("Operations & Promotion", "Distribution efficiency, stock adequacy, and promotion impact")

    avg_str     = df["sell_through_rate"].mean()
    stock_adeq  = df["stock_adequate"].mean() * 100
    promo_units = df[df["promotion_flag"] == 1]["units_sold"].mean()
    non_promo   = df[df["promotion_flag"] == 0]["units_sold"].mean()
    uplift      = (promo_units / non_promo - 1) * 100 if non_promo > 0 else 0
    avg_del     = df["delivery_days"].mean()

    c1, c2, c3, c4, c5 = st.columns(5)
    with c1: kpi("Avg Sell-Through",  f"{avg_str:.2f}%")
    with c2: kpi("Stock Adequacy",    f"{stock_adeq:.1f}%",
                 "Below 80% target" if stock_adeq < 80 else "On target",
                 "down" if stock_adeq < 80 else "up")
    with c3: kpi("Avg Units (Promo)",    f"{promo_units:.1f}")
    with c4: kpi("Avg Units (Non-Promo)",f"{non_promo:.1f}")
    with c5: kpi("Promo Uplift",      f"+{uplift:.1f}%", dtype="up")

    rule()

    # Sell-through by category + Stock adequacy
    c1, c2 = st.columns(2, gap="medium")

    with c1:
        avg_overall = df["sell_through_rate"].mean()
        str_cat = (df.groupby("category")["sell_through_rate"].mean()
                     .reset_index().sort_values("sell_through_rate", ascending=True))
        fig = go.Figure(go.Bar(
            x=str_cat["sell_through_rate"], y=str_cat["category"],
            orientation="h",
            marker_color=[CAT_PAL.get(c, TICK) for c in str_cat["category"]],
            marker_line_width=0,
            text=str_cat["sell_through_rate"].apply(lambda x: f"{x:.2f}%"),
            textposition="outside",
            textfont=dict(size=11, color=TICK, family=FONT),
            hovertemplate="<b>%{y}</b><br>Sell-Through: %{x:.2f}%<extra></extra>",
        ))
        fig.add_vline(
            x=avg_overall, line_dash="dot", line_color=AMBER, line_width=1.5,
            annotation_text=f"Avg {avg_overall:.1f}%",
            annotation_position="top right",
            annotation_font=dict(color=AMBER, size=11),
        )
        fig.update_layout(
            **base_layout(height=310), showlegend=False,
            xaxis=axis_x(ticksuffix="%"),
            yaxis=axis_y(),
        )
        ctitle("Avg Sell-Through Rate by Category", "Dotted line = overall average")
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    with c2:
        stk_cat = (df.groupby("category")["stock_adequate"].mean().reset_index())
        stk_cat["pct"] = stk_cat["stock_adequate"] * 100
        stk_cat = stk_cat.sort_values("pct", ascending=True)
        stk_cat["color"] = stk_cat["pct"].apply(lambda x: RED_SOFT if x < 80 else GREEN)
        fig = go.Figure(go.Bar(
            x=stk_cat["pct"], y=stk_cat["category"],
            orientation="h",
            marker_color=stk_cat["color"],
            marker_line_width=0,
            text=stk_cat["pct"].apply(lambda x: f"{x:.1f}%"),
            textposition="outside",
            textfont=dict(size=11, color=TICK, family=FONT),
            hovertemplate="<b>%{y}</b><br>Stock Adequacy: %{x:.1f}%<extra></extra>",
        ))
        fig.add_vline(
            x=80, line_dash="dot", line_color="#374151", line_width=1.5,
            annotation_text="Target 80%",
            annotation_position="top right",
            annotation_font=dict(color="#374151", size=11),
        )
        fig.update_layout(
            **base_layout(height=310), showlegend=False,
            xaxis=axis_x(ticksuffix="%", range=[0, 115]),
            yaxis=axis_y(),
        )
        ctitle("Stock Adequacy Rate by Category", "Red = below 80% target")
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    rule()

    # Promo vs non-promo + Delivery tier
    c1, c2 = st.columns(2, gap="medium")

    with c1:
        promo_cat = df.groupby(["category", "is_promoted"])["units_sold"].mean().reset_index()
        fig = go.Figure()
        for promo, color in PROMO_PAL.items():
            sub = promo_cat[promo_cat["is_promoted"] == promo]
            fig.add_trace(go.Bar(
                x=sub["category"], y=sub["units_sold"],
                name=promo, marker_color=color, marker_line_width=0,
                hovertemplate=f"<b>%{{x}}</b><br>{promo}: %{{y:.1f}} units<extra></extra>",
            ))
        fig.update_layout(
            **base_layout(height=310), barmode="group",
            yaxis=axis_y(),
            xaxis=axis_x(),
            legend=dict(orientation="h", y=-0.22, font=dict(size=11),
                        bgcolor="rgba(0,0,0,0)", borderwidth=0),
        )
        ctitle("Avg Units Sold — Promo vs Non-Promo")
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    with c2:
        del_tier = (df.groupby("delivery_tier", observed=True)["sell_through_rate"]
                      .mean().reset_index().dropna())
        tier_colors = [GREEN, GREEN_MID, AMBER, RED_SOFT]
        fig = go.Figure(go.Bar(
            x=del_tier["delivery_tier"].astype(str),
            y=del_tier["sell_through_rate"],
            marker_color=tier_colors[:len(del_tier)],
            marker_line_width=0,
            text=del_tier["sell_through_rate"].apply(lambda x: f"{x:.2f}%"),
            textposition="outside",
            textfont=dict(size=11, color=TICK, family=FONT),
            hovertemplate="<b>%{x}</b><br>Sell-Through: %{y:.2f}%<extra></extra>",
        ))
        fig.update_layout(
            **base_layout(height=310),
            yaxis=axis_y(ticksuffix="%"),
            xaxis=axis_x(),
            showlegend=False,
        )
        ctitle("Sell-Through Rate by Delivery Speed")
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    rule()

    # Sell-through per channel + Avg delivery per region
    c1, c2 = st.columns(2, gap="medium")

    with c1:
        str_ch = (df.groupby("channel")["sell_through_rate"].mean()
                    .reset_index().sort_values("sell_through_rate", ascending=True))
        fig = go.Figure(go.Bar(
            x=str_ch["sell_through_rate"], y=str_ch["channel"],
            orientation="h",
            marker_color=[CH_PAL.get(c, TICK) for c in str_ch["channel"]],
            marker_line_width=0,
            text=str_ch["sell_through_rate"].apply(lambda x: f"{x:.2f}%"),
            textposition="outside",
            textfont=dict(size=11, color=TICK, family=FONT),
            hovertemplate="<b>%{y}</b><br>%{x:.2f}%<extra></extra>",
        ))
        fig.update_layout(
            **base_layout(height=260), showlegend=False,
            xaxis=axis_x(ticksuffix="%"),
            yaxis=axis_y(),
        )
        ctitle("Avg Sell-Through Rate by Channel")
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    with c2:
        del_reg = (df.groupby("region")["delivery_days"].mean()
                     .reset_index().sort_values("delivery_days", ascending=True))
        fig = go.Figure(go.Bar(
            x=del_reg["delivery_days"], y=del_reg["region"],
            orientation="h",
            marker_color=[REG_PAL.get(r, TICK) for r in del_reg["region"]],
            marker_line_width=0,
            text=del_reg["delivery_days"].apply(lambda x: f"{x:.1f}d"),
            textposition="outside",
            textfont=dict(size=11, color=TICK, family=FONT),
            hovertemplate="<b>%{y}</b><br>Avg %{x:.1f} days<extra></extra>",
        ))
        fig.update_layout(
            **base_layout(height=260), showlegend=False,
            xaxis=axis_x(),
            yaxis=axis_y(),
        )
        ctitle("Avg Delivery Days by Region")
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="dash-footer">
    <span>FMCG Sales Performance Dashboard · 2022–2024</span>
    <span>Built with Streamlit & Plotly · Portfolio Project</span>
</div>
""", unsafe_allow_html=True)