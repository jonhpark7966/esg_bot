import streamlit as st
from st_app.utils.retrieval import retrieve_evidence
from st_app.utils.generation import generate_answer
from st_app.utils.ui_components import display_evidence_selection, display_answer
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="ESG Report Analysis - Chat",
    page_icon="💬",
    layout="wide"
)

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
    
if "current_question" not in st.session_state:
    st.session_state.current_question = None
    
if "retrieved_evidence" not in st.session_state:
    st.session_state.retrieved_evidence = []
    
if "selected_evidence" not in st.session_state:
    st.session_state.selected_evidence = []
    
if "current_answer" not in st.session_state:
    st.session_state.current_answer = None

if "processing_stage" not in st.session_state:
    st.session_state.processing_stage = None
    
if "selected_year" not in st.session_state:
    st.session_state.selected_year = None
    
if "selected_company" not in st.session_state:
    st.session_state.selected_company = None

# Sidebar for company and year selection
st.sidebar.title("ESG Report Analysis")

data_dir = Path("data/reports")
years = [d.name for d in data_dir.iterdir() if d.is_dir()]
selected_year = st.sidebar.selectbox("Select Year", years, key="year_select")

if selected_year:
    st.session_state.selected_year = selected_year
    year_dir = data_dir / selected_year
    companies = [d.name for d in year_dir.iterdir() if d.is_dir()]
    selected_company = st.sidebar.selectbox("Select Company", companies, key="company_select")
    
    if selected_company:
        st.session_state.selected_company = selected_company

# Function to handle question submission
def handle_question_submit():
    question = st.session_state.question_input
    if question:
        st.session_state.current_question = question
        st.session_state.processing_stage = "retrieving"
        st.session_state.question_input = ""  # Clear input

# Function to handle evidence selection
def handle_evidence_submit():
    selected_indices = [i for i, selected in enumerate(st.session_state.evidence_checkboxes) if selected]
    st.session_state.selected_evidence = [st.session_state.retrieved_evidence[i] for i in selected_indices]
    st.session_state.processing_stage = "generating"

# Function to handle chat reset
def reset_chat():
    st.session_state.chat_history = []
    st.session_state.current_question = None
    st.session_state.retrieved_evidence = []
    st.session_state.selected_evidence = []
    st.session_state.current_answer = None
    st.session_state.processing_stage = None

# App title and header
st.title("Chat Interface")
st.markdown("Ask questions about sustainability reports and annual reports.")

# Display selected company and year
if st.session_state.selected_year and st.session_state.selected_company:
    st.markdown(f"**Selected: {st.session_state.selected_company} ({st.session_state.selected_year})**")

# Chat container for history
chat_container = st.container()

# Display chat history
with chat_container:
    for exchange in st.session_state.chat_history:
        question = exchange.get("question", "")
        answer = exchange.get("answer", "")
        evidence = exchange.get("evidence", [])
        
        # Display the question
        st.markdown(f"**You:** {question}")
        
        # Display the answer with citations
        st.markdown(f"**AI Assistant:**")
        st.markdown(answer)
        
        # Option to display evidence used
        with st.expander("View sources used"):
            for i, source in enumerate(evidence):
                st.markdown(f"**Source {i+1}:** Page {source.get('page', 'N/A')} - {source.get('section', 'N/A')}")
                st.markdown(source.get('content', ''))
        
        st.markdown("---")

# Process current question if there is one
if st.session_state.processing_stage == "retrieving":
    with st.spinner("Retrieving relevant information..."):
        # Retrieve evidence, passing the selected year and company
        st.session_state.retrieved_evidence = retrieve_evidence(
            st.session_state.current_question,
            year=st.session_state.selected_year,
            company=st.session_state.selected_company
        )
        st.session_state.processing_stage = "selecting"
    st.rerun()
    
elif st.session_state.processing_stage == "selecting":
    # Display evidence selection interface
    st.markdown(f"**You asked:** {st.session_state.current_question}")
    display_evidence_selection(st.session_state.retrieved_evidence)
    
    # Generate answer button
    st.button("Generate Answer", on_click=handle_evidence_submit)
    
elif st.session_state.processing_stage == "generating":
    with st.spinner("Generating answer..."):
        # Generate answer based on selected evidence
        st.session_state.current_answer = generate_answer(
            st.session_state.current_question,
            st.session_state.selected_evidence
        )
        
        # Add to chat history
        st.session_state.chat_history.append({
            "question": st.session_state.current_question,
            "answer": st.session_state.current_answer,
            "evidence": st.session_state.selected_evidence
        })
        
        # Reset for next question
        st.session_state.current_question = None
        st.session_state.retrieved_evidence = []
        st.session_state.selected_evidence = []
        st.session_state.current_answer = None
        st.session_state.processing_stage = None
    
    st.rerun()

# Question input - only show if company and year are selected
if st.session_state.selected_year and st.session_state.selected_company:
    st.text_input(
        "Ask a question about sustainability or annual reports",
        key="question_input",
        on_change=handle_question_submit
    )
    
    # Reset chat button
    st.button("Reset Chat", on_click=reset_chat)
else:
    st.warning("Please select a year and company from the sidebar to start chatting.") 