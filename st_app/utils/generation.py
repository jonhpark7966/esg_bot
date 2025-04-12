import streamlit as st
import time
import base64
import os
from pathlib import Path

from esg_bot.choice_answer import get_answer_rag, get_streaming_answer

def encode_image(image_path):
    """
    Encode an image file as base64
    
    Parameters:
    -----------
    image_path : str
        Path to the image file
    
    Returns:
    --------
    str
        Base64 encoded image
    """
    if not os.path.exists(image_path):
        return None
        
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def generate_answer(question, evidence):
    """
    Generate an answer based on the question and selected evidence with streaming output
    
    Parameters:
    -----------
    question : str
        The user's question
    evidence : list
        List of evidence dictionaries selected by the user
    
    Returns:
    --------
    str
        The complete generated answer text
    """
    # Extract page numbers from evidence
    page_numbers = [item.get('page') for item in evidence if 'page' in item]
    
    # Prepare image paths based on selected company and year
    selected_year = st.session_state.selected_year
    selected_company = st.session_state.selected_company
    
    # Construct image paths and encode them
    image_paths = []
    for page in page_numbers:
        image_path = f"data/reports/{selected_year}/{selected_company}/pages/image_{page}.jpg"
        image_paths.append(image_path)
    
    # Encode images as base64
    retrieved_pages_encoded = [encode_image(path) for path in image_paths]
    
    # Filter out None values (images that couldn't be encoded)
    retrieved_pages_encoded = [img for img in retrieved_pages_encoded if img is not None]
    
    # Create a placeholder for streaming output
    answer_container = st.empty()
    full_response = ""
    
    # Generate streaming response
    for chunk in get_streaming_answer(question, retrieved_pages_encoded, model="gpt-4o"):
        if hasattr(chunk, 'content'):
            content = chunk.content
            full_response += content
            # Update the container with the accumulated response
            answer_container.markdown(full_response)
    
    return full_response

def generate_explanation(question, evidence, answer):
    """
    Generate a detailed explanation connecting evidence to the answer
    
    Parameters:
    -----------
    question : str
        The user's question
    evidence : list
        List of evidence dictionaries used
    answer : str
        The generated answer
    
    Returns:
    --------
    str
        Detailed explanation in markdown format
    """
    # To be implemented with a more sophisticated explanation generation
    pass 