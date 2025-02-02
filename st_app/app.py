import streamlit as st
from pathlib import Path
from utils.file_handler import load_data

# Set page config
st.set_page_config(
    page_title="ESG Report Analysis Dashboard",
    page_icon="📊",
    layout="wide"
)

def main():
    # Sidebar
    st.sidebar.title("ESG Report Analysis")
    
    # Get available years and companies
    data_dir = Path("data/reports")
    years = [d.name for d in data_dir.iterdir() if d.is_dir()]
    selected_year = st.sidebar.selectbox("Select Year", years)
    
    year_dir = data_dir / selected_year
    companies = [d.name for d in year_dir.iterdir() if d.is_dir()]
    selected_company = st.sidebar.selectbox("Select Company", companies)
    
    # Load data
    df = load_data(selected_year, selected_company)

    st.write("DASHBOARD (TBD)")
    

if __name__ == "__main__":
    main() 