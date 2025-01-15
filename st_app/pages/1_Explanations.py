import streamlit as st
from utils.file_handler import get_explanations

st.set_page_config(page_title="Explanations", page_icon="📚")

def main():
    st.title("Q&A with Explanations")
    
    if not st.session_state.get('selected_year') or not st.session_state.get('selected_company'):
        st.info("Please select a year and company from the sidebar on the main page.")
        return
    
    questions, explanations = get_explanations(
        st.session_state['selected_year'],
        st.session_state['selected_company']
    )
    
    if not explanations:
        st.warning("No explanations found for the selected company and year.")
        return

    num = 1 
    for question, explanation in zip(questions, explanations):
        # Display explanation
        st.markdown(f"# Questions {num}  ")
        st.markdown(question)
        st.markdown(explanation)
        st.markdown("---")
        num += 1

if __name__ == "__main__":
    main() 