import streamlit as st
from esg_bot.grader import retrieval_relevance
from esg_bot.reranker import rerank
from esg_bot.retriever import HybridRetriever
from st_app.utils.retrieval import vector_search, keyword_search, format_results
from st_app.utils.generation import generate_answer
from st_app.utils.ui_components import display_evidence_selection, display_answer
from pathlib import Path
import pandas as pd
import time
import os
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
    st.session_state.retrieved_evidence = {"semantic_results": [], "keyword_results": [], "reranked_results": []}
    
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

if "retrieval_status" not in st.session_state:
    st.session_state.retrieval_status = None
    
if "corpus_df" not in st.session_state:
    st.session_state.corpus_df = None
    
if "retrieval_substage" not in st.session_state:
    st.session_state.retrieval_substage = None

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
        st.session_state.retrieval_substage = "loading"
        st.session_state.question_input = ""  # Clear input

# Function to handle evidence selection
def handle_evidence_submit():
    selected_indices = [i for i, selected in enumerate(st.session_state.evidence_checkboxes) if selected]
    st.session_state.selected_evidence = [st.session_state.retrieved_evidence["reranked_results"][i] for i in selected_indices]
    st.session_state.processing_stage = "generating"

# Function to handle chat reset
def reset_chat():
    st.session_state.chat_history = []
    st.session_state.current_question = None
    st.session_state.retrieved_evidence = {"semantic_results": [], "keyword_results": [], "reranked_results": []}
    st.session_state.selected_evidence = []
    st.session_state.current_answer = None
    st.session_state.processing_stage = None
    st.session_state.retrieval_status = None
    st.session_state.corpus_df = None
    st.session_state.retrieval_substage = None

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
                st.markdown(f"**Source {i+1}:** Page {source.get('page', 'N/A')}")
                # Get image path for the page
                image_path = f"data/reports/{st.session_state.selected_year}/{st.session_state.selected_company}/pages/image_{source.get('page')}.jpg"
                if os.path.exists(image_path):
                    st.image(image_path, caption=f"Page {source.get('page')}")
                else:
                    st.markdown(source.get('content', ''))
        st.markdown("---")

