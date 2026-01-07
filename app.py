# =============================================================================
# UAE RETAIL ANALYTICS DASHBOARD - ROBUST VERSION
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
warnings.filterwarnings('ignore')

# =============================================================================
# PAGE CONFIG - MUST BE FIRST
# =============================================================================
st.set_page_config(
    page_title="UAE Retail Analytics",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================================================================
# CONSTANTS
# =============================================================================
CATEGORIES = ['Electronics', 'Fashion', 'Grocery', 'Home & Garden', 'Beauty', 'Sports']
CHANNELS = ['App', 'Web', 'Marketplace']
STANDARD_CITIES = ['Dubai', 'Abu Dhabi', 'Sharjah']
PAYMENT_METHODS = ['Credit Card', 'Debit Card', 'Cash', 'Digital Wallet']

# =============================================================================
# CSS STYLING
# =============================================================================
def apply_custom_css():
    st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #0f0f1a 0%, #1a1a2e 50%, #0f0f1a 100%);
    }
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #0f0f1a 100%);
        border-right: 1px solid rgba(99, 102, 241, 0.2);
    }
    h1, h2, h3, h4, h5, h6 { color: #ffffff !important; }
    div[data-testid="metric-container"] {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 16px;
    }
    .stButton > button {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white;
        border: none;
        border-radius: 8px;
    }
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 8px;
        color: #a1a1aa;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# =============================================================================
# DATA GENERATION - CREATES ALL REQUIRED DATA
# =============================================================================
@st.cache_data
def generate_all_data():
    """Generate complete synthetic retail data."""
    np.random.seed(42)
    random.seed(42)
    
    end_date = datetime.now()
    start_date = end_date - timedelta(days=120)
    
    # Generate Products
    products_list = []
    for i in range(200):
        cat = random.choice(CATEGORIES)
        products_list.append({
            'product_id': f'PROD_{i+1:04d}',
            'category': cat,
            'brand': f'Brand_{random.randint(1, 20)}',
            'unit_cost_aed': round(random.uniform(10, 500), 2)
        })
    products_df = pd.DataFrame(products_list)
    
    # Generate Stores
    stores_list = []
    for i in range(30):
        stores_list.append({
            'store_id': f'STORE_{i+1:03d}',
            'city': random.choice(STANDARD_CITIES),
            'channel': random.choice(CHANNELS)
        })
    stores_df = pd.DataFrame(stores_list)
    
    # Generate Sales
    sales_list = []
    for i in range(50000):
        order_date = start_date + timedelta(days=random.randint(0, 120))
        order_time = order_date.replace(hour=random.randint(8, 22), minute=random.randint(0, 59))
        product = random.choice(products_list)
        store = random.choice(stores_list)
        qty = random.randint(1, 5)
        unit_price = product['unit_cost_aed'] * random.uniform(1.2, 2.5)
        discount = random.choice([0, 5, 10, 15, 20, 25])
        selling_price = unit_price * (1 - discount/100)
        revenue = selling_price * qty
        
        sales_list.append({
            'order_id': f'ORD_{i+1:06d}',
            'order_time': order_time,
            'product_id': product['product_id'],
            'store_id': store['store_id'],
            'qty': qty,
            'unit_cost_aed': product['unit_cost_aed'],
            'selling_price_aed': round(selling_price, 2),
            'discount_pct': discount,
            'payment_method': random.choice(PAYMENT_METHODS),
            'payment_status': random.choices(['Completed', 'Pending', 'Failed'], weights=[0.9, 0.07, 0.03])[0],
            'return_flag': random.random() < 0.05,
            'category': product['category'],
            'city': store['city'],
            'channel': store['channel'],
            'revenue': round(revenue, 2)
        })
    
    sales_df = pd.DataFrame(sales_list)
    
    # Generate Inventory
    inventory_list = []
    for days_ago in range(0, 30, 7):
        snapshot_date = end_date - timedelta(days=days_ago)
        for product in products_list[:50]:  # Subset for performance
            for store in stores_list[:10]:  # Subset for performance
                stock = random.randint(-10, 500)
                reorder_point = random.randint(20, 100)
                inventory_list.append({
                    'snapshot_date': snapshot_date,
                    'product_id': product['product_id'],
                    'store_id': store['store_id'],
                    'stock_on_hand': stock,
                    'reorder_point': reorder_point,
                    'lead_time_days': random.randint(3, 14),
                    'category': product['category'],
                    'city': store['city'],
                    'channel': store['channel']
                })
    
    inventory_df = pd.DataFrame(inventory_list)
    inventory_df['snapshot_date'] = pd.to_datetime(inventory_df['snapshot_date'])
    inventory_df['stock_status'] = inventory_df.apply(
        lambda x: 'Critical' if x['stock_on_hand'] <= 0 
        else 'Low' if x['stock_on_hand'] <= x['reorder_point'] 
        else 'Healthy', axis=1
    )
    
    # Generate Campaigns
    campaigns_list = []
    for i in range(15):
        camp_start = start_date + timedelta(days=random.randint(0, 90))
        duration = random.randint(3, 14)
        campaigns_list.append({
            'campaign_id': f'CAMP_{i+1:03d}',
            'start_date': camp_start,
            'end_date': camp_start + timedelta(days=duration),
            'duration_days': duration,
            'city': random.choice(STANDARD_CITIES),
            'channel': random.choice(CHANNELS),
            'category': random.choice(CATEGORIES),
            'discount_pct': random.choice([10, 15, 20, 25, 30]),
            'promo_budget_aed': random.randint(10000, 100000),
            'is_active': camp_start <= end_date <= camp_start + timedelta(days=duration)
        })
    campaigns_df = pd.DataFrame(campaigns_list)
    
    return sales_df, products_df, stores_df, inventory_df, campaigns_df

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================
def format_currency(value):
    """Format value as AED currency."""
    try:
        value = float(value)
        if value >= 1_000_000:
            return f"AED {value/1_000_000:.2f}M"
        elif value >= 1_000:
            return f"AED {value/1_000:.1f}K"
        return f"AED {value:.2f}"
    except:
        return "AED 0"

def format_number(value):
    """Format large numbers."""
    try:
        value = float(value)
        if value >= 1_000_000:
            return f"{value/1_000_000:.2f}M"
        elif value >= 1_000:
            return f"{value/1_000:.1f}K"
        return f"{value:,.0f}"
    except:
        return "0"

def get_chart_colors():
    """Return standard chart colors."""
    return ['#6366f1', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#06b6d4']

def apply_chart_style(fig, height=400, show_legend=True):
    """Apply consistent styling to charts."""
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#a1a1aa'),
        height=height,
        showlegend=show_legend,
        margin=dict(l=20, r=20, t=40, b=20),
        legend=dict(bgcolor='rgba(0,0,0,0)', font=dict(color='#a1a1aa')),
        xaxis=dict(gridcolor='rgba(255,255,255,0.1)', zerolinecolor='rgba(255,255,255,0.1)'),
        yaxis=dict(gridcolor='rgba(255,255,255,0.1)', zerolinecolor='rgba(255,255,255,0.1)')
    )
    return fig

def safe_get_column(df, possible_names, default=None):
    """Safely get a column that might have different names."""
    for name in possible_names:
        if name in df.columns:
            return df[name]
    if default is not None:
        return pd.Series([default] * len(df))
    return pd.Series([0] * len(df))

# =============================================================================
# EXECUTIVE OVERVIEW TAB
# =============================================================================
def render_executive_overview(sales_df, inventory_df, campaigns_df, stores_df):
    """Render the executive overview dashboard."""
    st.markdown("## 🏠 Executive Overview")
    st.markdown("Real-time business performance snapshot")
    st.markdown("---")
    
    # Calculate metrics safely
    if 'revenue' in sales_df.columns:
        total_revenue = sales_df['revenue'].sum()
    elif 'selling_price_aed' in sales_df.columns and 'qty' in sales_df.columns:
        total_revenue = (sales_df['selling_price_aed'] * sales_df['qty']).sum()
    else:
        total_revenue = 0
    
    total_orders = sales_df['order_id'].nunique() if 'order_id' in sales_df.columns else len(sales_df)
    avg_order_value = total_revenue / total_orders if total_orders > 0 else 0
    total_units = sales_df['qty'].sum() if 'qty' in sales_df.columns else 0
    
    # KPIs Row
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("💰 Total Revenue", format_currency(total_revenue))
    col2.metric("🛒 Total Orders", format_number(total_orders))
    col3.metric("📦 Units Sold", format_number(total_units))
    col4.metric("💵 Avg Order Value", format_currency(avg_order_value))
    
    st.markdown("")
    
    # Charts Row 1
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📈 Daily Revenue Trend")
        if 'order_time' in sales_df.columns and 'revenue' in sales_df.columns:
            daily_revenue = sales_df.groupby(sales_df['order_time'].dt.date)['revenue'].sum().reset_index()
            daily_revenue.columns = ['date', 'revenue']
            fig = px.area(daily_revenue, x='date', y='revenue', color_discrete_sequence=['#6366f1'])
            fig.update_traces(fill='tozeroy', fillcolor='rgba(99, 102, 241, 0.2)')
            fig = apply_chart_style(fig, height=300, show_legend=False)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No time series data available")
    
    with col2:
        st.markdown("#### 📊 Revenue by Category")
        if 'category' in sales_df.columns and 'revenue' in sales_df.columns:
            cat_revenue = sales_df.groupby('category')['revenue'].sum().reset_index()
            fig = px.pie(cat_revenue, values='revenue', names='category', hole=0.4, color_discrete_sequence=get_chart_colors())
            fig = apply_chart_style(fig, height=300)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No category data available")
    
    # Charts Row 2
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🏙️ Revenue by City")
        if 'city' in sales_df.columns and 'revenue' in sales_df.columns:
            city_revenue = sales_df.groupby('city')['revenue'].sum().reset_index()
            fig = px.bar(city_revenue, x='city', y='revenue', color='city', color_discrete_sequence=get_chart_colors())
            fig = apply_chart_style(fig, height=300, show_legend=False)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No city data available")
    
    with col2:
        st.markdown("#### 📱 Revenue by Channel")
        if 'channel' in sales_df.columns and 'revenue' in sales_df.columns:
            channel_revenue = sales_df.groupby('channel')['revenue'].sum().reset_index()
            fig = px.bar(channel_revenue, x='channel', y='revenue', color='channel', color_discrete_sequence=get_chart_colors())
            fig = apply_chart_style(fig, height=300, show_legend=False)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No channel data available")
    
    # Inventory Status
    st.markdown("#### 📦 Inventory Health Status")
    if len(inventory_df) > 0 and 'stock_status' in inventory_df.columns:
        latest_inv = inventory_df[inventory_df['snapshot_date'] == inventory_df['snapshot_date'].max()]
        status_counts = latest_inv['stock_status'].value_counts()
        
        col1, col2, col3 = st.columns(3)
        col1.metric("✅ Healthy Items", status_counts.get('Healthy', 0))
        col2.metric("⚠️ Low Stock", status_counts.get('Low', 0))
        col3.metric("🔴 Critical", status_counts.get('Critical', 0))
    else:
        st.info("No inventory data available")

# =============================================================================
# SALES ANALYTICS TAB
# =============================================================================
def render_sales_analysis(sales_df, products_df, stores_df):
    """Render sales analytics dashboard."""
    st.markdown("## 📈 Sales Analytics")
    st.markdown("Deep dive into sales performance")
    st.markdown("---")
    
    # Get unique values for filters
    cities = sales_df['city'].unique().tolist() if 'city' in sales_df.columns else STANDARD_CITIES
    channels = sales_df['channel'].unique().tolist() if 'channel' in sales_df.columns else CHANNELS
    categories = sales_df['category'].unique().tolist() if 'category' in sales_df.columns else CATEGORIES
    
    # Filters
    col1, col2, col3 = st.columns(3)
    with col1:
        city_filter = st.selectbox("🏙️ City", ['All'] + cities, key='sales_city')
    with col2:
        channel_filter = st.selectbox("📱 Channel", ['All'] + channels, key='sales_channel')
    with col3:
        category_filter = st.selectbox("📦 Category", ['All'] + categories, key='sales_category')
    
    # Apply filters
    filtered_df = sales_df.copy()
    if city_filter != 'All' and 'city' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['city'] == city_filter]
    if channel_filter != 'All' and 'channel' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['channel'] == channel_filter]
    if category_filter != 'All' and 'category' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['category'] == category_filter]
    
    # Calculate metrics
    total_revenue = filtered_df['revenue'].sum() if 'revenue' in filtered_df.columns else 0
    total_orders = filtered_df['order_id'].nunique() if 'order_id' in filtered_df.columns else len(filtered_df)
    total_units = filtered_df['qty'].sum() if 'qty' in filtered_df.columns else 0
    avg_discount = filtered_df['discount_pct'].mean() if 'discount_pct' in filtered_df.columns else 0
    
    # KPIs
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("💰 Revenue", format_currency(total_revenue))
    col2.metric("🛒 Orders", format_number(total_orders))
    col3.metric("📦 Units", format_number(total_units))
    col4.metric("🏷️ Avg Discount", f"{avg_discount:.1f}%")
    
    st.markdown("")
    
    # Sales Trend
    st.markdown("#### 📈 Sales Trend")
    if 'order_time' in filtered_df.columns and 'revenue' in filtered_df.columns:
        daily = filtered_df.groupby(filtered_df['order_time'].dt.date).agg({
            'revenue': 'sum',
            'order_id': 'nunique'
        }).reset_index()
        daily.columns = ['date', 'revenue', 'orders']
        
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(go.Scatter(x=daily['date'], y=daily['revenue'], name='Revenue', fill='tozeroy', line=dict(color='#6366f1')), secondary_y=False)
        fig.add_trace(go.Scatter(x=daily['date'], y=daily['orders'], name='Orders', line=dict(color='#10b981')), secondary_y=True)
        fig = apply_chart_style(fig, height=350)
        fig.update_layout(yaxis_title="Revenue (AED)", yaxis2_title="Orders")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No time series data available")
    
    # Category and Payment Analysis
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📊 Revenue by Category")
        if 'category' in filtered_df.columns and 'revenue' in filtered_df.columns:
            cat_data = filtered_df.groupby('category')['revenue'].sum().reset_index().sort_values('revenue', ascending=True)
            fig = px.bar(cat_data, x='revenue', y='category', orientation='h', color='category', color_discrete_sequence=get_chart_colors())
            fig = apply_chart_style(fig, height=300, show_legend=False)
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### 💳 Payment Methods")
        if 'payment_method' in filtered_df.columns and 'revenue' in filtered_df.columns:
            payment_data = filtered_df.groupby('payment_method')['revenue'].sum().reset_index()
            fig = px.pie(payment_data, values='revenue', names='payment_method', hole=0.4, color_discrete_sequence=get_chart_colors())
            fig = apply_chart_style(fig, height=300)
            st.plotly_chart(fig, use_container_width=True)
    
    # Top Products
    st.markdown("#### 🏆 Top 10 Products")
    if 'product_id' in filtered_df.columns and 'revenue' in filtered_df.columns:
        top_products = filtered_df.groupby('product_id').agg({
            'revenue': 'sum',
            'qty': 'sum',
            'order_id': 'nunique'
        }).reset_index().sort_values('revenue', ascending=False).head(10)
        top_products.columns = ['Product', 'Revenue', 'Units', 'Orders']
        top_products['Revenue'] = top_products['Revenue'].apply(format_currency)
        st.dataframe(top_products, use_container_width=True, hide_index=True)

