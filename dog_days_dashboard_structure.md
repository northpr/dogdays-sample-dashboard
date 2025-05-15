# Dog Days - Retail Dog Food Company

## Dashboard Structure Overview

The Dog Days dashboard is built using Streamlit and follows a modular architecture with multiple specialized dashboards accessible through a sidebar navigation system. This structure is designed specifically for monitoring and analyzing dog food retail operations.

### Main Components

1. __Core Application (app.py)__

   - Sets up the page configuration with Dog Days branding (title, logo, and layout)
   - Loads and caches sales and inventory data
   - Implements the sidebar navigation with Dog Days branding
   - Renders the selected dashboard component

2. __Dashboard Modules__

   - Separate Python files for each dashboard type (sales, inventory, customer, product performance)
   - Each module contains a main function that receives data and renders visualizations
   - Modular design allows for easy extension and maintenance

3. __Data Management__

   - Centralized data loading with caching for performance
   - Support for multiple data sources (Excel files, CSV files, database connections)
   - Data preprocessing and cleaning functions

## Sidebar Navigation

The sidebar serves as the main navigation hub with:

- __Dashboard Selection__: Custom buttons for each dashboard type
- __Product Category Filter__: Dropdown for selecting specific product categories
- __Date Range Selection__: Date picker for time-based analysis
- __Footer Information__: Data update timestamp and company information
- __Custom CSS__: Styling with Dog Days branding colors

## Dashboard Types

### 1. Sales Overview Dashboard

__Key Elements__:

- Summary metrics in card format:
  - Daily/Monthly/Yearly Sales
  - Average Order Value
  - Number of Orders
  - Top Selling Products
  - Sales by Channel (Lazada, etc.)
- Interactive sales map by region/province
- Latest orders table with color-coding by status
- Sales trend charts with tabs for different time periods

__Data Visualization__:
- Bar charts for sales by product category
- Line charts for sales trends over time
- Pie charts for sales channel distribution
- Heatmap for sales by region

### 2. Product Performance Dashboard

__Key Elements__:

- Product status indicators with color-coding
- Time series analysis of product sales with date range selection
- Product category performance comparison
- Price point analysis
- Discount impact analysis

__Data Visualization__:
- Product performance scorecards
- Time series charts for individual product sales
- Comparative bar charts for product categories
- Scatter plots for price vs. sales volume
- Discount effectiveness analysis

### 3. Inventory Management Dashboard

__Key Elements__:

- Current inventory levels by product
- Stock alerts for low inventory
- Inventory turnover rates
- Reorder recommendations
- Warehouse/location inventory breakdown

__Data Visualization__:
- Gauge charts for inventory levels
- Bar charts for inventory by location
- Line charts for inventory trends
- Tables with conditional formatting for stock alerts
- Predictive charts for inventory forecasting

### 4. Customer Analytics Dashboard

__Key Elements__:

- Customer segmentation analysis
- Repeat purchase patterns
- Customer lifetime value calculations
- Geographic distribution of customers
- Customer acquisition channels

__Data Visualization__:
- Customer segmentation bubble charts
- Repeat purchase frequency histograms
- Geographic heatmaps of customer locations
- Customer journey funnel charts
- Retention rate charts

### 5. Marketing Performance Dashboard

__Key Elements__:

- Campaign performance metrics
- Discount and promotion analysis
- Channel effectiveness comparison
- Product bundle performance
- Seasonal trend analysis

__Data Visualization__:
- Campaign ROI bar charts
- Promotion impact before/after charts
- Channel comparison radar charts
- Bundle sales pie charts
- Seasonal trend line charts with moving averages

## Data Structure

The dashboard uses a structured data approach based on the existing sales data:

1. __Sales Data__

   - Transaction records from all sales channels
   - Fields include: order ID, customer details, product details, quantities, prices, discounts, payment methods, shipping information

2. __Product Information__

   - Metadata about products (SKU, name, category, size, price, etc.)
   - Inventory levels and locations

3. __Customer Data__

   - Customer profiles and purchase history
   - Geographic and demographic information

4. __Marketing Data__

   - Campaign information and performance metrics
   - Promotion details and discount codes

## Implementation Recommendations

1. __Data Integration and Preprocessing__:

   - Create automated data pipelines to process Excel files from various sales channels
   - Implement data cleaning and standardization procedures
   - Set up regular data refresh schedules

2. __Key Metrics to Track__:

   - Sales metrics:
     - Gross and net sales
     - Sales by product category
     - Sales by channel
     - Average order value
     - Order frequency

   - Product metrics:
     - Units sold by product
     - Revenue by product
     - Profit margin by product
     - Discount effectiveness

   - Customer metrics:
     - New vs. returning customers
     - Customer lifetime value
     - Geographic distribution
     - Purchase frequency

   - Inventory metrics:
     - Stock levels
     - Turnover rate
     - Days of supply
     - Reorder points

3. __Interactive Features__:

   - Date range selectors for all dashboards
   - Product category filters
   - Sales channel filters
   - Geographic filters
   - Export functionality for reports

4. __Alert System__:

   - Low inventory alerts
   - Sales anomaly detection
   - Order fulfillment status alerts
   - Payment processing alerts

This dashboard structure provides a comprehensive framework for Dog Days to monitor and optimize their retail dog food business operations, with a focus on sales performance, inventory management, customer analytics, and marketing effectiveness.
