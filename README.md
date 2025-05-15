# Dog Days Dashboard

A comprehensive dashboard for Dog Days, a retail dog food company, built with Streamlit. This dashboard provides insights into sales, products, inventory, customers, and marketing performance.

## Project Structure

```
dog-days/
├── data/
│   └── ตัวอย่างรายการขาย Online 05-67.xlsx  # Sample sales data
├── src/
│   ├── app.py                              # Main application file
│   └── dashboards/
│       ├── __init__.py                     # Package initialization
│       ├── sales_dashboard.py              # Sales overview dashboard
│       ├── product_dashboard.py            # Product performance dashboard
│       ├── inventory_dashboard.py          # Inventory management dashboard
│       ├── customer_dashboard.py           # Customer analytics dashboard
│       └── marketing_dashboard.py          # Marketing performance dashboard
├── requirements.txt                        # Project dependencies
├── README.md                               # Project documentation
└── dog_days_dashboard_structure.md         # Dashboard structure documentation
```

## Features

- **Sales Overview Dashboard**: Monitor daily/monthly/yearly sales, average order value, sales by channel, and regional sales distribution.
- **Product Performance Dashboard**: Analyze product sales, price points, discount impact, and category performance.
- **Inventory Management Dashboard**: Track inventory levels, stock alerts, inventory value, and warehouse distribution.
- **Customer Analytics Dashboard**: Segment customers, analyze repeat purchase patterns, geographic distribution, and customer lifetime value.
- **Marketing Performance Dashboard**: Evaluate campaign performance, channel effectiveness, discount impact, and seasonal trends.

## Setup Instructions

1. **Clone the repository**:
   ```
   git clone <repository-url>
   cd dogdays-internal-dashboard
   ```

2. **Create a virtual environment** (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```
   pip install -r requirements.txt
   ```

4. **Run the application locally**:
   ```
   streamlit run src/app.py
   ```

5. **Access the dashboard**:
   Open your web browser and navigate to `http://localhost:8501`

## Deployment Instructions

### GitHub Deployment

1. **Create a new GitHub repository**:
   - Go to GitHub and create a new repository
   - Initialize it with a README if you haven't already created one

2. **Push your code to GitHub**:
   ```
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/yourusername/dogdays-internal-dashboard.git
   git push -u origin main
   ```

### Streamlit Cloud Deployment

1. **Sign up for Streamlit Cloud**:
   - Go to [Streamlit Cloud](https://streamlit.io/cloud) and sign up or log in
   - Connect your GitHub account if you haven't already

2. **Deploy your app**:
   - Click "New app"
   - Select your repository, branch (main), and the main file path (`src/app.py`)
   - Click "Deploy"

3. **Configure your app** (optional):
   - Set up secrets if needed
   - Adjust advanced settings like Python version or package dependencies

4. **Access your deployed app**:
   - Once deployed, Streamlit Cloud will provide a URL to access your dashboard
   - Share this URL with your team or stakeholders

## Data Sources

The dashboard currently uses sample sales data from the `data/` directory. In a production environment, this would be connected to:

- Sales database
- Inventory management system
- Customer relationship management (CRM) system
- Marketing campaign management platform

## Customization

To customize the dashboard for your specific needs:

1. Update the data sources in `src/app.py`
2. Modify the dashboard modules in the `src/dashboards/` directory
3. Adjust the styling by editing the CSS in `src/app.py`

## Dependencies

- Streamlit: Web application framework
- Pandas: Data manipulation and analysis
- Plotly: Interactive visualizations
- NumPy: Numerical computing
- scikit-learn: Machine learning for customer segmentation
- openpyxl: Excel file handling

## License

[Specify your license here]

## Contact

[Your contact information]
