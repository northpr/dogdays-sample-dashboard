import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np

def render_dashboard(sales_df):
    """
    Render the sales overview dashboard
    
    Parameters:
    -----------
    sales_df : pandas.DataFrame
        DataFrame containing sales data
    """
    st.markdown("## แดชบอร์ดภาพรวมยอดขาย (Sales Overview Dashboard)")
    
    # Check if we have data
    if sales_df.empty:
        st.error("No sales data available. Please check your data source.")
        return
    
    # Data preprocessing
    # Convert date columns to datetime
    try:
        sales_df['วันที่ทำรายการ'] = pd.to_datetime(sales_df['วันที่ทำรายการ'], format='%d/%m/%Y', errors='coerce')
        
        # Filter out rows with invalid dates
        sales_df = sales_df.dropna(subset=['วันที่ทำรายการ'])
        
        # Extract additional date components
        sales_df['month'] = sales_df['วันที่ทำรายการ'].dt.month
        sales_df['year'] = sales_df['วันที่ทำรายการ'].dt.year
        sales_df['day'] = sales_df['วันที่ทำรายการ'].dt.day
        sales_df['weekday'] = sales_df['วันที่ทำรายการ'].dt.day_name()
    except Exception as e:
        st.warning(f"Error processing date fields: {e}")
    
    # Summary metrics section
    st.markdown("### ตัวชี้วัดหลัก (Key Metrics)")
    
    # Calculate metrics
    total_sales = sales_df['มูลค่า'].sum() if 'มูลค่า' in sales_df.columns else 0
    total_orders = sales_df['รายการ'].nunique() if 'รายการ' in sales_df.columns else 0
    avg_order_value = total_sales / total_orders if total_orders > 0 else 0
    
    # Get top selling products
    if 'ชื่อสินค้า' in sales_df.columns and 'จำนวน' in sales_df.columns:
        product_sales = sales_df.groupby('ชื่อสินค้า')['จำนวน'].sum().sort_values(ascending=False)
        top_product = product_sales.index[0] if not product_sales.empty else "N/A"
    else:
        top_product = "N/A"
    
    # Get top sales channel
    if 'ช่องทางการขาย' in sales_df.columns:
        channel_sales = sales_df.groupby('ช่องทางการขาย')['มูลค่า'].sum().sort_values(ascending=False)
        top_channel = channel_sales.index[0] if not channel_sales.empty else "N/A"
    else:
        top_channel = "N/A"
    
    # Display metrics in cards
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">฿{total_sales:,.2f}</div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-label">ยอดขายรวม</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">{total_orders:,}</div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-label">จำนวนออเดอร์</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">฿{avg_order_value:,.2f}</div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-label">มูลค่าออเดอร์เฉลี่ย</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">{top_product}</div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-label">สินค้าขายดี</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col5:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">{top_channel}</div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-label">ช่องทางขายดี</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Sales by region/province
    st.markdown("### ยอดขายตามภูมิภาค")
    
    # Check if we have geographic data
    if 'จังหวัด' in sales_df.columns:
        # Group by province and sum sales
        province_sales = sales_df.groupby('จังหวัด')['มูลค่า'].sum().reset_index()
        province_sales = province_sales.sort_values('มูลค่า', ascending=False)
        
        # Create bar chart
        fig = px.bar(
            province_sales,
            x='จังหวัด',
            y='มูลค่า',
            title='Sales by Province',
            labels={'จังหวัด': 'Province', 'มูลค่า': 'Sales Amount (฿)'},
            color='มูลค่า',
            color_continuous_scale='Viridis'
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Geographic data not available in the dataset.")
    
    # Sales trends over time
    st.markdown("### แนวโน้มยอดขาย")
    
    # Check if we have date data
    if 'วันที่ทำรายการ' in sales_df.columns:
        # Group by date and sum sales
        daily_sales = sales_df.groupby('วันที่ทำรายการ')['มูลค่า'].sum().reset_index()
        daily_sales = daily_sales.sort_values('วันที่ทำรายการ')
        
        # Create line chart
        fig = px.line(
            daily_sales,
            x='วันที่ทำรายการ',
            y='มูลค่า',
            title='Daily Sales Trend',
            labels={'วันที่ทำรายการ': 'Date', 'มูลค่า': 'Sales Amount (฿)'}
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Date data not available in the dataset.")
    
    # Sales by product category
    st.markdown("### ยอดขายตามหมวดหมู่สินค้า")
    
    # Check if we have product category data
    if 'หมวดหมู่' in sales_df.columns and 'มูลค่า' in sales_df.columns:
        # Group by category and sum sales
        category_sales = sales_df.groupby('หมวดหมู่')['มูลค่า'].sum().reset_index()
        category_sales = category_sales.sort_values('มูลค่า', ascending=False)
        
        # Create pie chart
        fig = px.pie(
            category_sales,
            values='มูลค่า',
            names='หมวดหมู่',
            title='Sales by Product Category',
            hole=0.4
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Product category data not available in the dataset.")
    
    # Sales by channel
    st.markdown("### ยอดขายตามช่องทางการขาย")
    
    # Check if we have channel data
    if 'ช่องทางการขาย' in sales_df.columns and 'มูลค่า' in sales_df.columns:
        # Group by channel and sum sales
        channel_sales_df = sales_df.groupby('ช่องทางการขาย')['มูลค่า'].sum().reset_index()
        channel_sales_df = channel_sales_df.sort_values('มูลค่า', ascending=False)
        
        # Create horizontal bar chart
        fig = px.bar(
            channel_sales_df,
            y='ช่องทางการขาย',
            x='มูลค่า',
            title='Sales by Channel',
            labels={'ช่องทางการขาย': 'Channel', 'มูลค่า': 'Sales Amount (฿)'},
            orientation='h',
            color='มูลค่า',
            color_continuous_scale='Viridis'
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Sales channel data not available in the dataset.")
    
    # Recent orders table
    st.markdown("### ออเดอร์ล่าสุด")
    
    # Check if we have order data
    if not sales_df.empty:
        # Sort by date (most recent first)
        recent_orders = sales_df.sort_values('วันที่ทำรายการ', ascending=False)
        
        # Select relevant columns for display
        display_columns = [
            'รายการ', 'วันที่ทำรายการ', 'ชื่อลูกค้า', 'ชื่อสินค้า', 
            'จำนวน', 'ราคาต่อหน่วย', 'มูลค่า', 'สถานะรายการ'
        ]
        
        # Filter columns that exist in the dataframe
        display_columns = [col for col in display_columns if col in recent_orders.columns]
        
        if display_columns:
            # Display the 10 most recent orders
            st.dataframe(recent_orders[display_columns].head(10), use_container_width=True)
        else:
            st.info("Order data columns not available in the dataset.")
    else:
        st.info("Order data not available in the dataset.")
