import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

def render_dashboard(sales_df, product_df):
    """
    Render the product performance dashboard
    
    Parameters:
    -----------
    sales_df : pandas.DataFrame
        DataFrame containing sales data
    product_df : pandas.DataFrame
        DataFrame containing product data
    """
    st.markdown("## แดชบอร์ดประสิทธิภาพสินค้า (Product Performance Dashboard)")
    
    # Check if we have data
    if sales_df.empty or product_df.empty:
        st.error("No product data available. Please check your data source.")
        return
    
    # Data preprocessing
    # Merge product data with sales data if needed
    
    # Product selection
    if 'ชื่อสินค้า' in sales_df.columns:
        # Get unique products
        products = sorted(sales_df['ชื่อสินค้า'].unique())
        
        # Create a selectbox for product selection
        selected_product = st.selectbox("เลือกสินค้าเพื่อวิเคราะห์โดยละเอียด", products)
        
        # Filter data for the selected product
        product_sales = sales_df[sales_df['ชื่อสินค้า'] == selected_product]
    else:
        st.warning("Product name column not found in the dataset.")
        return
    
    # Product performance metrics
    st.markdown("### ตัวชี้วัดประสิทธิภาพสินค้า")
    
    # Calculate metrics for the selected product
    total_units_sold = product_sales['จำนวน'].sum() if 'จำนวน' in product_sales.columns else 0
    total_revenue = product_sales['มูลค่า'].sum() if 'มูลค่า' in product_sales.columns else 0
    avg_price = product_sales['ราคาต่อหน่วย'].mean() if 'ราคาต่อหน่วย' in product_sales.columns else 0
    avg_discount = product_sales['ส่วนลดต่อหน่วย'].mean() if 'ส่วนลดต่อหน่วย' in product_sales.columns else 0
    
    # Display metrics in cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">{total_units_sold:,.0f}</div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-label">จำนวนที่ขายได้</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">฿{total_revenue:,.2f}</div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-label">รายได้รวม</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">฿{avg_price:,.2f}</div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-label">ราคาเฉลี่ย</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">฿{avg_discount:,.2f}</div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-label">ส่วนลดเฉลี่ย</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Product sales over time
    st.markdown("### แนวโน้มการขาย")
    
    # Check if we have date data
    if 'วันที่ทำรายการ' in product_sales.columns and 'มูลค่า' in product_sales.columns:
        try:
            # Convert date column to datetime if not already
            if not pd.api.types.is_datetime64_any_dtype(product_sales['วันที่ทำรายการ']):
                product_sales['วันที่ทำรายการ'] = pd.to_datetime(product_sales['วันที่ทำรายการ'], format='%d/%m/%Y', errors='coerce')
            
            # Group by date and sum sales
            daily_sales = product_sales.groupby('วันที่ทำรายการ')['มูลค่า'].sum().reset_index()
            daily_sales = daily_sales.sort_values('วันที่ทำรายการ')
            
            # Create line chart
            fig = px.line(
                daily_sales,
                x='วันที่ทำรายการ',
                y='มูลค่า',
                title=f'Daily Sales Trend for {selected_product}',
                labels={'วันที่ทำรายการ': 'Date', 'มูลค่า': 'Sales Amount (฿)'}
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.warning(f"Error processing date data: {e}")
    else:
        st.info("Date or sales amount data not available for trend analysis.")
    
    # Sales by channel for this product
    st.markdown("### ยอดขายตามช่องทาง")
    
    # Check if we have channel data
    if 'ช่องทางการขาย' in product_sales.columns and 'มูลค่า' in product_sales.columns:
        # Group by channel and sum sales
        channel_sales = product_sales.groupby('ช่องทางการขาย')['มูลค่า'].sum().reset_index()
        channel_sales = channel_sales.sort_values('มูลค่า', ascending=False)
        
        # Create pie chart
        fig = px.pie(
            channel_sales,
            values='มูลค่า',
            names='ช่องทางการขาย',
            title=f'Sales Channels for {selected_product}',
            hole=0.4
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Sales channel data not available for this product.")
    
    # Price point analysis
    st.markdown("### การวิเคราะห์ราคา")
    
    # Check if we have price data
    if 'ราคาต่อหน่วย' in product_sales.columns and 'จำนวน' in product_sales.columns:
        # Create a histogram of price points
        fig = px.histogram(
            product_sales,
            x='ราคาต่อหน่วย',
            y='จำนวน',
            title=f'Price Point Distribution for {selected_product}',
            labels={'ราคาต่อหน่วย': 'Price (฿)', 'จำนวน': 'Units Sold'},
            nbins=20
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Price data not available for price point analysis.")
    
    # Discount impact analysis
    st.markdown("### การวิเคราะห์ผลกระทบของส่วนลด")
    
    # Check if we have discount data
    if 'ส่วนลดต่อหน่วย' in product_sales.columns and 'จำนวน' in product_sales.columns:
        # Create a scatter plot of discount vs. units sold
        fig = px.scatter(
            product_sales,
            x='ส่วนลดต่อหน่วย',
            y='จำนวน',
            title=f'Discount Impact for {selected_product}',
            labels={'ส่วนลดต่อหน่วย': 'Discount Amount (฿)', 'จำนวน': 'Units Sold'},
            trendline="ols"
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Discount data not available for impact analysis.")
    
    # Product comparison
    st.markdown("### เปรียบเทียบสินค้าในหมวดหมู่เดียวกัน")
    
    # Check if we have category data
    if 'หมวดหมู่' in sales_df.columns and 'ชื่อสินค้า' in sales_df.columns and 'มูลค่า' in sales_df.columns:
        # Get the category of the selected product
        selected_category = product_sales['หมวดหมู่'].iloc[0] if not product_sales.empty and 'หมวดหมู่' in product_sales.columns else None
        
        if selected_category:
            # Filter sales data for the same category
            category_sales = sales_df[sales_df['หมวดหมู่'] == selected_category]
            
            # Group by product and sum sales
            product_comparison = category_sales.groupby('ชื่อสินค้า')['มูลค่า'].sum().reset_index()
            product_comparison = product_comparison.sort_values('มูลค่า', ascending=False)
            
            # Create bar chart
            fig = px.bar(
                product_comparison,
                x='ชื่อสินค้า',
                y='มูลค่า',
                title=f'Product Comparison in {selected_category} Category',
                labels={'ชื่อสินค้า': 'Product', 'มูลค่า': 'Sales Amount (฿)'},
                color='มูลค่า',
                color_continuous_scale='Viridis'
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Category information not available for the selected product.")
    else:
        st.info("Category data not available for product comparison.")