# =============================================================================
# INVENTORY HEALTH TAB
# =============================================================================
def render_inventory_analysis(inventory_df, sales_df, products_df, stores_df):
    """Render inventory health dashboard."""
    st.markdown("## 📦 Inventory Health")
    st.markdown("Stock levels and reorder alerts")
    st.markdown("---")
    
    if len(inventory_df) == 0:
        st.warning("No inventory data available")
        return
    
    # Get latest snapshot
    latest_date = inventory_df['snapshot_date'].max()
    latest_inv = inventory_df[inventory_df['snapshot_date'] == latest_date].copy()
    
    # Filters
    col1, col2 = st.columns(2)
    with col1:
        cities = latest_inv['city'].unique().tolist() if 'city' in latest_inv.columns else STANDARD_CITIES
        city_filter = st.selectbox("🏙️ City", ['All'] + cities, key='inv_city')
    with col2:
        status_filter = st.selectbox("📊 Stock Status", ['All', 'Healthy', 'Low', 'Critical'], key='inv_status')
    
    # Apply filters
    filtered_inv = latest_inv.copy()
    if city_filter != 'All' and 'city' in filtered_inv.columns:
        filtered_inv = filtered_inv[filtered_inv['city'] == city_filter]
    if status_filter != 'All' and 'stock_status' in filtered_inv.columns:
        filtered_inv = filtered_inv[filtered_inv['stock_status'] == status_filter]
    
    # KPIs
    total_stock = filtered_inv['stock_on_hand'].sum() if 'stock_on_hand' in filtered_inv.columns else 0
    total_skus = filtered_inv['product_id'].nunique() if 'product_id' in filtered_inv.columns else 0
    healthy_count = len(filtered_inv[filtered_inv['stock_status'] == 'Healthy']) if 'stock_status' in filtered_inv.columns else 0
    critical_count = len(filtered_inv[filtered_inv['stock_status'] == 'Critical']) if 'stock_status' in filtered_inv.columns else 0
    healthy_pct = healthy_count / len(filtered_inv) * 100 if len(filtered_inv) > 0 else 0
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("📦 Total Stock", format_number(total_stock))
    col2.metric("🏷️ SKUs", format_number(total_skus))
    col3.metric("✅ Health Rate", f"{healthy_pct:.1f}%")
    col4.metric("🔴 Critical Items", critical_count)
    
    st.markdown("")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📊 Stock Status Distribution")
        if 'stock_status' in filtered_inv.columns:
            status_counts = filtered_inv['stock_status'].value_counts().reset_index()
            status_counts.columns = ['status', 'count']
            colors_map = {'Healthy': '#10b981', 'Low': '#f59e0b', 'Critical': '#ef4444'}
            fig = px.pie(status_counts, values='count', names='status', hole=0.4, color='status', color_discrete_map=colors_map)
            fig = apply_chart_style(fig, height=300)
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### 📦 Stock by Category")
        if 'category' in filtered_inv.columns and 'stock_on_hand' in filtered_inv.columns:
            cat_stock = filtered_inv.groupby('category')['stock_on_hand'].sum().reset_index().sort_values('stock_on_hand', ascending=True)
            fig = px.bar(cat_stock, x='stock_on_hand', y='category', orientation='h', color='category', color_discrete_sequence=get_chart_colors())
            fig = apply_chart_style(fig, height=300, show_legend=False)
            st.plotly_chart(fig, use_container_width=True)
    
    # Critical Items Table
    st.markdown("#### 🔴 Critical Stock Items")
    if 'stock_status' in filtered_inv.columns:
        critical = filtered_inv[filtered_inv['stock_status'] == 'Critical']
        display_cols = [c for c in ['product_id', 'category', 'stock_on_hand', 'reorder_point', 'city', 'channel'] if c in critical.columns]
        if len(critical) > 0 and display_cols:
            st.dataframe(critical[display_cols].head(20), use_container_width=True, hide_index=True)
        else:
            st.success("No critical stock items!")

