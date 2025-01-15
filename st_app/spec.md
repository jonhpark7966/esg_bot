# ESG Report Analysis Dashboard — Specification

## Overview
A Streamlit application that provides:
1. A sidebar for selecting year and company name.
2. A navigation menu for pages: “Dashboard”, “Explanations”, “Chat”, and “Source”.
3. “Dashboard” and “Chat” sections are placeholders for future expansion.
4. “Explanations” displays markdown-based Q&A content with scrollable text.
5. “Source” displays the original PDF report.

---

## Sidebar
1. **Dropdowns**  
   - **Year Selection**: Displays available reporting years.  
   - **Company Selection**: Displays available company names.

2. **Page Navigation**  
   - **Dashboard** (TBD)  
   - **Explanations**: Displays a scrollable list of question-response markdown files.  
   - **Chat** (TBD)  
   - **Source**: Renders the original ESG report PDF.

---

## Explanations Page
- Loads multiple markdown files, each containing:
  - A question or prompt.
  - A detailed explanation or answer.
- Users can scroll through all Q&A markdown content.

---

## Source Page
- Shows the original ESG PDF report:
  - Embedded PDF viewer or link to open externally.

---

## Implementation Notes
- Use Streamlit’s `sidebar.selectbox` for dropdowns.
- Use Streamlit’s built-in multipage or custom navigation logic.
- For Q&A, store markdown files in a “content” folder. Load them dynamically.
- For PDF display, use `st.file_uploader` or a Streamlit-compatible PDF viewer package.

---

## Future Extensions
- **Dashboard**: Add analytics, charts, or summary visualizations of the ESG data.
- **Chat**: Integrate an LLM-based Q&A chat using the loaded ESG data.
