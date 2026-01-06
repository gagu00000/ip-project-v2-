# =============================================================================
# UAE RETAIL ANALYTICS DASHBOARD - COMPLETE SINGLE FILE
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
CITY_MAPPING = {
    'DXB': 'Dubai', 'Dubai': 'Dubai', 'DUBAI': 'Dubai',
    'AUH': 'Abu Dhabi', 'Abu Dhabi': 'Abu Dhabi', 'ABU DHABI': 'Abu Dhabi',
    'SHJ': 'Sharjah', 'Sharjah': 'Sharjah', 'SHARJAH': 'Sharjah'
}

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
        padding: 8px 24px;
        font-weight: 600;
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
# DATA GENERATION
# =============================================================================
@st.cache_data
def generate_data():
    np.random.seed(42)
    random.seed(42)
    
    # Date range
    end_date = datetime.now()
    start_date = end_date - timedelta(days=120)
    
    # Generate Products
    products = []
    for i in range(200):
        cat = random.choice(CATEGORIES)
        products.append({
            'product_id': f'PROD_{i+1:04d}',
            'category': cat,
            'brand': f'Brand_{random.randint(1, 20)}',
            'unit_cost_aed': round(random.uniform(10, 500), 2)
        })
    products_df = pd.DataFrame(products)
    
    # Generate Stores
    stores = []
    for i in range(30):
        stores.append({
            'store_id': f'STORE_{i+1:03d}',
            'city': random.choice(STANDARD_CITIES),
            'channel': random.choice(CHANNELS)
        })
    stores_df = pd.DataFrame(stores)
    
    # Generate Sales
    sales = []
    for i in range(50000):
        order_date = start_date + timedelta(days=random.randint(0, 120))
        order_time = order_date.replace(hour=random.randint(8, 22), minute=random.randint(0, 59))
        product = random.choice(products)
        store = random.choice(stores)
        qty = random.randint(1, 5)
        unit_price = product['unit_cost_aed'] * random.uniform(1.2, 2.5)
        discount = random.choice([0, 5, 10, 15, 20, 25])
        selling_price = unit_price * (1 - discount/100)
        
        sales.append({
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
            'channel': store['channel']
        })
    
    sales_df = pd.DataFrame(sales)
    sales_df['revenue'] = sales_df['selling_price_aed'] * sales_df['qty']
    sales_df['city_clean'] = sales_df['city'].replace(CITY_MAPPING)
    
    # Generate Inventory
    inventory = []
    for days_ago in range(0, 30, 7):
        snapshot_date = end_date - timedelta(days=days_ago)
        for product in products:
            for store in stores:
                stock = random.randint(-10, 500)
                reorder_point = random.randint(20, 100)
                inventory.append({
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
    
    inventory_df = pd.DataFrame(inventory)
    inventory_df['snapshot_date'] = pd.to_datetime(inventory_df['snapshot_date'])
    inventory_df['city_clean'] = inventory_df['city'].replace(CITY_MAPPING)
    inventory_df['stock_status'] = inventory_df.apply(
        lambda x: 'Critical' if x['stock_on_hand'] <= 0 
        else 'Low' if x['stock_on_hand'] <= x['reorder_point'] 
        else 'Healthy', axis=1
    )
    
    # Generate Campaigns
    campaigns = []
    for i in range(15):
        camp_start = start_date + timedelta(days=random.randint(0, 90))
        duration = random.randint(3, 14)
        campaigns.append({
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
    campaigns_df = pd.DataFrame(campaigns)
    
    return sales_df, products_df, stores_df, inventory_df, campaigns_df

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================
def format_currency(value):
    if value >= 1_000_000:
        return f"AED {value/1_000_000:.2f}M"
    elif value >= 1_000:
        return f"AED {value/1_000:.1f}K"
    return f"AED {value:.2f}"

def format_number(value):
    if value >= 1_000_000:
        return f"{value/1_000_000:.2f}M"
    elif value >= 1_000:
        return f"{value/1_000:.1f}K"
    return f"{value:,.0f}"

def get_chart_colors():
    return ['#6366f1', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#06b6d4']

def apply_chart_style(fig, height=400, show_legend=True):
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#a1a1aa'),
        height=height,
        showlegend=show_legend,
        margin=dict(l=20, r=20, t=40, b=20),
        legend=dict(
            bgcolor='rgba(0,0,0,0)',
            font=dict(color='#a1a1aa')
        ),
        xaxis=dict(gridcolor='rgba(255,255,255,0.1)', zerolinecolor='rgba(255,255,255,0.1)'),
        yaxis=dict(gridcolor='rgba(255,255,255,0.1)', zerolinecolor='rgba(255,255,255,0.1)')
    )
    return fig

# =============================================================================
# EXECUTIVE OVERVIEW TAB
# =============================================================================
def render_executive_overview(sales_df, inventory_df, campaigns_df, stores_df):
    st.markdown("## 🏠 Executive Overview")
    st.markdown("Real-time business performance snapshot")
    st.markdown("---")
    
    # KPIs
    total_revenue = sales_df['revenue'].sum()
    total_orders = sales_df['order_id'].nunique()
    avg_order_value = total_revenue / total_orders if total_orders > 0 else 0
    total_units = sales_df['qty'].sum()
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("💰 Total Revenue", format_currency(total_revenue))
    col2.metric("🛒 Total Orders", format_number(total_orders))
    col3.metric("📦 Units Sold", format_number(total_units))
    col4.metric("💵 Avg Order Value", format_currency(avg_order_value))
    
    st.markdown("")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📈 Daily Revenue Trend")
        daily_revenue = sales_df.groupby(sales_df['order_time'].dt.date)['revenue'].sum().reset_index()
        daily_revenue.columns = ['date', 'revenue']
        fig = px.area(daily_revenue, x='date', y='revenue', color_discrete_sequence=['#6366f1'])
        fig.update_traces(fill='tozeroy', fillcolor='rgba(99, 102, 241, 0.2)')
        fig = apply_chart_style(fig, height=300)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### 📊 Revenue by Category")
        cat_revenue = sales_df.groupby('category')['revenue'].sum().reset_index()
        fig = px.pie(cat_revenue, values='revenue', names='category', hole=0.4, color_discrete_sequence=get_chart_colors())
        fig = apply_chart_style(fig, height=300)
        st.plotly_chart(fig, use_container_width=True)
    
    # More charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🏙️ Revenue by City")
        city_revenue = sales_df.groupby('city_clean')['revenue'].sum().reset_index()
        fig = px.bar(city_revenue, x='city_clean', y='revenue', color='city_clean', color_discrete_sequence=get_chart_colors())
        fig = apply_chart_style(fig, height=300, show_legend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### 📱 Revenue by Channel")
        channel_revenue = sales_df.groupby('channel')['revenue'].sum().reset_index()
        fig = px.bar(channel_revenue, x='channel', y='revenue', color='channel', color_discrete_sequence=get_chart_colors())
        fig = apply_chart_style(fig, height=300, show_legend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    # Inventory Status
    st.markdown("#### 📦 Inventory Health Status")
    latest_inv = inventory_df[inventory_df['snapshot_date'] == inventory_df['snapshot_date'].max()]
    status_counts = latest_inv['stock_status'].value_counts()
    
    col1, col2, col3 = st.columns(3)
    col1.metric("✅ Healthy Items", status_counts.get('Healthy', 0))
    col2.metric("⚠️ Low Stock", status_counts.get('Low', 0))
    col3.metric("🔴 Critical", status_counts.get('Critical', 0))

# =============================================================================
# SALES ANALYTICS TAB
# =============================================================================
def render_sales_analysis(sales_df, products_df, stores_df):
    st.markdown("## 📈 Sales Analytics")
    st.markdown("Deep dive into sales performance")
    st.markdown("---")
    
    # Filters
    col1, col2, col3 = st.columns(3)
    with col1:
        city_filter = st.selectbox("🏙️ City", ['All'] + STANDARD_CITIES, key='sales_city')
    with col2:
        channel_filter = st.selectbox("📱 Channel", ['All'] + CHANNELS, key='sales_channel')
    with col3:
        category_filter = st.selectbox("📦 Category", ['All'] + CATEGORIES, key='sales_category')
    
    # Apply filters
    filtered_df = sales_df.copy()
    if city_filter != 'All':
        filtered_df = filtered_df[filtered_df['city_clean'] == city_filter]
    if channel_filter != 'All':
        filtered_df = filtered_df[filtered_df['channel'] == channel_filter]
    if category_filter != 'All':
        filtered_df = filtered_df[filtered_df['category'] == category_filter]
    
    # KPIs
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("💰 Revenue", format_currency(filtered_df['revenue'].sum()))
    col2.metric("🛒 Orders", format_number(filtered_df['order_id'].nunique()))
    col3.metric("📦 Units", format_number(filtered_df['qty'].sum()))
    col4.metric("🏷️ Avg Discount", f"{filtered_df['discount_pct'].mean():.1f}%")
    
    st.markdown("")
    
    # Sales Trend
    st.markdown("#### 📈 Sales Trend")
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
    
    # Category and Channel Analysis
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📊 Revenue by Category")
        cat_data = filtered_df.groupby('category')['revenue'].sum().reset_index().sort_values('revenue', ascending=True)
        fig = px.bar(cat_data, x='revenue', y='category', orientation='h', color='category', color_discrete_sequence=get_chart_colors())
        fig = apply_chart_style(fig, height=300, show_legend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### 💳 Payment Methods")
        payment_data = filtered_df.groupby('payment_method')['revenue'].sum().reset_index()
        fig = px.pie(payment_data, values='revenue', names='payment_method', hole=0.4, color_discrete_sequence=get_chart_colors())
        fig = apply_chart_style(fig, height=300)
        st.plotly_chart(fig, use_container_width=True)
    
    # Top Products
    st.markdown("#### 🏆 Top 10 Products")
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
    st.markdown("## 📦 Inventory Health")
    st.markdown("Stock levels and reorder alerts")
    st.markdown("---")
    
    # Get latest snapshot
    latest_date = inventory_df['snapshot_date'].max()
    latest_inv = inventory_df[inventory_df['snapshot_date'] == latest_date].copy()
    
    # Filters
    col1, col2 = st.columns(2)
    with col1:
        city_filter = st.selectbox("🏙️ City", ['All'] + STANDARD_CITIES, key='inv_city')
    with col2:
        status_filter = st.selectbox("📊 Stock Status", ['All', 'Healthy', 'Low', 'Critical'], key='inv_status')
    
    # Apply filters
    filtered_inv = latest_inv.copy()
    if city_filter != 'All':
        filtered_inv = filtered_inv[filtered_inv['city_clean'] == city_filter]
    if status_filter != 'All':
        filtered_inv = filtered_inv[filtered_inv['stock_status'] == status_filter]
    
    # KPIs
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("📦 Total Stock", format_number(filtered_inv['stock_on_hand'].sum()))
    col2.metric("🏷️ SKUs", format_number(filtered_inv['product_id'].nunique()))
    healthy_pct = len(filtered_inv[filtered_inv['stock_status'] == 'Healthy']) / len(filtered_inv) * 100 if len(filtered_inv) > 0 else 0
    col3.metric("✅ Health Rate", f"{healthy_pct:.1f}%")
    col4.metric("🔴 Critical Items", len(filtered_inv[filtered_inv['stock_status'] == 'Critical']))
    
    st.markdown("")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📊 Stock Status Distribution")
        status_counts = filtered_inv['stock_status'].value_counts().reset_index()
        status_counts.columns = ['status', 'count']
        colors_map = {'Healthy': '#10b981', 'Low': '#f59e0b', 'Critical': '#ef4444'}
        fig = px.pie(status_counts, values='count', names='status', hole=0.4, color='status', color_discrete_map=colors_map)
        fig = apply_chart_style(fig, height=300)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### 📦 Stock by Category")
        cat_stock = filtered_inv.groupby('category')['stock_on_hand'].sum().reset_index().sort_values('stock_on_hand', ascending=True)
        fig = px.bar(cat_stock, x='stock_on_hand', y='category', orientation='h', color='category', color_discrete_sequence=get_chart_colors())
        fig = apply_chart_style(fig, height=300, show_legend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    # Critical Items Table
    st.markdown("#### 🔴 Critical Stock Items")
    critical = filtered_inv[filtered_inv['stock_status'] == 'Critical'][['product_id', 'category', 'stock_on_hand', 'reorder_point', 'city_clean', 'channel']].head(20)
    critical.columns = ['Product', 'Category', 'Stock', 'Reorder Point', 'City', 'Channel']
    st.dataframe(critical, use_container_width=True, hide_index=True)

# =============================================================================
# CAMPAIGN PERFORMANCE TAB
# =============================================================================
def render_campaign_analysis(campaigns_df, sales_df, products_df, stores_df):
    st.markdown("## 🎯 Campaign Performance")
    st.markdown("Analyze campaigns and simulate promotions")
    st.markdown("---")
    
    # Campaign Overview
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("🎯 Total Campaigns", len(campaigns_df))
    col2.metric("✅ Active", campaigns_df['is_active'].sum())
    col3.metric("💰 Total Budget", format_currency(campaigns_df['promo_budget_aed'].sum()))
    col4.metric("🏷️ Avg Discount", f"{campaigns_df['discount_pct'].mean():.0f}%")
    
    st.markdown("")
    
    # Campaign Timeline
    st.markdown("#### 📅 Campaign Timeline")
    fig = px.timeline(campaigns_df, x_start='start_date', x_end='end_date', y='campaign_id', color='discount_pct',
                      color_continuous_scale=['#10b981', '#f59e0b', '#ef4444'])
    fig = apply_chart_style(fig, height=350)
    st.plotly_chart(fig, use_container_width=True)
    
    # Campaign Table
    st.markdown("#### 📋 Campaign Details")
    display_df = campaigns_df[['campaign_id', 'start_date', 'end_date', 'city', 'channel', 'category', 'discount_pct', 'promo_budget_aed', 'is_active']].copy()
    display_df['start_date'] = pd.to_datetime(display_df['start_date']).dt.strftime('%Y-%m-%d')
    display_df['end_date'] = pd.to_datetime(display_df['end_date']).dt.strftime('%Y-%m-%d')
    display_df['promo_budget_aed'] = display_df['promo_budget_aed'].apply(format_currency)
    display_df.columns = ['Campaign', 'Start', 'End', 'City', 'Channel', 'Category', 'Discount %', 'Budget', 'Active']
    st.dataframe(display_df, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # What-If Simulator
    st.markdown("### 🔬 What-If Promotion Simulator")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        sim_category = st.selectbox("Category", CATEGORIES, key='sim_cat')
    with col2:
        sim_discount = st.slider("Discount %", 5, 50, 20, key='sim_disc')
    with col3:
        sim_duration = st.slider("Duration (Days)", 1, 30, 7, key='sim_dur')
    with col4:
        sim_lift = st.slider("Expected Lift", 1.0, 3.0, 1.5, 0.1, key='sim_lift')
    
    # Calculate simulation
    cat_sales = sales_df[sales_df['category'] == sim_category]
    if len(cat_sales) > 0:
        date_range = (cat_sales['order_time'].max() - cat_sales['order_time'].min()).days
        date_range = max(1, date_range)
        
        baseline_daily_revenue = cat_sales['revenue'].sum() / date_range
        baseline_avg_price = cat_sales['selling_price_aed'].mean()
        
        promo_price = baseline_avg_price * (1 - sim_discount/100)
        baseline_total = baseline_daily_revenue * sim_duration
        promo_total = baseline_daily_revenue * sim_lift * (1 - sim_discount/100) * sim_duration
        incremental = promo_total - baseline_total
        
        col1, col2, col3 = st.columns(3)
        col1.metric("📊 Baseline Revenue", format_currency(baseline_total))
        col2.metric("🚀 Projected Revenue", format_currency(promo_total))
        
        delta_color = "normal" if incremental >= 0 else "inverse"
        col3.metric("📈 Incremental", format_currency(incremental), delta=f"{(incremental/baseline_total*100):.1f}%" if baseline_total > 0 else "0%")

# =============================================================================
# STORE PERFORMANCE TAB
# =============================================================================
def render_store_performance(stores_df, sales_df, inventory_df):
    st.markdown("## 🏪 Store Performance")
    st.markdown("Compare performance across locations")
    st.markdown("---")
    
    # Calculate store metrics
    store_metrics = sales_df.groupby('store_id').agg({
        'revenue': 'sum',
        'order_id': 'nunique',
        'qty': 'sum'
    }).reset_index()
    store_metrics.columns = ['store_id', 'revenue', 'orders', 'units']
    store_metrics['aov'] = store_metrics['revenue'] / store_metrics['orders']
    store_metrics = store_metrics.merge(stores_df[['store_id', 'city', 'channel']], on='store_id', how='left')
    
    # KPIs
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("🏪 Total Stores", len(store_metrics))
    col2.metric("💰 Total Revenue", format_currency(store_metrics['revenue'].sum()))
    col3.metric("📊 Avg Revenue/Store", format_currency(store_metrics['revenue'].mean()))
    col4.metric("💵 Avg AOV", format_currency(store_metrics['aov'].mean()))
    
    st.markdown("")
    
    # Top Stores
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🏆 Top 10 Stores by Revenue")
        top_10 = store_metrics.nlargest(10, 'revenue')
        fig = px.bar(top_10.sort_values('revenue'), x='revenue', y='store_id', orientation='h', color='city', color_discrete_sequence=get_chart_colors())
        fig = apply_chart_style(fig, height=350)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### 🏙️ Revenue by City")
        city_metrics = store_metrics.groupby('city')['revenue'].sum().reset_index()
        fig = px.pie(city_metrics, values='revenue', names='city', hole=0.4, color_discrete_sequence=get_chart_colors())
        fig = apply_chart_style(fig, height=350)
        st.plotly_chart(fig, use_container_width=True)
    
    # Store Table
    st.markdown("#### 📋 Store Rankings")
    display_df = store_metrics.sort_values('revenue', ascending=False).copy()
    display_df['revenue'] = display_df['revenue'].apply(format_currency)
    display_df['aov'] = display_df['aov'].apply(format_currency)
    display_df.columns = ['Store', 'Revenue', 'Orders', 'Units', 'AOV', 'City', 'Channel']
    st.dataframe(display_df, use_container_width=True, hide_index=True)

# =============================================================================
# TIME PATTERNS TAB
# =============================================================================
def render_time_patterns(sales_df):
    st.markdown("## ⏰ Time Pattern Analysis")
    st.markdown("Discover sales patterns across time")
    st.markdown("---")
    
    # Extract time components
    df = sales_df.copy()
    df['hour'] = df['order_time'].dt.hour
    df['day_name'] = df['order_time'].dt.day_name()
    df['day_num'] = df['order_time'].dt.dayofweek
    df['month'] = df['order_time'].dt.month_name()
    
    # Hourly Pattern
    st.markdown("#### 🕐 Hourly Sales Pattern")
    hourly = df.groupby('hour')['revenue'].sum().reset_index()
    fig = px.bar(hourly, x='hour', y='revenue', color='revenue', color_continuous_scale=['#312e81', '#6366f1', '#a5b4fc'])
    fig = apply_chart_style(fig, height=300, show_legend=False)
    fig.update_layout(xaxis_title="Hour of Day", yaxis_title="Revenue (AED)", coloraxis_showscale=False)
    st.plotly_chart(fig, use_container_width=True)
    
    # Daily Pattern
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📅 Daily Sales Pattern")
        daily = df.groupby(['day_num', 'day_name'])['revenue'].sum().reset_index().sort_values('day_num')
        fig = px.bar(daily, x='day_name', y='revenue', color='revenue', color_continuous_scale=['#312e81', '#6366f1', '#a5b4fc'])
        fig = apply_chart_style(fig, height=300, show_legend=False)
        fig.update_layout(coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### 📊 Hour × Day Heatmap")
        hour_day = df.groupby(['hour', 'day_num'])['revenue'].sum().reset_index()
        pivot = hour_day.pivot(index='hour', columns='day_num', values='revenue').fillna(0)
        pivot.columns = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        fig = px.imshow(pivot, color_continuous_scale='Purples', aspect='auto')
        fig = apply_chart_style(fig, height=300)
        st.plotly_chart(fig, use_container_width=True)

# =============================================================================
# DATA EXPLORER TAB
# =============================================================================
def render_data_explorer(sales_df, products_df, stores_df, inventory_df, campaigns_df):
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
    
    # Column selection
    cols = st.multiselect("Select Columns", df.columns.tolist(), default=df.columns.tolist()[:8])
    
    if cols:
        st.dataframe(df[cols], use_container_width=True, height=400)
        
        # Export
        csv = df[cols].to_csv(index=False)
        st.download_button("📥 Download CSV", csv, f"{selected.lower()}_export.csv", "text/csv")

# =============================================================================
# MAIN APPLICATION
# =============================================================================
def main():
    apply_custom_css()
    
    # Load data
    if 'data_loaded' not in st.session_state:
        with st.spinner("Loading data..."):
            sales_df, products_df, stores_df, inventory_df, campaigns_df = generate_data()
            st.session_state.sales_df = sales_df
            st.session_state.products_df = products_df
            st.session_state.stores_df = stores_df
            st.session_state.inventory_df = inventory_df
            st.session_state.campaigns_df = campaigns_df
            st.session_state.data_loaded = True
    
    sales_df = st.session_state.sales_df
    products_df = st.session_state.products_df
    stores_df = st.session_state.stores_df
    inventory_df = st.session_state.inventory_df
    campaigns_df = st.session_state.campaigns_df
    
    # Sidebar
    with st.sidebar:
        st.markdown("# 🛒 UAE Retail")
        st.markdown("Analytics Dashboard")
        st.markdown("---")
        
        nav = st.radio(
            "Navigation",
            ["🏠 Overview", "📈 Sales", "📦 Inventory", "🎯 Campaigns", "🏪 Stores", "⏰ Time Patterns", "🔍 Explorer"],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        st.markdown(f"**Revenue:** {format_currency(sales_df['revenue'].sum())}")
        st.markdown(f"**Orders:** {format_number(sales_df['order_id'].nunique())}")
        
        st.markdown("---")
        if st.button("🔄 Refresh"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
    
    # Render selected tab
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

if __name__ == "__main__":
    main()