# =============================================================================
# CAMPAIGN PERFORMANCE TAB
# =============================================================================
def render_campaign_analysis(campaigns_df, sales_df, products_df, stores_df):
    """Render campaign performance dashboard."""
    st.markdown("## 🎯 Campaign Performance")
    st.markdown("Analyze campaigns and simulate promotions")
    st.markdown("---")
    
    if len(campaigns_df) == 0:
        st.warning("No campaign data available")
        return
    
    # Campaign Overview
    total_campaigns = len(campaigns_df)
    active_campaigns = campaigns_df['is_active'].sum() if 'is_active' in campaigns_df.columns else 0
    total_budget = campaigns_df['promo_budget_aed'].sum() if 'promo_budget_aed' in campaigns_df.columns else 0
    avg_discount = campaigns_df['discount_pct'].mean() if 'discount_pct' in campaigns_df.columns else 0
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("🎯 Total Campaigns", total_campaigns)
    col2.metric("✅ Active", int(active_campaigns))
    col3.metric("💰 Total Budget", format_currency(total_budget))
    col4.metric("🏷️ Avg Discount", f"{avg_discount:.0f}%")
    
    st.markdown("")
    
    # Campaign Timeline
    st.markdown("#### 📅 Campaign Timeline")
    if 'start_date' in campaigns_df.columns and 'end_date' in campaigns_df.columns:
        fig = px.timeline(campaigns_df, x_start='start_date', x_end='end_date', y='campaign_id', 
                          color='discount_pct', color_continuous_scale=['#10b981', '#f59e0b', '#ef4444'])
        fig = apply_chart_style(fig, height=350)
        st.plotly_chart(fig, use_container_width=True)
    
    # Campaign Table
    st.markdown("#### 📋 Campaign Details")
    display_cols = [c for c in ['campaign_id', 'start_date', 'end_date', 'city', 'channel', 'category', 'discount_pct', 'promo_budget_aed', 'is_active'] if c in campaigns_df.columns]
    if display_cols:
        display_df = campaigns_df[display_cols].copy()
        if 'start_date' in display_df.columns:
            display_df['start_date'] = pd.to_datetime(display_df['start_date']).dt.strftime('%Y-%m-%d')
        if 'end_date' in display_df.columns:
            display_df['end_date'] = pd.to_datetime(display_df['end_date']).dt.strftime('%Y-%m-%d')
        if 'promo_budget_aed' in display_df.columns:
            display_df['promo_budget_aed'] = display_df['promo_budget_aed'].apply(format_currency)
        st.dataframe(display_df, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # What-If Simulator
    st.markdown("### 🔬 What-If Promotion Simulator")
    
    categories = sales_df['category'].unique().tolist() if 'category' in sales_df.columns else CATEGORIES
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        sim_category = st.selectbox("Category", categories, key='sim_cat')
    with col2:
        sim_discount = st.slider("Discount %", 5, 50, 20, key='sim_disc')
    with col3:
        sim_duration = st.slider("Duration (Days)", 1, 30, 7, key='sim_dur')
    with col4:
        sim_lift = st.slider("Expected Lift", 1.0, 3.0, 1.5, 0.1, key='sim_lift')
    
    # Calculate simulation
    if 'category' in sales_df.columns and 'revenue' in sales_df.columns:
        cat_sales = sales_df[sales_df['category'] == sim_category]
        if len(cat_sales) > 0 and 'order_time' in cat_sales.columns:
            date_range = (cat_sales['order_time'].max() - cat_sales['order_time'].min()).days
            date_range = max(1, date_range)
            
            baseline_daily_revenue = cat_sales['revenue'].sum() / date_range
            baseline_total = baseline_daily_revenue * sim_duration
            promo_total = baseline_daily_revenue * sim_lift * sim_duration * (1 - sim_discount/200)  # Adjusted formula
            incremental = promo_total - baseline_total
            
            col1, col2, col3 = st.columns(3)
            col1.metric("📊 Baseline Revenue", format_currency(baseline_total))
            col2.metric("🚀 Projected Revenue", format_currency(promo_total))
            col3.metric("📈 Incremental", format_currency(incremental), 
                       delta=f"{(incremental/baseline_total*100):.1f}%" if baseline_total > 0 else "0%")
        else:
            st.info("Not enough data for simulation")
    else:
        st.info("Category or revenue data not available for simulation")

# =============================================================================
# STORE PERFORMANCE TAB
# =============================================================================
def render_store_performance(stores_df, sales_df, inventory_df):
    """Render store performance dashboard."""
    st.markdown("## 🏪 Store Performance")
    st.markdown("Compare performance across locations")
    st.markdown("---")
    
    # Calculate store metrics
    if 'store_id' in sales_df.columns and 'revenue' in sales_df.columns:
        store_metrics = sales_df.groupby('store_id').agg({
            'revenue': 'sum',
            'order_id': 'nunique',
            'qty': 'sum'
        }).reset_index()
        store_metrics.columns = ['store_id', 'revenue', 'orders', 'units']
        store_metrics['aov'] = store_metrics['revenue'] / store_metrics['orders']
        
        # Merge store info
        if 'store_id' in stores_df.columns:
            store_metrics = store_metrics.merge(stores_df[['store_id', 'city', 'channel']], on='store_id', how='left')
    else:
        st.warning("Store performance data not available")
        return
    
    # KPIs
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("🏪 Total Stores", len(store_metrics))
    col2.metric("💰 Total Revenue", format_currency(store_metrics['revenue'].sum()))
    col3.metric("📊 Avg Revenue/Store", format_currency(store_metrics['revenue'].mean()))
    col4.metric("💵 Avg AOV", format_currency(store_metrics['aov'].mean()))
    
    st.markdown("")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🏆 Top 10 Stores by Revenue")
        top_10 = store_metrics.nlargest(10, 'revenue')
        fig = px.bar(top_10.sort_values('revenue'), x='revenue', y='store_id', orientation='h', 
                    color='city' if 'city' in top_10.columns else None, color_discrete_sequence=get_chart_colors())
        fig = apply_chart_style(fig, height=350)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### 🏙️ Revenue by City")
        if 'city' in store_metrics.columns:
            city_metrics = store_metrics.groupby('city')['revenue'].sum().reset_index()
            fig = px.pie(city_metrics, values='revenue', names='city', hole=0.4, color_discrete_sequence=get_chart_colors())
            fig = apply_chart_style(fig, height=350)
            st.plotly_chart(fig, use_container_width=True)
    
    # Store Table
    st.markdown("#### 📋 Store Rankings")
    display_df = store_metrics.sort_values('revenue', ascending=False).copy()
    display_df['revenue'] = display_df['revenue'].apply(format_currency)
    display_df['aov'] = display_df['aov'].apply(format_currency)
    st.dataframe(display_df, use_container_width=True, hide_index=True)

# =============================================================================
# TIME PATTERNS TAB
# =============================================================================
def render_time_patterns(sales_df):
    """Render time pattern analysis."""
    st.markdown("## ⏰ Time Pattern Analysis")
    st.markdown("Discover sales patterns across time")
    st.markdown("---")
    
    if 'order_time' not in sales_df.columns:
        st.warning("No timestamp data available for time pattern analysis")
        return
    
    # Extract time components
    df = sales_df.copy()
    df['hour'] = df['order_time'].dt.hour
    df['day_name'] = df['order_time'].dt.day_name()
    df['day_num'] = df['order_time'].dt.dayofweek
    
    revenue_col = 'revenue' if 'revenue' in df.columns else None
    if revenue_col is None:
        st.warning("No revenue data available")
        return
    
    # Hourly Pattern
    st.markdown("#### 🕐 Hourly Sales Pattern")
    hourly = df.groupby('hour')[revenue_col].sum().reset_index()
    fig = px.bar(hourly, x='hour', y=revenue_col, color=revenue_col, 
                color_continuous_scale=['#312e81', '#6366f1', '#a5b4fc'])
    fig = apply_chart_style(fig, height=300, show_legend=False)
    fig.update_layout(xaxis_title="Hour of Day", yaxis_title="Revenue (AED)", coloraxis_showscale=False)
    st.plotly_chart(fig, use_container_width=True)
    
    # Daily Pattern and Heatmap
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📅 Daily Sales Pattern")
        daily = df.groupby(['day_num', 'day_name'])[revenue_col].sum().reset_index().sort_values('day_num')
        fig = px.bar(daily, x='day_name', y=revenue_col, color=revenue_col, 
                    color_continuous_scale=['#312e81', '#6366f1', '#a5b4fc'])
        fig = apply_chart_style(fig, height=300, show_legend=False)
        fig.update_layout(coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### 📊 Hour × Day Heatmap")
        hour_day = df.groupby(['hour', 'day_num'])[revenue_col].sum().reset_index()
        pivot = hour_day.pivot(index='hour', columns='day_num', values=revenue_col).fillna(0)
        pivot.columns = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        fig = px.imshow(pivot, color_continuous_scale='Purples', aspect='auto')
        fig = apply_chart_style(fig, height=300)
        st.plotly_chart(fig, use_container_width=True)

# =============================================================================
# DATA EXPLORER TAB
# =============================================================================
def render_data_explorer(sales_df, products_df, stores_df, inventory_df, campaigns_df):
    """Render data explorer for ad-hoc analysis."""
    st.markdown("## 🔍 Data Explorer")
    st.markdown("Explore and export data")
    st.markdown("---")
    
    datasets = {
        "Sales": sales_df,
        "Products": products_df,
        "Stores": stores_df,
        "Inventory": inventory_df,
        "Campaigns": campaigns_df
    }
    
    selected = st.selectbox("Select Dataset", list(datasets.keys()))
    df = datasets[selected]
    
    st.markdown(f"**Rows:** {len(df):,} | **Columns:** {len(df.columns)}")
    
    # Show all columns by default or let user select
    all_cols = df.columns.tolist()
    default_cols = all_cols[:min(10, len(all_cols))]
    cols = st.multiselect("Select Columns", all_cols, default=default_cols)
    
    if cols:
        st.dataframe(df[cols], use_container_width=True, height=400)
        
        # Export button
        csv = df[cols].to_csv(index=False)
        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name=f"{selected.lower()}_export.csv",
            mime="text/csv"
        )
    else:
        st.info("Please select at least one column")

# =============================================================================
# MAIN APPLICATION
# =============================================================================
def main():
    """Main application entry point."""
    # Apply CSS
    apply_custom_css()
    
    # Load/Generate Data
    if 'data_loaded' not in st.session_state:
        with st.spinner("🔄 Loading data..."):
            try:
                sales_df, products_df, stores_df, inventory_df, campaigns_df = generate_all_data()
                st.session_state.sales_df = sales_df
                st.session_state.products_df = products_df
                st.session_state.stores_df = stores_df
                st.session_state.inventory_df = inventory_df
                st.session_state.campaigns_df = campaigns_df
                st.session_state.data_loaded = True
            except Exception as e:
                st.error(f"Error loading data: {str(e)}")
                return
    
    # Get data from session state
    sales_df = st.session_state.sales_df
    products_df = st.session_state.products_df
    stores_df = st.session_state.stores_df
    inventory_df = st.session_state.inventory_df
    campaigns_df = st.session_state.campaigns_df
    
    # Sidebar Navigation
    with st.sidebar:
        st.markdown("# 🛒 UAE Retail")
        st.markdown("**Analytics Dashboard**")
        st.markdown("---")
        
        nav = st.radio(
            "Navigation",
            options=[
                "🏠 Overview",
                "📈 Sales",
                "📦 Inventory",
                "🎯 Campaigns",
                "🏪 Stores",
                "⏰ Time Patterns",
                "🔍 Explorer"
            ],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        # Quick Stats
        if 'revenue' in sales_df.columns:
            st.markdown(f"**💰 Revenue:** {format_currency(sales_df['revenue'].sum())}")
        if 'order_id' in sales_df.columns:
            st.markdown(f"**🛒 Orders:** {format_number(sales_df['order_id'].nunique())}")
        
        st.markdown("---")
        
        # Refresh button
        if st.button("🔄 Refresh Data", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
        
        st.markdown("---")
        st.caption(f"Updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    
    # Render Selected Tab
    if nav == "🏠 Overview":
        render_executive_overview(sales_df, inventory_df, campaigns_df, stores_df)
    elif nav == "📈 Sales":
        render_sales_analysis(sales_df, products_df, stores_df)
    elif nav == "📦 Inventory":
        render_inventory_analysis(inventory_df, sales_df, products_df, stores_df)
    elif nav == "🎯 Campaigns":
        render_campaign_analysis(campaigns_df, sales_df, products_df, stores_df)
    elif nav == "🏪 Stores":
        render_store_performance(stores_df, sales_df, inventory_df)
    elif nav == "⏰ Time Patterns":
        render_time_patterns(sales_df)
    elif nav == "🔍 Explorer":
        render_data_explorer(sales_df, products_df, stores_df, inventory_df, campaigns_df)

# =============================================================================
# RUN APPLICATION
# =============================================================================
if __name__ == "__main__":
    main()
