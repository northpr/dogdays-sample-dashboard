import os
import sys
import pandas as pd

def test_data_loading():
    """Test if the data files can be loaded correctly"""
    print("Testing data loading...")
    
    # Test if data directory exists
    if not os.path.exists('data'):
        print("ERROR: data directory not found")
        return False
    
    # Test if sales data file exists
    sales_file = os.path.join('data', 'dog_days_sales_data.xlsx')
    if not os.path.exists(sales_file):
        print(f"ERROR: Sales data file not found at {sales_file}")
        return False
    
    # Test if logo file exists
    logo_file = os.path.join('data', 'logo_dogdays.png')
    if not os.path.exists(logo_file):
        print(f"WARNING: Logo file not found at {logo_file}")
    
    # Try to load the sales data
    try:
        df = pd.read_excel(sales_file)
        print(f"SUCCESS: Sales data loaded successfully with {len(df)} rows")
    except Exception as e:
        print(f"ERROR: Failed to load sales data: {e}")
        return False
    
    return True

def test_imports():
    """Test if all required modules can be imported"""
    print("Testing imports...")
    
    try:
        import streamlit
        import plotly.express
        import plotly.graph_objects
        import numpy
        print("SUCCESS: All required modules imported successfully")
        return True
    except ImportError as e:
        print(f"ERROR: Failed to import required modules: {e}")
        return False

if __name__ == "__main__":
    print("Running pre-deployment tests...")
    
    data_test = test_data_loading()
    import_test = test_imports()
    
    if data_test and import_test:
        print("\nAll tests passed! The app is ready for deployment.")
    else:
        print("\nSome tests failed. Please fix the issues before deployment.")
