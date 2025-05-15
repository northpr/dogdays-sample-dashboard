import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime, timedelta

def render_dashboard(sales_df, customer_df):
    """
    Render the customer analytics dashboard
    
    Parameters:
    -----------
    sales_df : pandas.DataFrame
        DataFrame containing sales data
    customer_df : pandas.DataFrame
        DataFrame containing customer data
    """
    st.markdown("## แดชบอร์ดวิเคราะห์ลูกค้า (Customer Analytics Dashboard)")
    
    # Check if we have data
    if sales_df.empty or customer_df.empty:
        st.error("No customer data available. Please check your data source.")
        return
    
    # In a real implementation, this would connect to actual customer data
    # For this demo, we'll use the customer information from the sales data
    
    st.info("นี่เป็นตัวอย่างแดชบอร์ดวิเคราะห์ลูกค้า ในการใช้งานจริง จะเชื่อมต่อกับฐานข้อมูลลูกค้าที่สมบูรณ์")
    
    # Data preprocessing
    # Convert date columns to datetime if needed
    try:
        if 'วันที่ทำรายการ' in sales_df.columns:
            if not pd.api.types.is_datetime64_any_dtype(sales_df['วันที่ทำรายการ']):
                sales_df['วันที่ทำรายการ'] = pd.to_datetime(sales_df['วันที่ทำรายการ'], format='%d/%m/%Y', errors='coerce')
    except Exception as e:
        st.warning(f"Error processing date fields: {e}")
    
    # Customer overview
    st.markdown("### ภาพรวมลูกค้า")
    
    # Calculate customer metrics
    if 'ชื่อลูกค้า' in sales_df.columns:
        # Count unique customers
        unique_customers = sales_df['ชื่อลูกค้า'].nunique()
        
        # Calculate average order value per customer
        customer_orders = sales_df.groupby('ชื่อลูกค้า')['มูลค่า'].sum()
        avg_customer_value = customer_orders.mean() if not customer_orders.empty else 0
        
        # Calculate orders per customer
        customer_order_counts = sales_df.groupby('ชื่อลูกค้า')['รายการ'].nunique()
        avg_orders_per_customer = customer_order_counts.mean() if not customer_order_counts.empty else 0
        
        # Identify repeat customers (more than 1 order)
        repeat_customers = (customer_order_counts > 1).sum()
        repeat_customer_rate = (repeat_customers / unique_customers) * 100 if unique_customers > 0 else 0
        
        # Display metrics in cards
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-value">{unique_customers:,}</div>', unsafe_allow_html=True)
            st.markdown('<div class="metric-label">จำนวนลูกค้าทั้งหมด</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-value">฿{avg_customer_value:,.2f}</div>', unsafe_allow_html=True)
            st.markdown('<div class="metric-label">มูลค่าลูกค้าเฉลี่ย</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col3:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-value">{avg_orders_per_customer:.2f}</div>', unsafe_allow_html=True)
            st.markdown('<div class="metric-label">จำนวนออเดอร์ต่อลูกค้า</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col4:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-value">{repeat_customer_rate:.1f}%</div>', unsafe_allow_html=True)
            st.markdown('<div class="metric-label">อัตราลูกค้าซื้อซ้ำ</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Customer segmentation
        st.markdown("### การแบ่งกลุ่มลูกค้า")
        
        # Create RFM (Recency, Frequency, Monetary) segmentation
        if 'วันที่ทำรายการ' in sales_df.columns and not sales_df['วันที่ทำรายการ'].isna().all():
            # Calculate the most recent date in the dataset
            max_date = sales_df['วันที่ทำรายการ'].max()
            
            # Calculate RFM metrics
            rfm = sales_df.groupby('ชื่อลูกค้า').agg({
                'วันที่ทำรายการ': lambda x: (max_date - x.max()).days,  # Recency
                'รายการ': 'nunique',  # Frequency
                'มูลค่า': 'sum'  # Monetary
            }).reset_index()
            
            # Rename columns
            rfm.columns = ['ชื่อลูกค้า', 'Recency', 'Frequency', 'Monetary']
            
            # Create segments
            rfm['RecencyScore'] = pd.qcut(rfm['Recency'], 3, labels=[3, 2, 1])
            rfm['FrequencyScore'] = pd.qcut(rfm['Frequency'].rank(method='first'), 3, labels=[1, 2, 3])
            rfm['MonetaryScore'] = pd.qcut(rfm['Monetary'].rank(method='first'), 3, labels=[1, 2, 3])
            
            # Calculate RFM Score
            rfm['RFMScore'] = rfm['RecencyScore'].astype(str) + rfm['FrequencyScore'].astype(str) + rfm['MonetaryScore'].astype(str)
            
            # Create segment labels
            segment_map = {
                '311': 'New High Spenders',
                '312': 'New High Spenders',
                '313': 'New High Spenders',
                '321': 'New Active Customers',
                '322': 'New Active Customers',
                '323': 'New Active Customers',
                '331': 'New Low Spenders',
                '332': 'New Low Spenders',
                '333': 'New Low Spenders',
                '211': 'Active High Spenders',
                '212': 'Active High Spenders',
                '213': 'Active High Spenders',
                '221': 'Active Regular Customers',
                '222': 'Active Regular Customers',
                '223': 'Active Regular Customers',
                '231': 'Active Low Spenders',
                '232': 'Active Low Spenders',
                '233': 'Active Low Spenders',
                '111': 'Inactive High Spenders',
                '112': 'Inactive High Spenders',
                '113': 'Inactive High Spenders',
                '121': 'Inactive Regular Customers',
                '122': 'Inactive Regular Customers',
                '123': 'Inactive Regular Customers',
                '131': 'Inactive Low Spenders',
                '132': 'Inactive Low Spenders',
                '133': 'Inactive Low Spenders'
            }
            
            rfm['Segment'] = rfm['RFMScore'].map(segment_map)
            
            # Create a bubble chart for customer segmentation
            fig = px.scatter(
                rfm,
                x='Recency',
                y='Frequency',
                size='Monetary',
                color='Segment',
                hover_name='ชื่อลูกค้า',
                title='Customer Segmentation (RFM Analysis)',
                labels={
                    'Recency': 'Days Since Last Purchase',
                    'Frequency': 'Number of Orders',
                    'Monetary': 'Total Spend (฿)'
                },
                size_max=50
            )
            fig.update_layout(height=500)
            st.plotly_chart(fig, use_container_width=True)
            
            # Segment distribution
            segment_counts = rfm['Segment'].value_counts().reset_index()
            segment_counts.columns = ['Segment', 'Count']
            
            fig = px.pie(
                segment_counts,
                values='Count',
                names='Segment',
                title='Customer Segment Distribution',
                hole=0.4
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Date data not available for customer segmentation.")
        
        # Geographic distribution
        st.markdown("### การกระจายตัวทางภูมิศาสตร์ของลูกค้า")
        
        # Check if we have geographic data
        if 'จังหวัด' in sales_df.columns:
            # Group by province and count customers
            province_customers = sales_df.groupby('จังหวัด')['ชื่อลูกค้า'].nunique().reset_index()
            province_customers.columns = ['จังหวัด', 'จำนวนลูกค้า']
            province_customers = province_customers.sort_values('จำนวนลูกค้า', ascending=False)
            
            # Create bar chart
            fig = px.bar(
                province_customers,
                x='จังหวัด',
                y='จำนวนลูกค้า',
                title='Customers by Province',
                labels={'จังหวัด': 'Province', 'จำนวนลูกค้า': 'Number of Customers'},
                color='จำนวนลูกค้า',
                color_continuous_scale='Viridis'
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Geographic data not available for customer distribution analysis.")
        
        # Top customers
        st.markdown("### ลูกค้าที่มียอดซื้อสูงสุด")
        
        # Group by customer and sum sales
        customer_sales = sales_df.groupby('ชื่อลูกค้า')['มูลค่า'].sum().reset_index()
        customer_sales = customer_sales.sort_values('มูลค่า', ascending=False)
        
        # Display top 10 customers
        fig = px.bar(
            customer_sales.head(10),
            x='ชื่อลูกค้า',
            y='มูลค่า',
            title='Top 10 Customers by Sales',
            labels={'ชื่อลูกค้า': 'Customer', 'มูลค่า': 'Total Sales (฿)'},
            color='มูลค่า',
            color_continuous_scale='Viridis'
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
        
        # Customer details table
        st.markdown("### รายละเอียดลูกค้า")
        
        # Create a searchable customer table
        if not customer_df.empty:
            st.dataframe(customer_df, use_container_width=True, height=400)
        else:
            st.info("Detailed customer data not available.")
    else:
        st.warning("Customer data not found in the dataset.")
