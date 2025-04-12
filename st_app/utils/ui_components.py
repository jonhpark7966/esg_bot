import streamlit as st

def display_evidence_selection(evidence_list):
    """
    Display the evidence selection interface
    
    Parameters:
    -----------
    evidence_list : list
        List of evidence dictionaries to display
    """
    st.markdown("### Review and Select Evidence")
    st.markdown("Select the most relevant information to include in the answer:")
    
    # Initialize checkboxes in session state if not already present
    if "evidence_checkboxes" not in st.session_state:
        st.session_state.evidence_checkboxes = [True] * len(evidence_list)
    
    for i, evidence in enumerate(evidence_list):
        with st.container():
            col1, col2 = st.columns([0.1, 0.9])
            
            with col1:
                st.checkbox(
                    label=f"Use",
                    value=st.session_state.evidence_checkboxes[i],
                    key=f"evidence_{i}",
                    on_change=update_checkbox,
                    args=(i,)
                )
            
            with col2:
                st.markdown(f"**Relevance Score:** {evidence['relevance']:.2f}")
                st.markdown(f"**Source:** {evidence['report_type']} - Page {evidence['page']} - {evidence['section']}")
                
                with st.expander("Preview Content"):
                    st.markdown(evidence['content'])
            
            st.markdown("---")

def update_checkbox(index):
    """Update the checkbox value in session state"""
    st.session_state.evidence_checkboxes[index] = st.session_state[f"evidence_{index}"]

def display_answer(answer, evidence):
    """
    Display the generated answer with citation information
    
    Parameters:
    -----------
    answer : str
        The generated answer text
    evidence : list
        List of evidence dictionaries used
    """
    st.markdown("### Answer")
    st.markdown(answer)
    
    with st.expander("View Sources"):
        for i, source in enumerate(evidence):
            st.markdown(f"**[{i+1}]** {source['report_type']} - Page {source['page']} - {source['section']}")
            st.markdown(source['content']) 