import streamlit as st
import os
from utils.file_handler import get_available_years, get_available_companies

st.set_page_config(
    page_title="ESG Report Analysis",
    page_icon="📊",
    layout="wide"
)

# Initialize session state
if 'selected_year' not in st.session_state:
    st.session_state['selected_year'] = None
if 'selected_company' not in st.session_state:
    st.session_state['selected_company'] = None

def main():
    st.title("ESG Report Analysis Dashboard")
    
    # Sidebar
    with st.sidebar:
        st.header("Settings")
        
        # Year selection
        years = get_available_years()
        selected_year = st.selectbox(
            "Select Year",
            options=years,
            key="year_selector"
        )
        
        # Company selection
        companies = get_available_companies(selected_year) if selected_year else []
        selected_company = st.selectbox(
            "Select Company",
            options=companies,
            key="company_selector"
        )
        
        # Update session state
        st.session_state['selected_year'] = selected_year
        st.session_state['selected_company'] = selected_company

    # Main area
    if not selected_year or not selected_company:
        st.info("Please select a year and company from the sidebar to begin.")
    else:
        st.write(f"Viewing reports for {selected_company} ({selected_year})")

if __name__ == "__main__":
    main() 