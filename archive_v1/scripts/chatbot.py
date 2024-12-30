import os

import pandas as pd
import streamlit as st
import base64
from PIL import Image
import io
from dotenv import load_dotenv
from langchain_core.tracers.context import collect_runs
from langsmith import Client
from streamlit_feedback import streamlit_feedback

from esg_bot.chain.rag_chain import ESGReportRAGChain
from esg_bot.data_handler.utils.image_base64_utils import ImageBase64Utils
from esg_bot.data_handler.utils.lc_callback_handler import RetrieveCallbackHandler

# Load the .env file
load_dotenv()

company_name = "현대차"
year = 2024
# Langsmith project change
os.environ["LANGCHAIN_PROJECT"] = "LogBlack Chatbot Tracing & Feedback"

client = Client()

# Set the page icon
st.set_page_config(
    page_title="Ask me about ESG Reports!",
    page_icon="🚀"
)

st.subheader("Ask me about ESG Reports!")

st.sidebar.info(
    """
LOGBLACK ESG Report Chatbot

links will be added. TBD.

"""
)

# TODO, make a database and get data from the database
def getYears(company):
    if company == "현대차":
        return [2024]
    elif company == "SK텔레콤":
        return [2023]
    else:
        return []

company_name = st.sidebar.selectbox(
    "Select a company",
    ["현대차", "SK텔레콤"]
)
year = st.sidebar.selectbox(
    "Select a year",
    getYears(company_name)
)

feedback_option = "faces"

with st.form("form"):
    text = st.text_area("Enter text:", "Ask me a question!")
    submitted = st.form_submit_button("Submit")
    if submitted:
        # get run_id from chain or lanchain run
        with collect_runs() as cb:
            rcb = RetrieveCallbackHandler()
            chain = ESGReportRAGChain(company_name=company_name, year=year)
            response = chain.invoke(text, callbacks=[rcb])

            st.info(response)
            docs = rcb.retrieved_docs

            for doc in docs:
                b64images = ImageBase64Utils.split_image_text_types([doc])["images"]
                image_data = base64.b64decode(b64images[0])
                img = Image.open(io.BytesIO(image_data))

                source = doc.metadata["source_url"]
                page_number = doc.metadata["page_num"]

                # wirte page nujmber and source, source is the url of the pdf file, show it in links
                st.write(f"Page: {page_number}, from [Source]({source})")
                st.image(img, use_column_width=True)

            st.session_state.run_id = cb.traced_runs[0].id

if st.session_state.get("run_id"):
    run_id = st.session_state.run_id
    feedback = streamlit_feedback(
        feedback_type=feedback_option,
        optional_text_label="[Optional] Please provide an explanation",
        key=f"feedback_{run_id}",
    )

    # Define score mappings for both "thumbs" and "faces" feedback systems
    score_mappings = {
        "thumbs": {"👍": 1, "👎": 0},
        "faces": {"😀": 1, "🙂": 0.75, "😐": 0.5, "🙁": 0.25, "😞": 0},
    }

    # Get the score mapping based on the selected feedback option
    scores = score_mappings[feedback_option]

    if feedback:
        # Get the score from the selected feedback option's score mapping
        score = scores.get(feedback["score"])

        if score is not None:
            # Formulate feedback type string incorporating the feedback option
            # and score value
            feedback_type_str = f"{feedback_option} {feedback['score']}"

            # Record the feedback with the formulated feedback type string
            # and optional comment
            feedback_record = client.create_feedback(
                run_id,
                feedback_type_str,
                score=score,
                comment=feedback.get("text"),
            )
            st.session_state.feedback = {
                "feedback_id": str(feedback_record.id),
                "score": score,
            }
        else:
            st.warning("Invalid feedback score.")