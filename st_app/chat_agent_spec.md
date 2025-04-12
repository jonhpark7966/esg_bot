# Chat Agent Specification

## Overview
The Chat Agent provides an interactive interface for users to ask questions about sustainability reports (SR) and annual reports (AR). It follows a transparent retrieval-augmented generation process where users can review and select the evidence sources before receiving answers.

## User Interface Components

### 1. Chat Interface
- Input box for user questions
- Chat history display showing previous exchanges 
- Loading indicators during processing steps

### 2. Evidence Selection Interface
- Display of retrieved document sections with relevance scores
- Checkboxes for selecting which sources to use
- Preview capability for source content

### 3. Answer Display
- Generated answer with citations
- Option to regenerate with different sources
- Option to ask follow-up questions

## Process Flow

### 1. Question Input
- User enters a question about ESG or financial information
- System begins retrieval process

### 2. Evidence Retrieval Process
The system performs a multi-step retrieval process:

#### Vector Search
- Convert question to vector representation
- Find semantically similar passages in the document corpus

#### Keyword Search
- Extract keywords from the question
- Find passages containing these keywords

#### Hybrid Search
- Combine results from vector and keyword searches
- Apply weighting to balance precision and recall

#### Reranking
- Apply a more sophisticated model to rerank top retrieved passages
- Calculate final relevance scores

### 3. Evidence Review
Display top 5 retrieved passages/sections by default. For each passage, show:
- Page number or section reference
- Relevance score
- Content preview
- Checkbox for selection

Additional features:
- Allow users to adjust selection (add/remove sources)
- Provide a "Generate Answer" button to proceed

### 4. Answer Generation
- Use selected evidence to generate a comprehensive answer
- Format answer with proper citations to source material
- Include relevant quotes where appropriate

### 5. Explanation Generation
- Generate detailed explanations connecting evidence to answer
- Format explanations in markdown for readability
- Include visual elements (charts, tables) when relevant

## Technical Implementation

### Data Sources
- Initially: Sustainability Reports (SR)
- Planned expansion: Annual Reports (AR)
- Document structure awareness (sections, subsections)

### Search Methods
- Vector embeddings using state-of-the-art models
- Keyword extraction with domain-specific enhancements
- Custom reranking algorithm for ESG content

### Answer Generation
- Context-aware LLM integration
- Citation mechanism for traceability
- Follow-up question handling

### UI Interactions
1. User submits question
2. System shows progress through each retrieval step
3. System displays retrieved evidence for selection
4. User selects preferred evidence sources
5. System generates and displays answer
6. User can request additional explanations or ask follow-ups

## Future Enhancements
- Integration of Annual Reports as additional context source
- Cross-referencing between SR and AR content
- User preference saving for evidence selection criteria
- Multi-lingual support for international reports
- Visualization of information relationships