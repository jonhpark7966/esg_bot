import streamlit as st
from pathlib import Path
from utils.file_handler import load_data
import pandas as pd

st.set_page_config(
    page_title="ESG Report Analysis - Explanations",
    page_icon="📚",
    layout="wide"
)

def main():
    # Sidebar - reuse the same selection logic as main app
    st.sidebar.title("ESG Report Analysis")
    
    data_dir = Path("data/reports")
    years = [d.name for d in data_dir.iterdir() if d.is_dir()]
    selected_year = st.sidebar.selectbox("Select Year", years)
    
    year_dir = data_dir / selected_year
    companies = [d.name for d in year_dir.iterdir() if d.is_dir()]
    selected_company = st.sidebar.selectbox("Select Company", companies)
    
    # Load data
    df = load_data(selected_year, selected_company)

    if df is not None:
        st.title("Detailed Explanations")
        
        # Search/Filter options
        search_term = st.text_input("Search questions or explanations")
        
        # Filter data based on search term
        if search_term:
            mask = (
                df['question'].str.contains(search_term, case=False, na=False) |
                df['explanation'].str.contains(search_term, case=False, na=False)
            )
            filtered_df = df[mask]
        else:
            filtered_df = df
            
        # Get unique categories and add "All" option
        categories = ["All"] + sorted(filtered_df['대분류'].unique().tolist())
        selected_category = st.tabs(categories)
        
        # Display filtered results based on selected tab
        for idx, category in enumerate(categories):
            with selected_category[idx]:
                if category == "All":
                    display_df = filtered_df
                else:
                    display_df = filtered_df[filtered_df['대분류'] == category]
                
                for _, row in display_df.iterrows():
                    with st.expander(f"Q{row['question_number']}: {row['question']}"):
                        st.markdown(f"**Category:** {row['대분류']} > {row['중분류']}")
                        st.markdown(f"**Grade:** {row['grade']}")
                        st.markdown("**Explanation:**")
                        st.markdown(row['rewrited_explanation_md'])
                        
                        if pd.notna(row['참고사항']):
                            st.markdown("**Additional Notes:**")
                            st.markdown(row['참고사항'])

if __name__ == "__main__":
    main() 