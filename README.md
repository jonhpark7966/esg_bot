# ESG Report Analysis Application

## Overview

This Streamlit-based application provides an interactive interface for analyzing both Sustainability Reports (SR) and Annual Reports (AR) of companies. It allows users to ask questions about ESG (Environmental, Social, and Governance) and financial information through a chat interface and get answers based on the content of these reports.

## Features

### 1. Dual Report Source Analysis
- **Sustainability Reports (SR)**: Search and analyze pages from sustainability reports
- **Annual Reports (AR)**: Search and analyze sections from annual reports divided by topic

### 2. Interactive Chat Interface
- Ask natural language questions about company reports
- View transparent retrieval process with progress indicators
- Select which evidence sources to use for answer generation
- Review past conversations in chat history

### 3. Smart Document Retrieval
- **Semantic Search**: Finds content semantically similar to your question
- **Keyword Search**: Locates documents containing specific keywords from your question
- **Reranking**: Evaluates and prioritizes the most relevant content
- **Relevance Checking**: Filters out irrelevant information

## Data Structure
The application expects data to be organized as follows:
