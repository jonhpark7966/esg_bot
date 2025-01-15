import streamlit as st
from utils.file_handler import get_source_pdf
import base64

st.set_page_config(page_title="Source", page_icon="📄")

def display_pdf(file_path):
    # Opening file from file path
    with open(file_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    
    # Embedding PDF in HTML
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="800" type="application/pdf"></iframe>'
    
    # Displaying File
    st.markdown(pdf_display, unsafe_allow_html=True)

def main():
    st.title("Source Document")
    
    if not st.session_state.get('selected_year') or not st.session_state.get('selected_company'):
        st.info("Please select a year and company from the sidebar on the main page.")
        return
    
    pdf_path = get_source_pdf(
        st.session_state['selected_year'],
        st.session_state['selected_company']
    )
    
    if not pdf_path:
        st.warning("No source PDF found for the selected company and year.")
        return
    
    display_pdf(pdf_path)

if __name__ == "__main__":
    main() 