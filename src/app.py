import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from dashboards import sales_dashboard, product_dashboard, inventory_dashboard, customer_dashboard, marketing_dashboard

# Page configuration
st.set_page_config(
    page_title="Dog Days Dashboard",
    page_icon="🐕",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom CSS
def apply_custom_css():
    st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #3a4f41;
        text-align: center;
        margin-bottom: 1rem;
    }
    .dashboard-card {
        background-color: #f9f9f9;
        border-radius: 5px;
        padding: 1rem;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: white;
        border-radius: 5px;
        padding: 1rem;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        text-align: center;
    }
    .metric-value {
        font-size: 1.8rem;
        font-weight: bold;
        color: #3a4f41;
    }
    .metric-label {
        font-size: 0.9rem;
        color: #666;
    }
    .sidebar-nav-active {
        background-color: #3a4f41;
        color: white !important;
        border-radius: 5px;
        padding: 0.5rem;
        margin-bottom: 0.5rem;
        text-align: center;
        cursor: pointer;
    }
    .sidebar-nav-inactive {
        background-color: #f0f0f0;
        color: #3a4f41 !important;
        border-radius: 5px;
        padding: 0.5rem;
        margin-bottom: 0.5rem;
        text-align: center;
        cursor: pointer;
    }
    </style>
    """, unsafe_allow_html=True)

apply_custom_css()

# Data loading and caching
@st.cache_data(ttl=3600)
def load_sales_data():
    """Load and cache sales data"""
    try:
        # Path is relative to the current working directory
        file_path = os.path.join('..', 'data', 'dog_days_sales_data.xlsx')
        df = pd.read_excel(file_path)
        return df
    except Exception as e:
        st.error(f"Error loading sales data: {e}")
        return pd.DataFrame()

@st.cache_data(ttl=3600)
def load_product_data():
    """Load and cache product data"""
    # In a real implementation, this would load actual product data
    # For now, we'll extract product info from the sales data
    sales_df = load_sales_data()
    if not sales_df.empty:
        product_df = sales_df[['รหัสสินค้า', 'ชื่อสินค้า', 'ราคาต่อหน่วย', 'หมวดหมู่']].drop_duplicates()
        return product_df
    return pd.DataFrame()

@st.cache_data(ttl=3600)
def load_customer_data():
    """Load and cache customer data"""
    # In a real implementation, this would load actual customer data
    # For now, we'll extract customer info from the sales data
    sales_df = load_sales_data()
    if not sales_df.empty:
        customer_df = sales_df[['ชื่อลูกค้า', 'อีเมลลูกค้า', 'เบอร์โทรศัพท์ลูกค้า', 'ที่อยู่ลูกค้า', 'จังหวัด']].drop_duplicates()
        return customer_df
    return pd.DataFrame()

# Load data
sales_df = load_sales_data()
product_df = load_product_data()
customer_df = load_customer_data()

# Sidebar navigation
def render_sidebar():
    with st.sidebar:
        # Use the logo from the data directory
        st.image("../data/logo_dogdays.png", width=150)
        st.markdown("### แดชบอร์ด Dog Days")
        
        # Dashboard selection
        st.markdown("#### เลือกแดชบอร์ด")
        
        # Store the current dashboard selection in session state
        if 'current_dashboard' not in st.session_state:
            st.session_state.current_dashboard = 'sales'
            
        # Create navigation buttons - full width
        if st.button("ยอดขาย (Sales)", key="sales_btn", 
                    help="ดูแดชบอร์ดภาพรวมยอดขาย"):
            st.session_state.current_dashboard = 'sales'
            
        if st.button("สินค้า (Products)", key="products_btn", 
                    help="ดูแดชบอร์ดประสิทธิภาพสินค้า"):
            st.session_state.current_dashboard = 'products'
            
        if st.button("คลังสินค้า (Inventory)", key="inventory_btn", 
                    help="ดูแดชบอร์ดการจัดการคลังสินค้า"):
            st.session_state.current_dashboard = 'inventory'
            
        if st.button("ลูกค้า (Customers)", key="customers_btn", 
                    help="ดูแดชบอร์ดวิเคราะห์ลูกค้า"):
            st.session_state.current_dashboard = 'customers'
            
        if st.button("การตลาด (Marketing)", key="marketing_btn", 
                    help="ดูแดชบอร์ดประสิทธิภาพการตลาด"):
            st.session_state.current_dashboard = 'marketing'
        
        # Apply styling to the active button using JavaScript
        active_dashboard = st.session_state.current_dashboard
        st.markdown(f"""
        <script>
            document.getElementById("{active_dashboard}_btn").classList.add("sidebar-nav-active");
            document.getElementById("{active_dashboard}_btn").classList.remove("sidebar-nav-inactive");
        </script>
        """, unsafe_allow_html=True)
        
        # Filters section
        st.markdown("---")
        st.markdown("#### ตัวกรอง")
        
        # Date range filter
        st.markdown("**ช่วงวันที่**")
        # Default to last 30 days
        default_start_date = datetime.now() - timedelta(days=30)
        default_end_date = datetime.now()
        
        start_date = st.date_input("วันที่เริ่มต้น", value=default_start_date)
        end_date = st.date_input("วันที่สิ้นสุด", value=default_end_date)
        
        # Product category filter
        if not product_df.empty and 'หมวดหมู่' in product_df.columns:
            categories = ['All'] + sorted(product_df['หมวดหมู่'].dropna().unique().tolist())
            selected_category = st.selectbox("หมวดหมู่สินค้า", categories)
        
        # Sales channel filter
        if not sales_df.empty and 'ช่องทางการขาย' in sales_df.columns:
            channels = ['All'] + sorted(sales_df['ช่องทางการขาย'].dropna().unique().tolist())
            selected_channel = st.selectbox("ช่องทางการขาย", channels)
        
        # Footer
        st.markdown("---")
        st.markdown(f"**อัปเดตล่าสุด:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        st.markdown("© 2025 Dog Days")

# Main content based on selected dashboard
def render_main_content():
    # Display header
    st.markdown('<h1 class="main-header">แดชบอร์ด Dog Days</h1>', unsafe_allow_html=True)
    
    # Render the selected dashboard
    current_dashboard = st.session_state.get('current_dashboard', 'sales')
    
    if current_dashboard == 'sales':
        sales_dashboard.render_dashboard(sales_df)
    elif current_dashboard == 'products':
        product_dashboard.render_dashboard(sales_df, product_df)
    elif current_dashboard == 'inventory':
        inventory_dashboard.render_dashboard(sales_df, product_df)
    elif current_dashboard == 'customers':
        customer_dashboard.render_dashboard(sales_df, customer_df)
    elif current_dashboard == 'marketing':
        marketing_dashboard.render_dashboard(sales_df)

# Main app layout
def main():
    render_sidebar()
    render_main_content()

if __name__ == "__main__":
    main()
