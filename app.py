# =============================================================================
# UAE RETAIL ANALYTICS DASHBOARD
# WITH DATA INPUT, CLEANING, AND LOGGING
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
import io
import logging
from typing import Dict, List, Tuple, Optional

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
# LOGGING SETUP
# =============================================================================
class DashboardLogger:
    """Custom logger for tracking dashboard activities and data operations."""
    
    def __init__(self):
        self.logs = []
        self.data_quality_logs = []
        self.max_logs = 1000
    
    def log(self, level: str, category: str, message: str, details: dict = None):
        """Add a log entry."""
        entry = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'level': level,
            'category': category,
            'message': message,
            'details': details or {}
        }
        self.logs.append(entry)
        
        # Keep only recent logs
        if len(self.logs) > self.max_logs:
            self.logs = self.logs[-self.max_logs:]
    
    def info(self, category: str, message: str, details: dict = None):
        self.log('INFO', category, message, details)
    
    def warning(self, category: str, message: str, details: dict = None):
        self.log('WARNING', category, message, details)
    
    def error(self, category: str, message: str, details: dict = None):
        self.log('ERROR', category, message, details)
    
    def data_quality(self, dataset: str, issue_type: str, description: str, affected_rows: int = 0):
        """Log data quality issues."""
        entry = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'dataset': dataset,
            'issue_type': issue_type,
            'description': description,
            'affected_rows': affected_rows
        }
        self.data_quality_logs.append(entry)
    
    def get_logs(self, level: str = None, category: str = None, limit: int = 100):
        """Get filtered logs."""
        filtered = self.logs.copy()
        if level:
            filtered = [l for l in filtered if l['level'] == level]
        if category:
            filtered = [l for l in filtered if l['category'] == category]
        return filtered[-limit:]
    
    def get_data_quality_logs(self, limit: int = 100):
        """Get data quality logs."""
        return self.data_quality_logs[-limit:]
    
    def get_logs_df(self):
        """Get logs as DataFrame."""
        if not self.logs:
            return pd.DataFrame(columns=['timestamp', 'level', 'category', 'message'])
        return pd.DataFrame(self.logs)
    
    def get_data_quality_df(self):
        """Get data quality logs as DataFrame."""
        if not self.data_quality_logs:
            return pd.DataFrame(columns=['timestamp', 'dataset', 'issue_type', 'description', 'affected_rows'])
        return pd.DataFrame(self.data_quality_logs)

# Initialize logger in session state
if 'logger' not in st.session_state:
    st.session_state.logger = DashboardLogger()

logger = st.session_state.logger

# =============================================================================
# CONSTANTS
# =============================================================================
CATEGORIES = ['Electronics', 'Fashion', 'Grocery', 'Home & Garden', 'Beauty', 'Sports']
CHANNELS = ['App', 'Web', 'Marketplace']
STANDARD_CITIES = ['Dubai', 'Abu Dhabi', 'Sharjah']
PAYMENT_METHODS = ['Credit Card', 'Debit Card', 'Cash', 'Digital Wallet']

CITY_MAPPING = {
    'DXB': 'Dubai', 'Dubai': 'Dubai', 'DUBAI': 'Dubai', 'dubai': 'Dubai',
    'AUH': 'Abu Dhabi', 'Abu Dhabi': 'Abu Dhabi', 'ABU DHABI': 'Abu Dhabi', 'abudhabi': 'Abu Dhabi',
    'SHJ': 'Sharjah', 'Sharjah': 'Sharjah', 'SHARJAH': 'Sharjah', 'sharjah': 'Sharjah'
}

