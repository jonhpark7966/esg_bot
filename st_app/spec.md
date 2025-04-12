# ESG Report Analysis Dashboard — Specification

## Overview
A Streamlit application that provides:
1. A sidebar for selecting year and company name.
2. A navigation menu for pages: “Dashboard”, “Explanations”, “Chat”, and “Source”.
3. “Dashboard” and “Chat” sections are placeholders for future expansion.
4. “Explanations” displays markdown-based Q&A content with scrollable text.
5. “Source” displays the original PDF report.

---

.
├── data
│   └── 2024
│       └── COMPANYNAME
│           ├── ar
│           │   ├── corpus_vector.csv
│           │   ├── I. 회사의 개요.md
│           │   ├── II. 사업의 내용.md 
│           │   ├── III. 재무에 관한 사항.md
│           │   └── IV. 이사의 경영진단.md
│           ├── corpus_vector_sr.csv
│           ├── graded.csv
│           └── pages
│               ├── image_1.jpg
│               ├── image_2.jpg
│               …
├── st_app
│   ├── pages
│   │   ├── explanations.py
│   │   └── chat.py (TBD)
│   ├── utils
│   │   └── file_handler.py
│   └── app.py

---

### CSV Schema

`graded.csv` has the following columns (headers):
1. **question_number**
2. **question**
3. **choices**
4. **category**
5. **대분류**
6. **중분류**
7. **참고사항** (optional)
8. **grade**
9. **explanation**
10. **retrieved_page_numbers**
11. **rewrited_explanation_md**

---

## Streamlit UI Requirements

1. **Sidebar (Year & Company Selection)**
   - A dropdown (or selectbox) to choose the Year (e.g., 2024).
   - A dropdown (or selectbox) to choose the Company (e.g., COMPANYNAME).
   - After user selection, the app reads `./data/{year}/{company}/graded.csv`.

2. **Tabs by "대분류"**
   - For each unique value in the `대분류` column, create a separate Tab in Streamlit.
   - Inside each Tab, provide a way to filter by `중분류`.

3. **Filtering by "중분류"**
   - Within each Tab, show a filter (dropdown or multiselect) for the unique `중분류` values that belong to the current `대분류`.
   - Default behavior might be "Show All" if no filter is selected.

4. **Display in a Scrollable List**
   - For each question row that matches the current tab’s `대분류` and the chosen `중분류` filter, display:
     - **question**
     - **grade**
     - **rewrited_explanation_md** (Markdown)

5. **Popover or Popup with Additional Details**
   - For each row, provide a small button (e.g., "Details").
   - Clicking it should open a Popover or Popup with:
     - **explanation**
     - **retrieved_page_numbers**
   - Optionally, show references or associated images from `pages/` folder if needed.

6. **Data Refresh or Reactive Behavior**
   - The app updates the displayed data automatically whenever the year, company, 대분류 tab, or 중분류 filter changes.

---

## Notes / Optional Enhancements

- Display images from `./data/{year}/{company}/pages/` based on `retrieved_page_numbers` if desired.
- Use Markdown rendering for `rewrited_explanation_md` content to preserve formatting.

---

## High-Level Outline

1. **Initialize**: 
   - Import Streamlit, pandas, etc.
   - Build the sidebar for Year & Company selection.
2. **Load CSV** (when selections change).
3. **Create Tabs** for each `대분류`.
4. **Inside Each Tab**:
   - Create a filter for `중분류`.
   - Show the filtered rows in a scrollable container.
   - Display question, grade, and rewrited_explanation_md.
   - Provide a "Details" button that opens a Popover/Popup with explanation and retrieved_page_numbers.
5. **Handle Images** (optional) if `retrieved_page_numbers` references images in the `pages/` folder.

---

## Example Workflow

1. User selects **2024** in the sidebar.
2. User selects **COMPANYNAME** in the sidebar.
3. App loads `./data/2024/COMPANYNAME/graded.csv`.
4. App creates Tabs for each unique `대분류` (e.g., "리더십과 거버넌스", etc.).
5. In "리더십과 거버넌스" tab, a filter by `중분류` (e.g., "거버넌스").
6. List the questions, each showing:
   - Question text
   - Grade
   - Rewritten explanation (Markdown)
   - A details button → opens popup with `explanation` + `retrieved_page_numbers`.
7. User can navigate to other tabs or choose a new company in the sidebar.

---

## End of Spec