# Process current question based on substage
if st.session_state.processing_stage == "retrieving":
    # Display question
    st.markdown(f"**You asked:** {st.session_state.current_question}")
    
    # Main retrieval card container
    retrieval_container = st.container()
    
    with retrieval_container:
        if st.session_state.retrieval_substage == "loading":
            # Step 1: Load corpus data
            with st.status("Loading corpus data...", state="running"):
                # Load corpus vector data
                corpus_path = Path(f"data/reports/{st.session_state.selected_year}/{st.session_state.selected_company}/corpus_vector_sr.csv")
                
                if not corpus_path.exists():
                    st.error(f"Data not found for {st.session_state.selected_company} ({st.session_state.selected_year})")
                    st.session_state.processing_stage = None
                    st.rerun()
                
                # Load corpus data
                corpus_df = pd.read_csv(corpus_path)
                corpus_df["vector"] = corpus_df["vector"].apply(lambda x: eval(x))
                st.session_state.corpus_df = corpus_df
                h_retriever = HybridRetriever(corpus_df)
                st.session_state.h_retriever = h_retriever
                
                st.write(f"Loaded {len(corpus_df)} documents")
            
            # Move to next substage
            st.session_state.retrieval_substage = "semantic"
            st.rerun()
            
        elif st.session_state.retrieval_substage == "semantic":
            # Show loading status for previous stages
            st.success("✓ Corpus data loaded")
            
            # Step 2: Perform semantic search
            with st.status("Performing semantic search...", state="running"):
                # Run semantic search
                semantic_results = vector_search(st.session_state.current_question, st.session_state.h_retriever)
                formatted_semantic = format_results(semantic_results, "distance")
                st.session_state.retrieved_evidence["semantic_results"] = formatted_semantic
                
                # Display a sample of results
                st.write(f"Found {len(formatted_semantic)} relevant documents by semantic search")
                if formatted_semantic:
                    st.write("Top pages found:")
                    for i, result in enumerate(formatted_semantic[:3]):
                        st.write(f"- Page {result['page']} (Score: {result['relevance']:.2f})")
            
            # Move to next substage
            st.session_state.retrieval_substage = "keyword"
            st.rerun()
            
        elif st.session_state.retrieval_substage == "keyword":
            # Show loading status for previous stages
            st.success("✓ Corpus data loaded")
            st.success("✓ Semantic search completed")
            
            # Step 3: Perform keyword search
            with st.status("Performing keyword search...", state="running"):
                # Run keyword search
                keyword_results = keyword_search(st.session_state.current_question, st.session_state.h_retriever)
                formatted_keyword = format_results(keyword_results, "bm25_score")
                st.session_state.retrieved_evidence["keyword_results"] = formatted_keyword
                
                # Display a sample of results
                st.write(f"Found {len(formatted_keyword)} relevant documents by keyword search")
                if formatted_keyword:
                    st.write("Top pages found:")
                    for i, result in enumerate(formatted_keyword[:3]):
                        st.write(f"- Page {result['page']} (Score: {result['relevance']:.2f})")
            
            # Move to next substage
            st.session_state.retrieval_substage = "reranking"
            st.rerun()
            
        elif st.session_state.retrieval_substage == "reranking":
            # Show loading status for previous stages
            st.success("✓ Corpus data loaded")
            st.success("✓ Semantic search completed")
            st.success("✓ Keyword search completed")
            
            # Step 4: Rerank combined results
            with st.status("Reranking results...", state="running"):
                # Convert semantic and keyword results back to dataframes
                semantic_df = pd.DataFrame(st.session_state.retrieved_evidence["semantic_results"][:10])
                semantic_df = semantic_df.rename(columns={'relevance': 'relevance_score', 'content': 'text', 'id': 'page_number'})
                
                keyword_df = pd.DataFrame(st.session_state.retrieved_evidence["keyword_results"][:10]) 
                keyword_df = keyword_df.rename(columns={'relevance': 'relevance_score', 'content': 'text', 'id': 'page_number'})
                
                combined_results = pd.concat([semantic_df, keyword_df]).drop_duplicates(['page_number'])
                reranked_results = rerank(st.session_state.current_question, combined_results)
                
                # Display a sample of preliminary reranked results
                st.write(f"Reranked {len(reranked_results)} documents by relevance")
                
            # Move to next substage
            st.session_state.retrieval_substage = "relevance_check"
            st.session_state.reranked_results = reranked_results  # Store for next step
            st.rerun()
            
        elif st.session_state.retrieval_substage == "relevance_check":
            # Show loading status for previous stages
            st.success("✓ Corpus data loaded")
            st.success("✓ Semantic search completed")
            st.success("✓ Keyword search completed")
            st.success("✓ Results reranked")
            
            # Step 5: Check relevance of each document
            with st.status("Checking document relevance...", state="running") as status:
                # get pages with relevance score above threshold, also consider min/max relevant pages
                GRADER_MODEL = "gpt-4o"
                
                # Get the reranked results from previous stage
                reranked_results = st.session_state.reranked_results
                
                # Create progress bar
                total_docs = len(reranked_results)
                progress_text = st.empty()
                progress_bar = st.progress(0)
                
                # Initialize empty columns for explanation and relevant
                reranked_results["explanation"] = None
                reranked_results["relevant"] = None
                
                # Process each document individually and show progress
                for idx, row in reranked_results.iterrows():
                    progress_text.text(f"Evaluating document {idx+1} of {total_docs}...")
                    
                    # Check relevance for this document
                    explanation, relevant = retrieval_relevance(
                        st.session_state.current_question, 
                        [row["text"]], 
                        GRADER_MODEL
                    )
                    
                    # Store results
                    reranked_results.at[idx, "explanation"] = explanation
                    reranked_results.at[idx, "relevant"] = relevant
                    
                    # Update progress
                    progress_bar.progress((idx + 1) / total_docs)
                    
                    # Show current document's relevance
                    st.write(f"Document on page {row['page_number']}: {'Relevant' if relevant else 'Not relevant'}")
                
                # Apply filtering logic
                min_relevant_pages = 3
                max_relevant_pages = 5
                relevance_score_threshold = 0.5
                
                # Count relevant documents
                relevant_count = reranked_results[reranked_results["relevant"] == True].shape[0]
                st.write(f"Found {relevant_count} relevant documents")

                if relevant_count < min_relevant_pages:
                    retrieved_pages = reranked_results.head(min_relevant_pages)
                    st.write(f"Taking top {min_relevant_pages} documents as minimum requirement")
                else:
                    retrieved_pages = reranked_results[reranked_results["relevant"] == True]
                    st.write(f"Taking all {relevant_count} relevant documents")

                high_relevance_count = retrieved_pages[retrieved_pages["rerank_relevance_score"] > relevance_score_threshold].shape[0]
                
                if high_relevance_count > max_relevant_pages:
                    retrieved_pages = retrieved_pages[retrieved_pages["rerank_relevance_score"] > relevance_score_threshold].head(max_relevant_pages)
                    st.write(f"Limiting to top {max_relevant_pages} high-relevance documents")
                elif high_relevance_count < min_relevant_pages:
                    retrieved_pages = retrieved_pages.head(min_relevant_pages)
                    st.write(f"Taking top {min_relevant_pages} documents as minimum requirement")
                else:
                    retrieved_pages = retrieved_pages[retrieved_pages["rerank_relevance_score"] > relevance_score_threshold]
                    st.write(f"Taking all {high_relevance_count} high-relevance documents")

                page_numbers = retrieved_pages["page_number"].tolist()

                formatted_reranked = format_results(retrieved_pages, "rerank_relevance_score")
                st.session_state.retrieved_evidence["reranked_results"] = formatted_reranked
                
                # Display final selected results
                st.write(f"Final selection: {len(formatted_reranked)} documents")
                if formatted_reranked:
                    st.write("Selected pages:")
                    for i, result in enumerate(formatted_reranked[:3]):
                        st.write(f"- Page {result['page']} (Score: {result['relevance']:.2f})")
                
                status.update(label="Document relevance evaluation completed", state="complete")
            
            # Finish retrieval process
            st.success("✓ Retrieval process completed")
            st.session_state.processing_stage = "selecting"
            st.rerun()
    
