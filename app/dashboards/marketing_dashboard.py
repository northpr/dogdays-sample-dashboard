import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime, timedelta

def render_dashboard(sales_df):
    """
    Render the marketing performance dashboard
    
    Parameters:
    -----------
    sales_df : pandas.DataFrame
        DataFrame containing sales data
    """
    st.markdown("## แดชบอร์ดประสิทธิภาพการตลาด (Marketing Performance Dashboard)")
    
    # Check if we have data
    if sales_df.empty:
        st.error("No sales data available. Please check your data source.")
        return
    
    # In a real implementation, this would connect to actual marketing data
    # For this demo, we'll simulate marketing data based on the sales data
    
    st.info("นี่เป็นตัวอย่างแดชบอร์ดประสิทธิภาพการตลาด ในการใช้งานจริง จะเชื่อมต่อกับข้อมูลแคมเปญการตลาดจริง")
    
    # Data preprocessing
    # Convert date columns to datetime if needed
    try:
        if 'วันที่ทำรายการ' in sales_df.columns:
            if not pd.api.types.is_datetime64_any_dtype(sales_df['วันที่ทำรายการ']):
                sales_df['วันที่ทำรายการ'] = pd.to_datetime(sales_df['วันที่ทำรายการ'], format='%d/%m/%Y', errors='coerce')
                
                # Extract month and year for trend analysis
                sales_df['month'] = sales_df['วันที่ทำรายการ'].dt.month
                sales_df['year'] = sales_df['วันที่ทำรายการ'].dt.year
                sales_df['month_year'] = sales_df['วันที่ทำรายการ'].dt.strftime('%Y-%m')
    except Exception as e:
        st.warning(f"Error processing date fields: {e}")
    
    # Simulate marketing campaign data
    # In a real implementation, this would come from actual marketing data
    np.random.seed(42)  # For reproducibility
    
    # Create simulated campaign data
    campaigns = [
        {"name": "Summer Sale", "start_date": "2024-05-01", "end_date": "2024-05-15", "budget": 15000, "channel": "Social Media"},
        {"name": "New Product Launch", "start_date": "2024-05-10", "end_date": "2024-05-20", "budget": 25000, "channel": "Email"},
        {"name": "Loyalty Program", "start_date": "2024-05-01", "end_date": "2024-05-31", "budget": 10000, "channel": "In-store"},
        {"name": "Flash Sale", "start_date": "2024-05-25", "end_date": "2024-05-27", "budget": 5000, "channel": "Social Media"},
        {"name": "Holiday Special", "start_date": "2024-05-28", "end_date": "2024-06-05", "budget": 20000, "channel": "Multi-channel"}
    ]
    
    # Convert to DataFrame
    campaign_df = pd.DataFrame(campaigns)
    campaign_df['start_date'] = pd.to_datetime(campaign_df['start_date'])
    campaign_df['end_date'] = pd.to_datetime(campaign_df['end_date'])
    
    # Simulate campaign performance metrics
    campaign_df['impressions'] = np.random.randint(5000, 50000, size=len(campaign_df))
    campaign_df['clicks'] = campaign_df['impressions'] * np.random.uniform(0.02, 0.08, size=len(campaign_df))
    campaign_df['conversions'] = campaign_df['clicks'] * np.random.uniform(0.05, 0.15, size=len(campaign_df))
    campaign_df['revenue'] = campaign_df['conversions'] * np.random.uniform(500, 2000, size=len(campaign_df))
    campaign_df['roi'] = ((campaign_df['revenue'] - campaign_df['budget']) / campaign_df['budget']) * 100
    
    # Marketing overview
    st.markdown("### ประสิทธิภาพแคมเปญการตลาด")
    
    # Display campaign metrics in cards
    total_budget = campaign_df['budget'].sum()
    total_revenue = campaign_df['revenue'].sum()
    total_roi = ((total_revenue - total_budget) / total_budget) * 100 if total_budget > 0 else 0
    best_campaign = campaign_df.loc[campaign_df['roi'].idxmax(), 'name'] if not campaign_df.empty else "N/A"
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">฿{total_budget:,.0f}</div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-label">งบประมาณการตลาดรวม</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">฿{total_revenue:,.0f}</div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-label">รายได้จากแคมเปญรวม</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">{total_roi:.1f}%</div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-label">ROI โดยรวม</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">{best_campaign}</div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-label">แคมเปญที่ดีที่สุด</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Campaign ROI comparison
    st.markdown("### เปรียบเทียบ ROI ของแคมเปญ")
    
    # Create bar chart for campaign ROI
    fig = px.bar(
        campaign_df.sort_values('roi', ascending=False),
        x='name',
        y='roi',
        title='Campaign ROI Comparison',
        labels={'name': 'Campaign', 'roi': 'ROI (%)'},
        color='roi',
        color_continuous_scale='RdYlGn',
        text='roi'
    )
    fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)
    
    # Campaign performance metrics
    st.markdown("### ตัวชี้วัดประสิทธิภาพแคมเปญ")
    
    # Create a table with campaign metrics
    campaign_metrics = campaign_df[['name', 'channel', 'budget', 'impressions', 'clicks', 'conversions', 'revenue', 'roi']]
    campaign_metrics['ctr'] = (campaign_metrics['clicks'] / campaign_metrics['impressions']) * 100  # Click-through rate
    campaign_metrics['cvr'] = (campaign_metrics['conversions'] / campaign_metrics['clicks']) * 100  # Conversion rate
    campaign_metrics['cpc'] = campaign_metrics['budget'] / campaign_metrics['clicks']  # Cost per click
    campaign_metrics['cpa'] = campaign_metrics['budget'] / campaign_metrics['conversions']  # Cost per acquisition
    
    # Format metrics for display
    display_metrics = campaign_metrics.copy()
    display_metrics['budget'] = display_metrics['budget'].apply(lambda x: f"฿{x:,.0f}")
    display_metrics['impressions'] = display_metrics['impressions'].apply(lambda x: f"{x:,.0f}")
    display_metrics['clicks'] = display_metrics['clicks'].apply(lambda x: f"{x:,.0f}")
    display_metrics['conversions'] = display_metrics['conversions'].apply(lambda x: f"{x:,.0f}")
    display_metrics['revenue'] = display_metrics['revenue'].apply(lambda x: f"฿{x:,.0f}")
    display_metrics['roi'] = display_metrics['roi'].apply(lambda x: f"{x:.1f}%")
    display_metrics['ctr'] = display_metrics['ctr'].apply(lambda x: f"{x:.2f}%")
    display_metrics['cvr'] = display_metrics['cvr'].apply(lambda x: f"{x:.2f}%")
    display_metrics['cpc'] = display_metrics['cpc'].apply(lambda x: f"฿{x:.2f}")
    display_metrics['cpa'] = display_metrics['cpa'].apply(lambda x: f"฿{x:.2f}")
    
    # Display the metrics table
    st.dataframe(display_metrics, use_container_width=True)
    
    # Channel performance
    st.markdown("### ประสิทธิภาพช่องทางการตลาด")
    
    # Group by channel and calculate metrics
    channel_metrics = campaign_df.groupby('channel').agg({
        'budget': 'sum',
        'revenue': 'sum',
        'impressions': 'sum',
        'clicks': 'sum',
        'conversions': 'sum'
    }).reset_index()
    
    # Calculate ROI and other metrics by channel
    channel_metrics['roi'] = ((channel_metrics['revenue'] - channel_metrics['budget']) / channel_metrics['budget']) * 100
    
    # Create radar chart for channel performance
    # Normalize metrics for radar chart
    radar_metrics = channel_metrics.copy()
    for col in ['budget', 'revenue', 'impressions', 'clicks', 'conversions', 'roi']:
        if col in radar_metrics.columns:
            max_val = radar_metrics[col].max()
            if max_val > 0:
                radar_metrics[col] = radar_metrics[col] / max_val * 100
    
    # Create radar chart
    fig = go.Figure()
    
    for i, channel in enumerate(radar_metrics['channel']):
        fig.add_trace(go.Scatterpolar(
            r=[
                radar_metrics.loc[radar_metrics['channel'] == channel, 'roi'].values[0],
                radar_metrics.loc[radar_metrics['channel'] == channel, 'revenue'].values[0],
                radar_metrics.loc[radar_metrics['channel'] == channel, 'conversions'].values[0],
                radar_metrics.loc[radar_metrics['channel'] == channel, 'clicks'].values[0],
                radar_metrics.loc[radar_metrics['channel'] == channel, 'impressions'].values[0]
            ],
            theta=['ROI', 'Revenue', 'Conversions', 'Clicks', 'Impressions'],
            fill='toself',
            name=channel
        ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )
        ),
        title='Channel Performance Comparison',
        height=500
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Sales trend with campaign overlay
    st.markdown("### แนวโน้มยอดขายพร้อมช่วงเวลาแคมเปญ")
    
    # Check if we have date data
    if 'วันที่ทำรายการ' in sales_df.columns and 'มูลค่า' in sales_df.columns:
        # Group by date and sum sales
        daily_sales = sales_df.groupby('วันที่ทำรายการ')['มูลค่า'].sum().reset_index()
        daily_sales = daily_sales.sort_values('วันที่ทำรายการ')
        
        # Create line chart with campaign periods highlighted
        fig = px.line(
            daily_sales,
            x='วันที่ทำรายการ',
            y='มูลค่า',
            title='Daily Sales with Campaign Periods',
            labels={'วันที่ทำรายการ': 'Date', 'มูลค่า': 'Sales Amount (฿)'}
        )
        
        # Add campaign periods as shaded regions
        for _, campaign in campaign_df.iterrows():
            fig.add_vrect(
                x0=campaign['start_date'],
                x1=campaign['end_date'],
                fillcolor=f"rgba({np.random.randint(0, 256)}, {np.random.randint(0, 256)}, {np.random.randint(0, 256)}, 0.2)",
                opacity=0.5,
                layer="below",
                line_width=0,
                annotation_text=campaign['name'],
                annotation_position="top left"
            )
        
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Date data not available for sales trend analysis.")
    
    # Discount analysis
    st.markdown("### การวิเคราะห์ผลกระทบของส่วนลด")
    
    # Check if we have discount data
    if 'ส่วนลด' in sales_df.columns and 'มูลค่า' in sales_df.columns:
        # Create a scatter plot of discount vs. sales
        fig = px.scatter(
            sales_df,
            x='ส่วนลด',
            y='มูลค่า',
            title='Discount Impact on Sales',
            labels={'ส่วนลด': 'Discount Amount (฿)', 'มูลค่า': 'Sales Amount (฿)'},
            trendline="ols",
            opacity=0.7
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
        
        # Group by discount percentage and calculate average order value
        if 'ส่วนลดต่อหน่วย' in sales_df.columns and 'ราคาต่อหน่วย' in sales_df.columns:
            # Calculate discount percentage
            sales_df['discount_pct'] = (sales_df['ส่วนลดต่อหน่วย'] / sales_df['ราคาต่อหน่วย']) * 100
            
            # Create discount bins
            sales_df['discount_bin'] = pd.cut(
                sales_df['discount_pct'],
                bins=[0, 5, 10, 15, 20, 100],
                labels=['0-5%', '5-10%', '10-15%', '15-20%', '20%+']
            )
            
            # Group by discount bin and calculate metrics
            discount_analysis = sales_df.groupby('discount_bin').agg({
                'มูลค่า': 'mean',
                'รายการ': 'count'
            }).reset_index()
            
            # Rename columns
            discount_analysis.columns = ['Discount Range', 'Avg. Order Value', 'Number of Orders']
            
            # Create bar chart
            fig = px.bar(
                discount_analysis,
                x='Discount Range',
                y='Avg. Order Value',
                title='Average Order Value by Discount Range',
                labels={'Discount Range': 'Discount Percentage', 'Avg. Order Value': 'Average Order Value (฿)'},
                color='Number of Orders',
                text='Avg. Order Value'
            )
            fig.update_traces(texttemplate='฿%{text:.2f}', textposition='outside')
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Discount data not available for impact analysis.")