# Expected columns for each dataset
EXPECTED_COLUMNS = {
    'sales': ['order_id', 'order_time', 'product_id', 'store_id', 'qty', 'selling_price_aed'],
    'products': ['product_id', 'category'],
    'stores': ['store_id', 'city', 'channel'],
    'inventory': ['product_id', 'store_id', 'stock_on_hand', 'snapshot_date'],
    'campaigns': ['campaign_id', 'start_date', 'end_date', 'discount_pct']
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
    .log-info { color: #10b981; }
    .log-warning { color: #f59e0b; }
    .log-error { color: #ef4444; }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# =============================================================================
# DATA CLEANING CLASS
# =============================================================================
class DataCleaner:
    """Handles all data cleaning and validation operations."""
    
    def __init__(self, logger: DashboardLogger):
        self.logger = logger
        self.cleaning_report = {}
    
    def clean_sales_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean and validate sales data."""
        original_rows = len(df)
        self.logger.info('DATA_CLEANING', f'Starting sales data cleaning. Original rows: {original_rows}')
        
        cleaned_df = df.copy()
        
        # 1. Standardize column names
        cleaned_df.columns = cleaned_df.columns.str.lower().str.strip().str.replace(' ', '_')
        self.logger.info('DATA_CLEANING', 'Standardized column names to lowercase')
        
        # 2. Handle date/time columns
        date_columns = ['order_time', 'order_date', 'date', 'timestamp']
        for col in date_columns:
            if col in cleaned_df.columns:
                try:
                    cleaned_df[col] = pd.to_datetime(cleaned_df[col], errors='coerce')
                    null_dates = cleaned_df[col].isna().sum()
                    if null_dates > 0:
                        self.logger.data_quality('sales', 'INVALID_DATE', f'{null_dates} invalid dates in {col}', null_dates)
                except Exception as e:
                    self.logger.error('DATA_CLEANING', f'Error parsing dates in {col}: {str(e)}')
        
        # Ensure order_time exists
        if 'order_time' not in cleaned_df.columns:
            if 'order_date' in cleaned_df.columns:
                cleaned_df['order_time'] = cleaned_df['order_date']
            elif 'date' in cleaned_df.columns:
                cleaned_df['order_time'] = cleaned_df['date']
            elif 'timestamp' in cleaned_df.columns:
                cleaned_df['order_time'] = cleaned_df['timestamp']
        
        # 3. Clean numeric columns
        numeric_cols = ['qty', 'quantity', 'selling_price_aed', 'price', 'unit_price', 'discount_pct', 'discount']
        for col in numeric_cols:
            if col in cleaned_df.columns:
                cleaned_df[col] = pd.to_numeric(cleaned_df[col], errors='coerce')
        
        # Standardize column names
        if 'quantity' in cleaned_df.columns and 'qty' not in cleaned_df.columns:
            cleaned_df['qty'] = cleaned_df['quantity']
        if 'price' in cleaned_df.columns and 'selling_price_aed' not in cleaned_df.columns:
            cleaned_df['selling_price_aed'] = cleaned_df['price']
        if 'unit_price' in cleaned_df.columns and 'selling_price_aed' not in cleaned_df.columns:
            cleaned_df['selling_price_aed'] = cleaned_df['unit_price']
        if 'discount' in cleaned_df.columns and 'discount_pct' not in cleaned_df.columns:
            cleaned_df['discount_pct'] = cleaned_df['discount']
        
        # 4. Handle missing values
        if 'qty' in cleaned_df.columns:
            null_qty = cleaned_df['qty'].isna().sum()
            if null_qty > 0:
                cleaned_df['qty'] = cleaned_df['qty'].fillna(1)
                self.logger.data_quality('sales', 'MISSING_VALUE', f'Filled {null_qty} missing qty with 1', null_qty)
        
        if 'selling_price_aed' in cleaned_df.columns:
            null_price = cleaned_df['selling_price_aed'].isna().sum()
            if null_price > 0:
                median_price = cleaned_df['selling_price_aed'].median()
                cleaned_df['selling_price_aed'] = cleaned_df['selling_price_aed'].fillna(median_price)
                self.logger.data_quality('sales', 'MISSING_VALUE', f'Filled {null_price} missing prices with median', null_price)
        
        if 'discount_pct' in cleaned_df.columns:
            cleaned_df['discount_pct'] = cleaned_df['discount_pct'].fillna(0)
        else:
            cleaned_df['discount_pct'] = 0
        
        # 5. Calculate revenue if not present
        if 'revenue' not in cleaned_df.columns:
            if 'selling_price_aed' in cleaned_df.columns and 'qty' in cleaned_df.columns:
                cleaned_df['revenue'] = cleaned_df['selling_price_aed'] * cleaned_df['qty']
                self.logger.info('DATA_CLEANING', 'Calculated revenue column (selling_price_aed * qty)')
            else:
                cleaned_df['revenue'] = 0
                self.logger.warning('DATA_CLEANING', 'Could not calculate revenue - missing price or qty columns')
        
        # 6. Clean city names
        if 'city' in cleaned_df.columns:
            original_cities = cleaned_df['city'].nunique()
            cleaned_df['city_clean'] = cleaned_df['city'].replace(CITY_MAPPING)
            cleaned_df['city_clean'] = cleaned_df['city_clean'].fillna('Unknown')
            new_cities = cleaned_df['city_clean'].nunique()
            self.logger.info('DATA_CLEANING', f'Standardized cities: {original_cities} -> {new_cities} unique values')
        else:
            cleaned_df['city'] = 'Unknown'
            cleaned_df['city_clean'] = 'Unknown'
        
        # 7. Clean channel names
        if 'channel' in cleaned_df.columns:
            cleaned_df['channel'] = cleaned_df['channel'].str.strip().str.title()
            cleaned_df['channel'] = cleaned_df['channel'].fillna('Unknown')
        else:
            cleaned_df['channel'] = 'Unknown'
        
        # 8. Clean category names
        if 'category' in cleaned_df.columns:
            cleaned_df['category'] = cleaned_df['category'].str.strip().str.title()
            cleaned_df['category'] = cleaned_df['category'].fillna('Unknown')
        else:
            cleaned_df['category'] = 'Unknown'
        
        # 9. Remove duplicates
        if 'order_id' in cleaned_df.columns:
            duplicates = cleaned_df.duplicated(subset=['order_id', 'product_id'], keep='first').sum()
            if duplicates > 0:
                cleaned_df = cleaned_df.drop_duplicates(subset=['order_id', 'product_id'], keep='first')
                self.logger.data_quality('sales', 'DUPLICATES', f'Removed {duplicates} duplicate rows', duplicates)
        
        # 10. Handle outliers
        if 'revenue' in cleaned_df.columns:
            q1 = cleaned_df['revenue'].quantile(0.01)
            q99 = cleaned_df['revenue'].quantile(0.99)
            outliers = ((cleaned_df['revenue'] < q1) | (cleaned_df['revenue'] > q99)).sum()
            if outliers > 0:
                self.logger.data_quality('sales', 'OUTLIERS', f'Detected {outliers} potential outliers in revenue', outliers)
        
        # 11. Remove negative values
        if 'qty' in cleaned_df.columns:
            negative_qty = (cleaned_df['qty'] < 0).sum()
            if negative_qty > 0:
                cleaned_df.loc[cleaned_df['qty'] < 0, 'qty'] = abs(cleaned_df.loc[cleaned_df['qty'] < 0, 'qty'])
                self.logger.data_quality('sales', 'NEGATIVE_VALUES', f'Converted {negative_qty} negative quantities to positive', negative_qty)
        
        # 12. Ensure required columns exist
        if 'order_id' not in cleaned_df.columns:
            cleaned_df['order_id'] = [f'ORD_{i:06d}' for i in range(len(cleaned_df))]
            self.logger.info('DATA_CLEANING', 'Generated order_id column')
        
        if 'product_id' not in cleaned_df.columns:
            cleaned_df['product_id'] = 'UNKNOWN'
            self.logger.warning('DATA_CLEANING', 'product_id column missing - filled with UNKNOWN')
        
        if 'store_id' not in cleaned_df.columns:
            cleaned_df['store_id'] = 'UNKNOWN'
            self.logger.warning('DATA_CLEANING', 'store_id column missing - filled with UNKNOWN')
        
        if 'payment_method' not in cleaned_df.columns:
            cleaned_df['payment_method'] = 'Unknown'
        
        if 'payment_status' not in cleaned_df.columns:
            cleaned_df['payment_status'] = 'Completed'
        
        if 'return_flag' not in cleaned_df.columns:
            cleaned_df['return_flag'] = False
        
        final_rows = len(cleaned_df)
        self.logger.info('DATA_CLEANING', f'Sales data cleaning complete. Final rows: {final_rows} (removed {original_rows - final_rows})')
        
        return cleaned_df
    
    def clean_products_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean and validate products data."""
        self.logger.info('DATA_CLEANING', f'Starting products data cleaning. Rows: {len(df)}')
        
        cleaned_df = df.copy()
        cleaned_df.columns = cleaned_df.columns.str.lower().str.strip().str.replace(' ', '_')
        
        # Ensure product_id exists
        if 'product_id' not in cleaned_df.columns:
            if 'sku' in cleaned_df.columns:
                cleaned_df['product_id'] = cleaned_df['sku']
            elif 'id' in cleaned_df.columns:
                cleaned_df['product_id'] = cleaned_df['id']
            else:
                cleaned_df['product_id'] = [f'PROD_{i:04d}' for i in range(len(cleaned_df))]
        
        # Clean category
        if 'category' in cleaned_df.columns:
            cleaned_df['category'] = cleaned_df['category'].str.strip().str.title()
            cleaned_df['category'] = cleaned_df['category'].fillna('Unknown')
        else:
            cleaned_df['category'] = 'Unknown'
        
        # Clean brand
        if 'brand' in cleaned_df.columns:
            cleaned_df['brand'] = cleaned_df['brand'].str.strip().str.title()
            cleaned_df['brand'] = cleaned_df['brand'].fillna('Unknown')
        else:
            cleaned_df['brand'] = 'Unknown'
        
        # Clean cost
        if 'unit_cost_aed' not in cleaned_df.columns:
            if 'cost' in cleaned_df.columns:
                cleaned_df['unit_cost_aed'] = pd.to_numeric(cleaned_df['cost'], errors='coerce')
            elif 'unit_cost' in cleaned_df.columns:
                cleaned_df['unit_cost_aed'] = pd.to_numeric(cleaned_df['unit_cost'], errors='coerce')
            else:
                cleaned_df['unit_cost_aed'] = 0
        
        cleaned_df['unit_cost_aed'] = cleaned_df['unit_cost_aed'].fillna(0)
        
        # Remove duplicates
        duplicates = cleaned_df.duplicated(subset=['product_id'], keep='first').sum()
        if duplicates > 0:
            cleaned_df = cleaned_df.drop_duplicates(subset=['product_id'], keep='first')
            self.logger.data_quality('products', 'DUPLICATES', f'Removed {duplicates} duplicate products', duplicates)
        
        self.logger.info('DATA_CLEANING', f'Products data cleaning complete. Final rows: {len(cleaned_df)}')
        return cleaned_df
    
    def clean_stores_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean and validate stores data."""
        self.logger.info('DATA_CLEANING', f'Starting stores data cleaning. Rows: {len(df)}')
        
        cleaned_df = df.copy()
        cleaned_df.columns = cleaned_df.columns.str.lower().str.strip().str.replace(' ', '_')
        
        # Ensure store_id exists
        if 'store_id' not in cleaned_df.columns:
            if 'id' in cleaned_df.columns:
                cleaned_df['store_id'] = cleaned_df['id']
            else:
                cleaned_df['store_id'] = [f'STORE_{i:03d}' for i in range(len(cleaned_df))]
        
        # Clean city
        if 'city' in cleaned_df.columns:
            cleaned_df['city'] = cleaned_df['city'].replace(CITY_MAPPING)
            cleaned_df['city'] = cleaned_df['city'].fillna('Unknown')
        else:
            cleaned_df['city'] = 'Unknown'
        
        # Clean channel
        if 'channel' in cleaned_df.columns:
            cleaned_df['channel'] = cleaned_df['channel'].str.strip().str.title()
            cleaned_df['channel'] = cleaned_df['channel'].fillna('Unknown')
        else:
            cleaned_df['channel'] = 'Unknown'
        
        self.logger.info('DATA_CLEANING', f'Stores data cleaning complete. Final rows: {len(cleaned_df)}')
        return cleaned_df
    
    def clean_inventory_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean and validate inventory data."""
        self.logger.info('DATA_CLEANING', f'Starting inventory data cleaning. Rows: {len(df)}')
        
        cleaned_df = df.copy()
        cleaned_df.columns = cleaned_df.columns.str.lower().str.strip().str.replace(' ', '_')
        
        # Handle date column
        date_cols = ['snapshot_date', 'date', 'inventory_date']
        for col in date_cols:
            if col in cleaned_df.columns:
                cleaned_df['snapshot_date'] = pd.to_datetime(cleaned_df[col], errors='coerce')
                break
        
        if 'snapshot_date' not in cleaned_df.columns:
            cleaned_df['snapshot_date'] = datetime.now()
        
        # Clean stock on hand
        stock_cols = ['stock_on_hand', 'stock', 'quantity', 'qty']
        for col in stock_cols:
            if col in cleaned_df.columns:
                cleaned_df['stock_on_hand'] = pd.to_numeric(cleaned_df[col], errors='coerce')
                break
        
        if 'stock_on_hand' not in cleaned_df.columns:
            cleaned_df['stock_on_hand'] = 0
        
        cleaned_df['stock_on_hand'] = cleaned_df['stock_on_hand'].fillna(0)
        
        # Clean reorder point
        if 'reorder_point' not in cleaned_df.columns:
            cleaned_df['reorder_point'] = 50  # Default
        
        # Clean lead time
        if 'lead_time_days' not in cleaned_df.columns:
            cleaned_df['lead_time_days'] = 7  # Default
        
        # Ensure IDs exist
        if 'product_id' not in cleaned_df.columns:
            cleaned_df['product_id'] = 'UNKNOWN'
        
        if 'store_id' not in cleaned_df.columns:
            cleaned_df['store_id'] = 'UNKNOWN'
        
        # Add city and channel from store
        if 'city' not in cleaned_df.columns:
            cleaned_df['city'] = 'Unknown'
        
        cleaned_df['city_clean'] = cleaned_df['city'].replace(CITY_MAPPING)
        
        if 'channel' not in cleaned_df.columns:
            cleaned_df['channel'] = 'Unknown'
        
        if 'category' not in cleaned_df.columns:
            cleaned_df['category'] = 'Unknown'
        
        # Calculate stock status
        cleaned_df['stock_status'] = cleaned_df.apply(
            lambda x: 'Critical' if x['stock_on_hand'] <= 0 
            else 'Low' if x['stock_on_hand'] <= x['reorder_point'] 
            else 'Healthy', axis=1
        )
        
        self.logger.info('DATA_CLEANING', f'Inventory data cleaning complete. Final rows: {len(cleaned_df)}')
        return cleaned_df
    
    def clean_campaigns_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean and validate campaigns data."""
        self.logger.info('DATA_CLEANING', f'Starting campaigns data cleaning. Rows: {len(df)}')
        
        cleaned_df = df.copy()
        cleaned_df.columns = cleaned_df.columns.str.lower().str.strip().str.replace(' ', '_')
        
        # Ensure campaign_id exists
        if 'campaign_id' not in cleaned_df.columns:
            if 'id' in cleaned_df.columns:
                cleaned_df['campaign_id'] = cleaned_df['id']
            else:
                cleaned_df['campaign_id'] = [f'CAMP_{i:03d}' for i in range(len(cleaned_df))]
        
        # Parse dates
        for col in ['start_date', 'end_date']:
            if col in cleaned_df.columns:
                cleaned_df[col] = pd.to_datetime(cleaned_df[col], errors='coerce')
        
        # Calculate duration
        if 'start_date' in cleaned_df.columns and 'end_date' in cleaned_df.columns:
            cleaned_df['duration_days'] = (cleaned_df['end_date'] - cleaned_df['start_date']).dt.days
        else:
            cleaned_df['duration_days'] = 7
        
        # Clean discount
        if 'discount_pct' not in cleaned_df.columns:
            if 'discount' in cleaned_df.columns:
                cleaned_df['discount_pct'] = pd.to_numeric(cleaned_df['discount'], errors='coerce')
            else:
                cleaned_df['discount_pct'] = 0
        
        cleaned_df['discount_pct'] = cleaned_df['discount_pct'].fillna(0)
        
        # Clean budget
        if 'promo_budget_aed' not in cleaned_df.columns:
            if 'budget' in cleaned_df.columns:
                cleaned_df['promo_budget_aed'] = pd.to_numeric(cleaned_df['budget'], errors='coerce')
            else:
                cleaned_df['promo_budget_aed'] = 0
        
        cleaned_df['promo_budget_aed'] = cleaned_df['promo_budget_aed'].fillna(0)
        
        # Determine if active
        now = datetime.now()
        if 'start_date' in cleaned_df.columns and 'end_date' in cleaned_df.columns:
            cleaned_df['is_active'] = (cleaned_df['start_date'] <= now) & (cleaned_df['end_date'] >= now)
        else:
            cleaned_df['is_active'] = False
        
        # Add other columns
        for col in ['city', 'channel', 'category']:
            if col not in cleaned_df.columns:
                cleaned_df[col] = 'All'
        
        self.logger.info('DATA_CLEANING', f'Campaigns data cleaning complete. Final rows: {len(cleaned_df)}')
        return cleaned_df
    
    def get_cleaning_summary(self, df: pd.DataFrame, dataset_name: str) -> dict:
        """Generate a cleaning summary for a dataset."""
        summary = {
            'dataset': dataset_name,
            'total_rows': len(df),
            'total_columns': len(df.columns),
            'missing_values': df.isnull().sum().sum(),
            'duplicate_rows': df.duplicated().sum(),
            'columns': list(df.columns),
            'dtypes': df.dtypes.astype(str).to_dict(),
            'memory_usage': f"{df.memory_usage(deep=True).sum() / 1024 / 1024:.2f} MB"
        }
        return summary

# =============================================================================
# DATA INPUT FUNCTIONS
# =============================================================================
def render_data_input_tab():
    """Render the data input and management tab."""
    st.markdown("## 📂 Data Input & Management")
    st.markdown("Upload, validate, and manage your data")
    st.markdown("---")
    
    # Data source selection
    data_source = st.radio(
        "Select Data Source",
        options=["📤 Upload Files", "🔄 Generate Sample Data", "📊 Current Data Info"],
        horizontal=True
    )
    
    st.markdown("---")
    
    if data_source == "📤 Upload Files":
        render_file_upload()
    elif data_source == "🔄 Generate Sample Data":
        render_generate_data()
    else:
        render_current_data_info()


def render_file_upload():
    """Render file upload interface."""
    st.markdown("### 📤 Upload Data Files")
    st.markdown("Upload your CSV or Excel files for each dataset.")
    
    cleaner = DataCleaner(logger)
    
    # File upload tabs
    upload_tabs = st.tabs(["📊 Sales", "📦 Products", "🏪 Stores", "📈 Inventory", "🎯 Campaigns"])
    
    with upload_tabs[0]:
        st.markdown("#### Sales Data")
        st.markdown("**Required columns:** order_id, order_time, product_id, qty, selling_price_aed")
        st.markdown("**Optional columns:** store_id, discount_pct, city, channel, category, payment_method")
        
        sales_file = st.file_uploader("Upload Sales Data", type=['csv', 'xlsx', 'xls'], key='sales_upload')
        
        if sales_file:
            try:
                if sales_file.name.endswith('.csv'):
                    df = pd.read_csv(sales_file)
                else:
                    df = pd.read_excel(sales_file)
                
                st.success(f"✅ Loaded {len(df):,} rows, {len(df.columns)} columns")
                logger.info('DATA_INPUT', f'Sales file uploaded: {sales_file.name}', {'rows': len(df), 'columns': len(df.columns)})
                
                # Preview
                with st.expander("Preview Raw Data"):
                    st.dataframe(df.head(10), use_container_width=True)
                
                # Clean button
                if st.button("🧹 Clean & Validate Sales Data", key='clean_sales'):
                    with st.spinner("Cleaning data..."):
                        cleaned_df = cleaner.clean_sales_data(df)
                        st.session_state.sales_df = cleaned_df
                        st.session_state.data_loaded = True
                        st.success(f"✅ Cleaned! {len(cleaned_df):,} rows ready")
                        
                        # Show cleaning summary
                        with st.expander("Cleaning Summary"):
                            summary = cleaner.get_cleaning_summary(cleaned_df, 'sales')
                            st.json(summary)
            
            except Exception as e:
                st.error(f"Error loading file: {str(e)}")
                logger.error('DATA_INPUT', f'Error loading sales file: {str(e)}')
    
    with upload_tabs[1]:
        st.markdown("#### Products Data")
        st.markdown("**Required columns:** product_id, category")
        st.markdown("**Optional columns:** brand, unit_cost_aed")
        
        products_file = st.file_uploader("Upload Products Data", type=['csv', 'xlsx', 'xls'], key='products_upload')
        
        if products_file:
            try:
                if products_file.name.endswith('.csv'):
                    df = pd.read_csv(products_file)
                else:
                    df = pd.read_excel(products_file)
                
                st.success(f"✅ Loaded {len(df):,} rows")
                logger.info('DATA_INPUT', f'Products file uploaded: {products_file.name}')
                
                if st.button("🧹 Clean & Validate Products Data", key='clean_products'):
                    cleaned_df = cleaner.clean_products_data(df)
                    st.session_state.products_df = cleaned_df
                    st.success(f"✅ Cleaned! {len(cleaned_df):,} products ready")
            
            except Exception as e:
                st.error(f"Error: {str(e)}")
                logger.error('DATA_INPUT', f'Error loading products file: {str(e)}')
    
    with upload_tabs[2]:
        st.markdown("#### Stores Data")
        st.markdown("**Required columns:** store_id, city, channel")
        
        stores_file = st.file_uploader("Upload Stores Data", type=['csv', 'xlsx', 'xls'], key='stores_upload')
        
        if stores_file:
            try:
                if stores_file.name.endswith('.csv'):
                    df = pd.read_csv(stores_file)
                else:
                    df = pd.read_excel(stores_file)
                
                st.success(f"✅ Loaded {len(df):,} rows")
                logger.info('DATA_INPUT', f'Stores file uploaded: {stores_file.name}')
                
                if st.button("🧹 Clean & Validate Stores Data", key='clean_stores'):
                    cleaned_df = cleaner.clean_stores_data(df)
                    st.session_state.stores_df = cleaned_df
                    st.success(f"✅ Cleaned! {len(cleaned_df):,} stores ready")
            
            except Exception as e:
                st.error(f"Error: {str(e)}")
                logger.error('DATA_INPUT', f'Error loading stores file: {str(e)}')
    
    with upload_tabs[3]:
        st.markdown("#### Inventory Data")
        st.markdown("**Required columns:** product_id, store_id, stock_on_hand")
        st.markdown("**Optional columns:** snapshot_date, reorder_point, lead_time_days")
        
        inventory_file = st.file_uploader("Upload Inventory Data", type=['csv', 'xlsx', 'xls'], key='inventory_upload')
        
        if inventory_file:
            try:
                if inventory_file.name.endswith('.csv'):
                    df = pd.read_csv(inventory_file)
                else:
                    df = pd.read_excel(inventory_file)
                
                st.success(f"✅ Loaded {len(df):,} rows")
                logger.info('DATA_INPUT', f'Inventory file uploaded: {inventory_file.name}')
                
                if st.button("🧹 Clean & Validate Inventory Data", key='clean_inventory'):
                    cleaned_df = cleaner.clean_inventory_data(df)
                    st.session_state.inventory_df = cleaned_df
                    st.success(f"✅ Cleaned! {len(cleaned_df):,} inventory records ready")
            
            except Exception as e:
                st.error(f"Error: {str(e)}")
                logger.error('DATA_INPUT', f'Error loading inventory file: {str(e)}')
    
    with upload_tabs[4]:
        st.markdown("#### Campaigns Data")
        st.markdown("**Required columns:** campaign_id, start_date, end_date, discount_pct")
        st.markdown("**Optional columns:** city, channel, category, promo_budget_aed")
        
        campaigns_file = st.file_uploader("Upload Campaigns Data", type=['csv', 'xlsx', 'xls'], key='campaigns_upload')
        
        if campaigns_file:
            try:
                if campaigns_file.name.endswith('.csv'):
                    df = pd.read_csv(campaigns_file)
                else:
                    df = pd.read_excel(campaigns_file)
                
                st.success(f"✅ Loaded {len(df):,} rows")
                logger.info('DATA_INPUT', f'Campaigns file uploaded: {campaigns_file.name}')
                
                if st.button("🧹 Clean & Validate Campaigns Data", key='clean_campaigns'):
                    cleaned_df = cleaner.clean_campaigns_data(df)
                    st.session_state.campaigns_df = cleaned_df
                    st.success(f"✅ Cleaned! {len(cleaned_df):,} campaigns ready")
            
            except Exception as e:
                st.error(f"Error: {str(e)}")
                logger.error('DATA_INPUT', f'Error loading campaigns file: {str(e)}')


def render_generate_data():
    """Render sample data generation interface."""
    st.markdown("### 🔄 Generate Sample Data")
    st.markdown("Generate synthetic retail data for testing and demonstration.")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        num_sales = st.number_input("Number of Sales Records", min_value=1000, max_value=100000, value=50000, step=1000)
    with col2:
        num_products = st.number_input("Number of Products", min_value=50, max_value=1000, value=200, step=50)
    with col3:
        num_stores = st.number_input("Number of Stores", min_value=5, max_value=100, value=30, step=5)
    
    col1, col2 = st.columns(2)
    with col1:
        days_of_data = st.slider("Days of Historical Data", 30, 365, 120)
    with col2:
        num_campaigns = st.slider("Number of Campaigns", 5, 50, 15)
    
    if st.button("🚀 Generate Data", type="primary"):
        with st.spinner("Generating data..."):
            sales_df, products_df, stores_df, inventory_df, campaigns_df = generate_all_data(
                num_sales=num_sales,
                num_products=num_products,
                num_stores=num_stores,
                days_of_data=days_of_data,
                num_campaigns=num_campaigns
            )
            
            st.session_state.sales_df = sales_df
            st.session_state.products_df = products_df
            st.session_state.stores_df = stores_df
            st.session_state.inventory_df = inventory_df
            st.session_state.campaigns_df = campaigns_df
            st.session_state.data_loaded = True
            
            logger.info('DATA_INPUT', 'Sample data generated', {
                'sales': len(sales_df),
                'products': len(products_df),
                'stores': len(stores_df),
                'inventory': len(inventory_df),
                'campaigns': len(campaigns_df)
            })
            
            st.success("✅ Data generated successfully!")
            
            # Show summary
            col1, col2, col3, col4, col5 = st.columns(5)
            col1.metric("Sales", f"{len(sales_df):,}")
            col2.metric("Products", f"{len(products_df):,}")
            col3.metric("Stores", f"{len(stores_df):,}")
            col4.metric("Inventory", f"{len(inventory_df):,}")
            col5.metric("Campaigns", f"{len(campaigns_df):,}")


def render_current_data_info():
    """Render current data information."""
    st.markdown("### 📊 Current Data Information")
    
    if not st.session_state.get('data_loaded', False):
        st.warning("⚠️ No data loaded. Please upload files or generate sample data.")
        return
    
    datasets = {
        'Sales': st.session_state.get('sales_df', pd.DataFrame()),
        'Products': st.session_state.get('products_df', pd.DataFrame()),
        'Stores': st.session_state.get('stores_df', pd.DataFrame()),
        'Inventory': st.session_state.get('inventory_df', pd.DataFrame()),
        'Campaigns': st.session_state.get('campaigns_df', pd.DataFrame())
    }
    
    # Summary cards
    cols = st.columns(5)
    for i, (name, df) in enumerate(datasets.items()):
        with cols[i]:
            st.markdown(f"""
            <div style="background: rgba(99, 102, 241, 0.1); border: 1px solid rgba(99, 102, 241, 0.3);
                        border-radius: 12px; padding: 16px; text-align: center;">
                <div style="font-size: 0.9rem; color: #a1a1aa;">{name}</div>
                <div style="font-size: 1.5rem; font-weight: 700; color: #6366f1;">{len(df):,}</div>
                <div style="font-size: 0.75rem; color: #71717a;">{len(df.columns)} columns</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("")
    
    # Detailed info
    selected_dataset = st.selectbox("Select Dataset for Details", list(datasets.keys()))
    df = datasets[selected_dataset]
    
    if len(df) > 0:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Column Information")
            col_info = pd.DataFrame({
                'Column': df.columns,
                'Type': df.dtypes.astype(str),
                'Non-Null': df.notnull().sum(),
                'Null': df.isnull().sum(),
                'Unique': df.nunique()
            })
            st.dataframe(col_info, use_container_width=True, hide_index=True)
        
        with col2:
            st.markdown("#### Sample Data")
            st.dataframe(df.head(10), use_container_width=True)
        
        # Data quality metrics
        st.markdown("#### Data Quality Metrics")
        total_cells = len(df) * len(df.columns)
        null_cells = df.isnull().sum().sum()
        completeness = (1 - null_cells / total_cells) * 100 if total_cells > 0 else 0
        duplicates = df.duplicated().sum()
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Completeness", f"{completeness:.1f}%")
        col2.metric("Missing Values", f"{null_cells:,}")
        col3.metric("Duplicate Rows", f"{duplicates:,}")
        col4.metric("Memory Usage", f"{df.memory_usage(deep=True).sum() / 1024 / 1024:.2f} MB")


# =============================================================================
# LOGGING TAB
# =============================================================================
def render_logs_tab():
    """Render the logs and audit trail tab."""
    st.markdown("## 📋 Logs & Audit Trail")
    st.markdown("View system logs and data quality reports")
    st.markdown("---")
    
    log_tabs = st.tabs(["📝 Activity Logs", "🔍 Data Quality", "📊 Statistics"])
    
    with log_tabs[0]:
        render_activity_logs()
    
    with log_tabs[1]:
        render_data_quality_logs()
    
    with log_tabs[2]:
        render_log_statistics()


def render_activity_logs():
    """Render activity logs."""
    st.markdown("### 📝 Activity Logs")
    
    # Filters
    col1, col2, col3 = st.columns(3)
    with col1:
        level_filter = st.selectbox("Level", ['All', 'INFO', 'WARNING', 'ERROR'], key='log_level')
    with col2:
        category_filter = st.selectbox("Category", ['All', 'DATA_INPUT', 'DATA_CLEANING', 'NAVIGATION', 'EXPORT'], key='log_category')
    with col3:
        limit = st.number_input("Show Last", min_value=10, max_value=500, value=50, key='log_limit')
    
    # Get logs
    logs_df = logger.get_logs_df()
    
    if len(logs_df) == 0:
        st.info("No logs recorded yet.")
        return
    
    # Apply filters
    filtered_logs = logs_df.copy()
    if level_filter != 'All':
        filtered_logs = filtered_logs[filtered_logs['level'] == level_filter]
    if category_filter != 'All':
        filtered_logs = filtered_logs[filtered_logs['category'] == category_filter]
    
    filtered_logs = filtered_logs.tail(limit).iloc[::-1]  # Reverse to show newest first
    
    st.markdown(f"**Showing {len(filtered_logs)} logs**")
    
    # Display logs with color coding
    for _, log in filtered_logs.iterrows():
        level = log['level']
        color = '#10b981' if level == 'INFO' else '#f59e0b' if level == 'WARNING' else '#ef4444'
        
        st.markdown(f"""
        <div style="background: rgba(255,255,255,0.03); border-left: 3px solid {color}; 
                    padding: 8px 12px; margin-bottom: 8px; border-radius: 4px;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
                <span style="color: {color}; font-weight: 600; font-size: 0.8rem;">[{level}] {log['category']}</span>
                <span style="color: #71717a; font-size: 0.75rem;">{log['timestamp']}</span>
            </div>
            <div style="color: #e5e5e5; font-size: 0.85rem;">{log['message']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Export logs
    st.markdown("---")
    if st.button("📥 Export Logs to CSV"):
        csv = logs_df.to_csv(index=False)
        st.download_button(
            label="Download Logs",
            data=csv,
            file_name=f"logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )


def render_data_quality_logs():
    """Render data quality logs."""
    st.markdown("### 🔍 Data Quality Issues")
    
    dq_df = logger.get_data_quality_df()
    
    if len(dq_df) == 0:
        st.success("✅ No data quality issues recorded.")
        return
    
    # Summary
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Issues", len(dq_df))
    col2.metric("Affected Rows", dq_df['affected_rows'].sum())
    col3.metric("Datasets", dq_df['dataset'].nunique())
    
    st.markdown("")
    
    # Issues by type
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Issues by Type")
        issue_counts = dq_df['issue_type'].value_counts().reset_index()
        issue_counts.columns = ['Issue Type', 'Count']
        fig = px.pie(issue_counts, values='Count', names='Issue Type', hole=0.4, 
                    color_discrete_sequence=['#6366f1', '#f59e0b', '#ef4444', '#10b981', '#8b5cf6'])
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#a1a1aa'),
            height=250
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### Issues by Dataset")
        dataset_counts = dq_df['dataset'].value_counts().reset_index()
        dataset_counts.columns = ['Dataset', 'Count']
        fig = px.bar(dataset_counts, x='Dataset', y='Count', color='Dataset',
                    color_discrete_sequence=['#6366f1', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6'])
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#a1a1aa'),
            height=250,
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Detailed table
    st.markdown("#### Issue Details")
    st.dataframe(dq_df.iloc[::-1], use_container_width=True, hide_index=True)


def render_log_statistics():
    """Render log statistics."""
    st.markdown("### 📊 Log Statistics")
    
    logs_df = logger.get_logs_df()
    
    if len(logs_df) == 0:
        st.info("No logs to analyze.")
        return
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Logs", len(logs_df))
    col2.metric("Info", len(logs_df[logs_df['level'] == 'INFO']))
    col3.metric("Warnings", len(logs_df[logs_df['level'] == 'WARNING']))
    col4.metric("Errors", len(logs_df[logs_df['level'] == 'ERROR']))
    
    st.markdown("")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Logs by Category")
        cat_counts = logs_df['category'].value_counts().reset_index()
        cat_counts.columns = ['Category', 'Count']
        fig = px.bar(cat_counts, x='Category', y='Count', color='Category',
                    color_discrete_sequence=['#6366f1', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6'])
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#a1a1aa'),
            height=300,
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### Logs by Level")
        level_counts = logs_df['level'].value_counts().reset_index()
        level_counts.columns = ['Level', 'Count']
        colors_map = {'INFO': '#10b981', 'WARNING': '#f59e0b', 'ERROR': '#ef4444'}
        fig = px.pie(level_counts, values='Count', names='Level', hole=0.4,
                    color='Level', color_discrete_map=colors_map)
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#a1a1aa'),
            height=300
        )
        st.plotly_chart(fig, use_container_width=True)


# =============================================================================
# DATA GENERATION
# =============================================================================
@st.cache_data
def generate_all_data(num_sales=50000, num_products=200, num_stores=30, days_of_data=120, num_campaigns=15):
    """Generate complete synthetic retail data."""
    np.random.seed(42)
    random.seed(42)
    
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days_of_data)
    
    # Generate Products
    products_list = []
    for i in range(num_products):
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
    for i in range(num_stores):
        stores_list.append({
            'store_id': f'STORE_{i+1:03d}',
            'city': random.choice(STANDARD_CITIES),
            'channel': random.choice(CHANNELS)
        })
    stores_df = pd.DataFrame(stores_list)
    
    # Generate Sales
    sales_list = []
    for i in range(num_sales):
        order_date = start_date + timedelta(days=random.randint(0, days_of_data))
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
    sales_df['city_clean'] = sales_df['city']
    
    # Generate Inventory
    inventory_list = []
    for days_ago in range(0, 30, 7):
        snapshot_date = end_date - timedelta(days=days_ago)
        for product in products_list[:50]:
            for store in stores_list[:10]:
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
    inventory_df['city_clean'] = inventory_df['city']
    inventory_df['stock_status'] = inventory_df.apply(
        lambda x: 'Critical' if x['stock_on_hand'] <= 0 
        else 'Low' if x['stock_on_hand'] <= x['reorder_point'] 
        else 'Healthy', axis=1
    )
    
    # Generate Campaigns
    campaigns_list = []
    for i in range(num_campaigns):
        camp_start = start_date + timedelta(days=random.randint(0, days_of_data - 14))
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
    return ['#6366f1', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#06b6d4']

def apply_chart_style(fig, height=400, show_legend=True):
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


# =============================================================================
# DASHBOARD TABS (Previous implementations - keeping them compact)
# =============================================================================
def render_executive_overview(sales_df, inventory_df, campaigns_df, stores_df):
    st.markdown("## 🏠 Executive Overview")
    st.markdown("---")
    
    total_revenue = sales_df['revenue'].sum() if 'revenue' in sales_df.columns else 0
    total_orders = sales_df['order_id'].nunique() if 'order_id' in sales_df.columns else len(sales_df)
    avg_order_value = total_revenue / total_orders if total_orders > 0 else 0
    total_units = sales_df['qty'].sum() if 'qty' in sales_df.columns else 0
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("💰 Total Revenue", format_currency(total_revenue))
    col2.metric("🛒 Total Orders", format_number(total_orders))
    col3.metric("📦 Units Sold", format_number(total_units))
    col4.metric("💵 Avg Order Value", format_currency(avg_order_value))
    
    logger.info('NAVIGATION', 'Viewed Executive Overview')
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📈 Daily Revenue Trend")
        if 'order_time' in sales_df.columns:
            daily = sales_df.groupby(sales_df['order_time'].dt.date)['revenue'].sum().reset_index()
            daily.columns = ['date', 'revenue']
            fig = px.area(daily, x='date', y='revenue', color_discrete_sequence=['#6366f1'])
            fig = apply_chart_style(fig, height=300, show_legend=False)
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### 📊 Revenue by Category")
        if 'category' in sales_df.columns:
            cat_rev = sales_df.groupby('category')['revenue'].sum().reset_index()
            fig = px.pie(cat_rev, values='revenue', names='category', hole=0.4, color_discrete_sequence=get_chart_colors())
            fig = apply_chart_style(fig, height=300)
            st.plotly_chart(fig, use_container_width=True)


def render_sales_analysis(sales_df, products_df, stores_df):
    st.markdown("## 📈 Sales Analytics")
    st.markdown("---")
    
    logger.info('NAVIGATION', 'Viewed Sales Analytics')
    
    col1, col2, col3 = st.columns(3)
    with col1:
        cities = ['All'] + (sales_df['city'].unique().tolist() if 'city' in sales_df.columns else STANDARD_CITIES)
        city_filter = st.selectbox("🏙️ City", cities, key='sales_city')
    with col2:
        channels = ['All'] + (sales_df['channel'].unique().tolist() if 'channel' in sales_df.columns else CHANNELS)
        channel_filter = st.selectbox("📱 Channel", channels, key='sales_channel')
    with col3:
        categories = ['All'] + (sales_df['category'].unique().tolist() if 'category' in sales_df.columns else CATEGORIES)
        category_filter = st.selectbox("📦 Category", categories, key='sales_category')
    
    filtered_df = sales_df.copy()
    if city_filter != 'All' and 'city' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['city'] == city_filter]
    if channel_filter != 'All' and 'channel' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['channel'] == channel_filter]
    if category_filter != 'All' and 'category' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['category'] == category_filter]
    
    total_revenue = filtered_df['revenue'].sum() if 'revenue' in filtered_df.columns else 0
    total_orders = filtered_df['order_id'].nunique() if 'order_id' in filtered_df.columns else len(filtered_df)
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("💰 Revenue", format_currency(total_revenue))
    col2.metric("🛒 Orders", format_number(total_orders))
    col3.metric("📦 Units", format_number(filtered_df['qty'].sum() if 'qty' in filtered_df.columns else 0))
    col4.metric("🏷️ Avg Discount", f"{filtered_df['discount_pct'].mean() if 'discount_pct' in filtered_df.columns else 0:.1f}%")
    
    if 'order_time' in filtered_df.columns:
        st.markdown("#### 📈 Sales Trend")
        daily = filtered_df.groupby(filtered_df['order_time'].dt.date).agg({'revenue': 'sum', 'order_id': 'nunique'}).reset_index()
        daily.columns = ['date', 'revenue', 'orders']
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(go.Scatter(x=daily['date'], y=daily['revenue'], name='Revenue', fill='tozeroy', line=dict(color='#6366f1')))
        fig.add_trace(go.Scatter(x=daily['date'], y=daily['orders'], name='Orders', line=dict(color='#10b981')), secondary_y=True)
        fig = apply_chart_style(fig, height=350)
        st.plotly_chart(fig, use_container_width=True)


def render_inventory_analysis(inventory_df, sales_df, products_df, stores_df):
    st.markdown("## 📦 Inventory Health")
    st.markdown("---")
    
    logger.info('NAVIGATION', 'Viewed Inventory Health')
    
    if len(inventory_df) == 0:
        st.warning("No inventory data available")
        return
    
    latest_date = inventory_df['snapshot_date'].max()
    latest_inv = inventory_df[inventory_df['snapshot_date'] == latest_date]
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("📦 Total Stock", format_number(latest_inv['stock_on_hand'].sum()))
    col2.metric("🏷️ SKUs", format_number(latest_inv['product_id'].nunique()))
    
    if 'stock_status' in latest_inv.columns:
        healthy = len(latest_inv[latest_inv['stock_status'] == 'Healthy'])
        critical = len(latest_inv[latest_inv['stock_status'] == 'Critical'])
        col3.metric("✅ Healthy", healthy)
        col4.metric("🔴 Critical", critical)


def render_campaign_analysis(campaigns_df, sales_df, products_df, stores_df):
    st.markdown("## 🎯 Campaign Performance")
    st.markdown("---")
    
    logger.info('NAVIGATION', 'Viewed Campaign Performance')
    
    if len(campaigns_df) == 0:
        st.warning("No campaign data available")
        return
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("🎯 Campaigns", len(campaigns_df))
    col2.metric("✅ Active", campaigns_df['is_active'].sum() if 'is_active' in campaigns_df.columns else 0)
    col3.metric("💰 Budget", format_currency(campaigns_df['promo_budget_aed'].sum() if 'promo_budget_aed' in campaigns_df.columns else 0))
    col4.metric("🏷️ Avg Discount", f"{campaigns_df['discount_pct'].mean() if 'discount_pct' in campaigns_df.columns else 0:.0f}%")
    
    if 'start_date' in campaigns_df.columns:
        st.markdown("#### 📅 Campaign Timeline")
        fig = px.timeline(campaigns_df, x_start='start_date', x_end='end_date', y='campaign_id', color='discount_pct')
        fig = apply_chart_style(fig, height=300)
        st.plotly_chart(fig, use_container_width=True)


def render_store_performance(stores_df, sales_df, inventory_df):
    st.markdown("## 🏪 Store Performance")
    st.markdown("---")
    
    logger.info('NAVIGATION', 'Viewed Store Performance')
    
    if 'store_id' not in sales_df.columns:
        st.warning("No store data in sales")
        return
    
    store_metrics = sales_df.groupby('store_id').agg({
        'revenue': 'sum',
        'order_id': 'nunique',
        'qty': 'sum'
    }).reset_index()
    store_metrics.columns = ['store_id', 'revenue', 'orders', 'units']
    store_metrics['aov'] = store_metrics['revenue'] / store_metrics['orders']
    
    if 'store_id' in stores_df.columns:
        store_metrics = store_metrics.merge(stores_df[['store_id', 'city', 'channel']], on='store_id', how='left')
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("🏪 Stores", len(store_metrics))
    col2.metric("💰 Revenue", format_currency(store_metrics['revenue'].sum()))
    col3.metric("📊 Avg/Store", format_currency(store_metrics['revenue'].mean()))
    col4.metric("💵 Avg AOV", format_currency(store_metrics['aov'].mean()))
    
    st.markdown("#### 🏆 Top Stores")
    top_10 = store_metrics.nlargest(10, 'revenue')
    fig = px.bar(top_10.sort_values('revenue'), x='revenue', y='store_id', orientation='h', color_discrete_sequence=['#6366f1'])
    fig = apply_chart_style(fig, height=350, show_legend=False)
    st.plotly_chart(fig, use_container_width=True)


def render_time_patterns(sales_df):
    st.markdown("## ⏰ Time Pattern Analysis")
    st.markdown("---")
    
    logger.info('NAVIGATION', 'Viewed Time Patterns')
    
    if 'order_time' not in sales_df.columns:
        st.warning("No timestamp data available")
        return
    
    df = sales_df.copy()
    df['hour'] = df['order_time'].dt.hour
    df['day_name'] = df['order_time'].dt.day_name()
    df['day_num'] = df['order_time'].dt.dayofweek
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🕐 Hourly Pattern")
        hourly = df.groupby('hour')['revenue'].sum().reset_index()
        fig = px.bar(hourly, x='hour', y='revenue', color_discrete_sequence=['#6366f1'])
        fig = apply_chart_style(fig, height=300, show_legend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### 📅 Daily Pattern")
        daily = df.groupby(['day_num', 'day_name'])['revenue'].sum().reset_index().sort_values('day_num')
        fig = px.bar(daily, x='day_name', y='revenue', color_discrete_sequence=['#10b981'])
        fig = apply_chart_style(fig, height=300, show_legend=False)
        st.plotly_chart(fig, use_container_width=True)


def render_data_explorer(sales_df, products_df, stores_df, inventory_df, campaigns_df):
    st.markdown("## 🔍 Data Explorer")
    st.markdown("---")
    
    logger.info('NAVIGATION', 'Viewed Data Explorer')
    
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
    
    cols = st.multiselect("Columns", df.columns.tolist(), default=df.columns.tolist()[:8])
    
    if cols:
        st.dataframe(df[cols], use_container_width=True, height=400)
        
        csv = df[cols].to_csv(index=False)
        st.download_button("📥 Download CSV", csv, f"{selected.lower()}_export.csv", "text/csv")
        logger.info('EXPORT', f'Exported {selected} data', {'rows': len(df), 'columns': len(cols)})


# =============================================================================
# MAIN APPLICATION
# =============================================================================
def main():
    apply_custom_css()
    
    # Initialize data if not loaded
    if 'data_loaded' not in st.session_state:
        st.session_state.data_loaded = False
    
    # Sidebar Navigation
    with st.sidebar:
        st.markdown("# 🛒 UAE Retail")
        st.markdown("**Analytics Dashboard**")
        st.markdown("---")
        
        nav = st.radio(
            "Navigation",
            options=[
                "📂 Data Input",
                "🏠 Overview",
                "📈 Sales",
                "📦 Inventory",
                "🎯 Campaigns",
                "🏪 Stores",
                "⏰ Time Patterns",
                "🔍 Explorer",
                "📋 Logs"
            ],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        # Data status
        if st.session_state.get('data_loaded', False):
            st.markdown("✅ **Data Loaded**")
            if 'sales_df' in st.session_state:
                st.markdown(f"📊 Sales: {len(st.session_state.sales_df):,}")
        else:
            st.markdown("⚠️ **No Data**")
            st.markdown("Go to Data Input")
        
        st.markdown("---")
        
        if st.button("🔄 Reset All", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
        
        st.caption(f"Updated: {datetime.now().strftime('%H:%M:%S')}")
    
    # Main Content
    if nav == "📂 Data Input":
        render_data_input_tab()
    
    elif nav == "📋 Logs":
        render_logs_tab()
    
    else:
        # Check if data is loaded
        if not st.session_state.get('data_loaded', False):
            st.warning("⚠️ No data loaded. Please go to **Data Input** to upload files or generate sample data.")
            
            if st.button("🔄 Generate Sample Data Now"):
                with st.spinner("Generating..."):
                    sales_df, products_df, stores_df, inventory_df, campaigns_df = generate_all_data()
                    st.session_state.sales_df = sales_df
                    st.session_state.products_df = products_df
                    st.session_state.stores_df = stores_df
                    st.session_state.inventory_df = inventory_df
                    st.session_state.campaigns_df = campaigns_df
                    st.session_state.data_loaded = True
                    logger.info('DATA_INPUT', 'Sample data generated from main page')
                    st.rerun()
            return
        
        # Get data
        sales_df = st.session_state.get('sales_df', pd.DataFrame())
        products_df = st.session_state.get('products_df', pd.DataFrame())
        stores_df = st.session_state.get('stores_df', pd.DataFrame())
        inventory_df = st.session_state.get('inventory_df', pd.DataFrame())
        campaigns_df = st.session_state.get('campaigns_df', pd.DataFrame())
        
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
