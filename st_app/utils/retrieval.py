import streamlit as st
import pandas as pd
import time
import os
from pathlib import Path

from esg_bot.retriever import HybridRetriever
from esg_bot.reranker import rerank
from esg_bot.grader import retrieval_relevance

def format_results(results_df, score_type):
    """Convert DataFrame results to list of dictionaries for display"""
    formatted = []
    for _, row in results_df.iterrows():
        formatted.append({
            "id": int(row.get('page_number', 0)),
            "content": row.get('text', ''),
            "relevance": float(row.get(score_type, 0)),
            "page": int(row.get('page_number', 0)),
            "section": row.get('section', 'Unknown'),
            "report_type": row.get('report_type', 'SR')
        })
    return formatted

def vector_search(question, h_retriever):
    """
    Perform vector similarity search
    
    Parameters:
    -----------
    question : str
        The user's question
    corpus_df : DataFrame
        DataFrame containing document embeddings
    
    Returns:
    --------
    DataFrame
        DataFrame of relevant documents with scores
    """
   
    vector_retreived_df = h_retriever.retrieve_df_vectors(question)

    return vector_retreived_df 

def keyword_search(question, h_retriever):
    """
    Perform keyword-based search
    
    Parameters:
    -----------
    question : str
        The user's question
    corpus_df : DataFrame
        DataFrame containing document text
    
    Returns:
    --------
    DataFrame
        DataFrame of relevant documents with scores
    """
    bm25_retreived_df = h_retriever.retrieve_df_bm25(question)
    
    return bm25_retreived_df