elif st.session_state.processing_stage == "selecting":
    # Display question
    st.markdown(f"**You asked:** {st.session_state.current_question}")
    
    # Create a prominent approve button at the top
    st.button("✅ Approve Selected Evidence", type="primary", on_click=handle_evidence_submit, key="approve_button_top")
    
    # Create tabs for different search results, but put reranked first
    search_tabs = st.tabs(["Reranked Results", "Semantic Search", "Keyword Search"])
    
    # Display reranked results with checkboxes for selection (now in first tab)
    with search_tabs[0]:
        st.markdown("### Reranked Results")
        st.markdown("Select the most relevant evidence to generate an answer:")
        
        if st.session_state.retrieved_evidence["reranked_results"]:
            # Create checkboxes for evidence selection, default 5 checked
            if "evidence_checkboxes" not in st.session_state:
                num_results = len(st.session_state.retrieved_evidence["reranked_results"])
                st.session_state.evidence_checkboxes = [i < 5 for i in range(num_results)]
            
            for i, result in enumerate(st.session_state.retrieved_evidence["reranked_results"]):
                col1, col2 = st.columns([1, 10])
                with col1:
                    st.session_state.evidence_checkboxes[i] = st.checkbox(f"Select", key=f"evidence_{i}", 
                                                                        value=st.session_state.evidence_checkboxes[i])
                with col2:
                    st.markdown(f"Relevance: {result['relevance']:.2f}")
                    with st.expander(f"View content", expanded=True):
                        # Try to show the page image
                        img_path = Path(f"data/reports/{st.session_state.selected_year}/{st.session_state.selected_company}/pages/image_{result['page']}.jpg")
                        if img_path.exists():
                            st.image(str(img_path), caption=f"Page {result['page']}")
                        else:
                            # Fallback to text if image not found
                            st.markdown(result['content'])
                            st.info("Original page image not available.")
        else:
            st.info("No reranked results found.")
    
    # Display semantic search results (now in second tab)
    with search_tabs[1]:
        st.markdown("### Semantic Search Results")
        if st.session_state.retrieved_evidence["semantic_results"]:
            for i, result in enumerate(st.session_state.retrieved_evidence["semantic_results"]):
                st.markdown(f"**Page {result['page']}** - Relevance: {result['relevance']:.2f}")
                with st.expander(f"View content"):
                    st.markdown(result['content'])
        else:
            st.info("No semantic search results found.")
    
    # Display keyword search results (now in third tab)
    with search_tabs[2]:
        st.markdown("### Keyword Search Results")
        if st.session_state.retrieved_evidence["keyword_results"]:
            for i, result in enumerate(st.session_state.retrieved_evidence["keyword_results"]):
                st.markdown(f"**Page {result['page']}** - Relevance: {result['relevance']:.2f}")
                with st.expander(f"View content"):
                    st.markdown(result['content'])
        else:
            st.info("No keyword search results found.")
    
    # Add approval button at the bottom too for convenience
    st.button("✅ Approve Selected Evidence", type="primary", on_click=handle_evidence_submit, key="approve_button_bottom")
    
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
        st.session_state.retrieved_evidence = {"semantic_results": [], "keyword_results": [], "reranked_results": []}
        st.session_state.selected_evidence = []
        st.session_state.current_answer = None
        st.session_state.processing_stage = None
        st.session_state.retrieval_status = None
        st.session_state.corpus_df = None
        st.session_state.retrieval_substage = None
    
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