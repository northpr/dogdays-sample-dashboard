import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

def render_dashboard(sales_df, product_df):
    """
    Render the inventory management dashboard
    
    Parameters:
    -----------
    sales_df : pandas.DataFrame
        DataFrame containing sales data
    product_df : pandas.DataFrame
        DataFrame containing product data
    """
    st.markdown("## แดชบอร์ดการจัดการคลังสินค้า (Inventory Management Dashboard)")
    
    # Check if we have data
    if sales_df.empty or product_df.empty:
        st.error("No inventory data available. Please check your data source.")
        return
    
    # In a real implementation, this would connect to actual inventory data
    # For this demo, we'll simulate inventory data based on the sales data
    
    st.info("นี่เป็นตัวอย่างแดชบอร์ดการจัดการคลังสินค้า ในการใช้งานจริง จะเชื่อมต่อกับข้อมูลคลังสินค้าจริง")
    
    # Create simulated inventory data
    if 'รหัสสินค้า' in product_df.columns and 'ชื่อสินค้า' in product_df.columns:
        # Get unique products
        unique_products = product_df[['รหัสสินค้า', 'ชื่อสินค้า']].drop_duplicates()
        
        # Simulate inventory levels
        np.random.seed(42)  # For reproducibility
        unique_products['คงเหลือ'] = np.random.randint(10, 200, size=len(unique_products))
        unique_products['มูลค่าคงเหลือ'] = unique_products['คงเหลือ'] * product_df['ราคาต่อหน่วย'].values
        unique_products['สถานะ'] = unique_products['คงเหลือ'].apply(
            lambda x: 'ต่ำ' if x < 30 else ('ปานกลาง' if x < 100 else 'สูง')
        )
        
        # Display inventory summary
        st.markdown("### สรุปคลังสินค้า")
        
        # Calculate summary metrics
        total_inventory_value = unique_products['มูลค่าคงเหลือ'].sum()
        total_inventory_units = unique_products['คงเหลือ'].sum()
        low_stock_count = (unique_products['สถานะ'] == 'ต่ำ').sum()
        avg_inventory_value = total_inventory_value / len(unique_products) if len(unique_products) > 0 else 0
        
        # Display metrics in cards
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-value">฿{total_inventory_value:,.2f}</div>', unsafe_allow_html=True)
            st.markdown('<div class="metric-label">มูลค่าคลังสินค้ารวม</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-value">{total_inventory_units:,}</div>', unsafe_allow_html=True)
            st.markdown('<div class="metric-label">จำนวนสินค้าคงเหลือ</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col3:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-value">{low_stock_count}</div>', unsafe_allow_html=True)
            st.markdown('<div class="metric-label">สินค้าใกล้หมด</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col4:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-value">฿{avg_inventory_value:,.2f}</div>', unsafe_allow_html=True)
            st.markdown('<div class="metric-label">มูลค่าสินค้าเฉลี่ย</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Inventory levels by product
        st.markdown("### ระดับสินค้าคงคลังตามสินค้า")
        
        # Sort by inventory level
        sorted_inventory = unique_products.sort_values('คงเหลือ')
        
        # Create bar chart
        fig = px.bar(
            sorted_inventory,
            x='ชื่อสินค้า',
            y='คงเหลือ',
            title='Current Inventory Levels',
            labels={'ชื่อสินค้า': 'Product', 'คงเหลือ': 'Units in Stock'},
            color='สถานะ',
            color_discrete_map={'ต่ำ': 'red', 'ปานกลาง': 'orange', 'สูง': 'green'}
        )
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
        
        # Inventory value by product
        st.markdown("### มูลค่าคลังสินค้าตามสินค้า")
        
        # Sort by inventory value
        sorted_by_value = unique_products.sort_values('มูลค่าคงเหลือ', ascending=False)
        
        # Create bar chart
        fig = px.bar(
            sorted_by_value.head(10),  # Top 10 products by value
            x='ชื่อสินค้า',
            y='มูลค่าคงเหลือ',
            title='Top 10 Products by Inventory Value',
            labels={'ชื่อสินค้า': 'Product', 'มูลค่าคงเหลือ': 'Inventory Value (฿)'},
            color='มูลค่าคงเหลือ',
            color_continuous_scale='Viridis'
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
        
        # Low stock alerts
        st.markdown("### แจ้งเตือนสินค้าใกล้หมด")
        
        # Filter products with low stock
        low_stock = unique_products[unique_products['สถานะ'] == 'ต่ำ'].sort_values('คงเหลือ')
        
        if not low_stock.empty:
            # Create a table with conditional formatting
            st.dataframe(
                low_stock[['รหัสสินค้า', 'ชื่อสินค้า', 'คงเหลือ', 'มูลค่าคงเหลือ']],
                use_container_width=True,
                height=400
            )
        else:
            st.success("ไม่มีสินค้าที่ใกล้หมด")
        
        # Inventory management table
        st.markdown("### การจัดการคลังสินค้า")
        
        # Display full inventory table with search and sort capabilities
        st.dataframe(
            unique_products[['รหัสสินค้า', 'ชื่อสินค้า', 'คงเหลือ', 'มูลค่าคงเหลือ', 'สถานะ']],
            use_container_width=True,
            height=400
        )
    else:
        st.warning("Product data columns not found in the dataset.")
