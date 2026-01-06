"""
=============================================================================
UAE PROMO PULSE SIMULATOR - PRODUCTION DASHBOARD
=============================================================================

A comprehensive promotional analytics platform for UAE retail operations.
Built by the Data Rescue Team.

Features:
    - Data Cleaning & Quality Analysis
    - Sales Analytics with Multi-dimensional Filtering
    - Inventory Health Monitoring
    - Campaign Performance Analysis
    - What-If Promotion Simulator
    - Store Performance Benchmarking
    - Time-based Pattern Analysis

Data Sources (from data_generator.py):
    1. products.csv - Product master data (300 rows)
    2. stores.csv - Store information (18 rows)
    3. sales_raw.csv - Sales transactions (~35,000 rows)
    4. inventory_snapshot.csv - Stock levels (~39,600 rows)
    5. campaign_plan.csv - Promotional campaigns (10 rows)

Author: Data Rescue Team
Version: 2.0 Production
Date: 2024
=============================================================================
"""

# =============================================================================
# IMPORTS
# =============================================================================
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import random
import warnings

# Suppress warnings for cleaner output
warnings.filterwarnings('ignore')

# =============================================================================
# PAGE CONFIGURATION
# =============================================================================
st.set_page_config(
    page_title="UAE Promo Pulse Simulator",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/data-rescue-team',
        'Report a bug': 'https://github.com/data-rescue-team/issues',
        'About': '### UAE Promo Pulse Simulator v2.0\nBuilt by Data Rescue Team'
    }
)

# =============================================================================
# CSS DESIGN SYSTEM - PREMIUM GLASSMORPHISM THEME
# =============================================================================

def load_premium_css():
    """
    Load comprehensive CSS design system with glassmorphism effects.
    
    Design Features:
        - Dark theme with purple/indigo accent colors
        - Glassmorphism cards with blur effects
        - Smooth animations and transitions
        - Responsive design
        - Custom scrollbars
        - Gradient backgrounds
    """
    st.markdown("""
    <style>
    /* ===================================================================
       CSS VARIABLES - Design Tokens
       =================================================================== */
    :root {
        /* Primary Colors */
        --primary-bg: #0a0a0f;
        --secondary-bg: #12121a;
        --card-bg: rgba(255, 255, 255, 0.03);
        --card-border: rgba(255, 255, 255, 0.08);
        --card-hover-border: rgba(99, 102, 241, 0.4);
        
        /* Accent Colors */
        --accent-primary: #6366f1;
        --accent-secondary: #8b5cf6;
        --accent-tertiary: #ec4899;
        --accent-success: #10b981;
        --accent-warning: #f59e0b;
        --accent-danger: #ef4444;
        
        /* Text Colors */
        --text-primary: #ffffff;
        --text-secondary: #a1a1aa;
        --text-muted: #71717a;
        
        /* Gradients */
        --gradient-primary: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #ec4899 100%);
        --gradient-success: linear-gradient(135deg, #10b981 0%, #34d399 100%);
        --gradient-warning: linear-gradient(135deg, #f59e0b 0%, #fbbf24 100%);
        --gradient-danger: linear-gradient(135deg, #ef4444 0%, #f87171 100%);
        
        /* Shadows */
        --shadow-sm: 0 2px 8px rgba(0, 0, 0, 0.3);
        --shadow-md: 0 4px 16px rgba(0, 0, 0, 0.4);
        --shadow-lg: 0 8px 32px rgba(0, 0, 0, 0.5);
        --shadow-glow: 0 0 40px rgba(99, 102, 241, 0.15);
        
        /* Spacing */
        --space-xs: 4px;
        --space-sm: 8px;
        --space-md: 16px;
        --space-lg: 24px;
        --space-xl: 32px;
        
        /* Border Radius */
        --radius-sm: 8px;
        --radius-md: 12px;
        --radius-lg: 16px;
        --radius-xl: 24px;
        
        /* Transitions */
        --transition-fast: 0.15s ease;
        --transition-normal: 0.3s ease;
        --transition-slow: 0.5s ease;
    }
    
    /* ===================================================================
       GLOBAL STYLES
       =================================================================== */
    .stApp {
        background: linear-gradient(180deg, var(--primary-bg) 0%, var(--secondary-bg) 100%);
        color: var(--text-primary);
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    ::-webkit-scrollbar-track {
        background: var(--secondary-bg);
    }
    ::-webkit-scrollbar-thumb {
        background: var(--accent-primary);
        border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: var(--accent-secondary);
    }
    
    /* ===================================================================
       GLASSMORPHISM CARDS
       =================================================================== */
    .glass-card {
        background: var(--card-bg);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid var(--card-border);
        border-radius: var(--radius-lg);
        padding: var(--space-lg);
        transition: all var(--transition-normal);
        box-shadow: var(--shadow-md);
    }
    
    .glass-card:hover {
        border-color: var(--card-hover-border);
        box-shadow: var(--shadow-glow);
        transform: translateY(-2px);
    }
    
    /* ===================================================================
       HERO HEADER
       =================================================================== */
    .hero-header {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.1) 0%, rgba(139, 92, 246, 0.1) 50%, rgba(236, 72, 153, 0.05) 100%);
        border: 1px solid rgba(99, 102, 241, 0.2);
        border-radius: var(--radius-xl);
        padding: var(--space-xl) var(--space-xl);
        margin-bottom: var(--space-xl);
        position: relative;
        overflow: hidden;
    }
    
    .hero-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: var(--gradient-primary);
    }
    
    .hero-title {
        font-size: 2.5rem;
        font-weight: 800;
        background: var(--gradient-primary);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0;
        letter-spacing: -0.02em;
    }
    
    .hero-subtitle {
        color: var(--text-secondary);
        font-size: 1.1rem;
        margin-top: var(--space-sm);
        font-weight: 400;
    }
    
    /* ===================================================================
       KPI CARDS
       =================================================================== */
    .kpi-container {
        display: flex;
        gap: var(--space-md);
        flex-wrap: wrap;
        margin: var(--space-lg) 0;
    }
    
    .kpi-card {
        flex: 1;
        min-width: 180px;
        background: var(--card-bg);
        backdrop-filter: blur(20px);
        border: 1px solid var(--card-border);
        border-radius: var(--radius-md);
        padding: var(--space-lg);
        text-align: center;
        transition: all var(--transition-normal);
    }
    
    .kpi-card:hover {
        border-color: var(--card-hover-border);
        transform: translateY(-3px);
        box-shadow: var(--shadow-glow);
    }
    
    .kpi-icon {
        font-size: 1.8rem;
        margin-bottom: var(--space-sm);
    }
    
    .kpi-value {
        font-size: 1.6rem;
        font-weight: 700;
        margin-bottom: var(--space-xs);
        letter-spacing: -0.02em;
    }
    
    .kpi-label {
        font-size: 0.85rem;
        color: var(--text-muted);
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    /* KPI Color Variants */
    .kpi-primary .kpi-value { color: var(--accent-primary); }
    .kpi-success .kpi-value { color: var(--accent-success); }
    .kpi-warning .kpi-value { color: var(--accent-warning); }
    .kpi-danger .kpi-value { color: var(--accent-danger); }
    .kpi-accent .kpi-value { color: var(--accent-tertiary); }
    .kpi-secondary .kpi-value { color: var(--accent-secondary); }
    
    /* ===================================================================
       SECTION HEADERS
       =================================================================== */
    .section-header {
        display: flex;
        align-items: center;
        gap: var(--space-md);
        margin: var(--space-xl) 0 var(--space-lg) 0;
        padding-bottom: var(--space-md);
        border-bottom: 1px solid var(--card-border);
    }
    
    .section-icon {
        font-size: 2rem;
        background: var(--gradient-primary);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .section-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: var(--text-primary);
        margin: 0;
    }
    
    .section-subtitle {
        font-size: 0.9rem;
        color: var(--text-muted);
        margin: 0;
    }
    
    /* ===================================================================
       CHART CONTAINERS
       =================================================================== */
    .chart-container {
        background: var(--card-bg);
        border: 1px solid var(--card-border);
        border-radius: var(--radius-lg);
        padding: var(--space-lg);
        margin: var(--space-md) 0;
    }
    
    .chart-title {
        font-size: 1rem;
        font-weight: 600;
        color: var(--text-primary);
        margin-bottom: var(--space-md);
        display: flex;
        align-items: center;
        gap: var(--space-sm);
    }
    
    /* ===================================================================
       INSIGHT BOXES
       =================================================================== */
    .insight-box {
        background: var(--card-bg);
        border-left: 4px solid var(--accent-primary);
        border-radius: 0 var(--radius-md) var(--radius-md) 0;
        padding: var(--space-lg);
        margin: var(--space-md) 0;
    }
    
    .insight-box.success { border-left-color: var(--accent-success); }
    .insight-box.warning { border-left-color: var(--accent-warning); }
    .insight-box.danger { border-left-color: var(--accent-danger); }
    .insight-box.accent { border-left-color: var(--accent-tertiary); }
    
    .insight-title {
        font-weight: 600;
        color: var(--text-primary);
        margin-bottom: var(--space-sm);
        display: flex;
        align-items: center;
        gap: var(--space-sm);
    }
    
    .insight-text {
        color: var(--text-secondary);
        font-size: 0.95rem;
        line-height: 1.6;
    }
    
    /* ===================================================================
       STATUS CARDS
       =================================================================== */
    .status-card {
        background: var(--card-bg);
        border: 1px solid var(--card-border);
        border-radius: var(--radius-md);
        padding: var(--space-md);
        text-align: center;
    }
    
    .status-label {
        font-size: 0.8rem;
        color: var(--text-muted);
        margin-bottom: var(--space-xs);
    }
    
    .status-value {
        font-size: 1.3rem;
        font-weight: 700;
    }
    
    .status-value.success { color: var(--accent-success); }
    .status-value.warning { color: var(--accent-warning); }
    .status-value.danger { color: var(--accent-danger); }
    .status-value.primary { color: var(--accent-primary); }
    
    /* ===================================================================
       RECOMMENDATION CARDS
       =================================================================== */
    .recommendation-card {
        background: rgba(99, 102, 241, 0.05);
        border: 1px solid rgba(99, 102, 241, 0.2);
        border-radius: var(--radius-md);
        padding: var(--space-md);
        margin: var(--space-sm) 0;
        display: flex;
        align-items: flex-start;
        gap: var(--space-md);
    }
    
    .recommendation-icon {
        font-size: 1.3rem;
        flex-shrink: 0;
    }
    
    .recommendation-text {
        color: var(--text-secondary);
        font-size: 0.9rem;
        line-height: 1.5;
    }
    
    /* ===================================================================
       EMPTY STATE
       =================================================================== */
    .empty-state {
        text-align: center;
        padding: var(--space-xl) var(--space-lg);
        color: var(--text-muted);
    }
    
    .empty-state-icon {
        font-size: 3rem;
        margin-bottom: var(--space-md);
        opacity: 0.5;
    }
    
    .empty-state-title {
        font-size: 1.2rem;
        font-weight: 600;
        color: var(--text-secondary);
        margin-bottom: var(--space-sm);
    }
    
    .empty-state-text {
        font-size: 0.9rem;
        color: var(--text-muted);
    }
    
    /* ===================================================================
       DIVIDERS
       =================================================================== */
    .divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, var(--card-border), transparent);
        margin: var(--space-xl) 0;
    }
    
    .divider-subtle {
        height: 1px;
        background: var(--card-border);
        margin: var(--space-lg) 0;
    }
    
    /* ===================================================================
       DATA QUALITY BADGES
       =================================================================== */
    .quality-badge {
        display: inline-flex;
        align-items: center;
        gap: var(--space-xs);
        padding: var(--space-xs) var(--space-sm);
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
    }
    
    .quality-badge.good {
        background: rgba(16, 185, 129, 0.2);
        color: var(--accent-success);
    }
    
    .quality-badge.warning {
        background: rgba(245, 158, 11, 0.2);
        color: var(--accent-warning);
    }
    
    .quality-badge.bad {
        background: rgba(239, 68, 68, 0.2);
        color: var(--accent-danger);
    }
    
    /* ===================================================================
       FOOTER
       =================================================================== */
    .footer {
        text-align: center;
        padding: var(--space-xl) 0;
        margin-top: var(--space-xl);
        border-top: 1px solid var(--card-border);
        color: var(--text-muted);
        font-size: 0.85rem;
    }
    
    .footer a {
        color: var(--accent-primary);
        text-decoration: none;
    }
    
    .footer a:hover {
        text-decoration: underline;
    }
    
    /* ===================================================================
       STREAMLIT COMPONENT OVERRIDES
       =================================================================== */
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: var(--space-sm);
        background: transparent;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: var(--card-bg);
        border: 1px solid var(--card-border);
        border-radius: var(--radius-md);
        padding: var(--space-sm) var(--space-lg);
        color: var(--text-secondary);
        font-weight: 500;
    }
    
    .stTabs [aria-selected="true"] {
        background: var(--accent-primary) !important;
        border-color: var(--accent-primary) !important;
        color: white !important;
    }
    
    /* Selectbox */
    .stSelectbox > div > div {
        background: var(--card-bg);
        border: 1px solid var(--card-border);
        border-radius: var(--radius-sm);
    }
    
    /* Multiselect */
    .stMultiSelect > div > div {
        background: var(--card-bg);
        border: 1px solid var(--card-border);
        border-radius: var(--radius-sm);
    }
    
    /* Slider */
    .stSlider > div > div > div {
        background: var(--accent-primary);
    }
    
    /* Buttons */
    .stButton > button {
        background: var(--gradient-primary);
        border: none;
        border-radius: var(--radius-md);
        padding: var(--space-sm) var(--space-lg);
        font-weight: 600;
        transition: all var(--transition-normal);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 20px rgba(99, 102, 241, 0.4);
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: var(--card-bg);
        border: 1px solid var(--card-border);
        border-radius: var(--radius-md);
    }
    
    /* Dataframe */
    .stDataFrame {
        border: 1px solid var(--card-border);
        border-radius: var(--radius-md);
    }
    
    /* Metrics */
    [data-testid="metric-container"] {
        background: var(--card-bg);
        border: 1px solid var(--card-border);
        border-radius: var(--radius-md);
        padding: var(--space-md);
    }
    
    /* Checkbox */
    .stCheckbox > label {
        color: var(--text-secondary);
    }
    
    /* File uploader */
    .stFileUploader > div {
        background: var(--card-bg);
        border: 1px dashed var(--card-border);
        border-radius: var(--radius-md);
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0d0d14 0%, #12121a 100%);
        border-right: 1px solid var(--card-border);
    }
    
    [data-testid="stSidebar"] .stMarkdown {
        color: var(--text-secondary);
    }
    
    /* ===================================================================
       RESPONSIVE DESIGN
       =================================================================== */
    @media (max-width: 768px) {
        .hero-title {
            font-size: 1.8rem;
        }
        
        .kpi-card {
            min-width: 140px;
        }
        
        .kpi-value {
            font-size: 1.3rem;
        }
    }
    
    /* ===================================================================
       ANIMATIONS
       =================================================================== */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.7; }
    }
    
    .animate-fade-in {
        animation: fadeIn 0.5s ease forwards;
    }
    
    .animate-pulse {
        animation: pulse 2s ease-in-out infinite;
    }
    </style>
    """, unsafe_allow_html=True)


# =============================================================================
# CHART THEME CONFIGURATION
# =============================================================================

def get_chart_colors():
    """
    Return consistent color palette for all charts.
    
    Returns:
        list: List of hex color codes
    """
    return [
        '#6366f1',  # Primary indigo
        '#8b5cf6',  # Purple
        '#ec4899',  # Pink
        '#10b981',  # Emerald
        '#f59e0b',  # Amber
        '#06b6d4',  # Cyan
        '#f97316',  # Orange
        '#84cc16',  # Lime
        '#14b8a6',  # Teal
        '#a855f7',  # Violet
    ]


def apply_chart_style(fig, height=400, show_legend=True):
    """
    Apply consistent styling to Plotly charts.
    
    Args:
        fig: Plotly figure object
        height: Chart height in pixels
        show_legend: Whether to show legend
    
    Returns:
        fig: Styled Plotly figure
    """
    fig.update_layout(
        height=height,
        showlegend=show_legend,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(size=11, color='#a1a1aa'),
            bgcolor='rgba(0,0,0,0)'
        ),
        margin=dict(l=20, r=20, t=40, b=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#a1a1aa', size=12),
        xaxis=dict(
            gridcolor='rgba(255,255,255,0.05)',
            zerolinecolor='rgba(255,255,255,0.1)',
            tickfont=dict(color='#71717a')
        ),
        yaxis=dict(
            gridcolor='rgba(255,255,255,0.05)',
            zerolinecolor='rgba(255,255,255,0.1)',
            tickfont=dict(color='#71717a')
        ),
        hoverlabel=dict(
            bgcolor='#1a1a2e',
            bordercolor='#6366f1',
            font=dict(color='white', size=12)
        )
    )
    return fig
# =============================================================================
# UI COMPONENT HELPER FUNCTIONS
# =============================================================================

def render_hero_header():
    """
    Render the main hero header with title and timestamp.
    
    Displays:
        - Application title with gradient styling
        - Subtitle with current date/time
        - Decorative gradient border
    """
    current_time = datetime.now().strftime("%B %d, %Y • %I:%M %p")
    
    st.markdown(f'''
    <div class="hero-header">
        <h1 class="hero-title">🚀 UAE Promo Pulse Simulator</h1>
        <p class="hero-subtitle">Advanced Promotional Analytics & Simulation Platform • {current_time}</p>
    </div>
    ''', unsafe_allow_html=True)


def render_section_header(icon, title, subtitle=""):
    """
    Render a styled section header with icon.
    
    Args:
        icon: Emoji or icon string
        title: Section title text
        subtitle: Optional subtitle/description
    """
    subtitle_html = f'<p class="section-subtitle">{subtitle}</p>' if subtitle else ''
    
    st.markdown(f'''
    <div class="section-header">
        <span class="section-icon">{icon}</span>
        <div>
            <h2 class="section-title">{title}</h2>
            {subtitle_html}
        </div>
    </div>
    ''', unsafe_allow_html=True)


def render_kpi_row(kpis):
    """
    Render a row of KPI cards with consistent styling.
    
    Args:
        kpis: List of dictionaries with keys:
            - icon: Emoji icon
            - value: Display value (formatted string)
            - label: KPI label
            - type: Color type ('primary', 'success', 'warning', 'danger', 'accent', 'secondary')
    
    Example:
        kpis = [
            {"icon": "💰", "value": "AED 1.2M", "label": "Revenue", "type": "success"},
            {"icon": "📦", "value": "5,234", "label": "Orders", "type": "primary"}
        ]
    """
    cols = st.columns(len(kpis))
    
    for col, kpi in zip(cols, kpis):
        with col:
            kpi_type = kpi.get('type', 'primary')
            st.markdown(f'''
            <div class="kpi-card kpi-{kpi_type}">
                <div class="kpi-icon">{kpi["icon"]}</div>
                <div class="kpi-value">{kpi["value"]}</div>
                <div class="kpi-label">{kpi["label"]}</div>
            </div>
            ''', unsafe_allow_html=True)


def render_kpi_row_compact(kpis):
    """
    Render a compact row of KPI cards for smaller sections.
    
    Args:
        kpis: List of KPI dictionaries (same structure as render_kpi_row)
    """
    cols = st.columns(len(kpis))
    
    for col, kpi in zip(cols, kpis):
        with col:
            kpi_type = kpi.get('type', 'primary')
            color_map = {
                'primary': '#6366f1',
                'success': '#10b981',
                'warning': '#f59e0b',
                'danger': '#ef4444',
                'accent': '#ec4899',
                'secondary': '#8b5cf6'
            }
            color = color_map.get(kpi_type, '#6366f1')
            
            st.markdown(f'''
            <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); 
                        border-radius: 10px; padding: 12px; text-align: center;">
                <div style="font-size: 1.2rem; margin-bottom: 4px;">{kpi["icon"]}</div>
                <div style="font-size: 1.2rem; font-weight: 700; color: {color};">{kpi["value"]}</div>
                <div style="font-size: 0.75rem; color: #71717a; text-transform: uppercase;">{kpi["label"]}</div>
            </div>
            ''', unsafe_allow_html=True)


def render_chart_title(title, icon="📊"):
    """
    Render a styled chart title.
    
    Args:
        title: Chart title text
        icon: Emoji icon (default: 📊)
    """
    st.markdown(f'''
    <div class="chart-title">
        <span>{icon}</span>
        <span>{title}</span>
    </div>
    ''', unsafe_allow_html=True)


def render_insight_box(icon, title, text, box_type="primary"):
    """
    Render an insight/information box with colored left border.
    
    Args:
        icon: Emoji icon
        title: Box title
        text: Description/insight text
        box_type: Color type ('primary', 'success', 'warning', 'danger', 'accent')
    """
    st.markdown(f'''
    <div class="insight-box {box_type}">
        <div class="insight-title">
            <span>{icon}</span>
            <span>{title}</span>
        </div>
        <div class="insight-text">{text}</div>
    </div>
    ''', unsafe_allow_html=True)


def render_recommendation_card(icon, text):
    """
    Render a recommendation card with icon.
    
    Args:
        icon: Emoji icon
        text: Recommendation text
    """
    st.markdown(f'''
    <div class="recommendation-card">
        <span class="recommendation-icon">{icon}</span>
        <span class="recommendation-text">{text}</span>
    </div>
    ''', unsafe_allow_html=True)


def render_status_card(label, value, status_type="primary"):
    """
    Render a compact status card.
    
    Args:
        label: Card label
        value: Display value
        status_type: Color type ('success', 'warning', 'danger', 'primary')
    """
    st.markdown(f'''
    <div class="status-card">
        <div class="status-label">{label}</div>
        <div class="status-value {status_type}">{value}</div>
    </div>
    ''', unsafe_allow_html=True)


def render_metric_card(icon, value, label, delta=None, delta_type="neutral"):
    """
    Render a metric card with optional delta indicator.
    
    Args:
        icon: Emoji icon
        value: Main metric value
        label: Metric label
        delta: Optional delta value (e.g., "+5.2%")
        delta_type: Delta color ('positive', 'negative', 'neutral')
    """
    delta_html = ""
    if delta:
        delta_color = {
            'positive': '#10b981',
            'negative': '#ef4444',
            'neutral': '#71717a'
        }.get(delta_type, '#71717a')
        
        delta_icon = "↑" if delta_type == "positive" else ("↓" if delta_type == "negative" else "→")
        delta_html = f'<div style="font-size: 0.85rem; color: {delta_color}; margin-top: 4px;">{delta_icon} {delta}</div>'
    
    st.markdown(f'''
    <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); 
                border-radius: 12px; padding: 16px; text-align: center;">
        <div style="font-size: 1.5rem; margin-bottom: 8px;">{icon}</div>
        <div style="font-size: 1.4rem; font-weight: 700; color: #6366f1;">{value}</div>
        <div style="font-size: 0.8rem; color: #71717a; text-transform: uppercase; margin-top: 4px;">{label}</div>
        {delta_html}
    </div>
    ''', unsafe_allow_html=True)


def render_empty_state(icon, title, text):
    """
    Render an empty state placeholder.
    
    Args:
        icon: Large emoji icon
        title: Empty state title
        text: Description text
    """
    st.markdown(f'''
    <div class="empty-state">
        <div class="empty-state-icon">{icon}</div>
        <div class="empty-state-title">{title}</div>
        <div class="empty-state-text">{text}</div>
    </div>
    ''', unsafe_allow_html=True)


def render_divider():
    """Render a gradient divider line."""
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)


def render_divider_subtle():
    """Render a subtle divider line."""
    st.markdown('<div class="divider-subtle"></div>', unsafe_allow_html=True)


def render_quality_badge(text, badge_type="good"):
    """
    Render a quality/status badge.
    
    Args:
        text: Badge text
        badge_type: Badge type ('good', 'warning', 'bad')
    
    Returns:
        str: HTML string for the badge
    """
    return f'<span class="quality-badge {badge_type}">{text}</span>'


def render_footer():
    """Render the application footer."""
    st.markdown('''
    <div class="footer">
        <p>🚀 <strong>UAE Promo Pulse Simulator</strong> v2.0 | Built by <strong>Data Rescue Team</strong></p>
        <p>Powered by Streamlit • Plotly • Pandas</p>
    </div>
    ''', unsafe_allow_html=True)


def render_data_quality_summary(df, df_name):
    """
    Render a compact data quality summary for a dataframe.
    
    Args:
        df: Pandas DataFrame
        df_name: Name of the dataset
    
    Returns:
        dict: Quality metrics dictionary
    """
    total_rows = len(df)
    total_cols = len(df.columns)
    total_cells = total_rows * total_cols
    missing_cells = df.isnull().sum().sum()
    duplicate_rows = df.duplicated().sum()
    
    completeness = ((total_cells - missing_cells) / total_cells * 100) if total_cells > 0 else 0
    uniqueness = ((total_rows - duplicate_rows) / total_rows * 100) if total_rows > 0 else 0
    
    # Calculate overall quality score
    quality_score = (completeness * 0.6 + uniqueness * 0.4)
    
    # Determine quality badge
    if quality_score >= 95:
        badge_type = "good"
        badge_text = "Excellent"
    elif quality_score >= 80:
        badge_type = "warning"
        badge_text = "Good"
    else:
        badge_type = "bad"
        badge_text = "Needs Attention"
    
    quality_metrics = {
        'total_rows': total_rows,
        'total_cols': total_cols,
        'missing_cells': missing_cells,
        'duplicate_rows': duplicate_rows,
        'completeness': completeness,
        'uniqueness': uniqueness,
        'quality_score': quality_score,
        'badge_type': badge_type,
        'badge_text': badge_text
    }
    
    return quality_metrics


# =============================================================================
# FORMATTING HELPER FUNCTIONS
# =============================================================================

def format_currency(value, currency="AED"):
    """
    Format a numeric value as currency.
    
    Args:
        value: Numeric value
        currency: Currency code (default: AED)
    
    Returns:
        str: Formatted currency string
    """
    if pd.isna(value) or value is None:
        return f"{currency} 0.00"
    
    if abs(value) >= 1_000_000:
        return f"{currency} {value/1_000_000:.2f}M"
    elif abs(value) >= 1_000:
        return f"{currency} {value/1_000:.1f}K"
    else:
        return f"{currency} {value:,.2f}"


def format_number(value, decimals=0):
    """
    Format a numeric value with thousand separators.
    
    Args:
        value: Numeric value
        decimals: Number of decimal places
    
    Returns:
        str: Formatted number string
    """
    if pd.isna(value) or value is None:
        return "0"
    
    if abs(value) >= 1_000_000:
        return f"{value/1_000_000:.{decimals}f}M"
    elif abs(value) >= 1_000:
        return f"{value/1_000:.{decimals}f}K"
    else:
        if decimals > 0:
            return f"{value:,.{decimals}f}"
        return f"{value:,.0f}"


def format_percentage(value, decimals=1):
    """
    Format a numeric value as percentage.
    
    Args:
        value: Numeric value (0-100 or 0-1)
        decimals: Number of decimal places
    
    Returns:
        str: Formatted percentage string
    """
    if pd.isna(value) or value is None:
        return "0%"
    
    # If value is between 0 and 1, multiply by 100
    if 0 <= value <= 1:
        value = value * 100
    
    return f"{value:.{decimals}f}%"


def format_delta(current, previous):
    """
    Calculate and format the delta between two values.
    
    Args:
        current: Current period value
        previous: Previous period value
    
    Returns:
        tuple: (delta_string, delta_type)
    """
    if pd.isna(previous) or previous == 0:
        return ("N/A", "neutral")
    
    delta = ((current - previous) / previous) * 100
    
    if delta > 0:
        return (f"+{delta:.1f}%", "positive")
    elif delta < 0:
        return (f"{delta:.1f}%", "negative")
    else:
        return ("0%", "neutral")


# =============================================================================
# DATA VALIDATION SCHEMAS (Matching data_generator.py)
# =============================================================================

EXPECTED_COLUMNS = {
    'products': [
        'product_id',      # Unique product identifier (PROD_00001)
        'category',        # Product category (Electronics, Fashion, etc.)
        'brand',           # Brand name
        'base_price_aed',  # Base retail price in AED
        'unit_cost_aed',   # Unit cost in AED (may have missing values)
        'tax_rate',        # VAT rate (0.05 for UAE)
        'launch_flag'      # New or Regular
    ],
    'stores': [
        'store_id',         # Unique store identifier (STORE_001)
        'city',             # City name (may have inconsistent values)
        'channel',          # Sales channel (App, Web, Marketplace)
        'fulfillment_type'  # Fulfillment type (Own, 3PL)
    ],
    'sales': [
        'order_id',          # Unique order identifier (ORD_0000001)
        'order_time',        # Order timestamp (may have corrupted values)
        'product_id',        # Foreign key to products
        'store_id',          # Foreign key to stores
        'qty',               # Quantity ordered (may have outliers)
        'selling_price_aed', # Actual selling price (may have outliers)
        'discount_pct',      # Discount percentage (may have missing values)
        'payment_status',    # Paid, Failed, or Refunded
        'return_flag'        # 1 if returned, 0 otherwise
    ],
    'inventory': [
        'snapshot_date',   # Date of inventory snapshot
        'product_id',      # Foreign key to products
        'store_id',        # Foreign key to stores
        'stock_on_hand',   # Current stock level (may have negative/extreme values)
        'reorder_point',   # Minimum stock level before reorder
        'lead_time_days'   # Supplier lead time in days
    ],
    'campaigns': [
        'campaign_id',      # Unique campaign identifier (CAMP_001)
        'start_date',       # Campaign start date
        'end_date',         # Campaign end date
        'city',             # Target city or 'All'
        'channel',          # Target channel or 'All'
        'category',         # Target category or 'All'
        'discount_pct',     # Discount percentage
        'promo_budget_aed'  # Campaign budget in AED
    ]
}

# City name standardization mapping (for dirty data cleaning)
CITY_MAPPING = {
    # Dubai variations
    'dubai': 'Dubai',
    'DUBAI': 'Dubai',
    'Dubayy': 'Dubai',
    'DXB': 'Dubai',
    'Dубай': 'Dubai',
    
    # Abu Dhabi variations
    'abu dhabi': 'Abu Dhabi',
    'ABU DHABI': 'Abu Dhabi',
    'AbuDhabi': 'Abu Dhabi',
    'AD': 'Abu Dhabi',
    'Abudhabi': 'Abu Dhabi',
    
    # Sharjah variations
    'sharjah': 'Sharjah',
    'SHARJAH': 'Sharjah',
    'Shj': 'Sharjah',
    'Sharijah': 'Sharjah',
    'Al Sharjah': 'Sharjah'
}

# Standard city names
STANDARD_CITIES = ['Dubai', 'Abu Dhabi', 'Sharjah']

# Sales channels
CHANNELS = ['App', 'Web', 'Marketplace']

# Product categories
CATEGORIES = ['Electronics', 'Fashion', 'Grocery', 'Home & Garden', 'Beauty', 'Sports']

# Payment statuses
PAYMENT_STATUSES = ['Paid', 'Failed', 'Refunded']

# Fulfillment types
FULFILLMENT_TYPES = ['Own', '3PL']


def validate_dataframe(df, schema_name):
    """
    Validate a dataframe against expected schema.
    
    Args:
        df: Pandas DataFrame to validate
        schema_name: Name of schema ('products', 'stores', 'sales', 'inventory', 'campaigns')
    
    Returns:
        tuple: (is_valid, missing_columns, extra_columns)
    """
    if schema_name not in EXPECTED_COLUMNS:
        return False, [], []
    
    expected = set(EXPECTED_COLUMNS[schema_name])
    actual = set(df.columns.str.lower().str.strip())
    
    missing = expected - actual
    extra = actual - expected
    
    is_valid = len(missing) == 0
    
    return is_valid, list(missing), list(extra)


def get_dirty_data_summary(df, df_type):
    """
    Get summary of dirty data issues in a dataframe.
    
    Args:
        df: Pandas DataFrame
        df_type: Type of data ('products', 'stores', 'sales', 'inventory', 'campaigns')
    
    Returns:
        dict: Summary of dirty data issues
    """
    issues = {}
    
    if df_type == 'products':
        # Check for missing unit_cost_aed
        if 'unit_cost_aed' in df.columns:
            missing_cost = df['unit_cost_aed'].isna().sum()
            issues['missing_unit_cost'] = {
                'count': missing_cost,
                'percentage': (missing_cost / len(df)) * 100
            }
    
    elif df_type == 'stores':
        # Check for inconsistent city values
        if 'city' in df.columns:
            inconsistent = df[~df['city'].isin(STANDARD_CITIES)]
            issues['inconsistent_cities'] = {
                'count': len(inconsistent),
                'percentage': (len(inconsistent) / len(df)) * 100,
                'values': inconsistent['city'].unique().tolist()
            }
    
    elif df_type == 'sales':
        # Check for missing discount_pct
        if 'discount_pct' in df.columns:
            missing_discount = df['discount_pct'].isna().sum()
            issues['missing_discount'] = {
                'count': missing_discount,
                'percentage': (missing_discount / len(df)) * 100
            }
        
        # Check for duplicate order_ids
        if 'order_id' in df.columns:
            duplicates = df['order_id'].duplicated().sum()
            issues['duplicate_orders'] = {
                'count': duplicates,
                'percentage': (duplicates / len(df)) * 100
            }
        
        # Check for corrupted timestamps
        if 'order_time' in df.columns:
            df_temp = df.copy()
            df_temp['parsed_time'] = pd.to_datetime(df_temp['order_time'], errors='coerce')
            corrupted = df_temp['parsed_time'].isna().sum()
            issues['corrupted_timestamps'] = {
                'count': corrupted,
                'percentage': (corrupted / len(df)) * 100
            }
        
        # Check for quantity outliers (qty > 20)
        if 'qty' in df.columns:
            outliers = (df['qty'] > 20).sum()
            issues['qty_outliers'] = {
                'count': outliers,
                'percentage': (outliers / len(df)) * 100
            }
        
        # Check for price outliers
        if 'selling_price_aed' in df.columns:
            q99 = df['selling_price_aed'].quantile(0.99)
            price_outliers = (df['selling_price_aed'] > q99 * 2).sum()
            issues['price_outliers'] = {
                'count': price_outliers,
                'percentage': (price_outliers / len(df)) * 100
            }
    
    elif df_type == 'inventory':
        # Check for negative stock
        if 'stock_on_hand' in df.columns:
            negative = (df['stock_on_hand'] < 0).sum()
            issues['negative_stock'] = {
                'count': negative,
                'percentage': (negative / len(df)) * 100
            }
            
            # Check for extreme stock values
            extreme = (df['stock_on_hand'] > 9000).sum()
            issues['extreme_stock'] = {
                'count': extreme,
                'percentage': (extreme / len(df)) * 100
            }
    
    return issues

# =============================================================================
# SAMPLE DATA GENERATOR
# =============================================================================
# This generator creates synthetic data matching the exact structure from
# data_generator.py, including all dirty data issues for demonstration.
# =============================================================================

@st.cache_data(ttl=3600, show_spinner=False)
def generate_sample_data():
    """
    Generate sample data matching the data_generator.py structure exactly.
    
    This function creates 5 interconnected datasets with intentionally
    injected dirty data issues for demonstration purposes:
    
    Dirty Data Issues Injected:
        1. Inconsistent city values in stores (40%)
        2. Missing unit_cost_aed in products (1.5%)
        3. Missing discount_pct in sales (3%)
        4. Duplicate order_ids in sales (0.75%)
        5. Corrupted timestamps in sales (1.5%)
        6. Qty/Price outliers in sales (0.4%)
        7. Negative stock in inventory (2%)
        8. Extreme stock values (9999) in inventory (1%)
    
    Returns:
        tuple: (products_df, stores_df, sales_df, inventory_df, campaigns_df)
    """
    # Set seeds for reproducibility
    np.random.seed(42)
    random.seed(42)
    
    # =========================================================================
    # CONFIGURATION (matching data_generator.py)
    # =========================================================================
    NUM_PRODUCTS = 300
    NUM_STORES = 18
    NUM_SALES = 35000
    NUM_CAMPAIGNS = 10
    
    TODAY = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    HISTORICAL_START = TODAY - timedelta(days=120)
    
    # Dirty data injection percentages
    MISSING_UNIT_COST_PCT = 0.015      # 1.5%
    MISSING_DISCOUNT_PCT = 0.03        # 3%
    DUPLICATE_ORDER_PCT = 0.0075       # 0.75%
    CORRUPTED_TIMESTAMP_PCT = 0.015    # 1.5%
    OUTLIER_PCT = 0.004                # 0.4%
    NEGATIVE_STOCK_PCT = 0.02          # 2%
    EXTREME_STOCK_PCT = 0.01           # 1%
    
    # Business configuration
    CITIES = ['Dubai', 'Abu Dhabi', 'Sharjah']
    CHANNELS = ['App', 'Web', 'Marketplace']
    FULFILLMENT_TYPES = ['Own', '3PL']
    PAYMENT_STATUSES = ['Paid', 'Failed', 'Refunded']
    
    # Product configuration
    CATEGORIES = ['Electronics', 'Fashion', 'Grocery', 'Home & Garden', 'Beauty', 'Sports']
    
    BRANDS = {
        'Electronics': ['Samsung', 'Apple', 'Sony', 'LG', 'Huawei', 'Lenovo', 'Dell', 'HP'],
        'Fashion': ['Zara', 'H&M', 'Nike', 'Adidas', 'Puma', 'Levis', 'Gap', 'Uniqlo'],
        'Grocery': ['Almarai', 'Nestle', 'Kelloggs', 'Heinz', 'Lipton', 'Masafi', 'Al Ain'],
        'Home & Garden': ['IKEA', 'HomeBox', 'PanEmirates', 'Danube', 'ACE', 'Pottery Barn'],
        'Beauty': ['Loreal', 'Maybelline', 'MAC', 'Nivea', 'Dove', 'Neutrogena', 'Olay'],
        'Sports': ['Nike', 'Adidas', 'Puma', 'UnderArmour', 'Reebok', 'Decathlon', 'Skechers']
    }
    
    PRICE_RANGES = {
        'Electronics': (100, 5000),
        'Fashion': (50, 1500),
        'Grocery': (5, 200),
        'Home & Garden': (30, 3000),
        'Beauty': (20, 800),
        'Sports': (40, 2000)
    }
    
    # Inconsistent city values for dirty data
    INCONSISTENT_CITIES = {
        'Dubai': ['Dubai', 'DUBAI', 'dubai', 'Dubayy', 'DXB'],
        'Abu Dhabi': ['Abu Dhabi', 'ABU DHABI', 'abu dhabi', 'AbuDhabi', 'AD'],
        'Sharjah': ['Sharjah', 'SHARJAH', 'sharjah', 'Shj', 'Sharijah']
    }
    
    # Corrupted timestamp values
    CORRUPTED_TIMESTAMPS = [
        'not_a_time', 'NULL', 'N/A', '00/00/0000',
        '2024-13-45 99:99:99', 'invalid_date', '', 'NaT'
    ]
    
    # =========================================================================
    # TABLE 1: PRODUCTS (300 rows)
    # =========================================================================
    products = []
    
    for i in range(NUM_PRODUCTS):
        category = random.choice(CATEGORIES)
        brand = random.choice(BRANDS[category])
        min_price, max_price = PRICE_RANGES[category]
        base_price = round(random.uniform(min_price, max_price), 2)
        
        # Unit cost is 40-70% of base price
        cost_margin = random.uniform(0.40, 0.70)
        unit_cost = round(base_price * cost_margin, 2)
        
        products.append({
            'product_id': f'PROD_{str(i+1).zfill(5)}',
            'category': category,
            'brand': brand,
            'base_price_aed': base_price,
            'unit_cost_aed': unit_cost,
            'tax_rate': 0.05,  # UAE VAT
            'launch_flag': 'New' if random.random() < 0.15 else 'Regular'
        })
    
    products_df = pd.DataFrame(products)
    
    # DIRTY DATA: Missing unit_cost_aed (1.5%)
    num_missing_cost = int(NUM_PRODUCTS * MISSING_UNIT_COST_PCT)
    missing_cost_indices = random.sample(range(NUM_PRODUCTS), num_missing_cost)
    products_df.loc[missing_cost_indices, 'unit_cost_aed'] = np.nan
    
    # =========================================================================
    # TABLE 2: STORES (18 rows = 3 cities × 3 channels × 2 fulfillment)
    # =========================================================================
    stores = []
    store_counter = 1
    
    for city in CITIES:
        for channel in CHANNELS:
            for fulfillment in FULFILLMENT_TYPES:
                # DIRTY DATA: Inconsistent city values (40%)
                if random.random() < 0.4:
                    city_value = random.choice(INCONSISTENT_CITIES[city])
                else:
                    city_value = city
                
                stores.append({
                    'store_id': f'STORE_{str(store_counter).zfill(3)}',
                    'city': city_value,
                    'channel': channel,
                    'fulfillment_type': fulfillment
                })
                store_counter += 1
    
    stores_df = pd.DataFrame(stores)
    
    # =========================================================================
    # TABLE 3: SALES_RAW (~35,000 rows)
    # =========================================================================
    product_ids = products_df['product_id'].tolist()
    store_ids = stores_df['store_id'].tolist()
    product_prices = products_df.set_index('product_id')['base_price_aed'].to_dict()
    
    sales = []
    
    for i in range(NUM_SALES):
        # Generate random order timestamp within 120 days historical period
        days_ago = random.randint(0, 120)
        hours = random.randint(0, 23)
        minutes = random.randint(0, 59)
        seconds = random.randint(0, 59)
        order_time = HISTORICAL_START + timedelta(
            days=days_ago, hours=hours, minutes=minutes, seconds=seconds
        )
        order_time_str = order_time.strftime('%Y-%m-%d %H:%M:%S')
        
        # Select random product and store
        product_id = random.choice(product_ids)
        store_id = random.choice(store_ids)
        
        # Generate quantity (most orders are 1-3 items)
        qty = np.random.choice(
            [1, 1, 1, 2, 2, 3, 4, 5],
            p=[0.4, 0.15, 0.1, 0.15, 0.08, 0.07, 0.03, 0.02]
        )
        
        # Calculate selling price with discount
        base_price = product_prices[product_id]
        discount_pct = random.choice([0, 0, 0, 5, 10, 10, 15, 20, 25, 30])
        selling_price = round(base_price * (1 - discount_pct / 100), 2)
        
        # Payment status distribution: 85% Paid, 8% Failed, 7% Refunded
        payment_status = np.random.choice(
            PAYMENT_STATUSES,
            p=[0.85, 0.08, 0.07]
        )
        
        # Return flag (5% of Paid orders are returned)
        if payment_status == 'Paid':
            return_flag = 1 if random.random() < 0.05 else 0
        else:
            return_flag = 0
        
        sales.append({
            'order_id': f'ORD_{str(i+1).zfill(7)}',
            'order_time': order_time_str,
            'product_id': product_id,
            'store_id': store_id,
            'qty': qty,
            'selling_price_aed': selling_price,
            'discount_pct': discount_pct,
            'payment_status': payment_status,
            'return_flag': return_flag
        })
    
    sales_df = pd.DataFrame(sales)
    
    # DIRTY DATA: Missing discount_pct (3%)
    num_missing_discount = int(NUM_SALES * MISSING_DISCOUNT_PCT)
    missing_discount_indices = random.sample(range(NUM_SALES), num_missing_discount)
    sales_df.loc[missing_discount_indices, 'discount_pct'] = np.nan
    
    # DIRTY DATA: Corrupted timestamps (1.5%)
    num_corrupted_ts = int(NUM_SALES * CORRUPTED_TIMESTAMP_PCT)
    corrupted_ts_indices = random.sample(range(NUM_SALES), num_corrupted_ts)
    for idx in corrupted_ts_indices:
        sales_df.loc[idx, 'order_time'] = random.choice(CORRUPTED_TIMESTAMPS)
    
    # DIRTY DATA: Outliers in qty and selling_price (0.4%)
    num_outliers = int(NUM_SALES * OUTLIER_PCT)
    outlier_indices = random.sample(range(NUM_SALES), num_outliers)
    for idx in outlier_indices:
        outlier_type = random.choice(['qty', 'price', 'both'])
        if outlier_type in ['qty', 'both']:
            sales_df.loc[idx, 'qty'] = random.choice([50, 75, 100, 150, 200])
        if outlier_type in ['price', 'both']:
            sales_df.loc[idx, 'selling_price_aed'] *= random.choice([10, 15, 20])
    
    # DIRTY DATA: Duplicate order_ids (0.75%)
    num_duplicates = int(NUM_SALES * DUPLICATE_ORDER_PCT)
    duplicate_indices = random.sample(range(NUM_SALES), num_duplicates)
    duplicate_rows = sales_df.iloc[duplicate_indices].copy()
    sales_df = pd.concat([sales_df, duplicate_rows], ignore_index=True)
    
    # Shuffle to mix dirty data throughout
    sales_df = sales_df.sample(frac=1, random_state=42).reset_index(drop=True)
    
    # =========================================================================
    # TABLE 4: INVENTORY_SNAPSHOT
    # For performance: 100 sampled products × 18 stores × 22 days
    # =========================================================================
    sampled_products = products_df.sample(n=100, random_state=42)['product_id'].tolist()
    
    # Generate dates: 7 days historical + 14 days future
    inventory_dates = [TODAY - timedelta(days=i) for i in range(7, -1, -1)]
    inventory_dates += [TODAY + timedelta(days=i) for i in range(1, 15)]
    
    inventory = []
    
    for snapshot_date in inventory_dates:
        for product_id in sampled_products:
            for store_id in store_ids:
                # Base stock between 10-500 units
                base_stock = random.randint(10, 500)
                
                # Simulate daily variance
                daily_variance = random.randint(-20, 30)
                stock_on_hand = max(0, base_stock + daily_variance)
                
                inventory.append({
                    'snapshot_date': snapshot_date.strftime('%Y-%m-%d'),
                    'product_id': product_id,
                    'store_id': store_id,
                    'stock_on_hand': stock_on_hand,
                    'reorder_point': random.randint(20, 80),
                    'lead_time_days': random.randint(1, 14)
                })
    
    inventory_df = pd.DataFrame(inventory)
    
    # DIRTY DATA: Negative stock (2%)
    num_negative = int(len(inventory_df) * NEGATIVE_STOCK_PCT)
    negative_indices = random.sample(range(len(inventory_df)), num_negative)
    for idx in negative_indices:
        inventory_df.loc[idx, 'stock_on_hand'] = random.choice([-10, -5, -1, -50, -100])
    
    # DIRTY DATA: Extreme stock values (1%)
    num_extreme = int(len(inventory_df) * EXTREME_STOCK_PCT)
    extreme_indices = random.sample(range(len(inventory_df)), num_extreme)
    for idx in extreme_indices:
        inventory_df.loc[idx, 'stock_on_hand'] = random.choice([9999, 99999, 10000])
    
    # =========================================================================
    # TABLE 5: CAMPAIGN_PLAN (10 rows)
    # =========================================================================
    campaign_templates = [
        {'name': 'Dubai Electronics Blitz', 'city': 'Dubai', 'channel': 'All', 'category': 'Electronics', 'discount': 20, 'budget': 100000},
        {'name': 'Abu Dhabi Fashion Week', 'city': 'Abu Dhabi', 'channel': 'All', 'category': 'Fashion', 'discount': 25, 'budget': 75000},
        {'name': 'Sharjah Grocery Sale', 'city': 'Sharjah', 'channel': 'All', 'category': 'Grocery', 'discount': 15, 'budget': 50000},
        {'name': 'App Exclusive Beauty', 'city': 'All', 'channel': 'App', 'category': 'Beauty', 'discount': 30, 'budget': 60000},
        {'name': 'Marketplace Madness', 'city': 'All', 'channel': 'Marketplace', 'category': 'All', 'discount': 35, 'budget': 150000},
        {'name': 'Web-Only Sports Deal', 'city': 'All', 'channel': 'Web', 'category': 'Sports', 'discount': 20, 'budget': 40000},
        {'name': 'UAE National Day Sale', 'city': 'All', 'channel': 'All', 'category': 'All', 'discount': 25, 'budget': 200000},
        {'name': 'Dubai Home & Garden', 'city': 'Dubai', 'channel': 'Web', 'category': 'Home & Garden', 'discount': 15, 'budget': 80000},
        {'name': 'Flash Electronics', 'city': 'All', 'channel': 'App', 'category': 'Electronics', 'discount': 40, 'budget': 120000},
        {'name': 'Weekend Special', 'city': 'All', 'channel': 'All', 'category': 'All', 'discount': 10, 'budget': 50000},
    ]
    
    campaigns = []
    
    for i, template in enumerate(campaign_templates):
        # Campaigns within simulation window
        start_offset = random.randint(0, 7)
        duration = random.randint(3, 14)
        start_date = TODAY + timedelta(days=start_offset)
        end_date = start_date + timedelta(days=duration)
        
        campaigns.append({
            'campaign_id': f'CAMP_{str(i+1).zfill(3)}',
            'start_date': start_date.strftime('%Y-%m-%d'),
            'end_date': end_date.strftime('%Y-%m-%d'),
            'city': template['city'],
            'channel': template['channel'],
            'category': template['category'],
            'discount_pct': template['discount'],
            'promo_budget_aed': template['budget']
        })
    
    campaigns_df = pd.DataFrame(campaigns)
    
    # =========================================================================
    # POST-PROCESSING: Add derived columns for analysis
    # =========================================================================
    
    # Process sales data
    sales_df['order_time'] = pd.to_datetime(sales_df['order_time'], errors='coerce')
    sales_df['date'] = sales_df['order_time'].dt.date
    sales_df['month'] = sales_df['order_time'].dt.to_period('M').astype(str)
    sales_df['week'] = sales_df['order_time'].dt.isocalendar().week.astype('Int64')
    sales_df['day_of_week'] = sales_df['order_time'].dt.day_name()
    sales_df['hour'] = sales_df['order_time'].dt.hour
    sales_df['year'] = sales_df['order_time'].dt.year
    sales_df['quarter'] = sales_df['order_time'].dt.quarter
    
    # Calculate revenue
    sales_df['revenue'] = sales_df['qty'] * sales_df['selling_price_aed']
    
    # Merge products info to sales
    sales_df = sales_df.merge(
        products_df[['product_id', 'category', 'brand', 'base_price_aed', 'unit_cost_aed']],
        on='product_id',
        how='left'
    )
    
    # Merge stores info to sales
    sales_df = sales_df.merge(
        stores_df[['store_id', 'city', 'channel', 'fulfillment_type']],
        on='store_id',
        how='left'
    )
    
    # Clean city names for analysis (keep original for dirty data demo)
    sales_df['city_clean'] = sales_df['city'].replace(CITY_MAPPING)
    sales_df['city_clean'] = sales_df['city_clean'].fillna(sales_df['city'])
    
    # Process inventory data
    inventory_df['snapshot_date'] = pd.to_datetime(inventory_df['snapshot_date'], errors='coerce')
    
    # Calculate stock status
    inventory_df['stock_status'] = inventory_df.apply(
        lambda x: 'Critical' if x['stock_on_hand'] <= 0
        else 'Low' if x['stock_on_hand'] <= x['reorder_point']
        else 'Healthy',
        axis=1
    )
    
    # Add dirty data flags
    inventory_df['is_negative'] = inventory_df['stock_on_hand'] < 0
    inventory_df['is_extreme'] = inventory_df['stock_on_hand'] > 9000
    
    # Merge products and stores to inventory
    inventory_df = inventory_df.merge(
        products_df[['product_id', 'category', 'brand']],
        on='product_id',
        how='left'
    )
    inventory_df = inventory_df.merge(
        stores_df[['store_id', 'city', 'channel', 'fulfillment_type']],
        on='store_id',
        how='left'
    )
    
    # Clean city names for inventory
    inventory_df['city_clean'] = inventory_df['city'].replace(CITY_MAPPING)
    inventory_df['city_clean'] = inventory_df['city_clean'].fillna(inventory_df['city'])
    
    # Process campaigns data
    campaigns_df['start_date'] = pd.to_datetime(campaigns_df['start_date'], errors='coerce')
    campaigns_df['end_date'] = pd.to_datetime(campaigns_df['end_date'], errors='coerce')
    campaigns_df['duration_days'] = (campaigns_df['end_date'] - campaigns_df['start_date']).dt.days
    campaigns_df['is_active'] = (
        (campaigns_df['start_date'] <= pd.Timestamp.now()) &
        (campaigns_df['end_date'] >= pd.Timestamp.now())
    )
    
    # Process stores data
    stores_df['city_clean'] = stores_df['city'].replace(CITY_MAPPING)
    stores_df['city_clean'] = stores_df['city_clean'].fillna(stores_df['city'])
    
    return products_df, stores_df, sales_df, inventory_df, campaigns_df


# =============================================================================
# DATA LOADING & PROCESSING FUNCTIONS
# =============================================================================

@st.cache_data(ttl=3600, show_spinner=False)
def load_and_process_data(products_file, stores_file, sales_file, inventory_file, campaigns_file):
    """
    Load and process all 5 uploaded CSV files with validation and enrichment.
    
    This function:
        1. Loads all CSV files
        2. Normalizes column names
        3. Validates against expected schema
        4. Adds derived columns for analysis
        5. Merges related data
        6. Cleans dirty data (standardizes cities)
    
    Args:
        products_file: Uploaded products.csv file
        stores_file: Uploaded stores.csv file
        sales_file: Uploaded sales_raw.csv file
        inventory_file: Uploaded inventory_snapshot.csv file
        campaigns_file: Uploaded campaign_plan.csv file
    
    Returns:
        tuple: (products_df, stores_df, sales_df, inventory_df, campaigns_df, error_message)
               error_message is None if successful, string if error occurred
    """
    try:
        # =====================================================================
        # STEP 1: Load all CSV files
        # =====================================================================
        products_df = pd.read_csv(products_file)
        stores_df = pd.read_csv(stores_file)
        sales_df = pd.read_csv(sales_file)
        inventory_df = pd.read_csv(inventory_file)
        campaigns_df = pd.read_csv(campaigns_file)
        
        # =====================================================================
        # STEP 2: Normalize column names (lowercase, strip whitespace)
        # =====================================================================
        products_df.columns = products_df.columns.str.lower().str.strip().str.replace(' ', '_')
        stores_df.columns = stores_df.columns.str.lower().str.strip().str.replace(' ', '_')
        sales_df.columns = sales_df.columns.str.lower().str.strip().str.replace(' ', '_')
        inventory_df.columns = inventory_df.columns.str.lower().str.strip().str.replace(' ', '_')
        campaigns_df.columns = campaigns_df.columns.str.lower().str.strip().str.replace(' ', '_')
        
        # =====================================================================
        # STEP 3: Process SALES data
        # =====================================================================
        # Parse order_time (handles corrupted timestamps gracefully)
        sales_df['order_time'] = pd.to_datetime(sales_df['order_time'], errors='coerce')
        
        # Add time-based derived columns
        sales_df['date'] = sales_df['order_time'].dt.date
        sales_df['month'] = sales_df['order_time'].dt.to_period('M').astype(str)
        sales_df['week'] = sales_df['order_time'].dt.isocalendar().week.astype('Int64')
        sales_df['day_of_week'] = sales_df['order_time'].dt.day_name()
        sales_df['hour'] = sales_df['order_time'].dt.hour
        sales_df['year'] = sales_df['order_time'].dt.year
        sales_df['quarter'] = sales_df['order_time'].dt.quarter
        
        # Calculate revenue
        sales_df['revenue'] = sales_df['qty'] * sales_df['selling_price_aed']
        
        # Merge with products to get category, brand, costs
        if 'category' not in sales_df.columns:
            sales_df = sales_df.merge(
                products_df[['product_id', 'category', 'brand', 'base_price_aed', 'unit_cost_aed']],
                on='product_id',
                how='left'
            )
        
        # Merge with stores to get city, channel, fulfillment_type
        if 'city' not in sales_df.columns:
            sales_df = sales_df.merge(
                stores_df[['store_id', 'city', 'channel', 'fulfillment_type']],
                on='store_id',
                how='left'
            )
        
        # Standardize city names (clean dirty data)
        sales_df['city_clean'] = sales_df['city'].replace(CITY_MAPPING)
        sales_df['city_clean'] = sales_df['city_clean'].fillna(sales_df['city'])
        
        # =====================================================================
        # STEP 4: Process INVENTORY data
        # =====================================================================
        inventory_df['snapshot_date'] = pd.to_datetime(inventory_df['snapshot_date'], errors='coerce')
        
        # Calculate stock status
        inventory_df['stock_status'] = inventory_df.apply(
            lambda x: 'Critical' if x['stock_on_hand'] <= 0
            else 'Low' if x['stock_on_hand'] <= x['reorder_point']
            else 'Healthy',
            axis=1
        )
        
        # Add dirty data flags for analysis
        inventory_df['is_negative'] = inventory_df['stock_on_hand'] < 0
        inventory_df['is_extreme'] = inventory_df['stock_on_hand'] > 9000
        
        # Merge with products
        if 'category' not in inventory_df.columns:
            inventory_df = inventory_df.merge(
                products_df[['product_id', 'category', 'brand']],
                on='product_id',
                how='left'
            )
        
        # Merge with stores
        if 'city' not in inventory_df.columns:
            inventory_df = inventory_df.merge(
                stores_df[['store_id', 'city', 'channel', 'fulfillment_type']],
                on='store_id',
                how='left'
            )
        
        # Clean city names
        inventory_df['city_clean'] = inventory_df['city'].replace(CITY_MAPPING)
        inventory_df['city_clean'] = inventory_df['city_clean'].fillna(inventory_df['city'])
        
        # =====================================================================
        # STEP 5: Process CAMPAIGNS data
        # =====================================================================
        campaigns_df['start_date'] = pd.to_datetime(campaigns_df['start_date'], errors='coerce')
        campaigns_df['end_date'] = pd.to_datetime(campaigns_df['end_date'], errors='coerce')
        campaigns_df['duration_days'] = (campaigns_df['end_date'] - campaigns_df['start_date']).dt.days
        campaigns_df['is_active'] = (
            (campaigns_df['start_date'] <= pd.Timestamp.now()) &
            (campaigns_df['end_date'] >= pd.Timestamp.now())
        )
        
        # =====================================================================
        # STEP 6: Process STORES data
        # =====================================================================
        stores_df['city_clean'] = stores_df['city'].replace(CITY_MAPPING)
        stores_df['city_clean'] = stores_df['city_clean'].fillna(stores_df['city'])
        
        # Return all dataframes with no error
        return products_df, stores_df, sales_df, inventory_df, campaigns_df, None
    
    except Exception as e:
        # Return None for all dataframes with error message
        return None, None, None, None, None, str(e)


def get_filtered_data(sales_df, inventory_df, filters):
    """
    Apply filters to sales and inventory dataframes.
    
    This function handles the multi-dimensional filtering logic with
    proper handling of 'All' selections and cascading dependencies.
    
    Args:
        sales_df: Sales DataFrame
        inventory_df: Inventory DataFrame
        filters: Dictionary with filter keys:
            - city: List of selected cities (or ['All'])
            - channel: List of selected channels (or ['All'])
            - category: List of selected categories (or ['All'])
            - brand: List of selected brands (or ['All'])
            - payment_status: List of selected statuses (or ['All'])
            - date_range: Tuple of (start_date, end_date)
    
    Returns:
        tuple: (filtered_sales_df, filtered_inventory_df)
    """
    filtered_sales = sales_df.copy()
    filtered_inventory = inventory_df.copy()
    
    # Apply city filter (use city_clean for standardized values)
    if 'city' in filters and filters['city'] and 'All' not in filters['city']:
        filtered_sales = filtered_sales[filtered_sales['city_clean'].isin(filters['city'])]
        filtered_inventory = filtered_inventory[filtered_inventory['city_clean'].isin(filters['city'])]
    
    # Apply channel filter
    if 'channel' in filters and filters['channel'] and 'All' not in filters['channel']:
        filtered_sales = filtered_sales[filtered_sales['channel'].isin(filters['channel'])]
        filtered_inventory = filtered_inventory[filtered_inventory['channel'].isin(filters['channel'])]
    
    # Apply category filter
    if 'category' in filters and filters['category'] and 'All' not in filters['category']:
        filtered_sales = filtered_sales[filtered_sales['category'].isin(filters['category'])]
        filtered_inventory = filtered_inventory[filtered_inventory['category'].isin(filters['category'])]
    
    # Apply brand filter
    if 'brand' in filters and filters['brand'] and 'All' not in filters['brand']:
        filtered_sales = filtered_sales[filtered_sales['brand'].isin(filters['brand'])]
        filtered_inventory = filtered_inventory[filtered_inventory['brand'].isin(filters['brand'])]
    
    # Apply payment status filter (sales only)
    if 'payment_status' in filters and filters['payment_status'] and 'All' not in filters['payment_status']:
        filtered_sales = filtered_sales[filtered_sales['payment_status'].isin(filters['payment_status'])]
    
    # Apply date range filter (sales only)
    if 'date_range' in filters and filters['date_range']:
        start_date, end_date = filters['date_range']
        if start_date and end_date:
            # Convert to datetime for comparison
            start_dt = pd.to_datetime(start_date)
            end_dt = pd.to_datetime(end_date)
            
            # Filter sales by order_time
            mask = (filtered_sales['order_time'] >= start_dt) & (filtered_sales['order_time'] <= end_dt)
            filtered_sales = filtered_sales[mask]
            
            # Filter inventory by snapshot_date
            inv_mask = (filtered_inventory['snapshot_date'] >= start_dt) & (filtered_inventory['snapshot_date'] <= end_dt)
            filtered_inventory = filtered_inventory[inv_mask]
    
    return filtered_sales, filtered_inventory


def calculate_kpi_metrics(sales_df, inventory_df, products_df, campaigns_df):
    """
    Calculate key performance indicators from the data.
    
    Args:
        sales_df: Sales DataFrame (enriched)
        inventory_df: Inventory DataFrame
        products_df: Products DataFrame
        campaigns_df: Campaigns DataFrame
    
    Returns:
        dict: Dictionary of calculated KPI values
    """
    # Filter to valid (non-null) sales data
    valid_sales = sales_df[sales_df['order_time'].notna()].copy()
    
    # Revenue metrics
    total_revenue = valid_sales['revenue'].sum()
    
    # Order metrics (unique orders, excluding duplicates for accurate count)
    total_orders = valid_sales['order_id'].nunique()
    total_qty = valid_sales['qty'].sum()
    
    # Average metrics
    avg_order_value = total_revenue / total_orders if total_orders > 0 else 0
    avg_qty_per_order = total_qty / total_orders if total_orders > 0 else 0
    
    # Payment status breakdown
    paid_orders = valid_sales[valid_sales['payment_status'] == 'Paid']
    paid_revenue = paid_orders['revenue'].sum()
    refund_rate = (valid_sales['payment_status'] == 'Refunded').sum() / len(valid_sales) * 100 if len(valid_sales) > 0 else 0
    
    # Return rate (among paid orders)
    return_rate = paid_orders['return_flag'].mean() * 100 if len(paid_orders) > 0 else 0
    
    # Discount metrics
    avg_discount = valid_sales['discount_pct'].mean()
    discounted_orders_pct = (valid_sales['discount_pct'] > 0).sum() / len(valid_sales) * 100 if len(valid_sales) > 0 else 0
    
    # Inventory metrics (latest snapshot)
    latest_date = inventory_df['snapshot_date'].max()
    latest_inventory = inventory_df[inventory_df['snapshot_date'] == latest_date]
    
    total_stock = latest_inventory['stock_on_hand'].sum()
    low_stock_count = len(latest_inventory[latest_inventory['stock_status'].isin(['Critical', 'Low'])])
    healthy_stock_count = len(latest_inventory[latest_inventory['stock_status'] == 'Healthy'])
    
    # Stock health percentage
    stock_health_pct = healthy_stock_count / len(latest_inventory) * 100 if len(latest_inventory) > 0 else 0
    
    # Dirty data counts
    negative_stock_count = latest_inventory['is_negative'].sum()
    extreme_stock_count = latest_inventory['is_extreme'].sum()
    
    # Campaign metrics
    active_campaigns = campaigns_df['is_active'].sum() if 'is_active' in campaigns_df.columns else 0
    total_campaign_budget = campaigns_df['promo_budget_aed'].sum()
    avg_campaign_discount = campaigns_df['discount_pct'].mean()
    
    # Product metrics
    total_products = len(products_df)
    new_products = (products_df['launch_flag'] == 'New').sum() if 'launch_flag' in products_df.columns else 0
    
    # Category performance
    category_revenue = valid_sales.groupby('category')['revenue'].sum()
    top_category = category_revenue.idxmax() if len(category_revenue) > 0 else "N/A"
    
    # Time-based metrics
    if len(valid_sales) > 0:
        date_range = (valid_sales['order_time'].max() - valid_sales['order_time'].min()).days
        daily_avg_revenue = total_revenue / date_range if date_range > 0 else total_revenue
        daily_avg_orders = total_orders / date_range if date_range > 0 else total_orders
    else:
        daily_avg_revenue = 0
        daily_avg_orders = 0
    
    return {
        # Revenue KPIs
        'total_revenue': total_revenue,
        'paid_revenue': paid_revenue,
        'daily_avg_revenue': daily_avg_revenue,
        'avg_order_value': avg_order_value,
        
        # Order KPIs
        'total_orders': total_orders,
        'total_qty': total_qty,
        'daily_avg_orders': daily_avg_orders,
        'avg_qty_per_order': avg_qty_per_order,
        
        # Rate KPIs
        'refund_rate': refund_rate,
        'return_rate': return_rate,
        'avg_discount': avg_discount,
        'discounted_orders_pct': discounted_orders_pct,
        
        # Inventory KPIs
        'total_stock': total_stock,
        'low_stock_count': low_stock_count,
        'healthy_stock_count': healthy_stock_count,
        'stock_health_pct': stock_health_pct,
        'negative_stock_count': negative_stock_count,
        'extreme_stock_count': extreme_stock_count,
        
        # Campaign KPIs
        'active_campaigns': active_campaigns,
        'total_campaign_budget': total_campaign_budget,
        'avg_campaign_discount': avg_campaign_discount,
        
        # Product KPIs
        'total_products': total_products,
        'new_products': new_products,
        'top_category': top_category
    }

# =============================================================================
# SIDEBAR CONFIGURATION
# =============================================================================

def render_sidebar():
    """
    Render the sidebar with data source selection and file uploaders.
    
    The sidebar provides two options:
        1. Sample Data (Demo) - Uses generated sample data
        2. Upload Your Files - Upload 5 CSV files from data_generator.py
    
    Returns:
        tuple: (products_df, stores_df, sales_df, inventory_df, campaigns_df)
               Returns (None, None, None, None, None) if data not available
    """
    with st.sidebar:
        # =====================================================================
        # LOGO & BRANDING
        # =====================================================================
        st.markdown('''
        <div style="text-align: center; padding: 20px 0;">
            <span style="font-size: 2.5rem;">🚀</span>
            <div style="font-size: 1.3rem; font-weight: 700; color: white; margin-top: 8px;">
                UAE Promo Pulse
            </div>
            <div style="font-size: 0.8rem; color: #71717a;">
                Promotional Analytics Platform
            </div>
        </div>
        ''', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # =====================================================================
        # DATA SOURCE SELECTION
        # =====================================================================
        st.markdown("### 📂 Data Source")
        
        data_source = st.radio(
            "Select data source:",
            ["📊 Sample Data (Demo)", "📁 Upload Your Files"],
            label_visibility="collapsed",
            key="sidebar_data_source_selector"
        )
        
        st.markdown("---")
        
        # =====================================================================
        # OPTION 1: UPLOAD FILES
        # =====================================================================
        if data_source == "📁 Upload Your Files":
            st.markdown("### 📤 Upload CSV Files")
            st.caption("Upload the 5 files generated by data_generator.py")
            
            # File uploader for products.csv
            products_file = st.file_uploader(
                "📦 products.csv",
                type=['csv'],
                key='sidebar_upload_products',
                help="Required columns: product_id, category, brand, base_price_aed, unit_cost_aed, tax_rate, launch_flag"
            )
            
            # File uploader for stores.csv
            stores_file = st.file_uploader(
                "🏪 stores.csv",
                type=['csv'],
                key='sidebar_upload_stores',
                help="Required columns: store_id, city, channel, fulfillment_type"
            )
            
            # File uploader for sales_raw.csv
            sales_file = st.file_uploader(
                "🛒 sales_raw.csv",
                type=['csv'],
                key='sidebar_upload_sales',
                help="Required columns: order_id, order_time, product_id, store_id, qty, selling_price_aed, discount_pct, payment_status, return_flag"
            )
            
            # File uploader for inventory_snapshot.csv
            inventory_file = st.file_uploader(
                "📊 inventory_snapshot.csv",
                type=['csv'],
                key='sidebar_upload_inventory',
                help="Required columns: snapshot_date, product_id, store_id, stock_on_hand, reorder_point, lead_time_days"
            )
            
            # File uploader for campaign_plan.csv
            campaigns_file = st.file_uploader(
                "🎯 campaign_plan.csv",
                type=['csv'],
                key='sidebar_upload_campaigns',
                help="Required columns: campaign_id, start_date, end_date, city, channel, category, discount_pct, promo_budget_aed"
            )
            
            # Check if all files are uploaded
            if all([products_file, stores_file, sales_file, inventory_file, campaigns_file]):
                with st.spinner("Loading and processing data..."):
                    result = load_and_process_data(
                        products_file, stores_file, sales_file, inventory_file, campaigns_file
                    )
                    products_df, stores_df, sales_df, inventory_df, campaigns_df, error = result
                
                if error:
                    st.error(f"❌ Error loading data: {error}")
                    render_sidebar_footer()
                    return None, None, None, None, None
                
                # Success message
                st.success("✅ All files loaded successfully!")
                
                # Data summary expander
                with st.expander("📊 Data Summary", expanded=False):
                    st.markdown(f"**Products:** {len(products_df):,} rows")
                    st.markdown(f"**Stores:** {len(stores_df):,} rows")
                    st.markdown(f"**Sales:** {len(sales_df):,} rows")
                    st.markdown(f"**Inventory:** {len(inventory_df):,} rows")
                    st.markdown(f"**Campaigns:** {len(campaigns_df):,} rows")
                    
                    st.markdown("---")
                    
                    # Quick dirty data summary
                    st.markdown("**🔍 Data Quality:**")
                    
                    # Check for issues
                    missing_cost = products_df['unit_cost_aed'].isna().sum()
                    inconsistent_cities = stores_df[~stores_df['city'].isin(STANDARD_CITIES)].shape[0]
                    duplicate_orders = sales_df['order_id'].duplicated().sum()
                    corrupted_times = sales_df['order_time'].isna().sum()
                    negative_stock = (inventory_df['stock_on_hand'] < 0).sum()
                    
                    if missing_cost > 0:
                        st.markdown(f"• Missing costs: {missing_cost}")
                    if inconsistent_cities > 0:
                        st.markdown(f"• Inconsistent cities: {inconsistent_cities}")
                    if duplicate_orders > 0:
                        st.markdown(f"• Duplicate orders: {duplicate_orders}")
                    if corrupted_times > 0:
                        st.markdown(f"• Invalid timestamps: {corrupted_times}")
                    if negative_stock > 0:
                        st.markdown(f"• Negative stock: {negative_stock}")
                
                render_sidebar_footer()
                return products_df, stores_df, sales_df, inventory_df, campaigns_df
            
            else:
                # Show which files are missing
                missing_files = []
                if not products_file:
                    missing_files.append("products.csv")
                if not stores_file:
                    missing_files.append("stores.csv")
                if not sales_file:
                    missing_files.append("sales_raw.csv")
                if not inventory_file:
                    missing_files.append("inventory_snapshot.csv")
                if not campaigns_file:
                    missing_files.append("campaign_plan.csv")
                
                st.info(f"📌 Please upload all 5 CSV files\n\nMissing: {', '.join(missing_files)}")
                
                # Schema reference
                with st.expander("📋 Expected File Schema", expanded=False):
                    st.markdown("**products.csv:**")
                    st.code("product_id, category, brand, base_price_aed, unit_cost_aed, tax_rate, launch_flag", language=None)
                    
                    st.markdown("**stores.csv:**")
                    st.code("store_id, city, channel, fulfillment_type", language=None)
                    
                    st.markdown("**sales_raw.csv:**")
                    st.code("order_id, order_time, product_id, store_id, qty, selling_price_aed, discount_pct, payment_status, return_flag", language=None)
                    
                    st.markdown("**inventory_snapshot.csv:**")
                    st.code("snapshot_date, product_id, store_id, stock_on_hand, reorder_point, lead_time_days", language=None)
                    
                    st.markdown("**campaign_plan.csv:**")
                    st.code("campaign_id, start_date, end_date, city, channel, category, discount_pct, promo_budget_aed", language=None)
                
                render_sidebar_footer()
                return None, None, None, None, None
        
        # =====================================================================
        # OPTION 2: SAMPLE DATA (DEFAULT)
        # =====================================================================
        else:
            st.markdown("### ℹ️ Sample Data Mode")
            st.caption("Using demonstration dataset with synthetic UAE retail data and injected dirty data issues.")
            
            # Generate sample data with spinner
            with st.spinner("Generating sample data..."):
                products_df, stores_df, sales_df, inventory_df, campaigns_df = generate_sample_data()
            
            st.success("✅ Sample data loaded!")
            
            # Data summary expander
            with st.expander("📊 Sample Data Info", expanded=False):
                st.markdown(f"**Products:** {len(products_df):,} rows")
                st.markdown(f"**Stores:** {len(stores_df):,} rows")
                st.markdown(f"**Sales:** {len(sales_df):,} rows")
                st.markdown(f"**Inventory:** {len(inventory_df):,} rows")
                st.markdown(f"**Campaigns:** {len(campaigns_df):,} rows")
                
                st.markdown("---")
                
                st.markdown(f"**Categories:** {sales_df['category'].nunique()}")
                st.markdown(f"**Brands:** {sales_df['brand'].nunique()}")
                st.markdown(f"**Cities:** {STANDARD_CITIES}")
                st.markdown(f"**Channels:** {CHANNELS}")
            
            # Dirty data info expander
            with st.expander("🔴 Injected Dirty Data", expanded=False):
                st.markdown("""
                **This sample data includes:**
                - ❌ Missing unit_cost (1.5%)
                - ❌ Inconsistent city names (40%)
                - ❌ Missing discount_pct (3%)
                - ❌ Duplicate orders (0.75%)
                - ❌ Corrupted timestamps (1.5%)
                - ❌ Qty/Price outliers (0.4%)
                - ❌ Negative stock values (2%)
                - ❌ Extreme stock values (1%)
                
                Use the **Data Cleaning** tab to explore and fix these issues!
                """)
            
            render_sidebar_footer()
            return products_df, stores_df, sales_df, inventory_df, campaigns_df


def render_sidebar_footer():
    """Render the sidebar footer with version info."""
    st.markdown("---")
    st.markdown('''
    <div style="text-align: center; color: #71717a; font-size: 0.75rem; padding: 10px 0;">
        <div>Version 2.0 Production</div>
        <div>© 2024 Data Rescue Team</div>
    </div>
    ''', unsafe_allow_html=True)


# =============================================================================
# GLOBAL FILTERS COMPONENT
# =============================================================================

def render_global_filters(sales_df, stores_df, products_df):
    """
    Render global filter controls that apply across all dashboard sections.
    
    Filters include:
        - City (multiselect with 'All' option)
        - Channel (multiselect with 'All' option)
        - Category (multiselect with 'All' option)
        - Date Range (date picker)
    
    Args:
        sales_df: Sales DataFrame for date range
        stores_df: Stores DataFrame for city/channel options
        products_df: Products DataFrame for category options
    
    Returns:
        dict: Dictionary of selected filter values
    """
    st.markdown("### 🎛️ Global Filters")
    
    # Create filter columns
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        # City filter
        city_options = ['All'] + STANDARD_CITIES
        selected_cities = st.multiselect(
            "🏙️ City",
            options=city_options,
            default=['All'],
            key="global_filter_city"
        )
        
        # Handle 'All' selection logic
        if 'All' in selected_cities or len(selected_cities) == 0:
            selected_cities = ['All']
    
    with col2:
        # Channel filter
        channel_options = ['All'] + CHANNELS
        selected_channels = st.multiselect(
            "📱 Channel",
            options=channel_options,
            default=['All'],
            key="global_filter_channel"
        )
        
        if 'All' in selected_channels or len(selected_channels) == 0:
            selected_channels = ['All']
    
    with col3:
        # Category filter
        category_options = ['All'] + CATEGORIES
        selected_categories = st.multiselect(
            "📦 Category",
            options=category_options,
            default=['All'],
            key="global_filter_category"
        )
        
        if 'All' in selected_categories or len(selected_categories) == 0:
            selected_categories = ['All']
    
    with col4:
        # Date range filter
        # Get min/max dates from sales data
        valid_dates = sales_df[sales_df['order_time'].notna()]['order_time']
        
        if len(valid_dates) > 0:
            min_date = valid_dates.min().date()
            max_date = valid_dates.max().date()
        else:
            min_date = datetime.now().date() - timedelta(days=120)
            max_date = datetime.now().date()
        
        date_range = st.date_input(
            "📅 Date Range",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date,
            key="global_filter_date_range"
        )
        
        # Handle single date selection
        if isinstance(date_range, tuple) and len(date_range) == 2:
            start_date, end_date = date_range
        else:
            start_date = min_date
            end_date = max_date
    
    # Build filters dictionary
    filters = {
        'city': selected_cities,
        'channel': selected_channels,
        'category': selected_categories,
        'date_range': (start_date, end_date)
    }
    
    # Show active filters summary
    active_filters = []
    if 'All' not in selected_cities:
        active_filters.append(f"Cities: {', '.join(selected_cities)}")
    if 'All' not in selected_channels:
        active_filters.append(f"Channels: {', '.join(selected_channels)}")
    if 'All' not in selected_categories:
        active_filters.append(f"Categories: {', '.join(selected_categories)}")
    
    if active_filters:
        st.caption(f"🔍 Active filters: {' | '.join(active_filters)}")
    
    return filters


def render_section_filters(sales_df, filter_prefix, include_brand=True, include_payment=False):
    """
    Render section-specific filters for individual tabs.
    
    Args:
        sales_df: Sales DataFrame for options
        filter_prefix: Unique prefix for filter keys (e.g., 'sales', 'inventory')
        include_brand: Whether to include brand filter
        include_payment: Whether to include payment status filter
    
    Returns:
        dict: Dictionary of selected filter values
    """
    # Determine number of columns based on included filters
    num_cols = 2 + int(include_brand) + int(include_payment)
    cols = st.columns(num_cols)
    
    filters = {}
    col_idx = 0
    
    # City filter
    with cols[col_idx]:
        city_options = ['All'] + STANDARD_CITIES
        selected_cities = st.selectbox(
            "🏙️ City",
            options=city_options,
            key=f"{filter_prefix}_filter_city"
        )
        filters['city'] = [selected_cities] if selected_cities != 'All' else ['All']
    col_idx += 1
    
    # Category filter
    with cols[col_idx]:
        category_options = ['All'] + CATEGORIES
        selected_category = st.selectbox(
            "📦 Category",
            options=category_options,
            key=f"{filter_prefix}_filter_category"
        )
        filters['category'] = [selected_category] if selected_category != 'All' else ['All']
    col_idx += 1
    
    # Brand filter (optional)
    if include_brand:
        with cols[col_idx]:
            # Get unique brands from data
            available_brands = sorted(sales_df['brand'].dropna().unique().tolist())
            brand_options = ['All'] + available_brands
            selected_brand = st.selectbox(
                "🏷️ Brand",
                options=brand_options,
                key=f"{filter_prefix}_filter_brand"
            )
            filters['brand'] = [selected_brand] if selected_brand != 'All' else ['All']
        col_idx += 1
    
    # Payment status filter (optional)
    if include_payment:
        with cols[col_idx]:
            payment_options = ['All'] + PAYMENT_STATUSES
            selected_payment = st.selectbox(
                "💳 Payment Status",
                options=payment_options,
                key=f"{filter_prefix}_filter_payment"
            )
            filters['payment_status'] = [selected_payment] if selected_payment != 'All' else ['All']
    
    return filters


# =============================================================================
# OVERVIEW KPIs COMPONENT
# =============================================================================

def render_overview_kpis(products_df, stores_df, sales_df, inventory_df, campaigns_df):
    """
    Render the top-level KPI dashboard with 8 key metrics.
    
    Displays:
        Row 1: Revenue, Orders, Units Sold, Avg Order Value
        Row 2: Stock Health, Low Stock Alerts, Active Campaigns, Campaign Budget
    
    Args:
        products_df: Products DataFrame
        stores_df: Stores DataFrame
        sales_df: Sales DataFrame (enriched)
        inventory_df: Inventory DataFrame
        campaigns_df: Campaigns DataFrame
    """
    # Calculate all metrics using helper function
    metrics = calculate_kpi_metrics(sales_df, inventory_df, products_df, campaigns_df)
    
    # =========================================================================
    # ROW 1: Revenue & Sales KPIs
    # =========================================================================
    row1_kpis = [
        {
            "icon": "💰",
            "value": format_currency(metrics['total_revenue']),
            "label": "Total Revenue",
            "type": "success"
        },
        {
            "icon": "🛒",
            "value": format_number(metrics['total_orders']),
            "label": "Total Orders",
            "type": "primary"
        },
        {
            "icon": "📦",
            "value": format_number(metrics['total_qty']),
            "label": "Units Sold",
            "type": "accent"
        },
        {
            "icon": "💵",
            "value": format_currency(metrics['avg_order_value']),
            "label": "Avg Order Value",
            "type": "secondary"
        }
    ]
    
    render_kpi_row(row1_kpis)
    
    st.markdown("")  # Spacing
    
    # =========================================================================
    # ROW 2: Inventory & Campaign KPIs
    # =========================================================================
    
    # Determine stock health status type
    if metrics['stock_health_pct'] >= 80:
        stock_health_type = "success"
    elif metrics['stock_health_pct'] >= 60:
        stock_health_type = "warning"
    else:
        stock_health_type = "danger"
    
    # Determine low stock alert type
    if metrics['low_stock_count'] > 500:
        low_stock_type = "danger"
    elif metrics['low_stock_count'] > 200:
        low_stock_type = "warning"
    else:
        low_stock_type = "success"
    
    row2_kpis = [
        {
            "icon": "📊",
            "value": format_percentage(metrics['stock_health_pct']),
            "label": "Stock Health",
            "type": stock_health_type
        },
        {
            "icon": "⚠️",
            "value": format_number(metrics['low_stock_count']),
            "label": "Low Stock Alerts",
            "type": low_stock_type
        },
        {
            "icon": "🎯",
            "value": str(int(metrics['active_campaigns'])),
            "label": "Active Campaigns",
            "type": "accent"
        },
        {
            "icon": "💼",
            "value": format_currency(metrics['total_campaign_budget']),
            "label": "Campaign Budget",
            "type": "secondary"
        }
    ]
    
    render_kpi_row(row2_kpis)


def render_overview_detailed(products_df, stores_df, sales_df, inventory_df, campaigns_df):
    """
    Render detailed overview section with charts and insights.
    
    Args:
        All 5 DataFrames
    """
    # Calculate metrics
    metrics = calculate_kpi_metrics(sales_df, inventory_df, products_df, campaigns_df)
    valid_sales = sales_df[sales_df['order_time'].notna()].copy()
    
    # Create two columns for charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Revenue Trend Chart
        render_chart_title("Revenue Trend (Daily)", "📈")
        
        if len(valid_sales) > 0:
            daily_revenue = valid_sales.groupby(valid_sales['order_time'].dt.date).agg({
                'revenue': 'sum',
                'order_id': 'nunique'
            }).reset_index()
            daily_revenue.columns = ['date', 'revenue', 'orders']
            
            fig = px.area(
                daily_revenue,
                x='date',
                y='revenue',
                color_discrete_sequence=['#6366f1']
            )
            fig.update_traces(
                fill='tozeroy',
                fillcolor='rgba(99, 102, 241, 0.2)',
                line=dict(width=2)
            )
            fig = apply_chart_style(fig, height=300, show_legend=False)
            fig.update_layout(
                xaxis_title="",
                yaxis_title="Revenue (AED)",
                yaxis_tickformat=",.0f"
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            render_empty_state("📈", "No Data", "No valid sales data available")
    
    with col2:
        # Category Distribution Chart
        render_chart_title("Revenue by Category", "📦")
        
        if len(valid_sales) > 0:
            category_revenue = valid_sales.groupby('category')['revenue'].sum().reset_index()
            category_revenue = category_revenue.sort_values('revenue', ascending=True)
            
            fig = px.bar(
                category_revenue,
                x='revenue',
                y='category',
                orientation='h',
                color='revenue',
                color_continuous_scale=['#312e81', '#6366f1', '#a5b4fc']
            )
            fig = apply_chart_style(fig, height=300, show_legend=False)
            fig.update_layout(
                xaxis_title="Revenue (AED)",
                yaxis_title="",
                coloraxis_showscale=False,
                xaxis_tickformat=",.0f"
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            render_empty_state("📦", "No Data", "No category data available")
    
    # Second row of charts
    col3, col4 = st.columns(2)
    
    with col3:
        # City Performance Chart
        render_chart_title("Performance by City", "🏙️")
        
        if len(valid_sales) > 0:
            city_metrics = valid_sales.groupby('city_clean').agg({
                'revenue': 'sum',
                'order_id': 'nunique',
                'qty': 'sum'
            }).reset_index()
            city_metrics.columns = ['city', 'revenue', 'orders', 'units']
            
            fig = px.bar(
                city_metrics,
                x='city',
                y='revenue',
                color='city',
                color_discrete_sequence=get_chart_colors()
            )
            fig = apply_chart_style(fig, height=280, show_legend=False)
            fig.update_layout(
                xaxis_title="",
                yaxis_title="Revenue (AED)",
                yaxis_tickformat=",.0f"
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            render_empty_state("🏙️", "No Data", "No city data available")
    
    with col4:
        # Channel Performance Chart
        render_chart_title("Performance by Channel", "📱")
        
        if len(valid_sales) > 0:
            channel_metrics = valid_sales.groupby('channel').agg({
                'revenue': 'sum',
                'order_id': 'nunique'
            }).reset_index()
            channel_metrics.columns = ['channel', 'revenue', 'orders']
            
            fig = px.pie(
                channel_metrics,
                values='revenue',
                names='channel',
                color_discrete_sequence=get_chart_colors(),
                hole=0.5
            )
            fig = apply_chart_style(fig, height=280, show_legend=True)
            fig.update_traces(
                textposition='outside',
                textinfo='label+percent'
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            render_empty_state("📱", "No Data", "No channel data available")
    
    # Insights Row
    render_divider_subtle()
    
    st.markdown("### 💡 Key Insights")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Top performing insight
        if metrics['top_category'] != "N/A":
            render_insight_box(
                "🏆",
                "Top Category",
                f"**{metrics['top_category']}** leads in revenue generation. Consider increasing inventory for this category.",
                "success"
            )
        else:
            render_insight_box("📊", "Analysis", "Insufficient data for category analysis.", "primary")
    
    with col2:
        # Stock health insight
        if metrics['stock_health_pct'] < 70:
            render_insight_box(
                "⚠️",
                "Stock Alert",
                f"Only **{metrics['stock_health_pct']:.1f}%** of items have healthy stock. {metrics['low_stock_count']} items need attention.",
                "warning"
            )
        else:
            render_insight_box(
                "✅",
                "Healthy Stock",
                f"**{metrics['stock_health_pct']:.1f}%** of inventory is at healthy levels. Well managed!",
                "success"
            )
    
    with col3:
        # Campaign insight
        if metrics['active_campaigns'] > 0:
            render_insight_box(
                "🎯",
                "Active Promotions",
                f"**{int(metrics['active_campaigns'])}** campaigns running with avg **{metrics['avg_campaign_discount']:.0f}%** discount.",
                "accent"
            )
        else:
            render_insight_box(
                "📅",
                "No Active Campaigns",
                "No promotions currently running. Consider launching a campaign to boost sales.",
                "primary"
            )


def render_data_quality_overview(products_df, stores_df, sales_df, inventory_df):
    """
    Render a quick data quality overview panel.
    
    Args:
        products_df, stores_df, sales_df, inventory_df: DataFrames to analyze
    """
    st.markdown("### 🔍 Data Quality Overview")
    
    # Calculate dirty data issues
    issues = {
        'missing_unit_cost': products_df['unit_cost_aed'].isna().sum(),
        'inconsistent_cities': stores_df[~stores_df['city'].isin(STANDARD_CITIES)].shape[0],
        'missing_discount': sales_df['discount_pct'].isna().sum(),
        'duplicate_orders': sales_df['order_id'].duplicated().sum(),
        'corrupted_timestamps': sales_df['order_time'].isna().sum(),
        'qty_outliers': (sales_df['qty'] > 20).sum(),
        'negative_stock': (inventory_df['stock_on_hand'] < 0).sum(),
        'extreme_stock': (inventory_df['stock_on_hand'] > 9000).sum()
    }
    
    total_issues = sum(issues.values())
    
    # Calculate overall quality score
    total_records = len(products_df) + len(stores_df) + len(sales_df) + len(inventory_df)
    quality_score = max(0, 100 - (total_issues / total_records * 100 * 10))
    quality_score = min(100, quality_score)
    
    # Display in columns
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        quality_color = '#10b981' if quality_score >= 80 else '#f59e0b' if quality_score >= 60 else '#ef4444'
        st.markdown(f'''
        <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); 
                    border-radius: 12px; padding: 16px; text-align: center;">
            <div style="font-size: 0.8rem; color: #71717a; margin-bottom: 4px;">Quality Score</div>
            <div style="font-size: 1.8rem; font-weight: 700; color: {quality_color};">{quality_score:.0f}/100</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col2:
        st.markdown(f'''
        <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); 
                    border-radius: 12px; padding: 16px; text-align: center;">
            <div style="font-size: 0.8rem; color: #71717a; margin-bottom: 4px;">Total Issues</div>
            <div style="font-size: 1.8rem; font-weight: 700; color: #f59e0b;">{total_issues:,}</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col3:
        critical_issues = issues['negative_stock'] + issues['corrupted_timestamps'] + issues['duplicate_orders']
        st.markdown(f'''
        <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); 
                    border-radius: 12px; padding: 16px; text-align: center;">
            <div style="font-size: 0.8rem; color: #71717a; margin-bottom: 4px;">Critical Issues</div>
            <div style="font-size: 1.8rem; font-weight: 700; color: #ef4444;">{critical_issues:,}</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col4:
        st.markdown(f'''
        <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); 
                    border-radius: 12px; padding: 16px; text-align: center;">
            <div style="font-size: 0.8rem; color: #71717a; margin-bottom: 4px;">Total Records</div>
            <div style="font-size: 1.8rem; font-weight: 700; color: #6366f1;">{total_records:,}</div>
        </div>
        ''', unsafe_allow_html=True)
    
    # Issue breakdown
    with st.expander("📋 Issue Breakdown", expanded=False):
        issue_data = pd.DataFrame({
            'Issue Type': [
                'Missing Unit Cost',
                'Inconsistent Cities',
                'Missing Discount %',
                'Duplicate Orders',
                'Corrupted Timestamps',
                'Quantity Outliers',
                'Negative Stock',
                'Extreme Stock Values'
            ],
            'Count': [
                issues['missing_unit_cost'],
                issues['inconsistent_cities'],
                issues['missing_discount'],
                issues['duplicate_orders'],
                issues['corrupted_timestamps'],
                issues['qty_outliers'],
                issues['negative_stock'],
                issues['extreme_stock']
            ],
            'Severity': [
                'Low', 'Medium', 'Low', 'High', 'High', 'Medium', 'High', 'Medium'
            ]
        })
        
        st.dataframe(issue_data, use_container_width=True, hide_index=True)

# =============================================================================
# DATA CLEANING & QUALITY ANALYSIS TAB
# =============================================================================
# This module provides comprehensive data quality analysis and cleaning tools
# for handling the dirty data issues injected by data_generator.py
# =============================================================================

def render_data_cleaning(products_df, stores_df, sales_df, inventory_df, campaigns_df):
    """
    Render the Data Cleaning & Quality Analysis tab.
    
    This tab provides:
        1. Data Quality Score Dashboard
        2. Issue-by-Issue Analysis
        3. Cleaning Tools & Options
        4. Before/After Comparisons
        5. Exportable Clean Data
    
    Args:
        products_df: Products DataFrame
        stores_df: Stores DataFrame
        sales_df: Sales DataFrame (enriched)
        inventory_df: Inventory DataFrame
        campaigns_df: Campaigns DataFrame
    """
    render_section_header(
        "🧹",
        "Data Cleaning & Quality Analysis",
        "Identify and fix data quality issues in your datasets"
    )
    
    # =========================================================================
    # CALCULATE ALL DATA QUALITY METRICS
    # =========================================================================
    quality_metrics = calculate_data_quality_metrics(
        products_df, stores_df, sales_df, inventory_df
    )
    
    # =========================================================================
    # DATA QUALITY SCORE DASHBOARD
    # =========================================================================
    render_quality_score_dashboard(quality_metrics)
    
    render_divider_subtle()
    
    # =========================================================================
    # SUB-TABS FOR DIFFERENT DATA QUALITY ASPECTS
    # =========================================================================
    quality_tabs = st.tabs([
        "📊 Overview",
        "❌ Missing Values",
        "🔄 Duplicates",
        "🏙️ Inconsistent Cities",
        "⏰ Invalid Timestamps",
        "📈 Outliers",
        "📦 Inventory Issues",
        "🔧 Apply Fixes"
    ])
    
    with quality_tabs[0]:
        render_quality_overview(quality_metrics, products_df, stores_df, sales_df, inventory_df)
    
    with quality_tabs[1]:
        render_missing_values_analysis(products_df, sales_df)
    
    with quality_tabs[2]:
        render_duplicates_analysis(sales_df)
    
    with quality_tabs[3]:
        render_inconsistent_cities_analysis(stores_df, sales_df)
    
    with quality_tabs[4]:
        render_invalid_timestamps_analysis(sales_df)
    
    with quality_tabs[5]:
        render_outliers_analysis(sales_df)
    
    with quality_tabs[6]:
        render_inventory_issues_analysis(inventory_df)
    
    with quality_tabs[7]:
        render_apply_fixes(products_df, stores_df, sales_df, inventory_df)


def calculate_data_quality_metrics(products_df, stores_df, sales_df, inventory_df):
    """
    Calculate comprehensive data quality metrics for all datasets.
    
    Returns:
        dict: Dictionary containing all quality metrics
    """
    metrics = {}
    
    # =========================================================================
    # PRODUCTS QUALITY METRICS
    # =========================================================================
    metrics['products'] = {
        'total_rows': len(products_df),
        'total_cols': len(products_df.columns),
        'missing_unit_cost': products_df['unit_cost_aed'].isna().sum(),
        'missing_unit_cost_pct': (products_df['unit_cost_aed'].isna().sum() / len(products_df)) * 100,
        'completeness': ((products_df.notna().sum().sum()) / (len(products_df) * len(products_df.columns))) * 100
    }
    
    # =========================================================================
    # STORES QUALITY METRICS
    # =========================================================================
    inconsistent_cities = stores_df[~stores_df['city'].isin(STANDARD_CITIES)]
    metrics['stores'] = {
        'total_rows': len(stores_df),
        'total_cols': len(stores_df.columns),
        'inconsistent_cities': len(inconsistent_cities),
        'inconsistent_cities_pct': (len(inconsistent_cities) / len(stores_df)) * 100,
        'unique_city_values': stores_df['city'].nunique(),
        'city_values': stores_df['city'].unique().tolist(),
        'completeness': ((stores_df.notna().sum().sum()) / (len(stores_df) * len(stores_df.columns))) * 100
    }
    
    # =========================================================================
    # SALES QUALITY METRICS
    # =========================================================================
    duplicate_orders = sales_df['order_id'].duplicated().sum()
    corrupted_timestamps = sales_df['order_time'].isna().sum()
    missing_discount = sales_df['discount_pct'].isna().sum()
    qty_outliers = (sales_df['qty'] > 20).sum()
    
    # Price outliers (values > 3x the 95th percentile)
    price_95 = sales_df['selling_price_aed'].quantile(0.95)
    price_outliers = (sales_df['selling_price_aed'] > price_95 * 3).sum()
    
    metrics['sales'] = {
        'total_rows': len(sales_df),
        'total_cols': len(sales_df.columns),
        'unique_orders': sales_df['order_id'].nunique(),
        'duplicate_orders': duplicate_orders,
        'duplicate_orders_pct': (duplicate_orders / len(sales_df)) * 100,
        'corrupted_timestamps': corrupted_timestamps,
        'corrupted_timestamps_pct': (corrupted_timestamps / len(sales_df)) * 100,
        'missing_discount': missing_discount,
        'missing_discount_pct': (missing_discount / len(sales_df)) * 100,
        'qty_outliers': qty_outliers,
        'qty_outliers_pct': (qty_outliers / len(sales_df)) * 100,
        'price_outliers': price_outliers,
        'price_outliers_pct': (price_outliers / len(sales_df)) * 100,
        'completeness': ((sales_df[['order_id', 'product_id', 'store_id', 'qty', 'selling_price_aed']].notna().sum().sum()) / 
                        (len(sales_df) * 5)) * 100
    }
    
    # =========================================================================
    # INVENTORY QUALITY METRICS
    # =========================================================================
    negative_stock = (inventory_df['stock_on_hand'] < 0).sum()
    extreme_stock = (inventory_df['stock_on_hand'] > 9000).sum()
    
    metrics['inventory'] = {
        'total_rows': len(inventory_df),
        'total_cols': len(inventory_df.columns),
        'negative_stock': negative_stock,
        'negative_stock_pct': (negative_stock / len(inventory_df)) * 100,
        'extreme_stock': extreme_stock,
        'extreme_stock_pct': (extreme_stock / len(inventory_df)) * 100,
        'completeness': ((inventory_df.notna().sum().sum()) / (len(inventory_df) * len(inventory_df.columns))) * 100
    }
    
    # =========================================================================
    # OVERALL QUALITY SCORE
    # =========================================================================
    total_issues = (
        metrics['products']['missing_unit_cost'] +
        metrics['stores']['inconsistent_cities'] +
        metrics['sales']['duplicate_orders'] +
        metrics['sales']['corrupted_timestamps'] +
        metrics['sales']['missing_discount'] +
        metrics['sales']['qty_outliers'] +
        metrics['sales']['price_outliers'] +
        metrics['inventory']['negative_stock'] +
        metrics['inventory']['extreme_stock']
    )
    
    total_records = (
        len(products_df) + len(stores_df) + len(sales_df) + len(inventory_df)
    )
    
    # Quality score: 100 - (weighted issues percentage)
    issue_rate = (total_issues / total_records) * 100
    quality_score = max(0, min(100, 100 - (issue_rate * 5)))  # 5x weight for visibility
    
    metrics['overall'] = {
        'total_records': total_records,
        'total_issues': total_issues,
        'issue_rate': issue_rate,
        'quality_score': quality_score
    }
    
    return metrics


def render_quality_score_dashboard(metrics):
    """
    Render the main quality score dashboard with visual indicators.
    
    Args:
        metrics: Dictionary of quality metrics from calculate_data_quality_metrics
    """
    overall = metrics['overall']
    
    # Determine quality level
    if overall['quality_score'] >= 90:
        quality_level = "Excellent"
        quality_color = "#10b981"
        quality_icon = "✅"
    elif overall['quality_score'] >= 75:
        quality_level = "Good"
        quality_color = "#84cc16"
        quality_icon = "👍"
    elif overall['quality_score'] >= 60:
        quality_level = "Fair"
        quality_color = "#f59e0b"
        quality_icon = "⚠️"
    else:
        quality_level = "Needs Attention"
        quality_color = "#ef4444"
        quality_icon = "🔴"
    
    # Main score display
    col1, col2, col3, col4, col5 = st.columns([2, 1, 1, 1, 1])
    
    with col1:
        st.markdown(f'''
        <div style="background: linear-gradient(135deg, rgba(99, 102, 241, 0.1), rgba(139, 92, 246, 0.1));
                    border: 1px solid rgba(99, 102, 241, 0.3); border-radius: 16px; padding: 24px; text-align: center;">
            <div style="font-size: 0.9rem; color: #a1a1aa; margin-bottom: 8px;">Overall Data Quality Score</div>
            <div style="font-size: 3.5rem; font-weight: 800; color: {quality_color}; line-height: 1;">
                {overall['quality_score']:.0f}
            </div>
            <div style="font-size: 1.1rem; color: {quality_color}; margin-top: 8px;">
                {quality_icon} {quality_level}
            </div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col2:
        st.markdown(f'''
        <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08);
                    border-radius: 12px; padding: 20px; text-align: center; height: 100%;">
            <div style="font-size: 0.8rem; color: #71717a; margin-bottom: 8px;">Total Records</div>
            <div style="font-size: 1.8rem; font-weight: 700; color: #6366f1;">{overall['total_records']:,}</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col3:
        issue_color = "#ef4444" if overall['total_issues'] > 1000 else "#f59e0b" if overall['total_issues'] > 500 else "#10b981"
        st.markdown(f'''
        <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08);
                    border-radius: 12px; padding: 20px; text-align: center; height: 100%;">
            <div style="font-size: 0.8rem; color: #71717a; margin-bottom: 8px;">Total Issues</div>
            <div style="font-size: 1.8rem; font-weight: 700; color: {issue_color};">{overall['total_issues']:,}</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col4:
        st.markdown(f'''
        <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08);
                    border-radius: 12px; padding: 20px; text-align: center; height: 100%;">
            <div style="font-size: 0.8rem; color: #71717a; margin-bottom: 8px;">Issue Rate</div>
            <div style="font-size: 1.8rem; font-weight: 700; color: #f59e0b;">{overall['issue_rate']:.2f}%</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col5:
        clean_records = overall['total_records'] - overall['total_issues']
        st.markdown(f'''
        <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08);
                    border-radius: 12px; padding: 20px; text-align: center; height: 100%;">
            <div style="font-size: 0.8rem; color: #71717a; margin-bottom: 8px;">Clean Records</div>
            <div style="font-size: 1.8rem; font-weight: 700; color: #10b981;">{clean_records:,}</div>
        </div>
        ''', unsafe_allow_html=True)


def render_quality_overview(metrics, products_df, stores_df, sales_df, inventory_df):
    """
    Render the quality overview sub-tab with issue breakdown and charts.
    """
    st.markdown("#### 📊 Data Quality Overview")
    st.markdown("A comprehensive view of all data quality issues across your datasets.")
    
    st.markdown("")
    
    # =========================================================================
    # ISSUE BREAKDOWN BY DATASET
    # =========================================================================
    col1, col2 = st.columns(2)
    
    with col1:
        # Issue type breakdown chart
        render_chart_title("Issues by Type", "🔴")
        
        issue_data = pd.DataFrame({
            'Issue Type': [
                'Missing Unit Cost',
                'Inconsistent Cities',
                'Duplicate Orders',
                'Corrupted Timestamps',
                'Missing Discount',
                'Qty Outliers',
                'Price Outliers',
                'Negative Stock',
                'Extreme Stock'
            ],
            'Count': [
                metrics['products']['missing_unit_cost'],
                metrics['stores']['inconsistent_cities'],
                metrics['sales']['duplicate_orders'],
                metrics['sales']['corrupted_timestamps'],
                metrics['sales']['missing_discount'],
                metrics['sales']['qty_outliers'],
                metrics['sales']['price_outliers'],
                metrics['inventory']['negative_stock'],
                metrics['inventory']['extreme_stock']
            ],
            'Severity': [
                'Low', 'Medium', 'High', 'High', 'Low',
                'Medium', 'Medium', 'High', 'Medium'
            ]
        })
        
        # Color by severity
        color_map = {'Low': '#10b981', 'Medium': '#f59e0b', 'High': '#ef4444'}
        issue_data['Color'] = issue_data['Severity'].map(color_map)
        
        fig = px.bar(
            issue_data[issue_data['Count'] > 0],
            x='Count',
            y='Issue Type',
            orientation='h',
            color='Severity',
            color_discrete_map=color_map
        )
        fig = apply_chart_style(fig, height=350)
        fig.update_layout(yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Issues by dataset
        render_chart_title("Issues by Dataset", "📁")
        
        dataset_issues = pd.DataFrame({
            'Dataset': ['Products', 'Stores', 'Sales', 'Inventory'],
            'Issues': [
                metrics['products']['missing_unit_cost'],
                metrics['stores']['inconsistent_cities'],
                (metrics['sales']['duplicate_orders'] + metrics['sales']['corrupted_timestamps'] +
                 metrics['sales']['missing_discount'] + metrics['sales']['qty_outliers'] +
                 metrics['sales']['price_outliers']),
                metrics['inventory']['negative_stock'] + metrics['inventory']['extreme_stock']
            ],
            'Total Records': [
                metrics['products']['total_rows'],
                metrics['stores']['total_rows'],
                metrics['sales']['total_rows'],
                metrics['inventory']['total_rows']
            ]
        })
        
        dataset_issues['Issue Rate'] = (dataset_issues['Issues'] / dataset_issues['Total Records'] * 100).round(2)
        
        fig = px.bar(
            dataset_issues,
            x='Dataset',
            y='Issues',
            color='Issue Rate',
            color_continuous_scale=['#10b981', '#f59e0b', '#ef4444'],
            text='Issues'
        )
        fig = apply_chart_style(fig, height=350, show_legend=False)
        fig.update_traces(textposition='outside')
        fig.update_layout(coloraxis_showscale=True)
        st.plotly_chart(fig, use_container_width=True)
    
    # =========================================================================
    # DETAILED ISSUE TABLE
    # =========================================================================
    st.markdown("")
    st.markdown("#### 📋 Detailed Issue Summary")
    
    detailed_issues = pd.DataFrame({
        'Dataset': ['Products', 'Products', 'Stores', 'Sales', 'Sales', 'Sales', 'Sales', 'Sales', 'Inventory', 'Inventory'],
        'Issue Type': [
            'Missing Unit Cost', 'Data Completeness',
            'Inconsistent City Names',
            'Duplicate Orders', 'Corrupted Timestamps', 'Missing Discount %', 'Quantity Outliers', 'Price Outliers',
            'Negative Stock Values', 'Extreme Stock Values'
        ],
        'Count': [
            metrics['products']['missing_unit_cost'],
            f"{metrics['products']['completeness']:.1f}%",
            metrics['stores']['inconsistent_cities'],
            metrics['sales']['duplicate_orders'],
            metrics['sales']['corrupted_timestamps'],
            metrics['sales']['missing_discount'],
            metrics['sales']['qty_outliers'],
            metrics['sales']['price_outliers'],
            metrics['inventory']['negative_stock'],
            metrics['inventory']['extreme_stock']
        ],
        'Percentage': [
            f"{metrics['products']['missing_unit_cost_pct']:.2f}%",
            "N/A",
            f"{metrics['stores']['inconsistent_cities_pct']:.1f}%",
            f"{metrics['sales']['duplicate_orders_pct']:.2f}%",
            f"{metrics['sales']['corrupted_timestamps_pct']:.2f}%",
            f"{metrics['sales']['missing_discount_pct']:.2f}%",
            f"{metrics['sales']['qty_outliers_pct']:.2f}%",
            f"{metrics['sales']['price_outliers_pct']:.2f}%",
            f"{metrics['inventory']['negative_stock_pct']:.2f}%",
            f"{metrics['inventory']['extreme_stock_pct']:.2f}%"
        ],
        'Severity': [
            'Low', 'Info', 'Medium', 'High', 'High', 'Low', 'Medium', 'Medium', 'High', 'Medium'
        ],
        'Recommended Action': [
            'Impute with category average or median',
            'Monitor completeness',
            'Standardize to Dubai/Abu Dhabi/Sharjah',
            'Remove duplicate records',
            'Remove or re-parse invalid dates',
            'Impute with 0 or median discount',
            'Cap at reasonable maximum or remove',
            'Cap at reasonable maximum or investigate',
            'Set to 0 or investigate data source',
            'Cap at reasonable maximum or remove'
        ]
    })
    
    st.dataframe(
        detailed_issues,
        use_container_width=True,
        hide_index=True,
        column_config={
            'Severity': st.column_config.TextColumn(
                'Severity',
                help='Impact level of the issue'
            )
        }
    )


def render_missing_values_analysis(products_df, sales_df):
    """
    Render detailed analysis of missing values across datasets.
    """
    st.markdown("#### ❌ Missing Values Analysis")
    st.markdown("Identify and understand patterns in missing data.")
    
    st.markdown("")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Products missing values
        st.markdown("##### 📦 Products: Missing Unit Cost")
        
        missing_cost = products_df[products_df['unit_cost_aed'].isna()]
        total_missing = len(missing_cost)
        
        if total_missing > 0:
            # KPI
            render_kpi_row_compact([
                {"icon": "❌", "value": str(total_missing), "label": "Missing Values", "type": "danger"},
                {"icon": "📊", "value": f"{(total_missing/len(products_df)*100):.1f}%", "label": "Percentage", "type": "warning"}
            ])
            
            st.markdown("")
            
            # Distribution by category
            missing_by_category = missing_cost.groupby('category').size().reset_index(name='count')
            
            if len(missing_by_category) > 0:
                fig = px.pie(
                    missing_by_category,
                    values='count',
                    names='category',
                    title='Missing Unit Cost by Category',
                    color_discrete_sequence=get_chart_colors()
                )
                fig = apply_chart_style(fig, height=280)
                st.plotly_chart(fig, use_container_width=True)
            
            # Sample of affected records
            with st.expander("View Affected Products"):
                st.dataframe(
                    missing_cost[['product_id', 'category', 'brand', 'base_price_aed']].head(20),
                    use_container_width=True,
                    hide_index=True
                )
        else:
            render_insight_box("✅", "No Missing Values", "All products have unit cost values.", "success")
    
    with col2:
        # Sales missing values
        st.markdown("##### 🛒 Sales: Missing Discount %")
        
        missing_discount = sales_df[sales_df['discount_pct'].isna()]
        total_missing = len(missing_discount)
        
        if total_missing > 0:
            # KPI
            render_kpi_row_compact([
                {"icon": "❌", "value": format_number(total_missing), "label": "Missing Values", "type": "danger"},
                {"icon": "📊", "value": f"{(total_missing/len(sales_df)*100):.1f}%", "label": "Percentage", "type": "warning"}
            ])
            
            st.markdown("")
            
            # Distribution by category
            valid_missing = missing_discount[missing_discount['category'].notna()]
            if len(valid_missing) > 0:
                missing_by_category = valid_missing.groupby('category').size().reset_index(name='count')
                
                fig = px.bar(
                    missing_by_category.sort_values('count', ascending=True),
                    x='count',
                    y='category',
                    orientation='h',
                    title='Missing Discount % by Category',
                    color_discrete_sequence=['#f59e0b']
                )
                fig = apply_chart_style(fig, height=280, show_legend=False)
                st.plotly_chart(fig, use_container_width=True)
            
            # Sample of affected records
            with st.expander("View Affected Sales"):
                display_cols = ['order_id', 'product_id', 'qty', 'selling_price_aed', 'category']
                st.dataframe(
                    missing_discount[display_cols].head(20),
                    use_container_width=True,
                    hide_index=True
                )
        else:
            render_insight_box("✅", "No Missing Values", "All sales have discount percentage values.", "success")
    
    # Recommendation
    st.markdown("")
    render_recommendation_card(
        "💡",
        "**Recommendation:** Missing unit costs can be imputed using the median cost ratio (unit_cost/base_price) "
        "for each category. Missing discount percentages can typically be set to 0 (no discount) or imputed with "
        "the category median if promotional patterns are known."
    )


def render_duplicates_analysis(sales_df):
    """
    Render detailed analysis of duplicate orders.
    """
    st.markdown("#### 🔄 Duplicate Orders Analysis")
    st.markdown("Identify and examine duplicate order records that may inflate metrics.")
    
    st.markdown("")
    
    # Find duplicates
    duplicate_mask = sales_df['order_id'].duplicated(keep=False)
    duplicates_df = sales_df[duplicate_mask].sort_values('order_id')
    
    unique_dup_orders = duplicates_df['order_id'].nunique()
    total_dup_records = len(duplicates_df)
    records_to_remove = total_dup_records - unique_dup_orders
    
    # KPIs
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        render_status_card("Duplicate Order IDs", format_number(unique_dup_orders), "warning")
    with col2:
        render_status_card("Total Duplicate Records", format_number(total_dup_records), "danger")
    with col3:
        render_status_card("Records to Remove", format_number(records_to_remove), "danger")
    with col4:
        dup_pct = (records_to_remove / len(sales_df)) * 100
        render_status_card("Impact on Data", f"{dup_pct:.2f}%", "warning")
    
    st.markdown("")
    
    if total_dup_records > 0:
        col1, col2 = st.columns(2)
        
        with col1:
            # Sample duplicate groups
            st.markdown("##### 🔍 Sample Duplicate Groups")
            
            # Get first few duplicate order_ids
            sample_dup_ids = duplicates_df['order_id'].unique()[:5]
            sample_dups = duplicates_df[duplicates_df['order_id'].isin(sample_dup_ids)]
            
            display_cols = ['order_id', 'product_id', 'qty', 'selling_price_aed', 'payment_status']
            st.dataframe(
                sample_dups[display_cols],
                use_container_width=True,
                hide_index=True
            )
        
        with col2:
            # Revenue impact
            st.markdown("##### 💰 Revenue Impact")
            
            # Calculate inflated revenue from duplicates
            inflated_revenue = duplicates_df.groupby('order_id')['revenue'].sum()
            true_revenue = duplicates_df.drop_duplicates(subset='order_id')['revenue'].sum()
            extra_revenue = inflated_revenue.sum() - true_revenue
            
            impact_data = pd.DataFrame({
                'Metric': ['Inflated Revenue', 'True Revenue', 'Over-counted Amount'],
                'Value (AED)': [inflated_revenue.sum(), true_revenue, extra_revenue]
            })
            
            fig = px.bar(
                impact_data,
                x='Metric',
                y='Value (AED)',
                color='Metric',
                color_discrete_sequence=['#ef4444', '#10b981', '#f59e0b']
            )
            fig = apply_chart_style(fig, height=280, show_legend=False)
            fig.update_layout(yaxis_tickformat=",.0f")
            st.plotly_chart(fig, use_container_width=True)
        
        # Recommendation
        render_recommendation_card(
            "💡",
            f"**Recommendation:** Remove {records_to_remove:,} duplicate records to prevent inflated metrics. "
            f"This will correct an over-count of approximately AED {extra_revenue:,.0f} in revenue calculations."
        )
    else:
        render_insight_box("✅", "No Duplicates Found", "All order IDs are unique.", "success")


def render_inconsistent_cities_analysis(stores_df, sales_df):
    """
    Render detailed analysis of inconsistent city values.
    """
    st.markdown("#### 🏙️ Inconsistent City Names Analysis")
    st.markdown("Identify and standardize city name variations to enable proper geographic analysis.")
    
    st.markdown("")
    
    # Find inconsistent cities
    inconsistent_stores = stores_df[~stores_df['city'].isin(STANDARD_CITIES)]
    
    col1, col2 = st.columns(2)
    
    with col1:
        # All city variations
        st.markdown("##### 📋 City Value Variations Found")
        
        city_counts = stores_df['city'].value_counts().reset_index()
        city_counts.columns = ['City Value', 'Count']
        city_counts['Standard?'] = city_counts['City Value'].isin(STANDARD_CITIES)
        city_counts['Mapped To'] = city_counts['City Value'].apply(
            lambda x: x if x in STANDARD_CITIES else CITY_MAPPING.get(x, 'Unknown')
        )
        
        # Style the dataframe
        st.dataframe(
            city_counts,
            use_container_width=True,
            hide_index=True,
            column_config={
                'Standard?': st.column_config.CheckboxColumn('Standard?', default=False)
            }
        )
    
    with col2:
        # Mapping visualization
        st.markdown("##### 🗺️ City Standardization Mapping")
        
        # Create mapping chart
        mapping_data = []
        for original, standard in CITY_MAPPING.items():
            if original != standard:
                mapping_data.append({'Original': original, 'Standard': standard})
        
        if mapping_data:
            mapping_df = pd.DataFrame(mapping_data)
            st.dataframe(mapping_df, use_container_width=True, hide_index=True)
        
        st.markdown("")
        st.markdown("**Standard City Names:**")
        for city in STANDARD_CITIES:
            st.markdown(f"- ✅ {city}")
    
    st.markdown("")
    
    # Impact analysis
    st.markdown("##### 📊 Impact on Sales Analysis")
    
    # Compare aggregation before/after standardization
    col1, col2 = st.columns(2)
    
    with col1:
        # Before standardization
        if 'city' in sales_df.columns:
            city_revenue_raw = sales_df.groupby('city')['revenue'].sum().reset_index()
            city_revenue_raw = city_revenue_raw.sort_values('revenue', ascending=True)
            
            fig = px.bar(
                city_revenue_raw,
                x='revenue',
                y='city',
                orientation='h',
                title='Revenue by City (Before Cleaning)',
                color_discrete_sequence=['#ef4444']
            )
            fig = apply_chart_style(fig, height=300, show_legend=False)
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # After standardization
        if 'city_clean' in sales_df.columns:
            city_revenue_clean = sales_df.groupby('city_clean')['revenue'].sum().reset_index()
            city_revenue_clean = city_revenue_clean.sort_values('revenue', ascending=True)
            
            fig = px.bar(
                city_revenue_clean,
                x='revenue',
                y='city_clean',
                orientation='h',
                title='Revenue by City (After Cleaning)',
                color_discrete_sequence=['#10b981']
            )
            fig = apply_chart_style(fig, height=300, show_legend=False)
            st.plotly_chart(fig, use_container_width=True)
    
    # Recommendation
    render_recommendation_card(
        "💡",
        "**Recommendation:** Use the `city_clean` column for all geographic analysis. "
        "The standardization maps all variations (case differences, abbreviations, typos) to the "
        "three standard UAE cities: Dubai, Abu Dhabi, and Sharjah."
    )


def render_invalid_timestamps_analysis(sales_df):
    """
    Render detailed analysis of corrupted/invalid timestamps.
    """
    st.markdown("#### ⏰ Invalid Timestamps Analysis")
    st.markdown("Identify and handle records with corrupted or unparseable date/time values.")
    
    st.markdown("")
    
    # Find invalid timestamps
    invalid_timestamps = sales_df[sales_df['order_time'].isna()]
    total_invalid = len(invalid_timestamps)
    
    # KPIs
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        render_status_card("Invalid Timestamps", format_number(total_invalid), "danger")
    with col2:
        pct = (total_invalid / len(sales_df)) * 100
        render_status_card("Percentage", f"{pct:.2f}%", "warning")
    with col3:
        valid_count = len(sales_df) - total_invalid
        render_status_card("Valid Records", format_number(valid_count), "success")
    with col4:
        revenue_lost = invalid_timestamps['revenue'].sum()
        render_status_card("Revenue Affected", format_currency(revenue_lost), "warning")
    
    st.markdown("")
    
    if total_invalid > 0:
        col1, col2 = st.columns(2)
        
        with col1:
            # Sample invalid records
            st.markdown("##### 🔍 Sample Invalid Records")
            
            # We need to look at the original order_time values before parsing
            # Since we've already parsed, let's show what we can
            display_cols = ['order_id', 'product_id', 'store_id', 'qty', 'selling_price_aed', 'revenue']
            st.dataframe(
                invalid_timestamps[display_cols].head(15),
                use_container_width=True,
                hide_index=True
            )
            
            st.caption("Note: These records had unparseable timestamp values like 'NULL', 'N/A', 'invalid_date', etc.")
        
        with col2:
            # Distribution of invalid by other dimensions
            st.markdown("##### 📊 Invalid Records Distribution")
            
            if 'category' in invalid_timestamps.columns:
                invalid_by_category = invalid_timestamps['category'].value_counts().reset_index()
                invalid_by_category.columns = ['Category', 'Count']
                
                fig = px.pie(
                    invalid_by_category,
                    values='Count',
                    names='Category',
                    color_discrete_sequence=get_chart_colors()
                )
                fig = apply_chart_style(fig, height=280)
                st.plotly_chart(fig, use_container_width=True)
        
        # Recommendation
        render_recommendation_card(
            "💡",
            f"**Recommendation:** The {total_invalid:,} records with invalid timestamps should be either: "
            "(1) Removed from time-based analysis, (2) Assigned to a default date if business logic allows, "
            "or (3) Investigated at the source system. These records are currently excluded from trend analysis "
            "but are included in aggregate metrics."
        )
    else:
        render_insight_box("✅", "All Timestamps Valid", "All order timestamps were parsed successfully.", "success")


def render_outliers_analysis(sales_df):
    """
    Render detailed analysis of quantity and price outliers.
    """
    st.markdown("#### 📈 Outliers Analysis")
    st.markdown("Identify extreme values in quantity and price that may indicate data errors.")
    
    st.markdown("")
    
    # Valid sales only
    valid_sales = sales_df[sales_df['order_time'].notna()].copy()
    
    # Define outlier thresholds
    QTY_THRESHOLD = 20
    price_95 = valid_sales['selling_price_aed'].quantile(0.95)
    PRICE_THRESHOLD = price_95 * 3
    
    qty_outliers = valid_sales[valid_sales['qty'] > QTY_THRESHOLD]
    price_outliers = valid_sales[valid_sales['selling_price_aed'] > PRICE_THRESHOLD]
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Quantity outliers
        st.markdown("##### 📦 Quantity Outliers")
        st.caption(f"Orders with qty > {QTY_THRESHOLD} units")
        
        render_kpi_row_compact([
            {"icon": "🔢", "value": str(len(qty_outliers)), "label": "Outlier Records", "type": "warning"},
            {"icon": "📊", "value": f"{(len(qty_outliers)/len(valid_sales)*100):.2f}%", "label": "Percentage", "type": "primary"}
        ])
        
        st.markdown("")
        
        if len(qty_outliers) > 0:
            # Distribution of outlier quantities
            fig = px.histogram(
                qty_outliers,
                x='qty',
                nbins=20,
                title='Distribution of Outlier Quantities',
                color_discrete_sequence=['#f59e0b']
            )
            fig = apply_chart_style(fig, height=250, show_legend=False)
            st.plotly_chart(fig, use_container_width=True)
            
            # Sample records
            with st.expander("View Quantity Outliers"):
                st.dataframe(
                    qty_outliers[['order_id', 'product_id', 'qty', 'selling_price_aed', 'category']].head(20),
                    use_container_width=True,
                    hide_index=True
                )
        else:
            render_insight_box("✅", "No Quantity Outliers", f"All orders have qty ≤ {QTY_THRESHOLD}.", "success")
    
    with col2:
        # Price outliers
        st.markdown("##### 💰 Price Outliers")
        st.caption(f"Orders with selling_price > AED {PRICE_THRESHOLD:,.0f}")
        
        render_kpi_row_compact([
            {"icon": "💵", "value": str(len(price_outliers)), "label": "Outlier Records", "type": "warning"},
            {"icon": "📊", "value": f"{(len(price_outliers)/len(valid_sales)*100):.2f}%", "label": "Percentage", "type": "primary"}
        ])
        
        st.markdown("")
        
        if len(price_outliers) > 0:
            # Distribution of outlier prices
            fig = px.histogram(
                price_outliers,
                x='selling_price_aed',
                nbins=20,
                title='Distribution of Outlier Prices',
                color_discrete_sequence=['#ef4444']
            )
            fig = apply_chart_style(fig, height=250, show_legend=False)
            st.plotly_chart(fig, use_container_width=True)
            
            # Sample records
            with st.expander("View Price Outliers"):
                st.dataframe(
                    price_outliers[['order_id', 'product_id', 'qty', 'selling_price_aed', 'category']].head(20),
                    use_container_width=True,
                    hide_index=True
                )
        else:
            render_insight_box("✅", "No Price Outliers", "All prices are within expected range.", "success")
    
    # Box plot comparison
    st.markdown("")
    st.markdown("##### 📊 Distribution Comparison")
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.box(
            valid_sales,
            y='qty',
            title='Quantity Distribution',
            color_discrete_sequence=['#6366f1']
        )
        fig = apply_chart_style(fig, height=280, show_legend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.box(
            valid_sales,
            y='selling_price_aed',
            title='Price Distribution',
            color_discrete_sequence=['#8b5cf6']
        )
        fig = apply_chart_style(fig, height=280, show_legend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    # Recommendation
    render_recommendation_card(
        "💡",
        "**Recommendation:** Outliers can be handled by: (1) Capping at threshold values (Winsorization), "
        "(2) Removing from analysis, or (3) Investigating individually if they represent valid large orders. "
        "The current data shows patterns consistent with data entry errors or system glitches."
    )


def render_inventory_issues_analysis(inventory_df):
    """
    Render detailed analysis of inventory data issues.
    """
    st.markdown("#### 📦 Inventory Data Issues")
    st.markdown("Identify impossible inventory values that indicate data quality problems.")
    
    st.markdown("")
    
    # Get latest snapshot for analysis
    latest_date = inventory_df['snapshot_date'].max()
    latest_inventory = inventory_df[inventory_df['snapshot_date'] == latest_date].copy()
    
    # Find issues
    negative_stock = inventory_df[inventory_df['stock_on_hand'] < 0]
    extreme_stock = inventory_df[inventory_df['stock_on_hand'] > 9000]
    
    # KPIs
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        render_status_card("Negative Stock Records", format_number(len(negative_stock)), "danger")
    with col2:
        render_status_card("Extreme Stock Records", format_number(len(extreme_stock)), "warning")
    with col3:
        total_issues = len(negative_stock) + len(extreme_stock)
        pct = (total_issues / len(inventory_df)) * 100
        render_status_card("Issue Rate", f"{pct:.2f}%", "warning")
    with col4:
        clean_records = len(inventory_df) - total_issues
        render_status_card("Clean Records", format_number(clean_records), "success")
    
    st.markdown("")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Negative stock analysis
        st.markdown("##### ❌ Negative Stock Analysis")
        
        if len(negative_stock) > 0:
            # Distribution of negative values
            fig = px.histogram(
                negative_stock,
                x='stock_on_hand',
                nbins=20,
                title='Distribution of Negative Stock Values',
                color_discrete_sequence=['#ef4444']
            )
            fig = apply_chart_style(fig, height=250, show_legend=False)
            st.plotly_chart(fig, use_container_width=True)
            
            # By category
            if 'category' in negative_stock.columns:
                neg_by_cat = negative_stock.groupby('category').size().reset_index(name='count')
                st.markdown("**Negative Stock by Category:**")
                st.dataframe(neg_by_cat, use_container_width=True, hide_index=True)
        else:
            render_insight_box("✅", "No Negative Stock", "All stock values are non-negative.", "success")
    
    with col2:
        # Extreme stock analysis
        st.markdown("##### ⚠️ Extreme Stock Analysis")
        
        if len(extreme_stock) > 0:
            # Distribution of extreme values
            fig = px.histogram(
                extreme_stock,
                x='stock_on_hand',
                nbins=20,
                title='Distribution of Extreme Stock Values',
                color_discrete_sequence=['#f59e0b']
            )
            fig = apply_chart_style(fig, height=250, show_legend=False)
            st.plotly_chart(fig, use_container_width=True)
            
            # Common extreme values
            extreme_values = extreme_stock['stock_on_hand'].value_counts().head(5).reset_index()
            extreme_values.columns = ['Stock Value', 'Occurrences']
            st.markdown("**Most Common Extreme Values:**")
            st.dataframe(extreme_values, use_container_width=True, hide_index=True)
        else:
            render_insight_box("✅", "No Extreme Stock", "All stock values are within normal range.", "success")
    
    # Sample problematic records
    st.markdown("")
    st.markdown("##### 🔍 Sample Problematic Records")
    
    problem_records = pd.concat([negative_stock.head(10), extreme_stock.head(10)])
    if len(problem_records) > 0:
        display_cols = ['snapshot_date', 'product_id', 'store_id', 'stock_on_hand', 'reorder_point', 'stock_status']
        st.dataframe(
            problem_records[display_cols],
            use_container_width=True,
            hide_index=True
        )
    
    # Recommendation
    render_recommendation_card(
        "💡",
        "**Recommendation:** Negative stock values should be set to 0 and flagged for investigation "
        "(may indicate timing issues between sales and inventory updates). Extreme values (9999, 99999) "
        "are often placeholder values and should be replaced with actual counts or removed from analysis."
    )


def render_apply_fixes(products_df, stores_df, sales_df, inventory_df):
    """
    Render the data cleaning/fixing interface with downloadable clean data.
    """
    st.markdown("#### 🔧 Apply Data Fixes")
    st.markdown("Select cleaning operations and download clean datasets.")
    
    st.markdown("")
    
    # Cleaning options
    st.markdown("##### ⚙️ Select Cleaning Operations")
    
    col1, col2 = st.columns(2)
    
    with col1:
        fix_cities = st.checkbox("✅ Standardize city names", value=True, help="Map all city variations to standard names")
        fix_duplicates = st.checkbox("✅ Remove duplicate orders", value=True, help="Remove duplicate order_id records")
        fix_timestamps = st.checkbox("✅ Remove invalid timestamps", value=True, help="Remove records with unparseable dates")
    
    with col2:
        fix_negative_stock = st.checkbox("✅ Fix negative stock (set to 0)", value=True, help="Replace negative stock with 0")
        fix_extreme_stock = st.checkbox("✅ Cap extreme stock values", value=True, help="Cap stock at 5000 units")
        impute_missing = st.checkbox("✅ Impute missing values", value=True, help="Fill missing discount with 0, missing cost with median")
    
    st.markdown("")
    
    # Apply fixes button
    if st.button("🚀 Apply Selected Fixes & Generate Clean Data", type="primary"):
        with st.spinner("Applying fixes..."):
            # Create copies
            clean_sales = sales_df.copy()
            clean_inventory = inventory_df.copy()
            clean_products = products_df.copy()
            clean_stores = stores_df.copy()
            
            fixes_applied = []
            
            # Fix 1: Standardize city names
            if fix_cities:
                clean_stores['city'] = clean_stores['city'].replace(CITY_MAPPING)
                clean_stores['city'] = clean_stores['city'].apply(
                    lambda x: x if x in STANDARD_CITIES else 'Dubai'  # Default unknown to Dubai
                )
                fixes_applied.append("✅ Standardized city names")
            
            # Fix 2: Remove duplicates
            if fix_duplicates:
                before_count = len(clean_sales)
                clean_sales = clean_sales.drop_duplicates(subset='order_id', keep='first')
                removed = before_count - len(clean_sales)
                fixes_applied.append(f"✅ Removed {removed:,} duplicate orders")
            
            # Fix 3: Remove invalid timestamps
            if fix_timestamps:
                before_count = len(clean_sales)
                clean_sales = clean_sales[clean_sales['order_time'].notna()]
                removed = before_count - len(clean_sales)
                fixes_applied.append(f"✅ Removed {removed:,} records with invalid timestamps")
            
            # Fix 4: Fix negative stock
            if fix_negative_stock:
                neg_count = (clean_inventory['stock_on_hand'] < 0).sum()
                clean_inventory.loc[clean_inventory['stock_on_hand'] < 0, 'stock_on_hand'] = 0
                fixes_applied.append(f"✅ Fixed {neg_count:,} negative stock values")
            
            # Fix 5: Cap extreme stock
            if fix_extreme_stock:
                extreme_count = (clean_inventory['stock_on_hand'] > 5000).sum()
                clean_inventory.loc[clean_inventory['stock_on_hand'] > 5000, 'stock_on_hand'] = 5000
                fixes_applied.append(f"✅ Capped {extreme_count:,} extreme stock values")
            
            # Fix 6: Impute missing values
            if impute_missing:
                # Missing discount -> 0
                discount_missing = clean_sales['discount_pct'].isna().sum()
                clean_sales['discount_pct'] = clean_sales['discount_pct'].fillna(0)
                
                # Missing unit cost -> category median
                if clean_products['unit_cost_aed'].isna().any():
                    cost_missing = clean_products['unit_cost_aed'].isna().sum()
                    # Calculate median cost ratio by category
                    clean_products['cost_ratio'] = clean_products['unit_cost_aed'] / clean_products['base_price_aed']
                    category_medians = clean_products.groupby('category')['cost_ratio'].median()
                    
                    for idx in clean_products[clean_products['unit_cost_aed'].isna()].index:
                        cat = clean_products.loc[idx, 'category']
                        base = clean_products.loc[idx, 'base_price_aed']
                        ratio = category_medians.get(cat, 0.5)
                        clean_products.loc[idx, 'unit_cost_aed'] = base * ratio
                    
                    clean_products = clean_products.drop('cost_ratio', axis=1)
                    fixes_applied.append(f"✅ Imputed {cost_missing} missing unit costs")
                
                fixes_applied.append(f"✅ Imputed {discount_missing:,} missing discount values")
            
            # Store in session state
            st.session_state['clean_sales'] = clean_sales
            st.session_state['clean_inventory'] = clean_inventory
            st.session_state['clean_products'] = clean_products
            st.session_state['clean_stores'] = clean_stores
        
        # Show results
        st.success("🎉 Data cleaning complete!")
        
        st.markdown("##### 📋 Fixes Applied:")
        for fix in fixes_applied:
            st.markdown(fix)
        
        st.markdown("")
        
        # Before/After comparison
        st.markdown("##### 📊 Before vs After Comparison")
        
        comparison_data = pd.DataFrame({
            'Metric': ['Total Sales Records', 'Duplicate Orders', 'Invalid Timestamps', 'Negative Stock', 'Extreme Stock'],
            'Before': [
                len(sales_df),
                sales_df['order_id'].duplicated().sum(),
                sales_df['order_time'].isna().sum(),
                (inventory_df['stock_on_hand'] < 0).sum(),
                (inventory_df['stock_on_hand'] > 9000).sum()
            ],
            'After': [
                len(clean_sales),
                clean_sales['order_id'].duplicated().sum() if fix_duplicates else sales_df['order_id'].duplicated().sum(),
                clean_sales['order_time'].isna().sum() if fix_timestamps else sales_df['order_time'].isna().sum(),
                (clean_inventory['stock_on_hand'] < 0).sum() if fix_negative_stock else (inventory_df['stock_on_hand'] < 0).sum(),
                (clean_inventory['stock_on_hand'] > 5000).sum() if fix_extreme_stock else (inventory_df['stock_on_hand'] > 9000).sum()
            ]
        })
        
        st.dataframe(comparison_data, use_container_width=True, hide_index=True)
        
        st.markdown("")
        
        # Download buttons
        st.markdown("##### 📥 Download Clean Data")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            csv_products = clean_products.to_csv(index=False)
            st.download_button(
                label="📦 products_clean.csv",
                data=csv_products,
                file_name="products_clean.csv",
                mime="text/csv"
            )
        
        with col2:
            csv_stores = clean_stores.to_csv(index=False)
            st.download_button(
                label="🏪 stores_clean.csv",
                data=csv_stores,
                file_name="stores_clean.csv",
                mime="text/csv"
            )
        
        with col3:
            csv_sales = clean_sales.to_csv(index=False)
            st.download_button(
                label="🛒 sales_clean.csv",
                data=csv_sales,
                file_name="sales_clean.csv",
                mime="text/csv"
            )
        
        with col4:
            csv_inventory = clean_inventory.to_csv(index=False)
            st.download_button(
                label="📊 inventory_clean.csv",
                data=csv_inventory,
                file_name="inventory_clean.csv",
                mime="text/csv"
            )
    
    else:
        # Show preview of current issues
        st.markdown("##### ℹ️ Current Data Issues Summary")
        
        issues_summary = {
            'Issue': [
                'Inconsistent Cities',
                'Duplicate Orders',
                'Invalid Timestamps',
                'Missing Discount %',
                'Missing Unit Cost',
                'Negative Stock',
                'Extreme Stock (>9000)'
            ],
            'Count': [
                stores_df[~stores_df['city'].isin(STANDARD_CITIES)].shape[0],
                sales_df['order_id'].duplicated().sum(),
                sales_df['order_time'].isna().sum(),
                sales_df['discount_pct'].isna().sum(),
                products_df['unit_cost_aed'].isna().sum(),
                (inventory_df['stock_on_hand'] < 0).sum(),
                (inventory_df['stock_on_hand'] > 9000).sum()
            ]
        }
        
        st.dataframe(pd.DataFrame(issues_summary), use_container_width=True, hide_index=True)
        
        render_insight_box(
            "ℹ️",
            "Ready to Clean",
            "Select the cleaning operations above and click 'Apply Selected Fixes' to generate clean datasets.",
            "primary"
        )

# =============================================================================
# SALES ANALYTICS TAB
# =============================================================================
# This module provides comprehensive sales analysis including revenue trends,
# category performance, geographic analysis, and channel insights.
# =============================================================================

def render_sales_analysis(sales_df, products_df, stores_df):
    """
    Render the Sales Analytics tab with comprehensive sales insights.
    
    This tab provides:
        1. Revenue & Order KPIs
        2. Time-series trend analysis
        3. Category performance breakdown
        4. Geographic (city) analysis
        5. Channel performance
        6. Payment status analysis
        7. Top products analysis
    
    Args:
        sales_df: Enriched sales DataFrame
        products_df: Products DataFrame
        stores_df: Stores DataFrame
    """
    render_section_header(
        "📈",
        "Sales Analytics",
        "Comprehensive analysis of sales performance across all dimensions"
    )
    
    # =========================================================================
    # SECTION FILTERS
    # =========================================================================
    st.markdown("##### 🎛️ Filters")
    
    filter_col1, filter_col2, filter_col3, filter_col4, filter_col5 = st.columns(5)
    
    with filter_col1:
        city_options = ['All'] + STANDARD_CITIES
        selected_city = st.selectbox(
            "🏙️ City",
            options=city_options,
            key="sales_filter_city"
        )
    
    with filter_col2:
        channel_options = ['All'] + CHANNELS
        selected_channel = st.selectbox(
            "📱 Channel",
            options=channel_options,
            key="sales_filter_channel"
        )
    
    with filter_col3:
        category_options = ['All'] + CATEGORIES
        selected_category = st.selectbox(
            "📦 Category",
            options=category_options,
            key="sales_filter_category"
        )
    
    with filter_col4:
        payment_options = ['All'] + PAYMENT_STATUSES
        selected_payment = st.selectbox(
            "💳 Payment Status",
            options=payment_options,
            key="sales_filter_payment"
        )
    
    with filter_col5:
        # Date range filter
        valid_dates = sales_df[sales_df['order_time'].notna()]['order_time']
        if len(valid_dates) > 0:
            min_date = valid_dates.min().date()
            max_date = valid_dates.max().date()
        else:
            min_date = datetime.now().date() - timedelta(days=120)
            max_date = datetime.now().date()
        
        date_range = st.date_input(
            "📅 Date Range",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date,
            key="sales_filter_date"
        )
    
    # =========================================================================
    # APPLY FILTERS
    # =========================================================================
    filtered_sales = sales_df[sales_df['order_time'].notna()].copy()
    
    # Apply city filter
    if selected_city != 'All':
        filtered_sales = filtered_sales[filtered_sales['city_clean'] == selected_city]
    
    # Apply channel filter
    if selected_channel != 'All':
        filtered_sales = filtered_sales[filtered_sales['channel'] == selected_channel]
    
    # Apply category filter
    if selected_category != 'All':
        filtered_sales = filtered_sales[filtered_sales['category'] == selected_category]
    
    # Apply payment status filter
    if selected_payment != 'All':
        filtered_sales = filtered_sales[filtered_sales['payment_status'] == selected_payment]
    
    # Apply date range filter
    if isinstance(date_range, tuple) and len(date_range) == 2:
        start_date, end_date = date_range
        filtered_sales = filtered_sales[
            (filtered_sales['order_time'].dt.date >= start_date) &
            (filtered_sales['order_time'].dt.date <= end_date)
        ]
    
    # Show filter summary
    if len(filtered_sales) < len(sales_df[sales_df['order_time'].notna()]):
        active_filters = []
        if selected_city != 'All':
            active_filters.append(f"City: {selected_city}")
        if selected_channel != 'All':
            active_filters.append(f"Channel: {selected_channel}")
        if selected_category != 'All':
            active_filters.append(f"Category: {selected_category}")
        if selected_payment != 'All':
            active_filters.append(f"Payment: {selected_payment}")
        
        st.caption(f"🔍 Showing {len(filtered_sales):,} of {len(sales_df[sales_df['order_time'].notna()]):,} records | Filters: {', '.join(active_filters)}")
    
    render_divider_subtle()
    
    # =========================================================================
    # CHECK FOR EMPTY DATA
    # =========================================================================
    if len(filtered_sales) == 0:
        render_empty_state(
            "📊",
            "No Data Available",
            "No sales data matches the selected filters. Try adjusting your filter criteria."
        )
        return
    
    # =========================================================================
    # KPI SUMMARY ROW
    # =========================================================================
    render_sales_kpis(filtered_sales)
    
    st.markdown("")
    
    # =========================================================================
    # SUB-TABS FOR DIFFERENT ANALYSIS VIEWS
    # =========================================================================
    analysis_tabs = st.tabs([
        "📈 Trends",
        "📦 Categories",
        "🏙️ Geography",
        "📱 Channels",
        "💳 Payments",
        "🏆 Top Products"
    ])
    
    with analysis_tabs[0]:
        render_sales_trends(filtered_sales)
    
    with analysis_tabs[1]:
        render_category_analysis(filtered_sales, products_df)
    
    with analysis_tabs[2]:
        render_geographic_analysis(filtered_sales)
    
    with analysis_tabs[3]:
        render_channel_analysis(filtered_sales)
    
    with analysis_tabs[4]:
        render_payment_analysis(filtered_sales)
    
    with analysis_tabs[5]:
        render_top_products(filtered_sales, products_df)


def render_sales_kpis(filtered_sales):
    """
    Render the KPI summary row for sales analytics.
    
    Args:
        filtered_sales: Filtered sales DataFrame
    """
    # Calculate KPIs
    total_revenue = filtered_sales['revenue'].sum()
    total_orders = filtered_sales['order_id'].nunique()
    total_units = filtered_sales['qty'].sum()
    avg_order_value = total_revenue / total_orders if total_orders > 0 else 0
    avg_discount = filtered_sales['discount_pct'].mean()
    
    # Calculate period-over-period if possible
    if len(filtered_sales) > 0:
        date_range = (filtered_sales['order_time'].max() - filtered_sales['order_time'].min()).days
        daily_revenue = total_revenue / date_range if date_range > 0 else total_revenue
        daily_orders = total_orders / date_range if date_range > 0 else total_orders
    else:
        daily_revenue = 0
        daily_orders = 0
    
    # Paid vs Refunded
    paid_revenue = filtered_sales[filtered_sales['payment_status'] == 'Paid']['revenue'].sum()
    refunded_revenue = filtered_sales[filtered_sales['payment_status'] == 'Refunded']['revenue'].sum()
    
    # KPI Row
    kpis = [
        {
            "icon": "💰",
            "value": format_currency(total_revenue),
            "label": "Total Revenue",
            "type": "success"
        },
        {
            "icon": "🛒",
            "value": format_number(total_orders),
            "label": "Total Orders",
            "type": "primary"
        },
        {
            "icon": "📦",
            "value": format_number(total_units),
            "label": "Units Sold",
            "type": "accent"
        },
        {
            "icon": "💵",
            "value": format_currency(avg_order_value),
            "label": "Avg Order Value",
            "type": "secondary"
        },
        {
            "icon": "🏷️",
            "value": f"{avg_discount:.1f}%",
            "label": "Avg Discount",
            "type": "warning"
        },
        {
            "icon": "📊",
            "value": format_currency(daily_revenue),
            "label": "Daily Avg Revenue",
            "type": "primary"
        }
    ]
    
    render_kpi_row(kpis)


def render_sales_trends(filtered_sales):
    """
    Render time-series trend analysis for sales.
    
    Args:
        filtered_sales: Filtered sales DataFrame
    """
    st.markdown("#### 📈 Sales Trends Over Time")
    st.markdown("Analyze revenue and order patterns across different time periods.")
    
    st.markdown("")
    
    # Time granularity selection
    col1, col2 = st.columns([1, 4])
    
    with col1:
        time_granularity = st.selectbox(
            "Time Period",
            options=['Daily', 'Weekly', 'Monthly'],
            key="sales_trend_granularity"
        )
    
    # Aggregate data based on granularity
    if time_granularity == 'Daily':
        trend_data = filtered_sales.groupby(filtered_sales['order_time'].dt.date).agg({
            'revenue': 'sum',
            'order_id': 'nunique',
            'qty': 'sum'
        }).reset_index()
        trend_data.columns = ['period', 'revenue', 'orders', 'units']
        x_label = 'Date'
    
    elif time_granularity == 'Weekly':
        filtered_sales['week_start'] = filtered_sales['order_time'].dt.to_period('W').dt.start_time
        trend_data = filtered_sales.groupby('week_start').agg({
            'revenue': 'sum',
            'order_id': 'nunique',
            'qty': 'sum'
        }).reset_index()
        trend_data.columns = ['period', 'revenue', 'orders', 'units']
        x_label = 'Week Starting'
    
    else:  # Monthly
        trend_data = filtered_sales.groupby(filtered_sales['month']).agg({
            'revenue': 'sum',
            'order_id': 'nunique',
            'qty': 'sum'
        }).reset_index()
        trend_data.columns = ['period', 'revenue', 'orders', 'units']
        x_label = 'Month'
    
    # Sort by period
    trend_data = trend_data.sort_values('period')
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Revenue trend
        render_chart_title("Revenue Trend", "💰")
        
        fig = px.area(
            trend_data,
            x='period',
            y='revenue',
            color_discrete_sequence=['#6366f1']
        )
        fig.update_traces(
            fill='tozeroy',
            fillcolor='rgba(99, 102, 241, 0.2)',
            line=dict(width=2, color='#6366f1')
        )
        fig = apply_chart_style(fig, height=320, show_legend=False)
        fig.update_layout(
            xaxis_title=x_label,
            yaxis_title="Revenue (AED)",
            yaxis_tickformat=",.0f"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Orders trend
        render_chart_title("Orders Trend", "🛒")
        
        fig = px.bar(
            trend_data,
            x='period',
            y='orders',
            color_discrete_sequence=['#8b5cf6']
        )
        fig = apply_chart_style(fig, height=320, show_legend=False)
        fig.update_layout(
            xaxis_title=x_label,
            yaxis_title="Number of Orders",
            yaxis_tickformat=","
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Combined chart with dual axis
    st.markdown("")
    render_chart_title("Revenue & Orders Combined", "📊")
    
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    # Add revenue trace
    fig.add_trace(
        go.Scatter(
            x=trend_data['period'],
            y=trend_data['revenue'],
            name='Revenue',
            line=dict(color='#6366f1', width=3),
            fill='tozeroy',
            fillcolor='rgba(99, 102, 241, 0.1)'
        ),
        secondary_y=False
    )
    
    # Add orders trace
    fig.add_trace(
        go.Bar(
            x=trend_data['period'],
            y=trend_data['orders'],
            name='Orders',
            marker_color='rgba(139, 92, 246, 0.6)'
        ),
        secondary_y=True
    )
    
    fig = apply_chart_style(fig, height=350)
    fig.update_layout(
        xaxis_title=x_label,
        yaxis_title="Revenue (AED)",
        yaxis2_title="Orders",
        yaxis_tickformat=",.0f",
        yaxis2_tickformat=","
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Trend insights
    st.markdown("")
    
    if len(trend_data) >= 2:
        # Calculate trend
        first_half = trend_data.head(len(trend_data)//2)['revenue'].mean()
        second_half = trend_data.tail(len(trend_data)//2)['revenue'].mean()
        
        if first_half > 0:
            trend_pct = ((second_half - first_half) / first_half) * 100
            
            if trend_pct > 10:
                render_insight_box(
                    "📈",
                    "Upward Trend",
                    f"Revenue shows a **{trend_pct:.1f}%** increase in the latter period. "
                    f"Sales momentum is positive.",
                    "success"
                )
            elif trend_pct < -10:
                render_insight_box(
                    "📉",
                    "Downward Trend",
                    f"Revenue shows a **{abs(trend_pct):.1f}%** decrease in the latter period. "
                    f"Consider investigating the cause or launching promotions.",
                    "warning"
                )
            else:
                render_insight_box(
                    "➡️",
                    "Stable Trend",
                    f"Revenue is relatively stable with **{trend_pct:.1f}%** change. "
                    f"Business performance is consistent.",
                    "primary"
                )


def render_category_analysis(filtered_sales, products_df):
    """
    Render category performance analysis.
    
    Args:
        filtered_sales: Filtered sales DataFrame
        products_df: Products DataFrame
    """
    st.markdown("#### 📦 Category Performance")
    st.markdown("Analyze sales performance across product categories.")
    
    st.markdown("")
    
    # Calculate category metrics
    category_metrics = filtered_sales.groupby('category').agg({
        'revenue': 'sum',
        'order_id': 'nunique',
        'qty': 'sum',
        'discount_pct': 'mean',
        'selling_price_aed': 'mean'
    }).reset_index()
    
    category_metrics.columns = ['category', 'revenue', 'orders', 'units', 'avg_discount', 'avg_price']
    category_metrics = category_metrics.sort_values('revenue', ascending=False)
    
    # Add percentage
    category_metrics['revenue_pct'] = (category_metrics['revenue'] / category_metrics['revenue'].sum() * 100)
    
    # Charts row
    col1, col2 = st.columns(2)
    
    with col1:
        # Revenue by category
        render_chart_title("Revenue by Category", "💰")
        
        fig = px.bar(
            category_metrics,
            x='category',
            y='revenue',
            color='revenue',
            color_continuous_scale=['#312e81', '#6366f1', '#a5b4fc'],
            text=category_metrics['revenue'].apply(lambda x: format_currency(x))
        )
        fig = apply_chart_style(fig, height=350, show_legend=False)
        fig.update_traces(textposition='outside')
        fig.update_layout(
            xaxis_title="",
            yaxis_title="Revenue (AED)",
            coloraxis_showscale=False,
            yaxis_tickformat=",.0f"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Revenue share pie
        render_chart_title("Revenue Share", "📊")
        
        fig = px.pie(
            category_metrics,
            values='revenue',
            names='category',
            color_discrete_sequence=get_chart_colors(),
            hole=0.4
        )
        fig = apply_chart_style(fig, height=350)
        fig.update_traces(
            textposition='outside',
            textinfo='label+percent'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Second row
    col3, col4 = st.columns(2)
    
    with col3:
        # Orders by category
        render_chart_title("Orders by Category", "🛒")
        
        fig = px.bar(
            category_metrics.sort_values('orders', ascending=True),
            x='orders',
            y='category',
            orientation='h',
            color='category',
            color_discrete_sequence=get_chart_colors()
        )
        fig = apply_chart_style(fig, height=320, show_legend=False)
        fig.update_layout(
            xaxis_title="Number of Orders",
            yaxis_title=""
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col4:
        # Average order value by category
        render_chart_title("Avg Order Value by Category", "💵")
        
        category_metrics['aov'] = category_metrics['revenue'] / category_metrics['orders']
        
        fig = px.bar(
            category_metrics.sort_values('aov', ascending=True),
            x='aov',
            y='category',
            orientation='h',
            color='aov',
            color_continuous_scale=['#10b981', '#84cc16', '#f59e0b']
        )
        fig = apply_chart_style(fig, height=320, show_legend=False)
        fig.update_layout(
            xaxis_title="Average Order Value (AED)",
            yaxis_title="",
            coloraxis_showscale=False
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Category metrics table
    st.markdown("")
    st.markdown("##### 📋 Category Metrics Summary")
    
    display_df = category_metrics[['category', 'revenue', 'orders', 'units', 'avg_discount', 'revenue_pct']].copy()
    display_df['revenue'] = display_df['revenue'].apply(lambda x: format_currency(x))
    display_df['orders'] = display_df['orders'].apply(lambda x: format_number(x))
    display_df['units'] = display_df['units'].apply(lambda x: format_number(x))
    display_df['avg_discount'] = display_df['avg_discount'].apply(lambda x: f"{x:.1f}%")
    display_df['revenue_pct'] = display_df['revenue_pct'].apply(lambda x: f"{x:.1f}%")
    display_df.columns = ['Category', 'Revenue', 'Orders', 'Units Sold', 'Avg Discount', 'Revenue Share']
    
    st.dataframe(display_df, use_container_width=True, hide_index=True)
    
    # Insights
    st.markdown("")
    
    top_category = category_metrics.iloc[0]
    bottom_category = category_metrics.iloc[-1]
    
    col1, col2 = st.columns(2)
    
    with col1:
        render_insight_box(
            "🏆",
            f"Top Performer: {top_category['category']}",
            f"Generates **{format_currency(top_category['revenue'])}** ({top_category['revenue_pct']:.1f}% of total) "
            f"with {format_number(top_category['orders'])} orders.",
            "success"
        )
    
    with col2:
        render_insight_box(
            "📊",
            f"Growth Opportunity: {bottom_category['category']}",
            f"Currently at **{format_currency(bottom_category['revenue'])}** ({bottom_category['revenue_pct']:.1f}%). "
            f"Consider promotional campaigns to boost performance.",
            "primary"
        )


def render_geographic_analysis(filtered_sales):
    """
    Render geographic (city-based) analysis.
    
    Args:
        filtered_sales: Filtered sales DataFrame
    """
    st.markdown("#### 🏙️ Geographic Analysis")
    st.markdown("Compare sales performance across UAE cities.")
    
    st.markdown("")
    
    # Calculate city metrics
    city_metrics = filtered_sales.groupby('city_clean').agg({
        'revenue': 'sum',
        'order_id': 'nunique',
        'qty': 'sum',
        'discount_pct': 'mean',
        'selling_price_aed': 'mean'
    }).reset_index()
    
    city_metrics.columns = ['city', 'revenue', 'orders', 'units', 'avg_discount', 'avg_price']
    city_metrics = city_metrics.sort_values('revenue', ascending=False)
    city_metrics['aov'] = city_metrics['revenue'] / city_metrics['orders']
    city_metrics['revenue_pct'] = (city_metrics['revenue'] / city_metrics['revenue'].sum() * 100)
    
    # KPI comparison row
    st.markdown("##### 📊 City Comparison")
    
    cols = st.columns(len(city_metrics))
    
    city_colors = {'Dubai': '#6366f1', 'Abu Dhabi': '#10b981', 'Sharjah': '#f59e0b'}
    
    for col, (_, row) in zip(cols, city_metrics.iterrows()):
        with col:
            color = city_colors.get(row['city'], '#6366f1')
            st.markdown(f'''
            <div style="background: rgba(255,255,255,0.03); border: 1px solid {color}40;
                        border-radius: 12px; padding: 16px; text-align: center;">
                <div style="font-size: 1.5rem; margin-bottom: 8px;">🏙️</div>
                <div style="font-size: 1.1rem; font-weight: 600; color: {color}; margin-bottom: 12px;">{row['city']}</div>
                <div style="font-size: 0.8rem; color: #71717a;">Revenue</div>
                <div style="font-size: 1.2rem; font-weight: 700; color: white;">{format_currency(row['revenue'])}</div>
                <div style="font-size: 0.75rem; color: #a1a1aa; margin-top: 8px;">{row['revenue_pct']:.1f}% of total</div>
            </div>
            ''', unsafe_allow_html=True)
    
    st.markdown("")
    
    # Charts row
    col1, col2 = st.columns(2)
    
    with col1:
        # Revenue comparison
        render_chart_title("Revenue by City", "💰")
        
        fig = px.bar(
            city_metrics,
            x='city',
            y='revenue',
            color='city',
            color_discrete_map=city_colors,
            text=city_metrics['revenue'].apply(lambda x: format_currency(x))
        )
        fig = apply_chart_style(fig, height=320, show_legend=False)
        fig.update_traces(textposition='outside')
        fig.update_layout(
            xaxis_title="",
            yaxis_title="Revenue (AED)",
            yaxis_tickformat=",.0f"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Orders comparison
        render_chart_title("Orders by City", "🛒")
        
        fig = px.bar(
            city_metrics,
            x='city',
            y='orders',
            color='city',
            color_discrete_map=city_colors,
            text=city_metrics['orders'].apply(lambda x: format_number(x))
        )
        fig = apply_chart_style(fig, height=320, show_legend=False)
        fig.update_traces(textposition='outside')
        fig.update_layout(
            xaxis_title="",
            yaxis_title="Number of Orders"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # City-Category heatmap
    st.markdown("")
    render_chart_title("Revenue Heatmap: City × Category", "🗺️")
    
    city_category = filtered_sales.groupby(['city_clean', 'category'])['revenue'].sum().reset_index()
    city_category_pivot = city_category.pivot(index='category', columns='city_clean', values='revenue').fillna(0)
    
    fig = px.imshow(
        city_category_pivot,
        labels=dict(x="City", y="Category", color="Revenue (AED)"),
        color_continuous_scale='Purples',
        aspect='auto'
    )
    fig = apply_chart_style(fig, height=350)
    fig.update_layout(
        xaxis_title="",
        yaxis_title=""
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # City metrics table
    st.markdown("")
    st.markdown("##### 📋 City Metrics Summary")
    
    display_df = city_metrics[['city', 'revenue', 'orders', 'units', 'aov', 'avg_discount']].copy()
    display_df['revenue'] = display_df['revenue'].apply(lambda x: format_currency(x))
    display_df['orders'] = display_df['orders'].apply(lambda x: format_number(x))
    display_df['units'] = display_df['units'].apply(lambda x: format_number(x))
    display_df['aov'] = display_df['aov'].apply(lambda x: format_currency(x))
    display_df['avg_discount'] = display_df['avg_discount'].apply(lambda x: f"{x:.1f}%")
    display_df.columns = ['City', 'Revenue', 'Orders', 'Units', 'Avg Order Value', 'Avg Discount']
    
    st.dataframe(display_df, use_container_width=True, hide_index=True)
    
    # Insight
    if len(city_metrics) > 1:
        top_city = city_metrics.iloc[0]
        render_insight_box(
            "🏆",
            f"Market Leader: {top_city['city']}",
            f"**{top_city['city']}** dominates with **{top_city['revenue_pct']:.1f}%** market share. "
            f"Average order value is **{format_currency(top_city['aov'])}** with "
            f"**{top_city['avg_discount']:.1f}%** average discount.",
            "success"
        )


def render_channel_analysis(filtered_sales):
    """
    Render channel (App, Web, Marketplace) analysis.
    
    Args:
        filtered_sales: Filtered sales DataFrame
    """
    st.markdown("#### 📱 Channel Performance")
    st.markdown("Compare sales performance across digital channels.")
    
    st.markdown("")
    
    # Calculate channel metrics
    channel_metrics = filtered_sales.groupby('channel').agg({
        'revenue': 'sum',
        'order_id': 'nunique',
        'qty': 'sum',
        'discount_pct': 'mean',
        'return_flag': 'mean'
    }).reset_index()
    
    channel_metrics.columns = ['channel', 'revenue', 'orders', 'units', 'avg_discount', 'return_rate']
    channel_metrics = channel_metrics.sort_values('revenue', ascending=False)
    channel_metrics['aov'] = channel_metrics['revenue'] / channel_metrics['orders']
    channel_metrics['revenue_pct'] = (channel_metrics['revenue'] / channel_metrics['revenue'].sum() * 100)
    channel_metrics['return_rate'] = channel_metrics['return_rate'] * 100
    
    # Channel icons
    channel_icons = {'App': '📱', 'Web': '🌐', 'Marketplace': '🏪'}
    channel_colors = {'App': '#6366f1', 'Web': '#10b981', 'Marketplace': '#f59e0b'}
    
    # KPI cards for each channel
    cols = st.columns(len(channel_metrics))
    
    for col, (_, row) in zip(cols, channel_metrics.iterrows()):
        with col:
            icon = channel_icons.get(row['channel'], '📊')
            color = channel_colors.get(row['channel'], '#6366f1')
            
            st.markdown(f'''
            <div style="background: rgba(255,255,255,0.03); border: 1px solid {color}40;
                        border-radius: 12px; padding: 20px; text-align: center;">
                <div style="font-size: 2rem; margin-bottom: 8px;">{icon}</div>
                <div style="font-size: 1.2rem; font-weight: 600; color: {color}; margin-bottom: 16px;">{row['channel']}</div>
                
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; text-align: left;">
                    <div>
                        <div style="font-size: 0.7rem; color: #71717a;">Revenue</div>
                        <div style="font-size: 0.9rem; font-weight: 600; color: white;">{format_currency(row['revenue'])}</div>
                    </div>
                    <div>
                        <div style="font-size: 0.7rem; color: #71717a;">Orders</div>
                        <div style="font-size: 0.9rem; font-weight: 600; color: white;">{format_number(row['orders'])}</div>
                    </div>
                    <div>
                        <div style="font-size: 0.7rem; color: #71717a;">AOV</div>
                        <div style="font-size: 0.9rem; font-weight: 600; color: white;">{format_currency(row['aov'])}</div>
                    </div>
                    <div>
                        <div style="font-size: 0.7rem; color: #71717a;">Return Rate</div>
                        <div style="font-size: 0.9rem; font-weight: 600; color: white;">{row['return_rate']:.1f}%</div>
                    </div>
                </div>
            </div>
            ''', unsafe_allow_html=True)
    
    st.markdown("")
    
    # Charts row
    col1, col2 = st.columns(2)
    
    with col1:
        # Revenue share donut
        render_chart_title("Revenue Share by Channel", "📊")
        
        fig = px.pie(
            channel_metrics,
            values='revenue',
            names='channel',
            color='channel',
            color_discrete_map=channel_colors,
            hole=0.5
        )
        fig = apply_chart_style(fig, height=320)
        fig.update_traces(
            textposition='outside',
            textinfo='label+percent'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Channel comparison bar
        render_chart_title("Average Order Value by Channel", "💵")
        
        fig = px.bar(
            channel_metrics,
            x='channel',
            y='aov',
            color='channel',
            color_discrete_map=channel_colors,
            text=channel_metrics['aov'].apply(lambda x: format_currency(x))
        )
        fig = apply_chart_style(fig, height=320, show_legend=False)
        fig.update_traces(textposition='outside')
        fig.update_layout(
            xaxis_title="",
            yaxis_title="Average Order Value (AED)"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Channel trend over time
    st.markdown("")
    render_chart_title("Channel Revenue Trend Over Time", "📈")
    
    channel_trend = filtered_sales.groupby([filtered_sales['order_time'].dt.to_period('W').dt.start_time, 'channel']).agg({
        'revenue': 'sum'
    }).reset_index()
    channel_trend.columns = ['week', 'channel', 'revenue']
    
    fig = px.line(
        channel_trend,
        x='week',
        y='revenue',
        color='channel',
        color_discrete_map=channel_colors,
        markers=True
    )
    fig = apply_chart_style(fig, height=320)
    fig.update_layout(
        xaxis_title="Week",
        yaxis_title="Revenue (AED)",
        yaxis_tickformat=",.0f"
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Insight
    best_channel = channel_metrics.iloc[0]
    highest_aov_channel = channel_metrics.loc[channel_metrics['aov'].idxmax()]
    
    col1, col2 = st.columns(2)
    
    with col1:
        render_insight_box(
            "🏆",
            f"Top Channel: {best_channel['channel']}",
            f"**{best_channel['channel']}** leads with **{best_channel['revenue_pct']:.1f}%** of total revenue "
            f"and **{format_number(best_channel['orders'])}** orders.",
            "success"
        )
    
    with col2:
        render_insight_box(
            "💎",
            f"Highest AOV: {highest_aov_channel['channel']}",
            f"**{highest_aov_channel['channel']}** has the highest average order value at "
            f"**{format_currency(highest_aov_channel['aov'])}** per order.",
            "accent"
        )


def render_payment_analysis(filtered_sales):
    """
    Render payment status analysis.
    
    Args:
        filtered_sales: Filtered sales DataFrame
    """
    st.markdown("#### 💳 Payment Status Analysis")
    st.markdown("Analyze payment outcomes and identify issues.")
    
    st.markdown("")
    
    # Calculate payment metrics
    payment_metrics = filtered_sales.groupby('payment_status').agg({
        'revenue': 'sum',
        'order_id': 'nunique',
        'qty': 'sum'
    }).reset_index()
    
    payment_metrics.columns = ['status', 'revenue', 'orders', 'units']
    payment_metrics['revenue_pct'] = (payment_metrics['revenue'] / payment_metrics['revenue'].sum() * 100)
    payment_metrics['orders_pct'] = (payment_metrics['orders'] / payment_metrics['orders'].sum() * 100)
    
    # Status colors
    status_colors = {'Paid': '#10b981', 'Failed': '#ef4444', 'Refunded': '#f59e0b'}
    status_icons = {'Paid': '✅', 'Failed': '❌', 'Refunded': '↩️'}
    
    # KPI cards
    cols = st.columns(len(payment_metrics))
    
    for col, (_, row) in zip(cols, payment_metrics.iterrows()):
        with col:
            icon = status_icons.get(row['status'], '📊')
            color = status_colors.get(row['status'], '#6366f1')
            
            st.markdown(f'''
            <div style="background: rgba(255,255,255,0.03); border: 1px solid {color}40;
                        border-radius: 12px; padding: 20px; text-align: center;">
                <div style="font-size: 2rem; margin-bottom: 8px;">{icon}</div>
                <div style="font-size: 1.1rem; font-weight: 600; color: {color}; margin-bottom: 12px;">{row['status']}</div>
                <div style="font-size: 1.4rem; font-weight: 700; color: white;">{format_currency(row['revenue'])}</div>
                <div style="font-size: 0.85rem; color: #a1a1aa; margin-top: 4px;">{format_number(row['orders'])} orders ({row['orders_pct']:.1f}%)</div>
            </div>
            ''', unsafe_allow_html=True)
    
    st.markdown("")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Payment status pie
        render_chart_title("Revenue by Payment Status", "📊")
        
        fig = px.pie(
            payment_metrics,
            values='revenue',
            names='status',
            color='status',
            color_discrete_map=status_colors,
            hole=0.4
        )
        fig = apply_chart_style(fig, height=320)
        fig.update_traces(
            textposition='inside',
            textinfo='label+percent'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Orders by status bar
        render_chart_title("Orders by Payment Status", "🛒")
        
        fig = px.bar(
            payment_metrics,
            x='status',
            y='orders',
            color='status',
            color_discrete_map=status_colors,
            text=payment_metrics['orders'].apply(lambda x: format_number(x))
        )
        fig = apply_chart_style(fig, height=320, show_legend=False)
        fig.update_traces(textposition='outside')
        fig.update_layout(
            xaxis_title="",
            yaxis_title="Number of Orders"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Failed/Refunded analysis
    failed_orders = filtered_sales[filtered_sales['payment_status'] == 'Failed']
    refunded_orders = filtered_sales[filtered_sales['payment_status'] == 'Refunded']
    
    if len(failed_orders) > 0 or len(refunded_orders) > 0:
        st.markdown("")
        st.markdown("##### ⚠️ Problem Orders Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if len(failed_orders) > 0:
                st.markdown("**Failed Orders by Category:**")
                failed_by_cat = failed_orders.groupby('category').size().reset_index(name='count')
                failed_by_cat = failed_by_cat.sort_values('count', ascending=False)
                
                fig = px.bar(
                    failed_by_cat,
                    x='count',
                    y='category',
                    orientation='h',
                    color_discrete_sequence=['#ef4444']
                )
                fig = apply_chart_style(fig, height=250, show_legend=False)
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            if len(refunded_orders) > 0:
                st.markdown("**Refunded Orders by Category:**")
                refunded_by_cat = refunded_orders.groupby('category').size().reset_index(name='count')
                refunded_by_cat = refunded_by_cat.sort_values('count', ascending=False)
                
                fig = px.bar(
                    refunded_by_cat,
                    x='count',
                    y='category',
                    orientation='h',
                    color_discrete_sequence=['#f59e0b']
                )
                fig = apply_chart_style(fig, height=250, show_legend=False)
                st.plotly_chart(fig, use_container_width=True)
    
    # Insights
    st.markdown("")
    
    paid_row = payment_metrics[payment_metrics['status'] == 'Paid'].iloc[0] if 'Paid' in payment_metrics['status'].values else None
    failed_row = payment_metrics[payment_metrics['status'] == 'Failed'].iloc[0] if 'Failed' in payment_metrics['status'].values else None
    refunded_row = payment_metrics[payment_metrics['status'] == 'Refunded'].iloc[0] if 'Refunded' in payment_metrics['status'].values else None
    
    if paid_row is not None:
        success_rate = paid_row['orders_pct']
        
        if success_rate >= 90:
            render_insight_box(
                "✅",
                "Excellent Payment Success Rate",
                f"**{success_rate:.1f}%** of orders are successfully paid. "
                f"Payment processing is performing well.",
                "success"
            )
        elif success_rate >= 80:
            render_insight_box(
                "⚠️",
                "Payment Issues Detected",
                f"**{100 - success_rate:.1f}%** of orders have failed or been refunded. "
                f"Consider investigating payment gateway issues or product quality.",
                "warning"
            )
        else:
            render_insight_box(
                "🔴",
                "Critical Payment Issues",
                f"Only **{success_rate:.1f}%** of orders are successfully paid. "
                f"Immediate investigation of payment processing is recommended.",
                "danger"
            )


def render_top_products(filtered_sales, products_df):
    """
    Render top products analysis.
    
    Args:
        filtered_sales: Filtered sales DataFrame
        products_df: Products DataFrame
    """
    st.markdown("#### 🏆 Top Products Analysis")
    st.markdown("Identify best-selling and highest revenue products.")
    
    st.markdown("")
    
    # Selection for top N
    col1, col2 = st.columns([1, 4])
    
    with col1:
        top_n = st.selectbox(
            "Show Top",
            options=[10, 20, 50],
            key="top_products_n"
        )
    
    # Calculate product metrics
    product_metrics = filtered_sales.groupby(['product_id', 'category', 'brand']).agg({
        'revenue': 'sum',
        'order_id': 'nunique',
        'qty': 'sum',
        'selling_price_aed': 'mean'
    }).reset_index()
    
    product_metrics.columns = ['product_id', 'category', 'brand', 'revenue', 'orders', 'units', 'avg_price']
    
    # Top by revenue
    top_by_revenue = product_metrics.nlargest(top_n, 'revenue')
    
    # Top by units
    top_by_units = product_metrics.nlargest(top_n, 'units')
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        render_chart_title(f"Top {top_n} Products by Revenue", "💰")
        
        fig = px.bar(
            top_by_revenue.sort_values('revenue', ascending=True).tail(15),
            x='revenue',
            y='product_id',
            orientation='h',
            color='category',
            color_discrete_sequence=get_chart_colors()
        )
        fig = apply_chart_style(fig, height=400)
        fig.update_layout(
            xaxis_title="Revenue (AED)",
            yaxis_title="",
            yaxis_tickfont=dict(size=10)
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        render_chart_title(f"Top {top_n} Products by Units Sold", "📦")
        
        fig = px.bar(
            top_by_units.sort_values('units', ascending=True).tail(15),
            x='units',
            y='product_id',
            orientation='h',
            color='category',
            color_discrete_sequence=get_chart_colors()
        )
        fig = apply_chart_style(fig, height=400)
        fig.update_layout(
            xaxis_title="Units Sold",
            yaxis_title="",
            yaxis_tickfont=dict(size=10)
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Top products table
    st.markdown("")
    st.markdown(f"##### 📋 Top {top_n} Products Details")
    
    display_df = top_by_revenue[['product_id', 'category', 'brand', 'revenue', 'orders', 'units', 'avg_price']].copy()
    display_df['revenue'] = display_df['revenue'].apply(lambda x: format_currency(x))
    display_df['orders'] = display_df['orders'].apply(lambda x: format_number(x))
    display_df['units'] = display_df['units'].apply(lambda x: format_number(x))
    display_df['avg_price'] = display_df['avg_price'].apply(lambda x: format_currency(x))
    display_df.columns = ['Product ID', 'Category', 'Brand', 'Revenue', 'Orders', 'Units', 'Avg Price']
    
    st.dataframe(display_df, use_container_width=True, hide_index=True)
    
    # Brand analysis
    st.markdown("")
    render_chart_title("Top 10 Brands by Revenue", "🏷️")
    
    brand_metrics = filtered_sales.groupby('brand').agg({
        'revenue': 'sum',
        'order_id': 'nunique'
    }).reset_index()
    brand_metrics.columns = ['brand', 'revenue', 'orders']
    brand_metrics = brand_metrics.nlargest(10, 'revenue')
    
    fig = px.bar(
        brand_metrics,
        x='brand',
        y='revenue',
        color='revenue',
        color_continuous_scale=['#312e81', '#6366f1', '#a5b4fc'],
        text=brand_metrics['revenue'].apply(lambda x: format_currency(x))
    )
    fig = apply_chart_style(fig, height=320, show_legend=False)
    fig.update_traces(textposition='outside')
    fig.update_layout(
        xaxis_title="",
        yaxis_title="Revenue (AED)",
        coloraxis_showscale=False
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Insight
    top_product = top_by_revenue.iloc[0]
    top_brand = brand_metrics.iloc[0]
    
    render_insight_box(
        "🏆",
        "Best Performers",
        f"**{top_product['product_id']}** ({top_product['brand']}) is the top product with "
        f"**{format_currency(top_product['revenue'])}** revenue. "
        f"**{top_brand['brand']}** is the leading brand overall.",
        "success"
    )

# =============================================================================
# INVENTORY HEALTH TAB
# =============================================================================
# This module provides comprehensive inventory analysis including stock levels,
# health monitoring, reorder alerts, and demand forecasting.
# =============================================================================

def render_inventory_analysis(inventory_df, sales_df, products_df, stores_df):
    """
    Render the Inventory Health tab with comprehensive stock analysis.
    
    This tab provides:
        1. Stock Health KPIs
        2. Stock Status Distribution
        3. Low Stock Alerts
        4. Inventory by Location
        5. Stock Trends Over Time
        6. Reorder Recommendations
        7. Demand Forecasting
    
    Args:
        inventory_df: Inventory DataFrame
        sales_df: Sales DataFrame for demand analysis
        products_df: Products DataFrame
        stores_df: Stores DataFrame
    """
    render_section_header(
        "📦",
        "Inventory Health Monitor",
        "Real-time stock levels, alerts, and reorder recommendations"
    )
    
    # =========================================================================
    # SECTION FILTERS
    # =========================================================================
    st.markdown("##### 🎛️ Filters")
    
    filter_col1, filter_col2, filter_col3, filter_col4 = st.columns(4)
    
    with filter_col1:
        city_options = ['All'] + STANDARD_CITIES
        selected_city = st.selectbox(
            "🏙️ City",
            options=city_options,
            key="inventory_filter_city"
        )
    
    with filter_col2:
        channel_options = ['All'] + CHANNELS
        selected_channel = st.selectbox(
            "📱 Channel",
            options=channel_options,
            key="inventory_filter_channel"
        )
    
    with filter_col3:
        category_options = ['All'] + CATEGORIES
        selected_category = st.selectbox(
            "📦 Category",
            options=category_options,
            key="inventory_filter_category"
        )
    
    with filter_col4:
        stock_status_options = ['All', 'Healthy', 'Low', 'Critical']
        selected_status = st.selectbox(
            "📊 Stock Status",
            options=stock_status_options,
            key="inventory_filter_status"
        )
    
    # =========================================================================
    # APPLY FILTERS
    # =========================================================================
    # Get latest snapshot for current analysis
    latest_date = inventory_df['snapshot_date'].max()
    filtered_inventory = inventory_df[inventory_df['snapshot_date'] == latest_date].copy()
    
    # Apply city filter
    if selected_city != 'All':
        filtered_inventory = filtered_inventory[filtered_inventory['city_clean'] == selected_city]
    
    # Apply channel filter
    if selected_channel != 'All':
        filtered_inventory = filtered_inventory[filtered_inventory['channel'] == selected_channel]
    
    # Apply category filter
    if selected_category != 'All':
        filtered_inventory = filtered_inventory[filtered_inventory['category'] == selected_category]
    
    # Apply stock status filter
    if selected_status != 'All':
        filtered_inventory = filtered_inventory[filtered_inventory['stock_status'] == selected_status]
    
    # Show filter summary
    total_inventory_records = len(inventory_df[inventory_df['snapshot_date'] == latest_date])
    if len(filtered_inventory) < total_inventory_records:
        st.caption(f"🔍 Showing {len(filtered_inventory):,} of {total_inventory_records:,} inventory records (Latest: {latest_date.strftime('%Y-%m-%d')})")
    else:
        st.caption(f"📅 Showing latest snapshot: {latest_date.strftime('%Y-%m-%d')}")
    
    render_divider_subtle()
    
    # =========================================================================
    # CHECK FOR EMPTY DATA
    # =========================================================================
    if len(filtered_inventory) == 0:
        render_empty_state(
            "📦",
            "No Inventory Data",
            "No inventory records match the selected filters. Try adjusting your criteria."
        )
        return
    
    # =========================================================================
    # INVENTORY KPIs
    # =========================================================================
    render_inventory_kpis(filtered_inventory, inventory_df)
    
    st.markdown("")
    
    # =========================================================================
    # SUB-TABS FOR DIFFERENT VIEWS
    # =========================================================================
    inventory_tabs = st.tabs([
        "📊 Overview",
        "⚠️ Stock Alerts",
        "🏙️ By Location",
        "📈 Trends",
        "🔄 Reorder Analysis",
        "🔮 Demand Forecast"
    ])
    
    with inventory_tabs[0]:
        render_inventory_overview(filtered_inventory, inventory_df)
    
    with inventory_tabs[1]:
        render_stock_alerts(filtered_inventory, sales_df)
    
    with inventory_tabs[2]:
        render_inventory_by_location(filtered_inventory)
    
    with inventory_tabs[3]:
        render_inventory_trends(inventory_df, selected_city, selected_category)
    
    with inventory_tabs[4]:
        render_reorder_analysis(filtered_inventory, sales_df)
    
    with inventory_tabs[5]:
        render_demand_forecast(inventory_df, sales_df, selected_category)


def render_inventory_kpis(filtered_inventory, full_inventory_df):
    """
    Render KPI summary row for inventory health.
    
    Args:
        filtered_inventory: Filtered inventory DataFrame (latest snapshot)
        full_inventory_df: Full inventory DataFrame for trend comparison
    """
    # Calculate KPIs
    total_stock = filtered_inventory['stock_on_hand'].sum()
    total_skus = filtered_inventory['product_id'].nunique()
    
    # Stock status counts
    healthy_count = len(filtered_inventory[filtered_inventory['stock_status'] == 'Healthy'])
    low_count = len(filtered_inventory[filtered_inventory['stock_status'] == 'Low'])
    critical_count = len(filtered_inventory[filtered_inventory['stock_status'] == 'Critical'])
    
    # Stock health percentage
    total_items = len(filtered_inventory)
    health_pct = (healthy_count / total_items * 100) if total_items > 0 else 0
    
    # Average lead time
    avg_lead_time = filtered_inventory['lead_time_days'].mean()
    
    # Data quality indicators
    negative_stock_count = (filtered_inventory['stock_on_hand'] < 0).sum()
    extreme_stock_count = (filtered_inventory['stock_on_hand'] > 9000).sum()
    
    # Determine KPI colors based on thresholds
    if health_pct >= 80:
        health_type = "success"
    elif health_pct >= 60:
        health_type = "warning"
    else:
        health_type = "danger"
    
    if critical_count > 100:
        critical_type = "danger"
    elif critical_count > 50:
        critical_type = "warning"
    else:
        critical_type = "success"
    
    # Render KPIs
    kpis = [
        {
            "icon": "📦",
            "value": format_number(total_stock),
            "label": "Total Stock Units",
            "type": "primary"
        },
        {
            "icon": "🏷️",
            "value": format_number(total_skus),
            "label": "Active SKUs",
            "type": "secondary"
        },
        {
            "icon": "✅",
            "value": f"{health_pct:.1f}%",
            "label": "Stock Health",
            "type": health_type
        },
        {
            "icon": "⚠️",
            "value": str(low_count),
            "label": "Low Stock Items",
            "type": "warning"
        },
        {
            "icon": "🔴",
            "value": str(critical_count),
            "label": "Critical Items",
            "type": critical_type
        },
        {
            "icon": "🚚",
            "value": f"{avg_lead_time:.1f} days",
            "label": "Avg Lead Time",
            "type": "primary"
        }
    ]
    
    render_kpi_row(kpis)


def render_inventory_overview(filtered_inventory, full_inventory_df):
    """
    Render inventory overview with status distribution and category breakdown.
    
    Args:
        filtered_inventory: Filtered inventory (latest snapshot)
        full_inventory_df: Full inventory DataFrame
    """
    st.markdown("#### 📊 Inventory Overview")
    st.markdown("Current stock status distribution and category breakdown.")
    
    st.markdown("")
    
    # Charts row
    col1, col2 = st.columns(2)
    
    with col1:
        # Stock status distribution
        render_chart_title("Stock Status Distribution", "📊")
        
        status_counts = filtered_inventory['stock_status'].value_counts().reset_index()
        status_counts.columns = ['status', 'count']
        
        # Define colors
        status_colors = {'Healthy': '#10b981', 'Low': '#f59e0b', 'Critical': '#ef4444'}
        
        fig = px.pie(
            status_counts,
            values='count',
            names='status',
            color='status',
            color_discrete_map=status_colors,
            hole=0.4
        )
        fig = apply_chart_style(fig, height=320)
        fig.update_traces(
            textposition='inside',
            textinfo='label+percent+value'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Stock by category
        render_chart_title("Stock Units by Category", "📦")
        
        category_stock = filtered_inventory.groupby('category')['stock_on_hand'].sum().reset_index()
        category_stock = category_stock.sort_values('stock_on_hand', ascending=True)
        
        fig = px.bar(
            category_stock,
            x='stock_on_hand',
            y='category',
            orientation='h',
            color='category',
            color_discrete_sequence=get_chart_colors()
        )
        fig = apply_chart_style(fig, height=320, show_legend=False)
        fig.update_layout(
            xaxis_title="Stock Units",
            yaxis_title=""
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Second row
    col3, col4 = st.columns(2)
    
    with col3:
        # Status by category heatmap
        render_chart_title("Stock Status by Category", "🗺️")
        
        status_by_cat = filtered_inventory.groupby(['category', 'stock_status']).size().reset_index(name='count')
        status_pivot = status_by_cat.pivot(index='category', columns='stock_status', values='count').fillna(0)
        
        # Ensure all status columns exist
        for status in ['Healthy', 'Low', 'Critical']:
            if status not in status_pivot.columns:
                status_pivot[status] = 0
        
        status_pivot = status_pivot[['Healthy', 'Low', 'Critical']]
        
        fig = px.imshow(
            status_pivot,
            labels=dict(x="Stock Status", y="Category", color="Count"),
            color_continuous_scale=['#1a1a2e', '#f59e0b', '#ef4444'],
            aspect='auto'
        )
        fig = apply_chart_style(fig, height=300)
        st.plotly_chart(fig, use_container_width=True)
    
    with col4:
        # Lead time distribution
        render_chart_title("Lead Time Distribution", "🚚")
        
        fig = px.histogram(
            filtered_inventory,
            x='lead_time_days',
            nbins=14,
            color_discrete_sequence=['#6366f1']
        )
        fig = apply_chart_style(fig, height=300, show_legend=False)
        fig.update_layout(
            xaxis_title="Lead Time (Days)",
            yaxis_title="Number of Items"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Stock value by category (if we have price data)
    st.markdown("")
    render_chart_title("Stock Distribution Summary", "📋")
    
    # Summary table
    summary_df = filtered_inventory.groupby('category').agg({
        'stock_on_hand': ['sum', 'mean', 'min', 'max'],
        'product_id': 'nunique',
        'reorder_point': 'mean',
        'lead_time_days': 'mean'
    }).reset_index()
    
    summary_df.columns = ['Category', 'Total Stock', 'Avg Stock', 'Min Stock', 'Max Stock', 
                          'SKU Count', 'Avg Reorder Point', 'Avg Lead Time']
    
    # Format columns
    summary_df['Total Stock'] = summary_df['Total Stock'].apply(lambda x: format_number(x))
    summary_df['Avg Stock'] = summary_df['Avg Stock'].apply(lambda x: f"{x:.0f}")
    summary_df['Min Stock'] = summary_df['Min Stock'].apply(lambda x: f"{x:.0f}")
    summary_df['Max Stock'] = summary_df['Max Stock'].apply(lambda x: f"{x:.0f}")
    summary_df['Avg Reorder Point'] = summary_df['Avg Reorder Point'].apply(lambda x: f"{x:.0f}")
    summary_df['Avg Lead Time'] = summary_df['Avg Lead Time'].apply(lambda x: f"{x:.1f} days")
    
    st.dataframe(summary_df, use_container_width=True, hide_index=True)
    
    # Insights
    st.markdown("")
    
    # Calculate key metrics for insights
    healthy_pct = len(filtered_inventory[filtered_inventory['stock_status'] == 'Healthy']) / len(filtered_inventory) * 100
    critical_count = len(filtered_inventory[filtered_inventory['stock_status'] == 'Critical'])
    
    col1, col2 = st.columns(2)
    
    with col1:
        if healthy_pct >= 80:
            render_insight_box(
                "✅",
                "Healthy Inventory",
                f"**{healthy_pct:.1f}%** of items have healthy stock levels. "
                f"Inventory management is performing well.",
                "success"
            )
        else:
            render_insight_box(
                "⚠️",
                "Inventory Attention Needed",
                f"Only **{healthy_pct:.1f}%** of items have healthy stock. "
                f"Review low and critical items for restocking.",
                "warning"
            )
    
    with col2:
        if critical_count > 0:
            render_insight_box(
                "🔴",
                f"{critical_count} Critical Items",
                f"**{critical_count}** items are at critical stock levels (at or below 0). "
                f"Immediate restocking action required.",
                "danger"
            )
        else:
            render_insight_box(
                "✅",
                "No Critical Items",
                "All inventory items are above critical levels. Great job maintaining stock!",
                "success"
            )


def render_stock_alerts(filtered_inventory, sales_df):
    """
    Render stock alerts for low and critical items.
    
    Args:
        filtered_inventory: Filtered inventory DataFrame
        sales_df: Sales DataFrame for velocity calculation
    """
    st.markdown("#### ⚠️ Stock Alerts & Reorder Priorities")
    st.markdown("Items requiring immediate attention based on stock levels and sales velocity.")
    
    st.markdown("")
    
    # Get low and critical items
    alert_items = filtered_inventory[filtered_inventory['stock_status'].isin(['Low', 'Critical'])].copy()
    
    if len(alert_items) == 0:
        render_insight_box(
            "✅",
            "No Stock Alerts",
            "All items have healthy stock levels. No immediate action required.",
            "success"
        )
        return
    
    # Calculate sales velocity for each product
    valid_sales = sales_df[sales_df['order_time'].notna()].copy()
    
    if len(valid_sales) > 0:
        # Calculate daily average sales by product
        date_range = (valid_sales['order_time'].max() - valid_sales['order_time'].min()).days
        if date_range > 0:
            product_velocity = valid_sales.groupby('product_id')['qty'].sum() / date_range
            product_velocity = product_velocity.reset_index()
            product_velocity.columns = ['product_id', 'daily_velocity']
            
            # Merge velocity with alert items
            alert_items = alert_items.merge(product_velocity, on='product_id', how='left')
            alert_items['daily_velocity'] = alert_items['daily_velocity'].fillna(0)
            
            # Calculate days until stockout
            alert_items['days_to_stockout'] = alert_items.apply(
                lambda x: x['stock_on_hand'] / x['daily_velocity'] if x['daily_velocity'] > 0 else 999,
                axis=1
            )
            
            # Calculate priority score (lower = more urgent)
            alert_items['priority_score'] = alert_items['days_to_stockout'] - alert_items['lead_time_days']
    else:
        alert_items['daily_velocity'] = 0
        alert_items['days_to_stockout'] = 999
        alert_items['priority_score'] = 999
    
    # KPI summary
    critical_items = alert_items[alert_items['stock_status'] == 'Critical']
    low_items = alert_items[alert_items['stock_status'] == 'Low']
    urgent_items = alert_items[alert_items['priority_score'] < 0]
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        render_status_card("Critical Items", str(len(critical_items)), "danger")
    with col2:
        render_status_card("Low Stock Items", str(len(low_items)), "warning")
    with col3:
        render_status_card("Urgent Reorder", str(len(urgent_items)), "danger")
    with col4:
        render_status_card("Total Alerts", str(len(alert_items)), "warning")
    
    st.markdown("")
    
    # Alert tables
    col1, col2 = st.columns(2)
    
    with col1:
        # Critical items table
        st.markdown("##### 🔴 Critical Stock (Immediate Action)")
        
        if len(critical_items) > 0:
            critical_display = critical_items.nsmallest(20, 'stock_on_hand')[
                ['product_id', 'category', 'stock_on_hand', 'reorder_point', 'lead_time_days', 'daily_velocity']
            ].copy()
            
            critical_display['stock_on_hand'] = critical_display['stock_on_hand'].apply(lambda x: f"{x:.0f}")
            critical_display['reorder_point'] = critical_display['reorder_point'].apply(lambda x: f"{x:.0f}")
            critical_display['lead_time_days'] = critical_display['lead_time_days'].apply(lambda x: f"{x:.0f}")
            critical_display['daily_velocity'] = critical_display['daily_velocity'].apply(lambda x: f"{x:.1f}")
            
            critical_display.columns = ['Product', 'Category', 'Stock', 'Reorder Point', 'Lead Time', 'Daily Sales']
            
            st.dataframe(critical_display, use_container_width=True, hide_index=True)
        else:
            st.info("No critical items found.")
    
    with col2:
        # Low stock items table
        st.markdown("##### 🟡 Low Stock (Plan Reorder)")
        
        if len(low_items) > 0:
            low_display = low_items.nsmallest(20, 'stock_on_hand')[
                ['product_id', 'category', 'stock_on_hand', 'reorder_point', 'lead_time_days', 'daily_velocity']
            ].copy()
            
            low_display['stock_on_hand'] = low_display['stock_on_hand'].apply(lambda x: f"{x:.0f}")
            low_display['reorder_point'] = low_display['reorder_point'].apply(lambda x: f"{x:.0f}")
            low_display['lead_time_days'] = low_display['lead_time_days'].apply(lambda x: f"{x:.0f}")
            low_display['daily_velocity'] = low_display['daily_velocity'].apply(lambda x: f"{x:.1f}")
            
            low_display.columns = ['Product', 'Category', 'Stock', 'Reorder Point', 'Lead Time', 'Daily Sales']
            
            st.dataframe(low_display, use_container_width=True, hide_index=True)
        else:
            st.info("No low stock items found.")
    
    # Urgent reorder chart
    st.markdown("")
    render_chart_title("Stockout Risk Analysis", "⏰")
    
    # Items with negative priority score (will stockout before reorder arrives)
    risk_items = alert_items[alert_items['days_to_stockout'] < 30].nsmallest(20, 'days_to_stockout')
    
    if len(risk_items) > 0:
        fig = px.bar(
            risk_items.sort_values('days_to_stockout'),
            x='product_id',
            y='days_to_stockout',
            color='stock_status',
            color_discrete_map={'Critical': '#ef4444', 'Low': '#f59e0b'},
            text='days_to_stockout'
        )
        fig = apply_chart_style(fig, height=350)
        fig.update_traces(texttemplate='%{text:.1f}d', textposition='outside')
        fig.update_layout(
            xaxis_title="Product ID",
            yaxis_title="Days to Stockout",
            xaxis_tickangle=-45
        )
        
        # Add lead time reference line
        avg_lead_time = risk_items['lead_time_days'].mean()
        fig.add_hline(
            y=avg_lead_time,
            line_dash="dash",
            line_color="#6366f1",
            annotation_text=f"Avg Lead Time ({avg_lead_time:.1f} days)"
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.caption("⚠️ Items below the lead time line will stockout before reorder arrives if ordered today.")
    else:
        render_insight_box(
            "✅",
            "No Immediate Stockout Risk",
            "No items are at risk of stocking out within the next 30 days based on current velocity.",
            "success"
        )
    
    # Recommendations
    st.markdown("")
    st.markdown("##### 💡 Recommended Actions")
    
    recommendations = []
    
    if len(critical_items) > 0:
        recommendations.append({
            "icon": "🔴",
            "text": f"**Immediate:** Place emergency orders for {len(critical_items)} critical items to prevent stockouts."
        })
    
    if len(urgent_items) > 0:
        recommendations.append({
            "icon": "⏰",
            "text": f"**Urgent:** {len(urgent_items)} items will stockout before reorder arrives. Consider expedited shipping."
        })
    
    if len(low_items) > 0:
        recommendations.append({
            "icon": "📋",
            "text": f"**Planned:** Schedule reorders for {len(low_items)} low stock items within the next week."
        })
    
    for rec in recommendations:
        render_recommendation_card(rec['icon'], rec['text'])


def render_inventory_by_location(filtered_inventory):
    """
    Render inventory analysis by location (city and channel).
    
    Args:
        filtered_inventory: Filtered inventory DataFrame
    """
    st.markdown("#### 🏙️ Inventory by Location")
    st.markdown("Stock distribution across cities and channels.")
    
    st.markdown("")
    
    # City breakdown
    col1, col2 = st.columns(2)
    
    with col1:
        # Stock by city
        render_chart_title("Stock by City", "🏙️")
        
        city_stock = filtered_inventory.groupby('city_clean').agg({
            'stock_on_hand': 'sum',
            'product_id': 'nunique'
        }).reset_index()
        city_stock.columns = ['city', 'total_stock', 'sku_count']
        
        city_colors = {'Dubai': '#6366f1', 'Abu Dhabi': '#10b981', 'Sharjah': '#f59e0b'}
        
        fig = px.bar(
            city_stock,
            x='city',
            y='total_stock',
            color='city',
            color_discrete_map=city_colors,
            text=city_stock['total_stock'].apply(lambda x: format_number(x))
        )
        fig = apply_chart_style(fig, height=300, show_legend=False)
        fig.update_traces(textposition='outside')
        fig.update_layout(
            xaxis_title="",
            yaxis_title="Stock Units"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Stock by channel
        render_chart_title("Stock by Channel", "📱")
        
        channel_stock = filtered_inventory.groupby('channel').agg({
            'stock_on_hand': 'sum',
            'product_id': 'nunique'
        }).reset_index()
        channel_stock.columns = ['channel', 'total_stock', 'sku_count']
        
        channel_colors = {'App': '#6366f1', 'Web': '#10b981', 'Marketplace': '#f59e0b'}
        
        fig = px.bar(
            channel_stock,
            x='channel',
            y='total_stock',
            color='channel',
            color_discrete_map=channel_colors,
            text=channel_stock['total_stock'].apply(lambda x: format_number(x))
        )
        fig = apply_chart_style(fig, height=300, show_legend=False)
        fig.update_traces(textposition='outside')
        fig.update_layout(
            xaxis_title="",
            yaxis_title="Stock Units"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # City-Channel heatmap
    st.markdown("")
    render_chart_title("Stock Distribution: City × Channel", "🗺️")
    
    city_channel = filtered_inventory.groupby(['city_clean', 'channel'])['stock_on_hand'].sum().reset_index()
    city_channel_pivot = city_channel.pivot(index='city_clean', columns='channel', values='stock_on_hand').fillna(0)
    
    fig = px.imshow(
        city_channel_pivot,
        labels=dict(x="Channel", y="City", color="Stock Units"),
        color_continuous_scale='Purples',
        aspect='auto',
        text_auto=True
    )
    fig = apply_chart_style(fig, height=280)
    st.plotly_chart(fig, use_container_width=True)
    
    # Stock status by location
    st.markdown("")
    render_chart_title("Stock Health by City", "📊")
    
    city_status = filtered_inventory.groupby(['city_clean', 'stock_status']).size().reset_index(name='count')
    
    fig = px.bar(
        city_status,
        x='city_clean',
        y='count',
        color='stock_status',
        color_discrete_map={'Healthy': '#10b981', 'Low': '#f59e0b', 'Critical': '#ef4444'},
        barmode='group'
    )
    fig = apply_chart_style(fig, height=320)
    fig.update_layout(
        xaxis_title="",
        yaxis_title="Number of Items"
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Location summary table
    st.markdown("")
    st.markdown("##### 📋 Location Summary")
    
    location_summary = filtered_inventory.groupby(['city_clean', 'channel']).agg({
        'stock_on_hand': 'sum',
        'product_id': 'nunique',
        'stock_status': lambda x: (x == 'Healthy').sum()
    }).reset_index()
    
    location_summary.columns = ['City', 'Channel', 'Total Stock', 'SKU Count', 'Healthy Items']
    location_summary['Health %'] = (location_summary['Healthy Items'] / location_summary['SKU Count'] * 100).round(1)
    
    location_summary['Total Stock'] = location_summary['Total Stock'].apply(lambda x: format_number(x))
    location_summary['Health %'] = location_summary['Health %'].apply(lambda x: f"{x}%")
    
    st.dataframe(location_summary, use_container_width=True, hide_index=True)


def render_inventory_trends(inventory_df, selected_city, selected_category):
    """
    Render inventory trends over time.
    
    Args:
        inventory_df: Full inventory DataFrame
        selected_city: Selected city filter
        selected_category: Selected category filter
    """
    st.markdown("#### 📈 Inventory Trends")
    st.markdown("Track stock level changes over time.")
    
    st.markdown("")
    
    # Filter for trends
    trend_data = inventory_df.copy()
    
    if selected_city != 'All':
        trend_data = trend_data[trend_data['city_clean'] == selected_city]
    
    if selected_category != 'All':
        trend_data = trend_data[trend_data['category'] == selected_category]
    
    # Aggregate by date
    daily_stock = trend_data.groupby('snapshot_date').agg({
        'stock_on_hand': 'sum',
        'product_id': 'nunique'
    }).reset_index()
    daily_stock.columns = ['date', 'total_stock', 'active_skus']
    daily_stock = daily_stock.sort_values('date')
    
    # Stock level trend
    render_chart_title("Total Stock Over Time", "📦")
    
    fig = px.area(
        daily_stock,
        x='date',
        y='total_stock',
        color_discrete_sequence=['#6366f1']
    )
    fig.update_traces(
        fill='tozeroy',
        fillcolor='rgba(99, 102, 241, 0.2)',
        line=dict(width=2)
    )
    fig = apply_chart_style(fig, height=300, show_legend=False)
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Total Stock Units"
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Stock status trend
    st.markdown("")
    render_chart_title("Stock Status Trend", "📊")
    
    status_trend = trend_data.groupby(['snapshot_date', 'stock_status']).size().reset_index(name='count')
    
    fig = px.area(
        status_trend,
        x='snapshot_date',
        y='count',
        color='stock_status',
        color_discrete_map={'Healthy': '#10b981', 'Low': '#f59e0b', 'Critical': '#ef4444'}
    )
    fig = apply_chart_style(fig, height=300)
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Number of Items"
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Category trend
    st.markdown("")
    render_chart_title("Stock by Category Over Time", "📦")
    
    category_trend = trend_data.groupby(['snapshot_date', 'category'])['stock_on_hand'].sum().reset_index()
    
    fig = px.line(
        category_trend,
        x='snapshot_date',
        y='stock_on_hand',
        color='category',
        color_discrete_sequence=get_chart_colors(),
        markers=True
    )
    fig = apply_chart_style(fig, height=320)
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Stock Units"
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Trend analysis insight
    if len(daily_stock) >= 2:
        first_stock = daily_stock['total_stock'].iloc[0]
        last_stock = daily_stock['total_stock'].iloc[-1]
        
        if first_stock > 0:
            change_pct = ((last_stock - first_stock) / first_stock) * 100
            
            if change_pct > 10:
                render_insight_box(
                    "📈",
                    "Stock Increasing",
                    f"Total stock has increased by **{change_pct:.1f}%** over the period. "
                    f"Ensure sales velocity matches inventory buildup.",
                    "primary"
                )
            elif change_pct < -10:
                render_insight_box(
                    "📉",
                    "Stock Decreasing",
                    f"Total stock has decreased by **{abs(change_pct):.1f}%** over the period. "
                    f"Review reorder schedules to maintain adequate levels.",
                    "warning"
                )
            else:
                render_insight_box(
                    "➡️",
                    "Stable Stock Levels",
                    f"Stock levels are relatively stable with **{change_pct:.1f}%** change. "
                    f"Good inventory turnover management.",
                    "success"
                )


def render_reorder_analysis(filtered_inventory, sales_df):
    """
    Render reorder analysis with quantity recommendations.
    
    Args:
        filtered_inventory: Filtered inventory DataFrame
        sales_df: Sales DataFrame for demand calculation
    """
    st.markdown("#### 🔄 Reorder Analysis")
    st.markdown("Calculate optimal reorder quantities based on sales velocity and lead times.")
    
    st.markdown("")
    
    # Safety stock multiplier selection
    col1, col2, col3 = st.columns([1, 1, 3])
    
    with col1:
        safety_stock_days = st.selectbox(
            "Safety Stock (Days)",
            options=[3, 5, 7, 10, 14],
            index=2,
            key="reorder_safety_days"
        )
    
    with col2:
        reorder_cycle = st.selectbox(
            "Reorder Cycle (Days)",
            options=[7, 14, 21, 30],
            index=1,
            key="reorder_cycle_days"
        )
    
    # Calculate reorder quantities
    valid_sales = sales_df[sales_df['order_time'].notna()].copy()
    
    if len(valid_sales) > 0:
        date_range = (valid_sales['order_time'].max() - valid_sales['order_time'].min()).days
        if date_range > 0:
            product_velocity = valid_sales.groupby('product_id')['qty'].sum() / date_range
            product_velocity = product_velocity.reset_index()
            product_velocity.columns = ['product_id', 'daily_velocity']
        else:
            product_velocity = pd.DataFrame({'product_id': [], 'daily_velocity': []})
    else:
        product_velocity = pd.DataFrame({'product_id': [], 'daily_velocity': []})
    
    # Merge with inventory
    reorder_df = filtered_inventory.merge(product_velocity, on='product_id', how='left')
    reorder_df['daily_velocity'] = reorder_df['daily_velocity'].fillna(0)
    
    # Calculate reorder quantities
    reorder_df['safety_stock'] = reorder_df['daily_velocity'] * safety_stock_days
    reorder_df['cycle_demand'] = reorder_df['daily_velocity'] * reorder_cycle
    reorder_df['lead_time_demand'] = reorder_df['daily_velocity'] * reorder_df['lead_time_days']
    reorder_df['reorder_qty'] = (
        reorder_df['safety_stock'] + 
        reorder_df['cycle_demand'] + 
        reorder_df['lead_time_demand'] - 
        reorder_df['stock_on_hand']
    ).clip(lower=0)
    
    # Filter to items that need reorder
    needs_reorder = reorder_df[reorder_df['reorder_qty'] > 0].copy()
    needs_reorder = needs_reorder.sort_values('reorder_qty', ascending=False)
    
    # KPIs
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        render_status_card("Items to Reorder", str(len(needs_reorder)), "warning")
    with col2:
        total_reorder = needs_reorder['reorder_qty'].sum()
        render_status_card("Total Units", format_number(total_reorder), "primary")
    with col3:
        avg_reorder = needs_reorder['reorder_qty'].mean() if len(needs_reorder) > 0 else 0
        render_status_card("Avg Reorder Qty", f"{avg_reorder:.0f}", "secondary")
    with col4:
        urgent_reorder = len(needs_reorder[needs_reorder['stock_status'] == 'Critical'])
        render_status_card("Urgent Orders", str(urgent_reorder), "danger")
    
    st.markdown("")
    
    if len(needs_reorder) > 0:
        # Top reorders chart
        render_chart_title("Top 20 Reorder Quantities", "📦")
        
        top_reorders = needs_reorder.head(20)
        
        fig = px.bar(
            top_reorders.sort_values('reorder_qty', ascending=True),
            x='reorder_qty',
            y='product_id',
            orientation='h',
            color='stock_status',
            color_discrete_map={'Healthy': '#10b981', 'Low': '#f59e0b', 'Critical': '#ef4444'}
        )
        fig = apply_chart_style(fig, height=450)
        fig.update_layout(
            xaxis_title="Recommended Reorder Quantity",
            yaxis_title=""
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Reorder summary table
        st.markdown("")
        st.markdown("##### 📋 Reorder Recommendations")
        
        display_df = needs_reorder.head(30)[
            ['product_id', 'category', 'stock_on_hand', 'daily_velocity', 
             'lead_time_days', 'reorder_qty', 'stock_status']
        ].copy()
        
        display_df['stock_on_hand'] = display_df['stock_on_hand'].apply(lambda x: f"{x:.0f}")
        display_df['daily_velocity'] = display_df['daily_velocity'].apply(lambda x: f"{x:.1f}")
        display_df['lead_time_days'] = display_df['lead_time_days'].apply(lambda x: f"{x:.0f}")
        display_df['reorder_qty'] = display_df['reorder_qty'].apply(lambda x: f"{x:.0f}")
        
        display_df.columns = ['Product', 'Category', 'Current Stock', 'Daily Sales', 
                             'Lead Time', 'Reorder Qty', 'Status']
        
        st.dataframe(display_df, use_container_width=True, hide_index=True)
        
        # Reorder by category
        st.markdown("")
        render_chart_title("Reorder Quantity by Category", "📊")
        
        cat_reorder = needs_reorder.groupby('category')['reorder_qty'].sum().reset_index()
        cat_reorder = cat_reorder.sort_values('reorder_qty', ascending=True)
        
        fig = px.bar(
            cat_reorder,
            x='reorder_qty',
            y='category',
            orientation='h',
            color='category',
            color_discrete_sequence=get_chart_colors()
        )
        fig = apply_chart_style(fig, height=280, show_legend=False)
        fig.update_layout(
            xaxis_title="Total Reorder Quantity",
            yaxis_title=""
        )
        st.plotly_chart(fig, use_container_width=True)
    
    else:
        render_insight_box(
            "✅",
            "No Immediate Reorders Needed",
            f"Based on current stock levels and {reorder_cycle}-day cycle demand with {safety_stock_days}-day safety stock, "
            f"no items require immediate reordering.",
            "success"
        )
    
    # Formula explanation
    with st.expander("📐 Reorder Formula Explained"):
        st.markdown(f"""
        **Reorder Quantity Calculation:**
        
        ```
        Reorder Qty = Safety Stock + Cycle Demand + Lead Time Demand - Current Stock
        ```
        
        Where:
        - **Safety Stock** = Daily Velocity × {safety_stock_days} days = Buffer for demand variability
        - **Cycle Demand** = Daily Velocity × {reorder_cycle} days = Expected sales during reorder cycle
        - **Lead Time Demand** = Daily Velocity × Lead Time = Stock needed while waiting for delivery
        - **Current Stock** = Current inventory on hand
        
        Items with Reorder Qty > 0 should be reordered to maintain optimal stock levels.
        """)


def render_demand_forecast(inventory_df, sales_df, selected_category):
    """
    Render simple demand forecasting based on historical sales.
    
    Args:
        inventory_df: Inventory DataFrame
        sales_df: Sales DataFrame
        selected_category: Selected category filter
    """
    st.markdown("#### 🔮 Demand Forecast")
    st.markdown("Projected demand based on historical sales patterns.")
    
    st.markdown("")
    
    # Filter sales data
    valid_sales = sales_df[sales_df['order_time'].notna()].copy()
    
    if selected_category != 'All':
        valid_sales = valid_sales[valid_sales['category'] == selected_category]
    
    if len(valid_sales) == 0:
        render_empty_state(
            "🔮",
            "Insufficient Data",
            "Not enough sales data available for forecasting."
        )
        return
    
    # Forecast horizon selection
    col1, col2 = st.columns([1, 4])
    
    with col1:
        forecast_days = st.selectbox(
            "Forecast Horizon",
            options=[7, 14, 30],
            index=1,
            key="forecast_horizon"
        )
    
    # Calculate historical daily metrics
    daily_sales = valid_sales.groupby(valid_sales['order_time'].dt.date).agg({
        'qty': 'sum',
        'revenue': 'sum',
        'order_id': 'nunique'
    }).reset_index()
    daily_sales.columns = ['date', 'units', 'revenue', 'orders']
    daily_sales = daily_sales.sort_values('date')
    
    # Calculate averages and trends
    avg_daily_units = daily_sales['units'].mean()
    avg_daily_revenue = daily_sales['revenue'].mean()
    avg_daily_orders = daily_sales['orders'].mean()
    
    # Simple trend calculation (last 14 days vs previous 14 days)
    if len(daily_sales) >= 28:
        recent = daily_sales.tail(14)['units'].mean()
        previous = daily_sales.tail(28).head(14)['units'].mean()
        trend_factor = recent / previous if previous > 0 else 1
    else:
        trend_factor = 1
    
    # Generate forecast
    last_date = daily_sales['date'].max()
    forecast_dates = [last_date + timedelta(days=i+1) for i in range(forecast_days)]
    
    forecast_df = pd.DataFrame({
        'date': forecast_dates,
        'forecasted_units': [avg_daily_units * (trend_factor ** (i/14)) for i in range(forecast_days)],
        'forecasted_revenue': [avg_daily_revenue * (trend_factor ** (i/14)) for i in range(forecast_days)]
    })
    
    # Combine historical and forecast
    daily_sales['type'] = 'Historical'
    forecast_df['type'] = 'Forecast'
    
    combined_df = pd.concat([
        daily_sales[['date', 'units', 'revenue']].rename(columns={'units': 'value'}),
    ])
    
    # Forecast KPIs
    total_forecast_units = forecast_df['forecasted_units'].sum()
    total_forecast_revenue = forecast_df['forecasted_revenue'].sum()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        render_status_card(f"{forecast_days}-Day Unit Forecast", format_number(total_forecast_units), "primary")
    with col2:
        render_status_card(f"{forecast_days}-Day Revenue Forecast", format_currency(total_forecast_revenue), "success")
    with col3:
        render_status_card("Daily Avg Units", f"{avg_daily_units:.0f}", "secondary")
    with col4:
        trend_pct = (trend_factor - 1) * 100
        trend_type = "success" if trend_pct > 0 else "danger" if trend_pct < 0 else "primary"
        render_status_card("Trend", f"{trend_pct:+.1f}%", trend_type)
    
    st.markdown("")
    
    # Forecast chart
    render_chart_title("Units Sold: Historical & Forecast", "📈")
    
    fig = go.Figure()
    
    # Historical data
    fig.add_trace(go.Scatter(
        x=daily_sales['date'],
        y=daily_sales['units'],
        name='Historical',
        line=dict(color='#6366f1', width=2),
        mode='lines'
    ))
    
    # Forecast data
    fig.add_trace(go.Scatter(
        x=forecast_df['date'],
        y=forecast_df['forecasted_units'],
        name='Forecast',
        line=dict(color='#f59e0b', width=2, dash='dash'),
        mode='lines'
    ))
    
    # Add confidence band
    upper_band = forecast_df['forecasted_units'] * 1.2
    lower_band = forecast_df['forecasted_units'] * 0.8
    
    fig.add_trace(go.Scatter(
        x=list(forecast_df['date']) + list(forecast_df['date'][::-1]),
        y=list(upper_band) + list(lower_band[::-1]),
        fill='toself',
        fillcolor='rgba(245, 158, 11, 0.1)',
        line=dict(color='rgba(255,255,255,0)'),
        name='Confidence Band'
    ))
    
    fig = apply_chart_style(fig, height=350)
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Units Sold"
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Weekly forecast breakdown
    st.markdown("")
    st.markdown("##### 📅 Forecast Breakdown")
    
    forecast_df['week'] = pd.to_datetime(forecast_df['date']).dt.isocalendar().week
    weekly_forecast = forecast_df.groupby('week').agg({
        'forecasted_units': 'sum',
        'forecasted_revenue': 'sum'
    }).reset_index()
    weekly_forecast.columns = ['Week', 'Units', 'Revenue']
    weekly_forecast['Units'] = weekly_forecast['Units'].apply(lambda x: format_number(x))
    weekly_forecast['Revenue'] = weekly_forecast['Revenue'].apply(lambda x: format_currency(x))
    
    st.dataframe(weekly_forecast, use_container_width=True, hide_index=True)
    
    # Insight
    render_insight_box(
        "🔮",
        "Forecast Summary",
        f"Based on historical data, expect approximately **{format_number(total_forecast_units)}** units "
        f"generating **{format_currency(total_forecast_revenue)}** in revenue over the next {forecast_days} days. "
        f"Trend is **{'+' if trend_pct > 0 else ''}{trend_pct:.1f}%** based on recent vs previous period comparison.",
        "primary"
    )
    
    # Methodology note
    with st.expander("📐 Forecast Methodology"):
        st.markdown("""
        **Simple Moving Average with Trend Adjustment**
        
        This forecast uses:
        1. **Base Rate**: Average daily units/revenue from historical data
        2. **Trend Factor**: Ratio of recent 14-day average to previous 14-day average
        3. **Confidence Band**: ±20% based on historical variability
        
        **Limitations:**
        - Does not account for seasonality
        - Does not incorporate promotional effects
        - Best used for short-term (1-4 week) forecasts
        
        For production use, consider implementing more sophisticated models like:
        - SARIMA for seasonal patterns
        - Prophet for holiday effects
        - Machine learning models for complex patterns
        """)

# =============================================================================
# CAMPAIGN PERFORMANCE TAB
# =============================================================================
# This module provides campaign analysis and the What-If Promotion Simulator
# for testing promotional scenarios before implementation.
# =============================================================================

def render_campaign_analysis(campaigns_df, sales_df, products_df, stores_df):
    """
    Render the Campaign Performance tab with analysis and simulator.
    
    This tab provides:
        1. Campaign Overview KPIs
        2. Active Campaign Status
        3. Campaign Performance Metrics
        4. What-If Promotion Simulator
        5. ROI Analysis
    
    Args:
        campaigns_df: Campaigns DataFrame
        sales_df: Sales DataFrame
        products_df: Products DataFrame
        stores_df: Stores DataFrame
    """
    render_section_header(
        "🎯",
        "Campaign Performance & Simulator",
        "Analyze promotional campaigns and simulate new scenarios"
    )
    
    # =========================================================================
    # SUB-TABS
    # =========================================================================
    campaign_tabs = st.tabs([
        "📊 Campaign Overview",
        "🔬 What-If Simulator",
        "📈 ROI Analysis"
    ])
    
    with campaign_tabs[0]:
        render_campaign_overview(campaigns_df, sales_df)
    
    with campaign_tabs[1]:
        render_whatif_simulator(campaigns_df, sales_df, products_df, stores_df)
    
    with campaign_tabs[2]:
        render_roi_analysis(campaigns_df, sales_df, products_df)


def render_campaign_overview(campaigns_df, sales_df):
    """
    Render campaign overview with status and performance metrics.
    
    Args:
        campaigns_df: Campaigns DataFrame
        sales_df: Sales DataFrame
    """
    st.markdown("#### 📊 Campaign Overview")
    st.markdown("Current and planned promotional campaigns with performance metrics.")
    
    st.markdown("")
    
    # Calculate campaign metrics
    total_campaigns = len(campaigns_df)
    active_campaigns = campaigns_df['is_active'].sum() if 'is_active' in campaigns_df.columns else 0
    total_budget = campaigns_df['promo_budget_aed'].sum()
    avg_discount = campaigns_df['discount_pct'].mean()
    avg_duration = campaigns_df['duration_days'].mean() if 'duration_days' in campaigns_df.columns else 0
    
    # KPIs
    kpis = [
        {
            "icon": "🎯",
            "value": str(total_campaigns),
            "label": "Total Campaigns",
            "type": "primary"
        },
        {
            "icon": "✅",
            "value": str(int(active_campaigns)),
            "label": "Active Now",
            "type": "success"
        },
        {
            "icon": "💰",
            "value": format_currency(total_budget),
            "label": "Total Budget",
            "type": "accent"
        },
        {
            "icon": "🏷️",
            "value": f"{avg_discount:.0f}%",
            "label": "Avg Discount",
            "type": "warning"
        },
        {
            "icon": "📅",
            "value": f"{avg_duration:.0f} days",
            "label": "Avg Duration",
            "type": "secondary"
        }
    ]
    
    render_kpi_row(kpis)
    
    st.markdown("")
    
    # Campaign timeline visualization
    render_chart_title("Campaign Timeline", "📅")
    
    # Prepare data for timeline
    timeline_df = campaigns_df.copy()
    timeline_df['start_date'] = pd.to_datetime(timeline_df['start_date'])
    timeline_df['end_date'] = pd.to_datetime(timeline_df['end_date'])
    
    # Create Gantt-style chart
    fig = px.timeline(
        timeline_df,
        x_start='start_date',
        x_end='end_date',
        y='campaign_id',
        color='discount_pct',
        color_continuous_scale=['#10b981', '#f59e0b', '#ef4444'],
        hover_data=['city', 'channel', 'category', 'promo_budget_aed']
    )
    
    fig = apply_chart_style(fig, height=350)
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Campaign",
        coloraxis_colorbar_title="Discount %"
    )
    
    # Add today marker
    fig.add_vline(
        x=pd.Timestamp.now(),
        line_dash="dash",
        line_color="#6366f1",
        annotation_text="Today"
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Campaign cards
    st.markdown("")
    st.markdown("##### 🎯 Campaign Details")
    
    # Split into active and upcoming
    active = campaigns_df[campaigns_df['is_active'] == True] if 'is_active' in campaigns_df.columns else pd.DataFrame()
    upcoming = campaigns_df[campaigns_df['is_active'] == False] if 'is_active' in campaigns_df.columns else campaigns_df
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**🟢 Active Campaigns**")
        
        if len(active) > 0:
            for _, campaign in active.iterrows():
                render_campaign_card(campaign, is_active=True)
        else:
            st.info("No active campaigns at the moment.")
    
    with col2:
        st.markdown("**🔵 Upcoming/Planned Campaigns**")
        
        if len(upcoming) > 0:
            for _, campaign in upcoming.head(5).iterrows():
                render_campaign_card(campaign, is_active=False)
        else:
            st.info("No upcoming campaigns planned.")
    
    # Campaign summary table
    st.markdown("")
    st.markdown("##### 📋 All Campaigns Summary")
    
    display_df = campaigns_df[[
        'campaign_id', 'start_date', 'end_date', 'city', 'channel', 
        'category', 'discount_pct', 'promo_budget_aed'
    ]].copy()
    
    display_df['start_date'] = pd.to_datetime(display_df['start_date']).dt.strftime('%Y-%m-%d')
    display_df['end_date'] = pd.to_datetime(display_df['end_date']).dt.strftime('%Y-%m-%d')
    display_df['discount_pct'] = display_df['discount_pct'].apply(lambda x: f"{x}%")
    display_df['promo_budget_aed'] = display_df['promo_budget_aed'].apply(lambda x: format_currency(x))
    
    display_df.columns = ['Campaign ID', 'Start Date', 'End Date', 'City', 'Channel', 
                          'Category', 'Discount', 'Budget']
    
    st.dataframe(display_df, use_container_width=True, hide_index=True)
    
    # Budget allocation chart
    st.markdown("")
    
    col1, col2 = st.columns(2)
    
    with col1:
        render_chart_title("Budget by Category", "💰")
        
        budget_by_cat = campaigns_df.groupby('category')['promo_budget_aed'].sum().reset_index()
        
        fig = px.pie(
            budget_by_cat,
            values='promo_budget_aed',
            names='category',
            color_discrete_sequence=get_chart_colors(),
            hole=0.4
        )
        fig = apply_chart_style(fig, height=300)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        render_chart_title("Budget by City", "🏙️")
        
        budget_by_city = campaigns_df.groupby('city')['promo_budget_aed'].sum().reset_index()
        
        fig = px.pie(
            budget_by_city,
            values='promo_budget_aed',
            names='city',
            color_discrete_sequence=get_chart_colors(),
            hole=0.4
        )
        fig = apply_chart_style(fig, height=300)
        st.plotly_chart(fig, use_container_width=True)


def render_campaign_card(campaign, is_active=False):
    """
    Render a single campaign card.
    
    Args:
        campaign: Campaign row from DataFrame
        is_active: Whether campaign is currently active
    """
    border_color = '#10b981' if is_active else '#6366f1'
    status_badge = '🟢 Active' if is_active else '🔵 Planned'
    
    start_date = pd.to_datetime(campaign['start_date']).strftime('%b %d')
    end_date = pd.to_datetime(campaign['end_date']).strftime('%b %d, %Y')
    
    st.markdown(f'''
    <div style="background: rgba(255,255,255,0.03); border: 1px solid {border_color}40;
                border-left: 4px solid {border_color}; border-radius: 8px; 
                padding: 12px 16px; margin-bottom: 12px;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
            <span style="font-weight: 600; color: white;">{campaign['campaign_id']}</span>
            <span style="font-size: 0.75rem; color: {border_color};">{status_badge}</span>
        </div>
        <div style="font-size: 0.85rem; color: #a1a1aa; margin-bottom: 8px;">
            📅 {start_date} - {end_date}
        </div>
        <div style="display: flex; gap: 16px; font-size: 0.8rem; color: #71717a;">
            <span>🏙️ {campaign['city']}</span>
            <span>📱 {campaign['channel']}</span>
            <span>📦 {campaign['category']}</span>
        </div>
        <div style="display: flex; justify-content: space-between; margin-top: 10px; 
                    padding-top: 10px; border-top: 1px solid rgba(255,255,255,0.1);">
            <span style="color: #f59e0b; font-weight: 600;">{campaign['discount_pct']}% OFF</span>
            <span style="color: #10b981; font-weight: 600;">{format_currency(campaign['promo_budget_aed'])}</span>
        </div>
    </div>
    ''', unsafe_allow_html=True)


def render_whatif_simulator(campaigns_df, sales_df, products_df, stores_df):
    """
    Render the What-If Promotion Simulator.
    
    This simulator allows users to:
        1. Select an existing campaign as baseline OR create custom scenario
        2. Adjust parameters (discount, duration, targeting)
        3. See projected impact on revenue, units, and margin
    
    Args:
        campaigns_df: Campaigns DataFrame
        sales_df: Sales DataFrame
        products_df: Products DataFrame
        stores_df: Stores DataFrame
    """
    st.markdown("#### 🔬 What-If Promotion Simulator")
    st.markdown("Simulate promotional scenarios and predict their impact on sales and revenue.")
    
    st.markdown("")
    
    # =========================================================================
    # SCENARIO CONFIGURATION
    # =========================================================================
    st.markdown("##### ⚙️ Configure Promotion Scenario")
    
    # Scenario type selection
    scenario_type = st.radio(
        "Scenario Type",
        options=["📋 Based on Existing Campaign", "✨ Create Custom Scenario"],
        horizontal=True,
        key="simulator_scenario_type"
    )
    
    st.markdown("")
    
    # Initialize scenario parameters
    scenario_params = {}
    
    if scenario_type == "📋 Based on Existing Campaign":
        # Select existing campaign as baseline
        campaign_options = campaigns_df['campaign_id'].tolist()
        
        col1, col2 = st.columns([1, 3])
        
        with col1:
            selected_campaign_id = st.selectbox(
                "Select Campaign",
                options=campaign_options,
                key="simulator_campaign_select"
            )
        
        # Get selected campaign details
        selected_campaign = campaigns_df[campaigns_df['campaign_id'] == selected_campaign_id].iloc[0]
        
        with col2:
            st.markdown(f"""
            **Selected Campaign Details:**
            - **City:** {selected_campaign['city']} | **Channel:** {selected_campaign['channel']} | **Category:** {selected_campaign['category']}
            - **Discount:** {selected_campaign['discount_pct']}% | **Budget:** {format_currency(selected_campaign['promo_budget_aed'])}
            - **Duration:** {selected_campaign['duration_days']} days
            """)
        
        st.markdown("")
        st.markdown("**Adjust Parameters:**")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            scenario_discount = st.slider(
                "Discount %",
                min_value=5,
                max_value=50,
                value=int(selected_campaign['discount_pct']),
                step=5,
                key="simulator_discount"
            )
        
        with col2:
            scenario_duration = st.slider(
                "Duration (Days)",
                min_value=1,
                max_value=30,
                value=int(selected_campaign['duration_days']),
                step=1,
                key="simulator_duration"
            )
        
        with col3:
            scenario_budget = st.number_input(
                "Budget (AED)",
                min_value=10000,
                max_value=500000,
                value=int(selected_campaign['promo_budget_aed']),
                step=10000,
                key="simulator_budget"
            )
        
        with col4:
            lift_multiplier = st.slider(
                "Expected Lift Factor",
                min_value=1.0,
                max_value=3.0,
                value=1.5,
                step=0.1,
                key="simulator_lift",
                help="Multiplier for sales increase during promotion"
            )
        
        # Set scenario parameters
        scenario_params = {
            'city': selected_campaign['city'],
            'channel': selected_campaign['channel'],
            'category': selected_campaign['category'],
            'discount_pct': scenario_discount,
            'duration_days': scenario_duration,
            'budget': scenario_budget,
            'lift_multiplier': lift_multiplier,
            'baseline_discount': selected_campaign['discount_pct'],
            'baseline_duration': selected_campaign['duration_days'],
            'baseline_budget': selected_campaign['promo_budget_aed']
        }
    
    else:
        # Custom scenario creation
        st.markdown("**Define Custom Scenario:**")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            scenario_city = st.selectbox(
                "Target City",
                options=['All'] + STANDARD_CITIES,
                key="custom_scenario_city"
            )
            
            scenario_discount = st.slider(
                "Discount %",
                min_value=5,
                max_value=50,
                value=20,
                step=5,
                key="custom_scenario_discount"
            )
        
        with col2:
            scenario_channel = st.selectbox(
                "Target Channel",
                options=['All'] + CHANNELS,
                key="custom_scenario_channel"
            )
            
            scenario_duration = st.slider(
                "Duration (Days)",
                min_value=1,
                max_value=30,
                value=7,
                step=1,
                key="custom_scenario_duration"
            )
        
        with col3:
            scenario_category = st.selectbox(
                "Target Category",
                options=['All'] + CATEGORIES,
                key="custom_scenario_category"
            )
            
            scenario_budget = st.number_input(
                "Budget (AED)",
                min_value=10000,
                max_value=500000,
                value=50000,
                step=10000,
                key="custom_scenario_budget"
            )
        
        # Lift factor
        lift_multiplier = st.slider(
            "Expected Lift Factor",
            min_value=1.0,
            max_value=3.0,
            value=1.5,
            step=0.1,
            key="custom_scenario_lift",
            help="Multiplier for sales increase during promotion (1.5 = 50% increase)"
        )
        
        scenario_params = {
            'city': scenario_city,
            'channel': scenario_channel,
            'category': scenario_category,
            'discount_pct': scenario_discount,
            'duration_days': scenario_duration,
            'budget': scenario_budget,
            'lift_multiplier': lift_multiplier,
            'baseline_discount': 0,
            'baseline_duration': 0,
            'baseline_budget': 0
        }
    
    render_divider_subtle()
    
    # =========================================================================
    # RUN SIMULATION
    # =========================================================================
    if st.button("🚀 Run Simulation", type="primary", key="run_simulation_btn"):
        with st.spinner("Running simulation..."):
            simulation_results = run_promotion_simulation(
                sales_df, products_df, scenario_params
            )
        
        # Display results
        render_simulation_results(simulation_results, scenario_params)
    
    else:
        # Show placeholder
        st.markdown("")
        render_insight_box(
            "💡",
            "Ready to Simulate",
            "Configure your promotion scenario above and click 'Run Simulation' to see projected results.",
            "primary"
        )
        
        # Show parameter summary
        st.markdown("")
        st.markdown("##### 📋 Current Scenario Summary")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            **Targeting:**
            - City: {scenario_params.get('city', 'All')}
            - Channel: {scenario_params.get('channel', 'All')}
            - Category: {scenario_params.get('category', 'All')}
            """)
        
        with col2:
            st.markdown(f"""
            **Promotion:**
            - Discount: {scenario_params.get('discount_pct', 0)}%
            - Duration: {scenario_params.get('duration_days', 0)} days
            """)
        
        with col3:
            st.markdown(f"""
            **Investment:**
            - Budget: {format_currency(scenario_params.get('budget', 0))}
            - Lift Factor: {scenario_params.get('lift_multiplier', 1.0)}x
            """)
        
        with col4:
            # Estimate reach
            valid_sales = sales_df[sales_df['order_time'].notna()]
            filtered = valid_sales.copy()
            
            if scenario_params.get('city') and scenario_params.get('city') != 'All':
                filtered = filtered[filtered['city_clean'] == scenario_params['city']]
            if scenario_params.get('channel') and scenario_params.get('channel') != 'All':
                filtered = filtered[filtered['channel'] == scenario_params['channel']]
            if scenario_params.get('category') and scenario_params.get('category') != 'All':
                filtered = filtered[filtered['category'] == scenario_params['category']]
            
            reach_pct = len(filtered) / len(valid_sales) * 100 if len(valid_sales) > 0 else 0
            
            st.markdown(f"""
            **Estimated Reach:**
            - {reach_pct:.1f}% of sales
            - {len(filtered):,} historical orders
            """)


def run_promotion_simulation(sales_df, products_df, params):
    """
    Run the promotion simulation and calculate projected metrics.
    
    Args:
        sales_df: Sales DataFrame
        products_df: Products DataFrame
        params: Scenario parameters dictionary
    
    Returns:
        dict: Simulation results
    """
    # Filter valid sales
    valid_sales = sales_df[sales_df['order_time'].notna()].copy()
    
    # Apply targeting filters
    filtered_sales = valid_sales.copy()
    
    if params.get('city') and params['city'] != 'All':
        filtered_sales = filtered_sales[filtered_sales['city_clean'] == params['city']]
    
    if params.get('channel') and params['channel'] != 'All':
        filtered_sales = filtered_sales[filtered_sales['channel'] == params['channel']]
    
    if params.get('category') and params['category'] != 'All':
        filtered_sales = filtered_sales[filtered_sales['category'] == params['category']]
    
    # Calculate baseline metrics (per day)
    if len(filtered_sales) > 0:
        date_range = (filtered_sales['order_time'].max() - filtered_sales['order_time'].min()).days
        date_range = max(1, date_range)
        
        baseline_daily_revenue = filtered_sales['revenue'].sum() / date_range
        baseline_daily_units = filtered_sales['qty'].sum() / date_range
        baseline_daily_orders = filtered_sales['order_id'].nunique() / date_range
        baseline_avg_price = filtered_sales['selling_price_aed'].mean()
        baseline_avg_discount = filtered_sales['discount_pct'].mean()
    else:
        baseline_daily_revenue = 0
        baseline_daily_units = 0
        baseline_daily_orders = 0
        baseline_avg_price = 0
        baseline_avg_discount = 0
    
    # Get cost information
    if 'unit_cost_aed' in filtered_sales.columns:
        avg_unit_cost = filtered_sales['unit_cost_aed'].mean()
        if pd.isna(avg_unit_cost):
            avg_unit_cost = baseline_avg_price * 0.55  # Assume 55% cost if missing
    else:
        avg_unit_cost = baseline_avg_price * 0.55
    
    # Calculate promotion impact
    discount_pct = params['discount_pct']
    duration_days = params['duration_days']
    lift_multiplier = params['lift_multiplier']
    budget = params['budget']
    
    # New price after discount
    promo_price = baseline_avg_price * (1 - discount_pct / 100)
    
    # Projected daily metrics during promotion
    promo_daily_units = baseline_daily_units * lift_multiplier
    promo_daily_orders = baseline_daily_orders * lift_multiplier
    promo_daily_revenue = promo_daily_units * promo_price
    
    # Total promotion period metrics
    promo_total_revenue = promo_daily_revenue * duration_days
    promo_total_units = promo_daily_units * duration_days
    promo_total_orders = promo_daily_orders * duration_days
    
    # Baseline metrics for same period (without promotion)
    baseline_total_revenue = baseline_daily_revenue * duration_days
    baseline_total_units = baseline_daily_units * duration_days
    baseline_total_orders = baseline_daily_orders * duration_days
    
    # Calculate incremental impact
    incremental_revenue = promo_total_revenue - baseline_total_revenue
    incremental_units = promo_total_units - baseline_total_units
    incremental_orders = promo_total_orders - baseline_total_orders
    
    # Calculate gross margin
    baseline_margin = (baseline_avg_price - avg_unit_cost) * baseline_total_units
    promo_margin = (promo_price - avg_unit_cost) * promo_total_units
    
    # Margin impact (promo margin - baseline margin - budget)
    margin_impact = promo_margin - baseline_margin - budget
    
    # ROI calculation
    if budget > 0:
        roi = (incremental_revenue - budget) / budget * 100
        roi_margin = margin_impact / budget * 100
    else:
        roi = 0
        roi_margin = 0
    
    # Break-even analysis
    revenue_per_discount_pct = incremental_revenue / discount_pct if discount_pct > 0 else 0
    
    # Cannibalization estimate (assume 10-20% of lift is cannibalized from non-promo period)
    cannibalization_factor = 0.15
    true_incremental_revenue = incremental_revenue * (1 - cannibalization_factor)
    true_incremental_units = incremental_units * (1 - cannibalization_factor)
    
    return {
        # Baseline metrics
        'baseline_daily_revenue': baseline_daily_revenue,
        'baseline_daily_units': baseline_daily_units,
        'baseline_daily_orders': baseline_daily_orders,
        'baseline_avg_price': baseline_avg_price,
        'baseline_total_revenue': baseline_total_revenue,
        'baseline_total_units': baseline_total_units,
        'baseline_total_orders': baseline_total_orders,
        'baseline_margin': baseline_margin,
        
        # Promo metrics
        'promo_price': promo_price,
        'promo_daily_revenue': promo_daily_revenue,
        'promo_daily_units': promo_daily_units,
        'promo_total_revenue': promo_total_revenue,
        'promo_total_units': promo_total_units,
        'promo_total_orders': promo_total_orders,
        'promo_margin': promo_margin,
        
        # Incremental impact
        'incremental_revenue': incremental_revenue,
        'incremental_units': incremental_units,
        'incremental_orders': incremental_orders,
        'true_incremental_revenue': true_incremental_revenue,
        'true_incremental_units': true_incremental_units,
        
        # Financial metrics
        'margin_impact': margin_impact,
        'roi': roi,
        'roi_margin': roi_margin,
        'budget': budget,
        
        # Additional
        'avg_unit_cost': avg_unit_cost,
        'discount_pct': discount_pct,
        'duration_days': duration_days,
        'lift_multiplier': lift_multiplier,
        'cannibalization_factor': cannibalization_factor
    }


def render_simulation_results(results, params):
    """
    Render the simulation results dashboard.
    
    Args:
        results: Simulation results dictionary
        params: Scenario parameters
    """
    st.markdown("### 📊 Simulation Results")
    
    st.markdown("")
    
    # =========================================================================
    # KEY OUTCOME KPIs
    # =========================================================================
    st.markdown("##### 🎯 Projected Outcomes")
    
    # Determine ROI status
    if results['roi'] >= 100:
        roi_type = "success"
        outcome_verdict = "✅ Highly Profitable"
    elif results['roi'] >= 0:
        roi_type = "warning"
        outcome_verdict = "⚠️ Marginally Profitable"
    else:
        roi_type = "danger"
        outcome_verdict = "❌ Unprofitable"
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.markdown(f'''
        <div style="background: rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.3);
                    border-radius: 12px; padding: 16px; text-align: center;">
            <div style="font-size: 0.8rem; color: #71717a;">Projected Revenue</div>
            <div style="font-size: 1.4rem; font-weight: 700; color: #10b981;">{format_currency(results['promo_total_revenue'])}</div>
            <div style="font-size: 0.75rem; color: #a1a1aa;">for {results['duration_days']} days</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col2:
        st.markdown(f'''
        <div style="background: rgba(99, 102, 241, 0.1); border: 1px solid rgba(99, 102, 241, 0.3);
                    border-radius: 12px; padding: 16px; text-align: center;">
            <div style="font-size: 0.8rem; color: #71717a;">Incremental Revenue</div>
            <div style="font-size: 1.4rem; font-weight: 700; color: #6366f1;">{format_currency(results['incremental_revenue'])}</div>
            <div style="font-size: 0.75rem; color: #a1a1aa;">vs no promotion</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col3:
        st.markdown(f'''
        <div style="background: rgba(139, 92, 246, 0.1); border: 1px solid rgba(139, 92, 246, 0.3);
                    border-radius: 12px; padding: 16px; text-align: center;">
            <div style="font-size: 0.8rem; color: #71717a;">Incremental Units</div>
            <div style="font-size: 1.4rem; font-weight: 700; color: #8b5cf6;">{format_number(results['incremental_units'])}</div>
            <div style="font-size: 0.75rem; color: #a1a1aa;">+{(results['lift_multiplier']-1)*100:.0f}% lift</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col4:
        margin_color = '#10b981' if results['margin_impact'] > 0 else '#ef4444'
        st.markdown(f'''
        <div style="background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.1);
                    border-radius: 12px; padding: 16px; text-align: center;">
            <div style="font-size: 0.8rem; color: #71717a;">Margin Impact</div>
            <div style="font-size: 1.4rem; font-weight: 700; color: {margin_color};">{format_currency(results['margin_impact'])}</div>
            <div style="font-size: 0.75rem; color: #a1a1aa;">after budget</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col5:
        roi_color = '#10b981' if results['roi'] >= 100 else '#f59e0b' if results['roi'] >= 0 else '#ef4444'
        st.markdown(f'''
        <div style="background: rgba(255, 255, 255, 0.03); border: 1px solid {roi_color}40;
                    border-radius: 12px; padding: 16px; text-align: center;">
            <div style="font-size: 0.8rem; color: #71717a;">Revenue ROI</div>
            <div style="font-size: 1.4rem; font-weight: 700; color: {roi_color};">{results['roi']:.0f}%</div>
            <div style="font-size: 0.75rem; color: {roi_color};">{outcome_verdict}</div>
        </div>
        ''', unsafe_allow_html=True)
    
    st.markdown("")
    
    # =========================================================================
    # COMPARISON CHARTS
    # =========================================================================
    col1, col2 = st.columns(2)
    
    with col1:
        # Revenue comparison
        render_chart_title("Revenue Comparison", "💰")
        
        comparison_data = pd.DataFrame({
            'Scenario': ['Without Promotion', 'With Promotion'],
            'Revenue': [results['baseline_total_revenue'], results['promo_total_revenue']]
        })
        
        fig = px.bar(
            comparison_data,
            x='Scenario',
            y='Revenue',
            color='Scenario',
            color_discrete_sequence=['#71717a', '#10b981'],
            text=comparison_data['Revenue'].apply(lambda x: format_currency(x))
        )
        fig = apply_chart_style(fig, height=280, show_legend=False)
        fig.update_traces(textposition='outside')
        fig.update_layout(
            xaxis_title="",
            yaxis_title="Revenue (AED)"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Units comparison
        render_chart_title("Units Sold Comparison", "📦")
        
        units_data = pd.DataFrame({
            'Scenario': ['Without Promotion', 'With Promotion'],
            'Units': [results['baseline_total_units'], results['promo_total_units']]
        })
        
        fig = px.bar(
            units_data,
            x='Scenario',
            y='Units',
            color='Scenario',
            color_discrete_sequence=['#71717a', '#6366f1'],
            text=units_data['Units'].apply(lambda x: format_number(x))
        )
        fig = apply_chart_style(fig, height=280, show_legend=False)
        fig.update_traces(textposition='outside')
        fig.update_layout(
            xaxis_title="",
            yaxis_title="Units"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # =========================================================================
    # DAILY PROJECTION CHART
    # =========================================================================
    st.markdown("")
    render_chart_title("Daily Revenue Projection", "📈")
    
    # Create daily projection data
    days = list(range(1, results['duration_days'] + 1))
    baseline_daily = [results['baseline_daily_revenue']] * results['duration_days']
    promo_daily = [results['promo_daily_revenue']] * results['duration_days']
    
    projection_df = pd.DataFrame({
        'Day': days + days,
        'Revenue': baseline_daily + promo_daily,
        'Scenario': ['Without Promotion'] * results['duration_days'] + ['With Promotion'] * results['duration_days']
    })
    
    fig = px.area(
        projection_df,
        x='Day',
        y='Revenue',
        color='Scenario',
        color_discrete_map={'Without Promotion': '#71717a', 'With Promotion': '#6366f1'}
    )
    fig = apply_chart_style(fig, height=300)
    fig.update_layout(
        xaxis_title="Campaign Day",
        yaxis_title="Daily Revenue (AED)"
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # =========================================================================
    # DETAILED METRICS TABLE
    # =========================================================================
    st.markdown("")
    st.markdown("##### 📋 Detailed Metrics")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**Baseline (No Promo)**")
        st.markdown(f"- Daily Revenue: {format_currency(results['baseline_daily_revenue'])}")
        st.markdown(f"- Daily Units: {results['baseline_daily_units']:.0f}")
        st.markdown(f"- Avg Price: {format_currency(results['baseline_avg_price'])}")
        st.markdown(f"- Period Revenue: {format_currency(results['baseline_total_revenue'])}")
        st.markdown(f"- Period Margin: {format_currency(results['baseline_margin'])}")
    
    with col2:
        st.markdown("**With Promotion**")
        st.markdown(f"- Daily Revenue: {format_currency(results['promo_daily_revenue'])}")
        st.markdown(f"- Daily Units: {results['promo_daily_units']:.0f}")
        st.markdown(f"- Promo Price: {format_currency(results['promo_price'])}")
        st.markdown(f"- Period Revenue: {format_currency(results['promo_total_revenue'])}")
        st.markdown(f"- Period Margin: {format_currency(results['promo_margin'])}")
    
    with col3:
        st.markdown("**Incremental Impact**")
        rev_change = (results['promo_total_revenue'] / results['baseline_total_revenue'] - 1) * 100 if results['baseline_total_revenue'] > 0 else 0
        units_change = (results['promo_total_units'] / results['baseline_total_units'] - 1) * 100 if results['baseline_total_units'] > 0 else 0
        
        st.markdown(f"- Revenue Change: **+{rev_change:.1f}%**")
        st.markdown(f"- Units Change: **+{units_change:.1f}%**")
        st.markdown(f"- Incremental Revenue: {format_currency(results['incremental_revenue'])}")
        st.markdown(f"- True Incremental*: {format_currency(results['true_incremental_revenue'])}")
        st.markdown(f"- Budget: {format_currency(results['budget'])}")
    
    st.caption("*True incremental accounts for 15% cannibalization from other periods")
    
    # =========================================================================
    # RECOMMENDATION
    # =========================================================================
    st.markdown("")
    
    if results['roi'] >= 100:
        render_insight_box(
            "✅",
            "Recommendation: PROCEED",
            f"This promotion is projected to be **highly profitable** with **{results['roi']:.0f}% ROI**. "
            f"Expected to generate **{format_currency(results['incremental_revenue'])}** in incremental revenue "
            f"with a margin impact of **{format_currency(results['margin_impact'])}** after budget costs.",
            "success"
        )
    elif results['roi'] >= 0:
        render_insight_box(
            "⚠️",
            "Recommendation: CONSIDER ADJUSTMENTS",
            f"This promotion shows **marginal profitability** with **{results['roi']:.0f}% ROI**. "
            f"Consider increasing the lift factor through better marketing or reducing the discount depth "
            f"to improve returns.",
            "warning"
        )
    else:
        render_insight_box(
            "❌",
            "Recommendation: DO NOT PROCEED",
            f"This promotion is projected to be **unprofitable** with **{results['roi']:.0f}% ROI**. "
            f"The discount depth and budget costs exceed the incremental revenue generated. "
            f"Consider a lower discount or targeting a higher-margin category.",
            "danger"
        )
    
    # Suggestions for improvement
    st.markdown("")
    st.markdown("##### 💡 Optimization Suggestions")
    
    suggestions = []
    
    if results['discount_pct'] > 25:
        suggestions.append({
            "icon": "🏷️",
            "text": f"**Reduce Discount:** Current {results['discount_pct']}% discount may be too deep. "
                   f"Try 15-20% for better margins while maintaining customer interest."
        })
    
    if results['lift_multiplier'] < 1.5:
        suggestions.append({
            "icon": "📈",
            "text": "**Increase Lift:** Enhance promotional visibility through email campaigns, "
                   "push notifications, and homepage placement to boost the lift factor."
        })
    
    if params.get('category') == 'All':
        suggestions.append({
            "icon": "🎯",
            "text": "**Target High-Margin Categories:** Focus on Electronics or Beauty categories "
                   "which typically have higher margins to improve ROI."
        })
    
    if results['budget'] > results['incremental_revenue'] * 0.5:
        suggestions.append({
            "icon": "💰",
            "text": "**Optimize Budget:** Marketing budget is high relative to expected returns. "
                   "Consider reallocating to digital channels with lower CPM."
        })
    
    if not suggestions:
        suggestions.append({
            "icon": "✅",
            "text": "**Well Optimized:** This promotion scenario is well-configured. "
                   "Monitor actual performance and adjust in real-time if needed."
        })
    
    for suggestion in suggestions:
        render_recommendation_card(suggestion['icon'], suggestion['text'])


def render_roi_analysis(campaigns_df, sales_df, products_df):
    """
    Render ROI analysis for campaigns.
    
    Args:
        campaigns_df: Campaigns DataFrame
        sales_df: Sales DataFrame
        products_df: Products DataFrame
    """
    st.markdown("#### 📈 Campaign ROI Analysis")
    st.markdown("Analyze return on investment across different campaign parameters.")
    
    st.markdown("")
    
    # =========================================================================
    # SENSITIVITY ANALYSIS
    # =========================================================================
    st.markdown("##### 🔬 Discount vs Lift Sensitivity Analysis")
    st.markdown("See how different discount levels and lift factors affect ROI.")
    
    # Get baseline metrics
    valid_sales = sales_df[sales_df['order_time'].notna()]
    
    if len(valid_sales) > 0:
        date_range = (valid_sales['order_time'].max() - valid_sales['order_time'].min()).days
        date_range = max(1, date_range)
        
        baseline_daily_revenue = valid_sales['revenue'].sum() / date_range
        baseline_avg_price = valid_sales['selling_price_aed'].mean()
        baseline_daily_units = valid_sales['qty'].sum() / date_range
        
        # Assume cost is 55% of price
        avg_cost = baseline_avg_price * 0.55
    else:
        baseline_daily_revenue = 10000
        baseline_avg_price = 200
        baseline_daily_units = 50
        avg_cost = 110
    
    # Create sensitivity matrix
    discounts = [10, 15, 20, 25, 30, 35, 40]
    lifts = [1.2, 1.3, 1.4, 1.5, 1.6, 1.8, 2.0]
    
    # Calculate ROI for each combination (7-day campaign, 50K budget)
    duration = 7
    budget = 50000
    
    roi_matrix = []
    for discount in discounts:
        row = []
        for lift in lifts:
            promo_price = baseline_avg_price * (1 - discount / 100)
            promo_units = baseline_daily_units * lift * duration
            baseline_units = baseline_daily_units * duration
            
            promo_revenue = promo_units * promo_price
            baseline_revenue = baseline_units * baseline_avg_price
            
            incremental_revenue = promo_revenue - baseline_revenue
            roi = (incremental_revenue - budget) / budget * 100 if budget > 0 else 0
            
            row.append(roi)
        roi_matrix.append(row)
    
    roi_df = pd.DataFrame(roi_matrix, index=[f"{d}%" for d in discounts], columns=[f"{l}x" for l in lifts])
    
    # Heatmap
    fig = px.imshow(
        roi_df,
        labels=dict(x="Lift Factor", y="Discount %", color="ROI %"),
        color_continuous_scale=['#ef4444', '#f59e0b', '#10b981'],
        aspect='auto',
        text_auto='.0f'
    )
    fig = apply_chart_style(fig, height=400)
    fig.update_layout(
        xaxis_title="Sales Lift Factor",
        yaxis_title="Discount Percentage"
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.caption("ROI calculated for 7-day campaign with AED 50,000 budget. Green = profitable, Red = unprofitable.")
    
    # =========================================================================
    # BREAK-EVEN ANALYSIS
    # =========================================================================
    st.markdown("")
    st.markdown("##### ⚖️ Break-Even Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Break-even lift by discount
        render_chart_title("Break-Even Lift Factor by Discount", "📊")
        
        break_even_data = []
        for discount in discounts:
            promo_price = baseline_avg_price * (1 - discount / 100)
            
            # Solve for lift where incremental revenue = budget
            # (lift * base_units * promo_price) - (base_units * base_price) = budget
            # lift = (budget + base_revenue) / (base_units * promo_price)
            base_revenue = baseline_daily_units * duration * baseline_avg_price
            base_units = baseline_daily_units * duration
            
            if promo_price > 0 and base_units > 0:
                break_even_lift = (budget + base_revenue) / (base_units * promo_price)
            else:
                break_even_lift = 0
            
            break_even_data.append({
                'Discount': f"{discount}%",
                'Break-Even Lift': break_even_lift
            })
        
        be_df = pd.DataFrame(break_even_data)
        
        fig = px.bar(
            be_df,
            x='Discount',
            y='Break-Even Lift',
            color_discrete_sequence=['#6366f1'],
            text=be_df['Break-Even Lift'].apply(lambda x: f"{x:.2f}x")
        )
        fig = apply_chart_style(fig, height=300, show_legend=False)
        fig.update_traces(textposition='outside')
        fig.update_layout(
            xaxis_title="Discount Level",
            yaxis_title="Required Lift Factor"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Budget efficiency curve
        render_chart_title("Budget Efficiency Curve", "💰")
        
        budgets = [10000, 25000, 50000, 75000, 100000, 150000, 200000]
        
        efficiency_data = []
        for b in budgets:
            # Assume 20% discount, 1.5x lift
            lift = 1.5
            discount = 20
            promo_price = baseline_avg_price * (1 - discount / 100)
            promo_units = baseline_daily_units * lift * duration
            baseline_units = baseline_daily_units * duration
            
            promo_revenue = promo_units * promo_price
            baseline_revenue = baseline_units * baseline_avg_price
            incremental = promo_revenue - baseline_revenue
            
            roi = (incremental - b) / b * 100 if b > 0 else 0
            
            efficiency_data.append({
                'Budget': b,
                'ROI': roi
            })
        
        eff_df = pd.DataFrame(efficiency_data)
        
        fig = px.line(
            eff_df,
            x='Budget',
            y='ROI',
            markers=True,
            color_discrete_sequence=['#10b981']
        )
        fig = apply_chart_style(fig, height=300, show_legend=False)
        fig.update_layout(
            xaxis_title="Campaign Budget (AED)",
            yaxis_title="ROI %"
        )
        
        # Add break-even line
        fig.add_hline(y=0, line_dash="dash", line_color="#ef4444", annotation_text="Break-even")
        
        st.plotly_chart(fig, use_container_width=True)
    
    # =========================================================================
    # CATEGORY ROI COMPARISON
    # =========================================================================
    st.markdown("")
    render_chart_title("Estimated ROI by Category (20% discount, 1.5x lift)", "📦")
    
    # Calculate ROI by category
    category_roi = []
    
    for category in CATEGORIES:
        cat_sales = valid_sales[valid_sales['category'] == category] if 'category' in valid_sales.columns else valid_sales
        
        if len(cat_sales) > 0:
            cat_daily_revenue = cat_sales['revenue'].sum() / date_range
            cat_avg_price = cat_sales['selling_price_aed'].mean()
            cat_daily_units = cat_sales['qty'].sum() / date_range
            
            # Assume 20% discount, 1.5x lift, 7 days, 50K budget
            promo_price = cat_avg_price * 0.8
            promo_units = cat_daily_units * 1.5 * 7
            baseline_units = cat_daily_units * 7
            
            promo_revenue = promo_units * promo_price
            baseline_revenue = baseline_units * cat_avg_price
            incremental = promo_revenue - baseline_revenue
            
            roi = (incremental - 50000) / 50000 * 100
            
            category_roi.append({
                'Category': category,
                'ROI': roi,
                'Incremental Revenue': incremental
            })
    
    cat_roi_df = pd.DataFrame(category_roi)
    cat_roi_df = cat_roi_df.sort_values('ROI', ascending=True)
    
    fig = px.bar(
        cat_roi_df,
        x='ROI',
        y='Category',
        orientation='h',
        color='ROI',
        color_continuous_scale=['#ef4444', '#f59e0b', '#10b981'],
        text=cat_roi_df['ROI'].apply(lambda x: f"{x:.0f}%")
    )
    fig = apply_chart_style(fig, height=300, show_legend=False)
    fig.update_traces(textposition='outside')
    fig.update_layout(
        xaxis_title="Projected ROI %",
        yaxis_title="",
        coloraxis_showscale=False
    )
    
    # Add break-even line
    fig.add_vline(x=0, line_dash="dash", line_color="#6366f1", annotation_text="Break-even")
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Insights
    st.markdown("")
    
    best_category = cat_roi_df.iloc[-1] if len(cat_roi_df) > 0 else None
    worst_category = cat_roi_df.iloc[0] if len(cat_roi_df) > 0 else None
    
    col1, col2 = st.columns(2)
    
    with col1:
        if best_category is not None:
            render_insight_box(
                "🏆",
                f"Best ROI: {best_category['Category']}",
                f"Promotions in **{best_category['Category']}** show the highest projected ROI at "
                f"**{best_category['ROI']:.0f}%**. Consider prioritizing this category for upcoming campaigns.",
                "success"
            )
    
    with col2:
        if worst_category is not None and worst_category['ROI'] < 0:
            render_insight_box(
                "⚠️",
                f"Low ROI: {worst_category['Category']}",
                f"**{worst_category['Category']}** shows negative ROI at **{worst_category['ROI']:.0f}%**. "
                f"Avoid deep discounts in this category or increase marketing efficiency.",
                "warning"
            )
        else:
            render_insight_box(
                "✅",
                "All Categories Profitable",
                "All categories show positive ROI at standard discount and lift levels. "
                "Portfolio approach to promotions recommended.",
                "success"
            )

# =============================================================================
# STORE PERFORMANCE TAB
# =============================================================================
# This module provides detailed store-level performance analysis including
# rankings, comparisons, and operational insights.
# =============================================================================

def render_store_performance(stores_df, sales_df, inventory_df):
    """
    Render the Store Performance tab with detailed store analysis.
    
    This tab provides:
        1. Store Performance Rankings
        2. Store Comparison Tool
        3. Store Health Scorecards
        4. Geographic Performance Map
        5. Channel Mix by Store
    
    Args:
        stores_df: Stores DataFrame
        sales_df: Sales DataFrame
        inventory_df: Inventory DataFrame
    """
    render_section_header(
        "🏪",
        "Store Performance Analysis",
        "Compare and analyze performance across all retail locations"
    )
    
    # =========================================================================
    # FILTERS
    # =========================================================================
    st.markdown("##### 🎛️ Filters")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        city_options = ['All'] + STANDARD_CITIES
        selected_city = st.selectbox(
            "🏙️ City",
            options=city_options,
            key="store_perf_city"
        )
    
    with col2:
        channel_options = ['All'] + CHANNELS
        selected_channel = st.selectbox(
            "📱 Channel",
            options=channel_options,
            key="store_perf_channel"
        )
    
    with col3:
        metric_options = ['Revenue', 'Orders', 'Units Sold', 'Avg Order Value']
        selected_metric = st.selectbox(
            "📊 Ranking Metric",
            options=metric_options,
            key="store_perf_metric"
        )
    
    render_divider_subtle()
    
    # =========================================================================
    # CALCULATE STORE METRICS
    # =========================================================================
    store_metrics = calculate_store_metrics(sales_df, inventory_df, stores_df)
    
    # Apply filters
    filtered_metrics = store_metrics.copy()
    
    if selected_city != 'All':
        filtered_metrics = filtered_metrics[filtered_metrics['city'] == selected_city]
    
    if selected_channel != 'All':
        filtered_metrics = filtered_metrics[filtered_metrics['channel'] == selected_channel]
    
    if len(filtered_metrics) == 0:
        render_empty_state(
            "🏪",
            "No Stores Found",
            "No stores match the selected filters."
        )
        return
    
    # =========================================================================
    # KPIs
    # =========================================================================
    total_stores = len(filtered_metrics)
    total_revenue = filtered_metrics['revenue'].sum()
    avg_revenue = filtered_metrics['revenue'].mean()
    total_orders = filtered_metrics['orders'].sum()
    avg_aov = filtered_metrics['aov'].mean()
    
    kpis = [
        {"icon": "🏪", "value": str(total_stores), "label": "Total Stores", "type": "primary"},
        {"icon": "💰", "value": format_currency(total_revenue), "label": "Total Revenue", "type": "success"},
        {"icon": "📊", "value": format_currency(avg_revenue), "label": "Avg Revenue/Store", "type": "secondary"},
        {"icon": "🛒", "value": format_number(total_orders), "label": "Total Orders", "type": "accent"},
        {"icon": "💵", "value": format_currency(avg_aov), "label": "Avg AOV", "type": "warning"}
    ]
    
    render_kpi_row(kpis)
    
    st.markdown("")
    
    # =========================================================================
    # SUB-TABS
    # =========================================================================
    store_tabs = st.tabs([
        "🏆 Rankings",
        "📊 Comparison",
        "📋 Scorecards",
        "🗺️ Geographic View"
    ])
    
    with store_tabs[0]:
        render_store_rankings(filtered_metrics, selected_metric)
    
    with store_tabs[1]:
        render_store_comparison(filtered_metrics, stores_df)
    
    with store_tabs[2]:
        render_store_scorecards(filtered_metrics)
    
    with store_tabs[3]:
        render_store_geographic(filtered_metrics)


def calculate_store_metrics(sales_df, inventory_df, stores_df):
    """
    Calculate comprehensive metrics for each store.
    
    Args:
        sales_df: Sales DataFrame
        inventory_df: Inventory DataFrame
        stores_df: Stores DataFrame
    
    Returns:
        DataFrame: Store metrics
    """
    # Filter valid sales
    valid_sales = sales_df[sales_df['order_time'].notna()].copy()
    
    # Aggregate sales by store
    store_sales = valid_sales.groupby('store_id').agg({
        'revenue': 'sum',
        'order_id': 'nunique',
        'qty': 'sum',
        'discount_pct': 'mean',
        'return_flag': 'mean'
    }).reset_index()
    
    store_sales.columns = ['store_id', 'revenue', 'orders', 'units', 'avg_discount', 'return_rate']
    store_sales['aov'] = store_sales['revenue'] / store_sales['orders']
    store_sales['return_rate'] = store_sales['return_rate'] * 100
    
    # Get latest inventory metrics
    if len(inventory_df) > 0:
        latest_date = inventory_df['snapshot_date'].max()
        latest_inventory = inventory_df[inventory_df['snapshot_date'] == latest_date]
        
        store_inventory = latest_inventory.groupby('store_id').agg({
            'stock_on_hand': 'sum',
            'product_id': 'nunique'
        }).reset_index()
        store_inventory.columns = ['store_id', 'total_stock', 'sku_count']
        
        # Merge inventory
        store_sales = store_sales.merge(store_inventory, on='store_id', how='left')
        store_sales['total_stock'] = store_sales['total_stock'].fillna(0)
        store_sales['sku_count'] = store_sales['sku_count'].fillna(0)
    else:
        store_sales['total_stock'] = 0
        store_sales['sku_count'] = 0
    
    # Merge store info
    store_info = stores_df[['store_id', 'city', 'channel']].copy()
    store_info['city'] = store_info['city'].replace(CITY_MAPPING)
    
    store_metrics = store_sales.merge(store_info, on='store_id', how='left')
    
    # Calculate percentile ranks
    store_metrics['revenue_rank'] = store_metrics['revenue'].rank(ascending=False)
    store_metrics['revenue_percentile'] = store_metrics['revenue'].rank(pct=True) * 100
    
    return store_metrics


def render_store_rankings(store_metrics, selected_metric):
    """
    Render store performance rankings.
    
    Args:
        store_metrics: Store metrics DataFrame
        selected_metric: Metric to rank by
    """
    st.markdown("#### 🏆 Store Performance Rankings")
    st.markdown("Top and bottom performing stores based on selected metric.")
    
    st.markdown("")
    
    # Map metric selection to column
    metric_map = {
        'Revenue': 'revenue',
        'Orders': 'orders',
        'Units Sold': 'units',
        'Avg Order Value': 'aov'
    }
    
    metric_col = metric_map.get(selected_metric, 'revenue')
    
    # Sort by selected metric
    sorted_stores = store_metrics.sort_values(metric_col, ascending=False)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Top performers
        render_chart_title(f"Top 10 Stores by {selected_metric}", "🥇")
        
        top_10 = sorted_stores.head(10)
        
        fig = px.bar(
            top_10.sort_values(metric_col, ascending=True),
            x=metric_col,
            y='store_id',
            orientation='h',
            color=metric_col,
            color_continuous_scale=['#6366f1', '#10b981']
        )
        fig = apply_chart_style(fig, height=350, show_legend=False)
        fig.update_layout(
            xaxis_title=selected_metric,
            yaxis_title="",
            coloraxis_showscale=False
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Bottom performers
        render_chart_title(f"Bottom 10 Stores by {selected_metric}", "📉")
        
        bottom_10 = sorted_stores.tail(10)
        
        fig = px.bar(
            bottom_10.sort_values(metric_col, ascending=True),
            x=metric_col,
            y='store_id',
            orientation='h',
            color=metric_col,
            color_continuous_scale=['#ef4444', '#f59e0b']
        )
        fig = apply_chart_style(fig, height=350, show_legend=False)
        fig.update_layout(
            xaxis_title=selected_metric,
            yaxis_title="",
            coloraxis_showscale=False
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Distribution chart
    st.markdown("")
    render_chart_title(f"{selected_metric} Distribution Across Stores", "📊")
    
    fig = px.histogram(
        store_metrics,
        x=metric_col,
        nbins=20,
        color_discrete_sequence=['#6366f1']
    )
    fig = apply_chart_style(fig, height=280, show_legend=False)
    fig.update_layout(
        xaxis_title=selected_metric,
        yaxis_title="Number of Stores"
    )
    
    # Add mean line
    mean_val = store_metrics[metric_col].mean()
    fig.add_vline(
        x=mean_val,
        line_dash="dash",
        line_color="#f59e0b",
        annotation_text=f"Mean: {mean_val:,.0f}"
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Rankings table
    st.markdown("")
    st.markdown("##### 📋 Complete Rankings")
    
    display_df = sorted_stores[[
        'store_id', 'city', 'channel', 'revenue', 'orders', 'units', 'aov', 'revenue_rank'
    ]].copy()
    
    display_df['revenue'] = display_df['revenue'].apply(lambda x: format_currency(x))
    display_df['orders'] = display_df['orders'].apply(lambda x: format_number(x))
    display_df['units'] = display_df['units'].apply(lambda x: format_number(x))
    display_df['aov'] = display_df['aov'].apply(lambda x: format_currency(x))
    display_df['revenue_rank'] = display_df['revenue_rank'].apply(lambda x: f"#{int(x)}")
    
    display_df.columns = ['Store ID', 'City', 'Channel', 'Revenue', 'Orders', 'Units', 'AOV', 'Rank']
    
    st.dataframe(display_df, use_container_width=True, hide_index=True, height=400)


def render_store_comparison(store_metrics, stores_df):
    """
    Render store comparison tool.
    
    Args:
        store_metrics: Store metrics DataFrame
        stores_df: Stores DataFrame
    """
    st.markdown("#### 📊 Store Comparison Tool")
    st.markdown("Select stores to compare side-by-side.")
    
    st.markdown("")
    
    # Store selection
    store_options = store_metrics['store_id'].tolist()
    
    col1, col2 = st.columns(2)
    
    with col1:
        store_1 = st.selectbox(
            "Select Store 1",
            options=store_options,
            key="compare_store_1"
        )
    
    with col2:
        remaining_stores = [s for s in store_options if s != store_1]
        store_2 = st.selectbox(
            "Select Store 2",
            options=remaining_stores,
            key="compare_store_2"
        )
    
    # Get store data
    store_1_data = store_metrics[store_metrics['store_id'] == store_1].iloc[0]
    store_2_data = store_metrics[store_metrics['store_id'] == store_2].iloc[0]
    
    st.markdown("")
    
    # Comparison cards
    col1, col2 = st.columns(2)
    
    with col1:
        render_store_comparison_card(store_1_data, "🏪")
    
    with col2:
        render_store_comparison_card(store_2_data, "🏬")
    
    # Comparison chart
    st.markdown("")
    render_chart_title("Metric Comparison", "📊")
    
    metrics_to_compare = ['revenue', 'orders', 'units', 'aov']
    metric_labels = ['Revenue', 'Orders', 'Units', 'AOV']
    
    comparison_data = []
    for metric, label in zip(metrics_to_compare, metric_labels):
        val_1 = store_1_data[metric]
        val_2 = store_2_data[metric]
        
        # Normalize for visualization
        max_val = max(val_1, val_2)
        if max_val > 0:
            norm_1 = val_1 / max_val * 100
            norm_2 = val_2 / max_val * 100
        else:
            norm_1 = norm_2 = 0
        
        comparison_data.append({'Metric': label, 'Store': store_1, 'Value': norm_1, 'Actual': val_1})
        comparison_data.append({'Metric': label, 'Store': store_2, 'Value': norm_2, 'Actual': val_2})
    
    comp_df = pd.DataFrame(comparison_data)
    
    fig = px.bar(
        comp_df,
        x='Metric',
        y='Value',
        color='Store',
        barmode='group',
        color_discrete_sequence=['#6366f1', '#10b981']
    )
    fig = apply_chart_style(fig, height=320)
    fig.update_layout(
        xaxis_title="",
        yaxis_title="Relative Performance (%)"
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Winner summary
    st.markdown("")
    st.markdown("##### 🏆 Comparison Summary")
    
    winners = []
    for metric, label in zip(metrics_to_compare, metric_labels):
        val_1 = store_1_data[metric]
        val_2 = store_2_data[metric]
        
        if val_1 > val_2:
            winner = store_1
            diff = (val_1 - val_2) / val_2 * 100 if val_2 > 0 else 100
        else:
            winner = store_2
            diff = (val_2 - val_1) / val_1 * 100 if val_1 > 0 else 100
        
        winners.append({
            'Metric': label,
            'Winner': winner,
            'Lead': f"+{diff:.1f}%"
        })
    
    winner_df = pd.DataFrame(winners)
    st.dataframe(winner_df, use_container_width=True, hide_index=True)


def render_store_comparison_card(store_data, icon):
    """
    Render a single store comparison card.
    
    Args:
        store_data: Store data row
        icon: Icon to display
    """
    st.markdown(f'''
    <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(99, 102, 241, 0.3);
                border-radius: 12px; padding: 20px;">
        <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 16px;">
            <span style="font-size: 2rem;">{icon}</span>
            <div>
                <div style="font-size: 1.1rem; font-weight: 600; color: white;">{store_data['store_id']}</div>
                <div style="font-size: 0.85rem; color: #a1a1aa;">{store_data['city']} • {store_data['channel']}</div>
            </div>
        </div>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px;">
            <div style="background: rgba(255,255,255,0.02); border-radius: 8px; padding: 12px;">
                <div style="font-size: 0.75rem; color: #71717a;">Revenue</div>
                <div style="font-size: 1.1rem; font-weight: 600; color: #10b981;">{format_currency(store_data['revenue'])}</div>
            </div>
            <div style="background: rgba(255,255,255,0.02); border-radius: 8px; padding: 12px;">
                <div style="font-size: 0.75rem; color: #71717a;">Orders</div>
                <div style="font-size: 1.1rem; font-weight: 600; color: #6366f1;">{format_number(store_data['orders'])}</div>
            </div>
            <div style="background: rgba(255,255,255,0.02); border-radius: 8px; padding: 12px;">
                <div style="font-size: 0.75rem; color: #71717a;">Units Sold</div>
                <div style="font-size: 1.1rem; font-weight: 600; color: #8b5cf6;">{format_number(store_data['units'])}</div>
            </div>
            <div style="background: rgba(255,255,255,0.02); border-radius: 8px; padding: 12px;">
                <div style="font-size: 0.75rem; color: #71717a;">AOV</div>
                <div style="font-size: 1.1rem; font-weight: 600; color: #f59e0b;">{format_currency(store_data['aov'])}</div>
            </div>
        </div>
        <div style="margin-top: 12px; padding-top: 12px; border-top: 1px solid rgba(255,255,255,0.1);
                    display: flex; justify-content: space-between; font-size: 0.85rem;">
            <span style="color: #71717a;">Rank: <span style="color: #6366f1;">#{int(store_data['revenue_rank'])}</span></span>
            <span style="color: #71717a;">Stock: <span style="color: #10b981;">{format_number(store_data['total_stock'])}</span></span>
        </div>
    </div>
    ''', unsafe_allow_html=True)


def render_store_scorecards(store_metrics):
    """
    Render store health scorecards.
    
    Args:
        store_metrics: Store metrics DataFrame
    """
    st.markdown("#### 📋 Store Health Scorecards")
    st.markdown("Comprehensive health scores based on multiple performance indicators.")
    
    st.markdown("")
    
    # Calculate health scores
    scorecard_df = store_metrics.copy()
    
    # Normalize each metric to 0-100 scale
    for col in ['revenue', 'orders', 'aov', 'units']:
        min_val = scorecard_df[col].min()
        max_val = scorecard_df[col].max()
        if max_val > min_val:
            scorecard_df[f'{col}_score'] = ((scorecard_df[col] - min_val) / (max_val - min_val)) * 100
        else:
            scorecard_df[f'{col}_score'] = 50
    
    # Return rate score (lower is better)
    max_return = scorecard_df['return_rate'].max()
    if max_return > 0:
        scorecard_df['return_score'] = (1 - scorecard_df['return_rate'] / max_return) * 100
    else:
        scorecard_df['return_score'] = 100
    
    # Overall health score (weighted average)
    scorecard_df['health_score'] = (
        scorecard_df['revenue_score'] * 0.35 +
        scorecard_df['orders_score'] * 0.25 +
        scorecard_df['aov_score'] * 0.20 +
        scorecard_df['units_score'] * 0.10 +
        scorecard_df['return_score'] * 0.10
    )
    
    # Categorize health
    scorecard_df['health_status'] = scorecard_df['health_score'].apply(
        lambda x: 'Excellent' if x >= 80 else 'Good' if x >= 60 else 'Fair' if x >= 40 else 'Needs Attention'
    )
    
    # Health distribution
    col1, col2 = st.columns(2)
    
    with col1:
        render_chart_title("Health Score Distribution", "📊")
        
        fig = px.histogram(
            scorecard_df,
            x='health_score',
            nbins=10,
            color_discrete_sequence=['#6366f1']
        )
        fig = apply_chart_style(fig, height=280, show_legend=False)
        fig.update_layout(
            xaxis_title="Health Score",
            yaxis_title="Number of Stores"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        render_chart_title("Health Status Breakdown", "📈")
        
        status_counts = scorecard_df['health_status'].value_counts().reset_index()
        status_counts.columns = ['status', 'count']
        
        status_colors = {
            'Excellent': '#10b981',
            'Good': '#84cc16',
            'Fair': '#f59e0b',
            'Needs Attention': '#ef4444'
        }
        
        fig = px.pie(
            status_counts,
            values='count',
            names='status',
            color='status',
            color_discrete_map=status_colors,
            hole=0.4
        )
        fig = apply_chart_style(fig, height=280)
        st.plotly_chart(fig, use_container_width=True)
    
    # Top and bottom health scores
    st.markdown("")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("##### 🌟 Top Health Scores")
        
        top_health = scorecard_df.nlargest(10, 'health_score')[
            ['store_id', 'city', 'channel', 'health_score', 'health_status']
        ]
        top_health['health_score'] = top_health['health_score'].apply(lambda x: f"{x:.1f}")
        top_health.columns = ['Store', 'City', 'Channel', 'Score', 'Status']
        
        st.dataframe(top_health, use_container_width=True, hide_index=True)
    
    with col2:
        st.markdown("##### ⚠️ Stores Needing Attention")
        
        bottom_health = scorecard_df.nsmallest(10, 'health_score')[
            ['store_id', 'city', 'channel', 'health_score', 'health_status']
        ]
        bottom_health['health_score'] = bottom_health['health_score'].apply(lambda x: f"{x:.1f}")
        bottom_health.columns = ['Store', 'City', 'Channel', 'Score', 'Status']
        
        st.dataframe(bottom_health, use_container_width=True, hide_index=True)
    
    # Score component breakdown
    st.markdown("")
    render_chart_title("Score Components for Top 10 Stores", "📊")
    
    top_10_stores = scorecard_df.nlargest(10, 'health_score')
    
    component_data = []
    for _, row in top_10_stores.iterrows():
        component_data.append({'Store': row['store_id'], 'Component': 'Revenue', 'Score': row['revenue_score']})
        component_data.append({'Store': row['store_id'], 'Component': 'Orders', 'Score': row['orders_score']})
        component_data.append({'Store': row['store_id'], 'Component': 'AOV', 'Score': row['aov_score']})
        component_data.append({'Store': row['store_id'], 'Component': 'Units', 'Score': row['units_score']})
        component_data.append({'Store': row['store_id'], 'Component': 'Returns', 'Score': row['return_score']})
    
    comp_df = pd.DataFrame(component_data)
    
    fig = px.bar(
        comp_df,
        x='Store',
        y='Score',
        color='Component',
        barmode='group',
        color_discrete_sequence=get_chart_colors()
    )
    fig = apply_chart_style(fig, height=350)
    fig.update_layout(
        xaxis_title="",
        yaxis_title="Component Score",
        xaxis_tickangle=-45
    )
    st.plotly_chart(fig, use_container_width=True)


def render_store_geographic(store_metrics):
    """
    Render geographic view of store performance.
    
    Args:
        store_metrics: Store metrics DataFrame
    """
    st.markdown("#### 🗺️ Geographic Performance View")
    st.markdown("Store performance distribution across cities.")
    
    st.markdown("")
    
    # City aggregation
    city_metrics = store_metrics.groupby('city').agg({
        'store_id': 'count',
        'revenue': ['sum', 'mean'],
        'orders': ['sum', 'mean'],
        'aov': 'mean'
    }).reset_index()
    
    city_metrics.columns = ['city', 'store_count', 'total_revenue', 'avg_revenue', 
                           'total_orders', 'avg_orders', 'avg_aov']
    
    # City cards
    city_colors = {'Dubai': '#6366f1', 'Abu Dhabi': '#10b981', 'Sharjah': '#f59e0b'}
    
    cols = st.columns(len(city_metrics))
    
    for col, (_, row) in zip(cols, city_metrics.iterrows()):
        with col:
            color = city_colors.get(row['city'], '#6366f1')
            st.markdown(f'''
            <div style="background: rgba(255,255,255,0.03); border: 1px solid {color}40;
                        border-top: 4px solid {color}; border-radius: 12px; padding: 20px; text-align: center;">
                <div style="font-size: 1.3rem; font-weight: 600; color: {color}; margin-bottom: 16px;">
                    🏙️ {row['city']}
                </div>
                <div style="font-size: 2rem; font-weight: 700; color: white; margin-bottom: 8px;">
                    {int(row['store_count'])} Stores
                </div>
                <div style="display: grid; grid-template-columns: 1fr; gap: 8px; margin-top: 16px; text-align: left;">
                    <div style="display: flex; justify-content: space-between;">
                        <span style="color: #71717a; font-size: 0.85rem;">Total Revenue</span>
                        <span style="color: white; font-weight: 600;">{format_currency(row['total_revenue'])}</span>
                    </div>
                    <div style="display: flex; justify-content: space-between;">
                        <span style="color: #71717a; font-size: 0.85rem;">Avg/Store</span>
                        <span style="color: white; font-weight: 600;">{format_currency(row['avg_revenue'])}</span>
                    </div>
                    <div style="display: flex; justify-content: space-between;">
                        <span style="color: #71717a; font-size: 0.85rem;">Avg AOV</span>
                        <span style="color: white; font-weight: 600;">{format_currency(row['avg_aov'])}</span>
                    </div>
                </div>
            </div>
            ''', unsafe_allow_html=True)
    
    st.markdown("")
    
    # City comparison charts
    col1, col2 = st.columns(2)
    
    with col1:
        render_chart_title("Total Revenue by City", "💰")
        
        fig = px.bar(
            city_metrics,
            x='city',
            y='total_revenue',
            color='city',
            color_discrete_map=city_colors,
            text=city_metrics['total_revenue'].apply(lambda x: format_currency(x))
        )
        fig = apply_chart_style(fig, height=300, show_legend=False)
        fig.update_traces(textposition='outside')
        fig.update_layout(xaxis_title="", yaxis_title="Revenue (AED)")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        render_chart_title("Average Revenue per Store", "📊")
        
        fig = px.bar(
            city_metrics,
            x='city',
            y='avg_revenue',
            color='city',
            color_discrete_map=city_colors,
            text=city_metrics['avg_revenue'].apply(lambda x: format_currency(x))
        )
        fig = apply_chart_style(fig, height=300, show_legend=False)
        fig.update_traces(textposition='outside')
        fig.update_layout(xaxis_title="", yaxis_title="Avg Revenue (AED)")
        st.plotly_chart(fig, use_container_width=True)
    
    # Store scatter by city
    st.markdown("")
    render_chart_title("Store Performance Scatter: Revenue vs Orders", "📈")
    
    fig = px.scatter(
        store_metrics,
        x='orders',
        y='revenue',
        color='city',
        color_discrete_map=city_colors,
        size='aov',
        hover_data=['store_id', 'channel'],
        size_max=20
    )
    fig = apply_chart_style(fig, height=400)
    fig.update_layout(
        xaxis_title="Number of Orders",
        yaxis_title="Revenue (AED)"
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.caption("Bubble size represents Average Order Value (AOV)")


# =============================================================================
# TIME PATTERN ANALYSIS TAB
# =============================================================================
# This module provides time-based pattern analysis including hourly, daily,
# weekly, and monthly patterns in sales data.
# =============================================================================

def render_time_patterns(sales_df):
    """
    Render the Time Pattern Analysis tab.
    
    This tab provides:
        1. Hourly Sales Patterns
        2. Day-of-Week Analysis
        3. Monthly Trends
        4. Peak Period Identification
        5. Seasonality Analysis
    
    Args:
        sales_df: Sales DataFrame
    """
    render_section_header(
        "⏰",
        "Time Pattern Analysis",
        "Discover sales patterns across hours, days, weeks, and months"
    )
    
    # Filter valid sales with timestamps
    valid_sales = sales_df[sales_df['order_time'].notna()].copy()
    
    if len(valid_sales) == 0:
        render_empty_state(
            "⏰",
            "No Time Data Available",
            "No sales with valid timestamps found for pattern analysis."
        )
        return
    
    # Extract time components
    valid_sales['hour'] = valid_sales['order_time'].dt.hour
    valid_sales['day_of_week'] = valid_sales['order_time'].dt.day_name()
    valid_sales['day_num'] = valid_sales['order_time'].dt.dayofweek
    valid_sales['week'] = valid_sales['order_time'].dt.isocalendar().week
    valid_sales['month_name'] = valid_sales['order_time'].dt.month_name()
    valid_sales['month_num'] = valid_sales['order_time'].dt.month
    valid_sales['date'] = valid_sales['order_time'].dt.date
    
    # =========================================================================
    # KPIs
    # =========================================================================
    # Find peak periods
    hourly_revenue = valid_sales.groupby('hour')['revenue'].sum()
    peak_hour = hourly_revenue.idxmax()
    
    daily_revenue = valid_sales.groupby('day_num')['revenue'].sum()
    peak_day_num = daily_revenue.idxmax()
    day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    peak_day = day_names[peak_day_num]
    
    monthly_revenue = valid_sales.groupby('month_num')['revenue'].sum()
    peak_month_num = monthly_revenue.idxmax()
    month_names = ['', 'January', 'February', 'March', 'April', 'May', 'June',
                   'July', 'August', 'September', 'October', 'November', 'December']
    peak_month = month_names[peak_month_num]
    
    # Average daily metrics
    daily_metrics = valid_sales.groupby('date').agg({
        'revenue': 'sum',
        'order_id': 'nunique'
    })
    avg_daily_revenue = daily_metrics['revenue'].mean()
    avg_daily_orders = daily_metrics['order_id'].mean()
    
    kpis = [
        {"icon": "⏰", "value": f"{peak_hour}:00", "label": "Peak Hour", "type": "primary"},
        {"icon": "📅", "value": peak_day, "label": "Peak Day", "type": "secondary"},
        {"icon": "📆", "value": peak_month, "label": "Peak Month", "type": "accent"},
        {"icon": "💰", "value": format_currency(avg_daily_revenue), "label": "Avg Daily Revenue", "type": "success"},
        {"icon": "🛒", "value": f"{avg_daily_orders:.0f}", "label": "Avg Daily Orders", "type": "warning"}
    ]
    
    render_kpi_row(kpis)
    
    st.markdown("")
    
    # =========================================================================
    # SUB-TABS
    # =========================================================================
    time_tabs = st.tabs([
        "🕐 Hourly",
        "📅 Daily",
        "📆 Weekly",
        "📈 Monthly",
        "🔥 Heatmaps"
    ])
    
    with time_tabs[0]:
        render_hourly_patterns(valid_sales)
    
    with time_tabs[1]:
        render_daily_patterns(valid_sales)
    
    with time_tabs[2]:
        render_weekly_patterns(valid_sales)
    
    with time_tabs[3]:
        render_monthly_patterns(valid_sales)
    
    with time_tabs[4]:
        render_time_heatmaps(valid_sales)


def render_hourly_patterns(sales_df):
    """
    Render hourly sales patterns.
    
    Args:
        sales_df: Sales DataFrame with hour column
    """
    st.markdown("#### 🕐 Hourly Sales Patterns")
    st.markdown("Understand when customers are most active throughout the day.")
    
    st.markdown("")
    
    # Hourly aggregation
    hourly_metrics = sales_df.groupby('hour').agg({
        'revenue': 'sum',
        'order_id': 'nunique',
        'qty': 'sum'
    }).reset_index()
    
    hourly_metrics.columns = ['hour', 'revenue', 'orders', 'units']
    
    # Calculate averages (per day)
    num_days = sales_df['date'].nunique()
    hourly_metrics['avg_revenue'] = hourly_metrics['revenue'] / num_days
    hourly_metrics['avg_orders'] = hourly_metrics['orders'] / num_days
    
    # Format hour labels
    hourly_metrics['hour_label'] = hourly_metrics['hour'].apply(
        lambda x: f"{x:02d}:00"
    )
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        render_chart_title("Revenue by Hour", "💰")
        
        fig = px.bar(
            hourly_metrics,
            x='hour_label',
            y='revenue',
            color='revenue',
            color_continuous_scale=['#312e81', '#6366f1', '#a5b4fc']
        )
        fig = apply_chart_style(fig, height=320, show_legend=False)
        fig.update_layout(
            xaxis_title="Hour of Day",
            yaxis_title="Total Revenue (AED)",
            coloraxis_showscale=False,
            xaxis_tickangle=-45
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        render_chart_title("Orders by Hour", "🛒")
        
        fig = px.bar(
            hourly_metrics,
            x='hour_label',
            y='orders',
            color='orders',
            color_continuous_scale=['#064e3b', '#10b981', '#6ee7b7']
        )
        fig = apply_chart_style(fig, height=320, show_legend=False)
        fig.update_layout(
            xaxis_title="Hour of Day",
            yaxis_title="Number of Orders",
            coloraxis_showscale=False,
            xaxis_tickangle=-45
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Average hourly pattern line chart
    st.markdown("")
    render_chart_title("Average Hourly Pattern (Per Day)", "📈")
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=hourly_metrics['hour_label'],
        y=hourly_metrics['avg_revenue'],
        name='Avg Revenue',
        line=dict(color='#6366f1', width=3),
        mode='lines+markers'
    ))
    
    fig = apply_chart_style(fig, height=300, show_legend=False)
    fig.update_layout(
        xaxis_title="Hour of Day",
        yaxis_title="Average Revenue (AED)",
        xaxis_tickangle=-45
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Insights
    st.markdown("")
    
    peak_hour = hourly_metrics.loc[hourly_metrics['revenue'].idxmax()]
    low_hour = hourly_metrics.loc[hourly_metrics['revenue'].idxmin()]
    
    col1, col2 = st.columns(2)
    
    with col1:
        render_insight_box(
            "🔥",
            f"Peak Hour: {peak_hour['hour_label']}",
            f"Highest activity at **{peak_hour['hour_label']}** with "
            f"**{format_currency(peak_hour['avg_revenue'])}** average revenue per day. "
            f"Ensure adequate inventory and staff during this time.",
            "success"
        )
    
    with col2:
        render_insight_box(
            "📉",
            f"Low Hour: {low_hour['hour_label']}",
            f"Lowest activity at **{low_hour['hour_label']}** with "
            f"**{format_currency(low_hour['avg_revenue'])}** average revenue. "
            f"Consider targeted promotions to boost off-peak sales.",
            "primary"
        )


def render_daily_patterns(sales_df):
    """
    Render day-of-week sales patterns.
    
    Args:
        sales_df: Sales DataFrame with day_of_week column
    """
    st.markdown("#### 📅 Day of Week Patterns")
    st.markdown("Understand which days perform best.")
    
    st.markdown("")
    
    # Daily aggregation
    daily_metrics = sales_df.groupby(['day_num', 'day_of_week']).agg({
        'revenue': 'sum',
        'order_id': 'nunique',
        'qty': 'sum',
        'date': 'nunique'
    }).reset_index()
    
    daily_metrics.columns = ['day_num', 'day_of_week', 'revenue', 'orders', 'units', 'num_days']
    daily_metrics = daily_metrics.sort_values('day_num')
    
    # Calculate averages
    daily_metrics['avg_revenue'] = daily_metrics['revenue'] / daily_metrics['num_days']
    daily_metrics['avg_orders'] = daily_metrics['orders'] / daily_metrics['num_days']
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        render_chart_title("Revenue by Day of Week", "💰")
        
        # Color weekend differently
        daily_metrics['is_weekend'] = daily_metrics['day_num'].isin([5, 6])
        colors = ['#f59e0b' if w else '#6366f1' for w in daily_metrics['is_weekend']]
        
        fig = px.bar(
            daily_metrics,
            x='day_of_week',
            y='revenue',
            text=daily_metrics['revenue'].apply(lambda x: format_currency(x))
        )
        fig.update_traces(marker_color=colors, textposition='outside')
        fig = apply_chart_style(fig, height=320, show_legend=False)
        fig.update_layout(
            xaxis_title="",
            yaxis_title="Total Revenue (AED)"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        render_chart_title("Average Daily Revenue", "📊")
        
        fig = px.bar(
            daily_metrics,
            x='day_of_week',
            y='avg_revenue',
            color='avg_revenue',
            color_continuous_scale=['#312e81', '#6366f1', '#a5b4fc'],
            text=daily_metrics['avg_revenue'].apply(lambda x: format_currency(x))
        )
        fig = apply_chart_style(fig, height=320, show_legend=False)
        fig.update_traces(textposition='outside')
        fig.update_layout(
            xaxis_title="",
            yaxis_title="Avg Revenue (AED)",
            coloraxis_showscale=False
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Weekday vs Weekend comparison
    st.markdown("")
    render_chart_title("Weekday vs Weekend Comparison", "📈")
    
    weekday_revenue = daily_metrics[~daily_metrics['is_weekend']]['revenue'].sum()
    weekend_revenue = daily_metrics[daily_metrics['is_weekend']]['revenue'].sum()
    
    weekday_days = daily_metrics[~daily_metrics['is_weekend']]['num_days'].sum()
    weekend_days = daily_metrics[daily_metrics['is_weekend']]['num_days'].sum()
    
    weekday_avg = weekday_revenue / weekday_days if weekday_days > 0 else 0
    weekend_avg = weekend_revenue / weekend_days if weekend_days > 0 else 0
    
    comparison_data = pd.DataFrame({
        'Period': ['Weekdays (Mon-Fri)', 'Weekend (Sat-Sun)'],
        'Total Revenue': [weekday_revenue, weekend_revenue],
        'Avg Daily Revenue': [weekday_avg, weekend_avg]
    })
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.pie(
            comparison_data,
            values='Total Revenue',
            names='Period',
            color_discrete_sequence=['#6366f1', '#f59e0b'],
            hole=0.4
        )
        fig = apply_chart_style(fig, height=280)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.bar(
            comparison_data,
            x='Period',
            y='Avg Daily Revenue',
            color='Period',
            color_discrete_sequence=['#6366f1', '#f59e0b'],
            text=comparison_data['Avg Daily Revenue'].apply(lambda x: format_currency(x))
        )
        fig = apply_chart_style(fig, height=280, show_legend=False)
        fig.update_traces(textposition='outside')
        fig.update_layout(xaxis_title="", yaxis_title="Avg Daily Revenue (AED)")
        st.plotly_chart(fig, use_container_width=True)
    
    # Day metrics table
    st.markdown("")
    st.markdown("##### 📋 Day of Week Summary")
    
    display_df = daily_metrics[['day_of_week', 'revenue', 'orders', 'avg_revenue', 'avg_orders']].copy()
    display_df['revenue'] = display_df['revenue'].apply(lambda x: format_currency(x))
    display_df['orders'] = display_df['orders'].apply(lambda x: format_number(x))
    display_df['avg_revenue'] = display_df['avg_revenue'].apply(lambda x: format_currency(x))
    display_df['avg_orders'] = display_df['avg_orders'].apply(lambda x: f"{x:.0f}")
    display_df.columns = ['Day', 'Total Revenue', 'Total Orders', 'Avg Revenue', 'Avg Orders']
    
    st.dataframe(display_df, use_container_width=True, hide_index=True)


def render_weekly_patterns(sales_df):
    """
    Render weekly sales patterns.
    
    Args:
        sales_df: Sales DataFrame with week column
    """
    st.markdown("#### 📆 Weekly Trends")
    st.markdown("Track week-over-week performance.")
    
    st.markdown("")
    
    # Weekly aggregation
    weekly_metrics = sales_df.groupby('week').agg({
        'revenue': 'sum',
        'order_id': 'nunique',
        'qty': 'sum',
        'order_time': 'min'
    }).reset_index()
    
    weekly_metrics.columns = ['week', 'revenue', 'orders', 'units', 'week_start']
    weekly_metrics = weekly_metrics.sort_values('week')
    
    # Calculate week-over-week change
    weekly_metrics['revenue_change'] = weekly_metrics['revenue'].pct_change() * 100
    weekly_metrics['orders_change'] = weekly_metrics['orders'].pct_change() * 100
    
    # Charts
    render_chart_title("Weekly Revenue Trend", "💰")
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=weekly_metrics['week'],
        y=weekly_metrics['revenue'],
        name='Revenue',
        line=dict(color='#6366f1', width=3),
        fill='tozeroy',
        fillcolor='rgba(99, 102, 241, 0.1)'
    ))
    
    fig = apply_chart_style(fig, height=320, show_legend=False)
    fig.update_layout(
        xaxis_title="Week Number",
        yaxis_title="Revenue (AED)"
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # WoW change
    st.markdown("")
    render_chart_title("Week-over-Week Revenue Change", "📈")
    
    wow_data = weekly_metrics[weekly_metrics['revenue_change'].notna()].copy()
    wow_data['color'] = wow_data['revenue_change'].apply(lambda x: '#10b981' if x >= 0 else '#ef4444')
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=wow_data['week'],
        y=wow_data['revenue_change'],
        marker_color=wow_data['color'],
        text=wow_data['revenue_change'].apply(lambda x: f"{x:+.1f}%"),
        textposition='outside'
    ))
    
    fig = apply_chart_style(fig, height=280, show_legend=False)
    fig.update_layout(
        xaxis_title="Week Number",
        yaxis_title="Change (%)"
    )
    fig.add_hline(y=0, line_dash="dash", line_color="#71717a")
    st.plotly_chart(fig, use_container_width=True)
    
    # Weekly summary
    st.markdown("")
    st.markdown("##### 📋 Weekly Summary")
    
    display_df = weekly_metrics[['week', 'revenue', 'orders', 'units', 'revenue_change']].copy()
    display_df['revenue'] = display_df['revenue'].apply(lambda x: format_currency(x))
    display_df['orders'] = display_df['orders'].apply(lambda x: format_number(x))
    display_df['units'] = display_df['units'].apply(lambda x: format_number(x))
    display_df['revenue_change'] = display_df['revenue_change'].apply(
        lambda x: f"{x:+.1f}%" if pd.notna(x) else "N/A"
    )
    display_df.columns = ['Week', 'Revenue', 'Orders', 'Units', 'WoW Change']
    
    st.dataframe(display_df, use_container_width=True, hide_index=True, height=300)


def render_monthly_patterns(sales_df):
    """
    Render monthly sales patterns.
    
    Args:
        sales_df: Sales DataFrame with month columns
    """
    st.markdown("#### 📈 Monthly Trends")
    st.markdown("Track month-over-month performance and seasonality.")
    
    st.markdown("")
    
    # Monthly aggregation
    monthly_metrics = sales_df.groupby(['month_num', 'month_name']).agg({
        'revenue': 'sum',
        'order_id': 'nunique',
        'qty': 'sum'
    }).reset_index()
    
    monthly_metrics.columns = ['month_num', 'month_name', 'revenue', 'orders', 'units']
    monthly_metrics = monthly_metrics.sort_values('month_num')
    
    # Calculate MoM change
    monthly_metrics['revenue_change'] = monthly_metrics['revenue'].pct_change() * 100
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        render_chart_title("Monthly Revenue", "💰")
        
        fig = px.bar(
            monthly_metrics,
            x='month_name',
            y='revenue',
            color='revenue',
            color_continuous_scale=['#312e81', '#6366f1', '#a5b4fc'],
            text=monthly_metrics['revenue'].apply(lambda x: format_currency(x))
        )
        fig = apply_chart_style(fig, height=320, show_legend=False)
        fig.update_traces(textposition='outside')
        fig.update_layout(
            xaxis_title="",
            yaxis_title="Revenue (AED)",
            coloraxis_showscale=False
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        render_chart_title("Monthly Orders", "🛒")
        
        fig = px.bar(
            monthly_metrics,
            x='month_name',
            y='orders',
            color='orders',
            color_continuous_scale=['#064e3b', '#10b981', '#6ee7b7'],
            text=monthly_metrics['orders'].apply(lambda x: format_number(x))
        )
        fig = apply_chart_style(fig, height=320, show_legend=False)
        fig.update_traces(textposition='outside')
        fig.update_layout(
            xaxis_title="",
            yaxis_title="Number of Orders",
            coloraxis_showscale=False
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # MoM trend line
    st.markdown("")
    render_chart_title("Revenue Trend with MoM Change", "📈")
    
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    fig.add_trace(
        go.Scatter(
            x=monthly_metrics['month_name'],
            y=monthly_metrics['revenue'],
            name='Revenue',
            line=dict(color='#6366f1', width=3),
            mode='lines+markers'
        ),
        secondary_y=False
    )
    
    # Add MoM change bars
    mom_data = monthly_metrics[monthly_metrics['revenue_change'].notna()]
    colors = ['#10b981' if x >= 0 else '#ef4444' for x in mom_data['revenue_change']]
    
    fig.add_trace(
        go.Bar(
            x=mom_data['month_name'],
            y=mom_data['revenue_change'],
            name='MoM Change',
            marker_color=colors,
            opacity=0.5
        ),
        secondary_y=True
    )
    
    fig = apply_chart_style(fig, height=350)
    fig.update_layout(
        xaxis_title="",
        yaxis_title="Revenue (AED)",
        yaxis2_title="MoM Change (%)"
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Insights
    st.markdown("")
    
    best_month = monthly_metrics.loc[monthly_metrics['revenue'].idxmax()]
    worst_month = monthly_metrics.loc[monthly_metrics['revenue'].idxmin()]
    
    col1, col2 = st.columns(2)
    
    with col1:
        render_insight_box(
            "🏆",
            f"Best Month: {best_month['month_name']}",
            f"**{best_month['month_name']}** had the highest revenue at "
            f"**{format_currency(best_month['revenue'])}** with "
            f"**{format_number(best_month['orders'])}** orders.",
            "success"
        )
    
    with col2:
        render_insight_box(
            "📊",
            f"Lowest Month: {worst_month['month_name']}",
            f"**{worst_month['month_name']}** had the lowest revenue at "
            f"**{format_currency(worst_month['revenue'])}**. "
            f"Consider running promotions during this period.",
            "primary"
        )


def render_time_heatmaps(sales_df):
    """
    Render time-based heatmaps.
    
    Args:
        sales_df: Sales DataFrame with time components
    """
    st.markdown("#### 🔥 Sales Heatmaps")
    st.markdown("Visualize sales intensity across time dimensions.")
    
    st.markdown("")
    
    # Hour × Day of Week heatmap
    render_chart_title("Sales Heatmap: Hour × Day of Week", "📊")
    
    hour_day = sales_df.groupby(['hour', 'day_num'])['revenue'].sum().reset_index()
    hour_day_pivot = hour_day.pivot(index='hour', columns='day_num', values='revenue').fillna(0)
    
    # Rename columns to day names
    day_names = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    hour_day_pivot.columns = [day_names[i] for i in hour_day_pivot.columns]
    
    fig = px.imshow(
        hour_day_pivot,
        labels=dict(x="Day of Week", y="Hour of Day", color="Revenue (AED)"),
        color_continuous_scale='Purples',
        aspect='auto'
    )
    fig = apply_chart_style(fig, height=450)
    fig.update_layout(
        xaxis_title="Day of Week",
        yaxis_title="Hour of Day"
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Category × Day heatmap
    st.markdown("")
    render_chart_title("Sales Heatmap: Category × Day of Week", "📦")
    
    if 'category' in sales_df.columns:
        cat_day = sales_df.groupby(['category', 'day_num'])['revenue'].sum().reset_index()
        cat_day_pivot = cat_day.pivot(index='category', columns='day_num', values='revenue').fillna(0)
        cat_day_pivot.columns = [day_names[i] for i in cat_day_pivot.columns]
        
        fig = px.imshow(
            cat_day_pivot,
            labels=dict(x="Day of Week", y="Category", color="Revenue (AED)"),
            color_continuous_scale='Greens',
            aspect='auto',
            text_auto='.2s'
        )
        fig = apply_chart_style(fig, height=350)
        fig.update_layout(
            xaxis_title="Day of Week",
            yaxis_title=""
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Channel × Hour heatmap
    st.markdown("")
    render_chart_title("Sales Heatmap: Channel × Hour", "📱")
    
    if 'channel' in sales_df.columns:
        channel_hour = sales_df.groupby(['channel', 'hour'])['revenue'].sum().reset_index()
        channel_hour_pivot = channel_hour.pivot(index='channel', columns='hour', values='revenue').fillna(0)
        
        fig = px.imshow(
            channel_hour_pivot,
            labels=dict(x="Hour of Day", y="Channel", color="Revenue (AED)"),
            color_continuous_scale='Blues',
            aspect='auto'
        )
        fig = apply_chart_style(fig, height=250)
        fig.update_layout(
            xaxis_title="Hour of Day",
            yaxis_title=""
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Peak time summary
    st.markdown("")
    st.markdown("##### 🎯 Peak Time Summary")
    
    # Find top 5 hour-day combinations
    hour_day_flat = hour_day.nlargest(5, 'revenue')
    hour_day_flat['day_name'] = hour_day_flat['day_num'].apply(lambda x: day_names[x])
    hour_day_flat['hour_label'] = hour_day_flat['hour'].apply(lambda x: f"{x:02d}:00")
    hour_day_flat['time_slot'] = hour_day_flat['day_name'] + ' ' + hour_day_flat['hour_label']
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        fig = px.bar(
            hour_day_flat.sort_values('revenue', ascending=True),
            x='revenue',
            y='time_slot',
            orientation='h',
            color='revenue',
            color_continuous_scale=['#6366f1', '#10b981']
        )
        fig = apply_chart_style(fig, height=250, show_legend=False)
        fig.update_layout(
            xaxis_title="Revenue (AED)",
            yaxis_title="",
            coloraxis_showscale=False
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("**Top 5 Peak Times:**")
        for i, (_, row) in enumerate(hour_day_flat.iterrows(), 1):
            st.markdown(f"{i}. **{row['time_slot']}** - {format_currency(row['revenue'])}")
        
        st.markdown("")
        st.caption("Focus marketing and inventory during these peak periods for maximum impact.")

# =============================================================================
# DATA EXPLORER TAB
# =============================================================================
# This module provides a flexible data exploration interface for ad-hoc
# analysis, filtering, and data export capabilities.
# =============================================================================

def render_data_explorer(sales_df, products_df, stores_df, inventory_df, campaigns_df):
    """
    Render the Data Explorer tab for ad-hoc analysis.
    
    This tab provides:
        1. Dataset Selection
        2. Dynamic Filtering
        3. Column Selection
        4. Data Preview
        5. Summary Statistics
        6. Export Capabilities
    
    Args:
        sales_df: Sales DataFrame
        products_df: Products DataFrame
        stores_df: Stores DataFrame
        inventory_df: Inventory DataFrame
        campaigns_df: Campaigns DataFrame
    """
    render_section_header(
        "🔍",
        "Data Explorer",
        "Explore, filter, and export data for custom analysis"
    )
    
    # =========================================================================
    # DATASET SELECTION
    # =========================================================================
    st.markdown("##### 📁 Select Dataset")
    
    dataset_options = {
        "Sales Data": sales_df,
        "Products Data": products_df,
        "Stores Data": stores_df,
        "Inventory Data": inventory_df,
        "Campaigns Data": campaigns_df
    }
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        selected_dataset = st.selectbox(
            "Dataset",
            options=list(dataset_options.keys()),
            key="explorer_dataset"
        )
    
    # Get selected dataframe
    df = dataset_options[selected_dataset].copy()
    
    with col2:
        st.markdown(f"""
        **Dataset Info:** {len(df):,} rows × {len(df.columns)} columns
        """)
    
    render_divider_subtle()
    
    # =========================================================================
    # COLUMN SELECTION
    # =========================================================================
    st.markdown("##### 📋 Select Columns")
    
    all_columns = df.columns.tolist()
    
    # Default to first 10 columns or all if less
    default_columns = all_columns[:min(10, len(all_columns))]
    
    selected_columns = st.multiselect(
        "Choose columns to display",
        options=all_columns,
        default=default_columns,
        key="explorer_columns"
    )
    
    if not selected_columns:
        st.warning("Please select at least one column to display.")
        return
    
    # Filter dataframe to selected columns
    filtered_df = df[selected_columns].copy()
    
    render_divider_subtle()
    
    # =========================================================================
    # DYNAMIC FILTERS
    # =========================================================================
    st.markdown("##### 🎛️ Apply Filters")
    
    with st.expander("Configure Filters", expanded=False):
        filter_columns = st.multiselect(
            "Select columns to filter",
            options=selected_columns,
            key="explorer_filter_columns"
        )
        
        filters_applied = {}
        
        if filter_columns:
            filter_cols = st.columns(min(3, len(filter_columns)))
            
            for i, col_name in enumerate(filter_columns):
                with filter_cols[i % 3]:
                    col_dtype = filtered_df[col_name].dtype
                    
                    if col_dtype == 'object' or col_dtype.name == 'category':
                        # Categorical filter
                        unique_values = filtered_df[col_name].dropna().unique().tolist()
                        if len(unique_values) <= 50:
                            selected_values = st.multiselect(
                                f"Filter: {col_name}",
                                options=unique_values,
                                key=f"filter_{col_name}"
                            )
                            if selected_values:
                                filters_applied[col_name] = ('isin', selected_values)
                        else:
                            search_value = st.text_input(
                                f"Search: {col_name}",
                                key=f"filter_{col_name}"
                            )
                            if search_value:
                                filters_applied[col_name] = ('contains', search_value)
                    
                    elif pd.api.types.is_numeric_dtype(col_dtype):
                        # Numeric filter
                        min_val = float(filtered_df[col_name].min())
                        max_val = float(filtered_df[col_name].max())
                        
                        if min_val != max_val:
                            range_values = st.slider(
                                f"Range: {col_name}",
                                min_value=min_val,
                                max_value=max_val,
                                value=(min_val, max_val),
                                key=f"filter_{col_name}"
                            )
                            if range_values != (min_val, max_val):
                                filters_applied[col_name] = ('range', range_values)
                    
                    elif pd.api.types.is_datetime64_any_dtype(col_dtype):
                        # Date filter
                        min_date = filtered_df[col_name].min()
                        max_date = filtered_df[col_name].max()
                        
                        if pd.notna(min_date) and pd.notna(max_date):
                            date_range = st.date_input(
                                f"Date Range: {col_name}",
                                value=(min_date.date(), max_date.date()),
                                key=f"filter_{col_name}"
                            )
                            if isinstance(date_range, tuple) and len(date_range) == 2:
                                filters_applied[col_name] = ('date_range', date_range)
        
        # Apply filters
        for col_name, (filter_type, filter_value) in filters_applied.items():
            if filter_type == 'isin':
                filtered_df = filtered_df[filtered_df[col_name].isin(filter_value)]
            elif filter_type == 'contains':
                filtered_df = filtered_df[filtered_df[col_name].astype(str).str.contains(filter_value, case=False, na=False)]
            elif filter_type == 'range':
                filtered_df = filtered_df[(filtered_df[col_name] >= filter_value[0]) & (filtered_df[col_name] <= filter_value[1])]
            elif filter_type == 'date_range':
                filtered_df = filtered_df[
                    (filtered_df[col_name].dt.date >= filter_value[0]) &
                    (filtered_df[col_name].dt.date <= filter_value[1])
                ]
    
    # Show filter summary
    if len(filtered_df) < len(df[selected_columns]):
        st.caption(f"🔍 Showing {len(filtered_df):,} of {len(df):,} rows after filtering")
    
    render_divider_subtle()
    
    # =========================================================================
    # DATA PREVIEW
    # =========================================================================
    st.markdown("##### 📊 Data Preview")
    
    # Pagination
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        rows_per_page = st.selectbox(
            "Rows per page",
            options=[25, 50, 100, 250, 500],
            index=1,
            key="explorer_rows_per_page"
        )
    
    total_pages = max(1, len(filtered_df) // rows_per_page + (1 if len(filtered_df) % rows_per_page > 0 else 0))
    
    with col2:
        current_page = st.number_input(
            "Page",
            min_value=1,
            max_value=total_pages,
            value=1,
            key="explorer_page"
        )
    
    with col3:
        st.markdown(f"**Total Pages:** {total_pages}")
    
    # Calculate slice indices
    start_idx = (current_page - 1) * rows_per_page
    end_idx = min(start_idx + rows_per_page, len(filtered_df))
    
    # Display dataframe
    display_df = filtered_df.iloc[start_idx:end_idx]
    
    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
        height=400
    )
    
    st.caption(f"Showing rows {start_idx + 1} to {end_idx} of {len(filtered_df):,}")
    
    # =========================================================================
    # SUMMARY STATISTICS
    # =========================================================================
    st.markdown("")
    st.markdown("##### 📈 Summary Statistics")
    
    stats_tabs = st.tabs(["Numeric Stats", "Categorical Stats", "Missing Values"])
    
    with stats_tabs[0]:
        # Numeric columns
        numeric_cols = filtered_df.select_dtypes(include=['number']).columns.tolist()
        
        if numeric_cols:
            numeric_stats = filtered_df[numeric_cols].describe().T
            numeric_stats['sum'] = filtered_df[numeric_cols].sum()
            numeric_stats['median'] = filtered_df[numeric_cols].median()
            
            # Format for display
            numeric_stats = numeric_stats.round(2)
            st.dataframe(numeric_stats, use_container_width=True)
        else:
            st.info("No numeric columns in selection.")
    
    with stats_tabs[1]:
        # Categorical columns
        cat_cols = filtered_df.select_dtypes(include=['object', 'category']).columns.tolist()
        
        if cat_cols:
            cat_stats = []
            for col in cat_cols:
                cat_stats.append({
                    'Column': col,
                    'Unique Values': filtered_df[col].nunique(),
                    'Most Common': filtered_df[col].mode().iloc[0] if len(filtered_df[col].mode()) > 0 else 'N/A',
                    'Most Common Count': filtered_df[col].value_counts().iloc[0] if len(filtered_df[col].value_counts()) > 0 else 0,
                    'Missing': filtered_df[col].isna().sum()
                })
            
            cat_stats_df = pd.DataFrame(cat_stats)
            st.dataframe(cat_stats_df, use_container_width=True, hide_index=True)
        else:
            st.info("No categorical columns in selection.")
    
    with stats_tabs[2]:
        # Missing values
        missing_data = []
        for col in selected_columns:
            missing_count = filtered_df[col].isna().sum()
            missing_pct = (missing_count / len(filtered_df) * 100) if len(filtered_df) > 0 else 0
            missing_data.append({
                'Column': col,
                'Missing Count': missing_count,
                'Missing %': f"{missing_pct:.2f}%",
                'Data Type': str(filtered_df[col].dtype)
            })
        
        missing_df = pd.DataFrame(missing_data)
        missing_df = missing_df.sort_values('Missing Count', ascending=False)
        st.dataframe(missing_df, use_container_width=True, hide_index=True)
    
    # =========================================================================
    # QUICK VISUALIZATIONS
    # =========================================================================
    st.markdown("")
    st.markdown("##### 📊 Quick Visualizations")
    
    viz_col1, viz_col2 = st.columns(2)
    
    with viz_col1:
        numeric_cols = filtered_df.select_dtypes(include=['number']).columns.tolist()
        
        if numeric_cols:
            selected_num_col = st.selectbox(
                "Select numeric column for histogram",
                options=numeric_cols,
                key="explorer_hist_col"
            )
            
            fig = px.histogram(
                filtered_df,
                x=selected_num_col,
                nbins=30,
                color_discrete_sequence=['#6366f1']
            )
            fig = apply_chart_style(fig, height=300, show_legend=False)
            fig.update_layout(xaxis_title=selected_num_col, yaxis_title="Count")
            st.plotly_chart(fig, use_container_width=True)
    
    with viz_col2:
        cat_cols = filtered_df.select_dtypes(include=['object', 'category']).columns.tolist()
        
        if cat_cols:
            selected_cat_col = st.selectbox(
                "Select categorical column for bar chart",
                options=cat_cols,
                key="explorer_bar_col"
            )
            
            value_counts = filtered_df[selected_cat_col].value_counts().head(10).reset_index()
            value_counts.columns = ['value', 'count']
            
            fig = px.bar(
                value_counts,
                x='value',
                y='count',
                color_discrete_sequence=['#10b981']
            )
            fig = apply_chart_style(fig, height=300, show_legend=False)
            fig.update_layout(xaxis_title=selected_cat_col, yaxis_title="Count")
            st.plotly_chart(fig, use_container_width=True)
    
    # =========================================================================
    # EXPORT OPTIONS
    # =========================================================================
    st.markdown("")
    st.markdown("##### 💾 Export Data")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # CSV Export
        csv_data = filtered_df.to_csv(index=False)
        st.download_button(
            label="📥 Download CSV",
            data=csv_data,
            file_name=f"{selected_dataset.lower().replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            key="export_csv"
        )
    
    with col2:
        # JSON Export
        json_data = filtered_df.to_json(orient='records', date_format='iso')
        st.download_button(
            label="📥 Download JSON",
            data=json_data,
            file_name=f"{selected_dataset.lower().replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json",
            key="export_json"
        )
    
    with col3:
        st.markdown(f"**Export Size:** {len(filtered_df):,} rows")
        st.caption("Filtered data will be exported")


# =============================================================================
# ABOUT / HELP TAB
# =============================================================================

def render_about_section():
    """
    Render the About/Help section with documentation.
    """
    render_section_header(
        "ℹ️",
        "About This Dashboard",
        "Documentation, data sources, and help information"
    )
    
    # =========================================================================
    # OVERVIEW
    # =========================================================================
    st.markdown("""
    ### 📊 Dashboard Overview
    
    This **UAE Retail Analytics Dashboard** provides comprehensive insights into retail operations
    across multiple dimensions including sales, inventory, campaigns, and store performance.
    
    **Key Features:**
    - 📈 **Executive Overview** - High-level KPIs and business health indicators
    - 💰 **Sales Analytics** - Deep-dive into revenue, orders, and product performance
    - 📦 **Inventory Health** - Stock monitoring, alerts, and reorder recommendations
    - 🎯 **Campaign Performance** - Promotion analysis and What-If simulator
    - 🏪 **Store Performance** - Location-level rankings and comparisons
    - ⏰ **Time Patterns** - Temporal analysis of sales patterns
    - 🔍 **Data Explorer** - Ad-hoc data exploration and export
    """)
    
    render_divider_subtle()
    
    # =========================================================================
    # DATA SOURCES
    # =========================================================================
    st.markdown("### 📁 Data Sources")
    
    data_info = [
        {
            "name": "Sales Data",
            "description": "Transaction-level sales records including order details, products, revenue, and customer information",
            "key_fields": "order_id, product_id, qty, selling_price_aed, discount_pct, channel, payment_status"
        },
        {
            "name": "Products Data",
            "description": "Product catalog with categories, brands, and pricing information",
            "key_fields": "product_id, category, brand, unit_cost_aed"
        },
        {
            "name": "Stores Data",
            "description": "Store locations and channel assignments",
            "key_fields": "store_id, city, channel"
        },
        {
            "name": "Inventory Data",
            "description": "Daily inventory snapshots with stock levels and reorder points",
            "key_fields": "product_id, store_id, stock_on_hand, reorder_point, lead_time_days"
        },
        {
            "name": "Campaigns Data",
            "description": "Promotional campaign definitions and budgets",
            "key_fields": "campaign_id, start_date, end_date, discount_pct, promo_budget_aed"
        }
    ]
    
    for data in data_info:
        with st.expander(f"📄 {data['name']}"):
            st.markdown(f"**Description:** {data['description']}")
            st.markdown(f"**Key Fields:** `{data['key_fields']}`")
    
    render_divider_subtle()
    
    # =========================================================================
    # METRICS GLOSSARY
    # =========================================================================
    st.markdown("### 📖 Metrics Glossary")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Sales Metrics:**
        - **Revenue** - Total sales value in AED
        - **AOV** - Average Order Value (Revenue / Orders)
        - **Units Sold** - Total quantity of items sold
        - **Discount %** - Average discount percentage applied
        
        **Inventory Metrics:**
        - **Stock on Hand** - Current inventory level
        - **Reorder Point** - Stock level triggering reorder
        - **Lead Time** - Days to receive new stock
        - **Stock Status** - Healthy/Low/Critical classification
        """)
    
    with col2:
        st.markdown("""
        **Performance Metrics:**
        - **Health Score** - Weighted composite score (0-100)
        - **Return Rate** - Percentage of orders returned
        - **Conversion** - Orders as % of total traffic
        
        **Campaign Metrics:**
        - **ROI** - Return on Investment percentage
        - **Lift** - Sales increase multiplier during promotion
        - **Incremental Revenue** - Additional revenue vs baseline
        - **Margin Impact** - Net profit change after costs
        """)
    
    render_divider_subtle()
    
    # =========================================================================
    # USAGE TIPS
    # =========================================================================
    st.markdown("### 💡 Usage Tips")
    
    tips = [
        "**Use Filters Effectively** - Most tabs have filters at the top. Apply them to focus on specific cities, channels, or categories.",
        "**Hover for Details** - All charts are interactive. Hover over data points for detailed values.",
        "**Export Data** - Use the Data Explorer tab to filter and export data for external analysis.",
        "**What-If Simulator** - Test promotional scenarios before implementation to predict ROI.",
        "**Monitor Stock Alerts** - Check the Inventory Health tab regularly for low stock warnings.",
        "**Compare Stores** - Use the Store Performance comparison tool to identify best practices."
    ]
    
    for i, tip in enumerate(tips, 1):
        st.markdown(f"{i}. {tip}")
    
    render_divider_subtle()
    
    # =========================================================================
    # TECHNICAL INFO
    # =========================================================================
    st.markdown("### 🔧 Technical Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Built With:**
        - Python 3.9+
        - Streamlit
        - Plotly Express
        - Pandas
        - NumPy
        """)
    
    with col2:
        st.markdown("""
        **Data Refresh:**
        - Simulated data generated on load
        - ~120 days of historical data
        - ~100,000 transaction records
        """)
    
    # Version info
    st.markdown("")
    st.markdown(f"""
    ---
    **Dashboard Version:** 2.0.0  
    **Last Updated:** {datetime.now().strftime('%Y-%m-%d')}  
    **Developed for:** UAE Retail Operations Analytics
    """)


# =============================================================================
# MAIN APPLICATION
# =============================================================================

def main():
    """
    Main application entry point.
    
    This function:
        1. Applies global styling
        2. Loads/generates data
        3. Renders the sidebar navigation
        4. Renders the selected tab content
    """
    # =========================================================================
    # APPLY GLOBAL STYLES
    # =========================================================================
    def apply_custom_css():
    """Apply custom CSS styling for the dark theme dashboard."""
    st.markdown("""
    <style>
    /* Main app styling */
    .stApp {
        background: linear-gradient(135deg, #0f0f1a 0%, #1a1a2e 50%, #0f0f1a 100%);
    }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #0f0f1a 100%);
        border-right: 1px solid rgba(99, 102, 241, 0.2);
    }
    
    /* Headers */
    h1, h2, h3, h4, h5, h6 {
        color: #ffffff !important;
    }
    
    /* Metric cards */
    div[data-testid="metric-container"] {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 16px;
    }
    
    div[data-testid="metric-container"] label {
        color: #a1a1aa !important;
    }
    
    div[data-testid="metric-container"] div[data-testid="stMetricValue"] {
        color: #ffffff !important;
    }
    
    /* DataFrames */
    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 8px 24px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 20px rgba(99, 102, 241, 0.4);
    }
    
    /* Selectbox */
    .stSelectbox > div > div {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 8px;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: transparent;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 8px;
        color: #a1a1aa;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 8px;
    }
    
    /* Progress bar */
    .stProgress > div > div {
        background: linear-gradient(90deg, #6366f1, #10b981);
    }
    
    /* Slider */
    .stSlider > div > div > div {
        background: #6366f1;
    }
    
    /* Info/Warning/Error boxes */
    .stAlert {
        border-radius: 8px;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #1a1a2e;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #6366f1;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #8b5cf6;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # =========================================================================
    # LOAD DATA
    # =========================================================================
    # Use session state to cache data
    if 'data_loaded' not in st.session_state:
        with st.spinner("Loading data..."):
            (
                st.session_state.sales_df,
                st.session_state.products_df,
                st.session_state.stores_df,
                st.session_state.inventory_df,
                st.session_state.campaigns_df
            ) = load_and_prepare_data()
            st.session_state.data_loaded = True
    
    # Retrieve data from session state
    sales_df = st.session_state.sales_df
    products_df = st.session_state.products_df
    stores_df = st.session_state.stores_df
    inventory_df = st.session_state.inventory_df
    campaigns_df = st.session_state.campaigns_df
    
    # =========================================================================
    # SIDEBAR
    # =========================================================================
    with st.sidebar:
        # Logo/Title
        st.markdown("""
        <div style="text-align: center; padding: 20px 0;">
            <div style="font-size: 3rem; margin-bottom: 10px;">🛒</div>
            <div style="font-size: 1.2rem; font-weight: 700; color: white;">UAE Retail</div>
            <div style="font-size: 0.9rem; color: #a1a1aa;">Analytics Dashboard</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Navigation
        st.markdown("### 📍 Navigation")
        
        nav_options = {
            "🏠 Executive Overview": "overview",
            "📈 Sales Analytics": "sales",
            "📦 Inventory Health": "inventory",
            "🎯 Campaign Performance": "campaigns",
            "🏪 Store Performance": "stores",
            "⏰ Time Patterns": "time",
            "🔍 Data Explorer": "explorer",
            "ℹ️ About": "about"
        }
        
        selected_nav = st.radio(
            "Select View",
            options=list(nav_options.keys()),
            label_visibility="collapsed",
            key="main_navigation"
        )
        
        selected_tab = nav_options[selected_nav]
        
        st.markdown("---")
        
        # Data Summary
        st.markdown("### 📊 Data Summary")
        
        st.markdown(f"""
        <div style="font-size: 0.85rem; color: #a1a1aa;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                <span>Sales Records</span>
                <span style="color: white; font-weight: 600;">{len(sales_df):,}</span>
            </div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                <span>Products</span>
                <span style="color: white; font-weight: 600;">{len(products_df):,}</span>
            </div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                <span>Stores</span>
                <span style="color: white; font-weight: 600;">{len(stores_df):,}</span>
            </div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                <span>Campaigns</span>
                <span style="color: white; font-weight: 600;">{len(campaigns_df):,}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Quick Stats
        st.markdown("### 💰 Quick Stats")
        
        total_revenue = sales_df['revenue'].sum()
        total_orders = sales_df['order_id'].nunique()
        
        st.markdown(f"""
        <div style="background: rgba(99, 102, 241, 0.1); border-radius: 8px; padding: 12px; margin-bottom: 10px;">
            <div style="font-size: 0.75rem; color: #a1a1aa;">Total Revenue</div>
            <div style="font-size: 1.1rem; font-weight: 700; color: #6366f1;">{format_currency(total_revenue)}</div>
        </div>
        <div style="background: rgba(16, 185, 129, 0.1); border-radius: 8px; padding: 12px;">
            <div style="font-size: 0.75rem; color: #a1a1aa;">Total Orders</div>
            <div style="font-size: 1.1rem; font-weight: 700; color: #10b981;">{format_number(total_orders)}</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Refresh button
        if st.button("🔄 Refresh Data", use_container_width=True):
            # Clear session state to force reload
            for key in ['sales_df', 'products_df', 'stores_df', 'inventory_df', 'campaigns_df', 'data_loaded']:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()
        
        # Footer
        st.markdown("")
        st.markdown(f"""
        <div style="text-align: center; font-size: 0.75rem; color: #71717a; padding-top: 20px;">
            Last updated<br>
            {datetime.now().strftime('%Y-%m-%d %H:%M')}
        </div>
        """, unsafe_allow_html=True)
    
    # =========================================================================
    # MAIN CONTENT AREA
    # =========================================================================
    
    # Render selected tab
    if selected_tab == "overview":
        render_executive_overview(sales_df, inventory_df, campaigns_df, stores_df)
    
    elif selected_tab == "sales":
        render_sales_analysis(sales_df, products_df, stores_df)
    
    elif selected_tab == "inventory":
        render_inventory_analysis(inventory_df, sales_df, products_df, stores_df)
    
    elif selected_tab == "campaigns":
        render_campaign_analysis(campaigns_df, sales_df, products_df, stores_df)
    
    elif selected_tab == "stores":
        render_store_performance(stores_df, sales_df, inventory_df)
    
    elif selected_tab == "time":
        render_time_patterns(sales_df)
    
    elif selected_tab == "explorer":
        render_data_explorer(sales_df, products_df, stores_df, inventory_df, campaigns_df)
    
    elif selected_tab == "about":
        render_about_section()
    
    # =========================================================================
    # FOOTER
    # =========================================================================
    st.markdown("")
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 20px 0; color: #71717a; font-size: 0.85rem;">
        <div>UAE Retail Analytics Dashboard v2.0</div>
        <div style="margin-top: 4px;">Built with Streamlit • Data is simulated for demonstration</div>
    </div>
    """, unsafe_allow_html=True)


# =============================================================================
# APPLICATION ENTRY POINT
# =============================================================================

if __name__ == "__main__":

    main()
