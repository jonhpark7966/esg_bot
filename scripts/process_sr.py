from scripts.prepare_sr import process_sr_report
from scripts.rag_eval_sr import process_question

from dotenv import load_dotenv

import os

# CHECK the pwd. It should be the root directory of the project
# get path of last directory, check if it is the "egs_bot" directory
if os.path.basename(os.getcwd()) != "esg_bot":
    # print error and end
    print("Please run this script from the root directory of the project")
    exit()

# Load .env file
load_dotenv()

SR_REPORT_PATH = "./data/reports/2024/삼성바이오로직스/"
SR_REPORT_IMAGE_PATH = SR_REPORT_PATH + "pages"
SR_REPORT_CORPUS_VECTOR_PATH = SR_REPORT_PATH 
PREPROCESS_MODEL = "o1"

#process_sr_report(SR_REPORT_PATH+"sr.pdf",
#                  SR_REPORT_IMAGE_PATH,
#                  SR_REPORT_CORPUS_VECTOR_PATH, PREPROCESS_MODEL)



import pandas as pd
import os
import time

q_df = pd.read_csv("./data/questions_with_ref.csv")

if os.path.isfile(SR_REPORT_PATH + "graded.csv"):
    q_df = pd.read_csv(SR_REPORT_PATH + "graded.csv")


j = 0
for i in range(len(q_df)):


    if 'grade' in q_df.columns:
        if not pd.isna(q_df.loc[i, 'grade']):
            print(f"Question {i} / {len(q_df)} already processed")
            continue
    
    j = j + 1
    print(f"Question {i} / {len(q_df)} processing... {j} questions processed")

    # TODO, tmporal code for free token usage, change it to batch api call
    # when j got 90, sleep 24 hours 
    if j == 90:
        print("Sleeping for 24 hours...")
        time.sleep(24 * 60 * 60)  # 24 hours in seconds

    question = q_df.loc[i, "question"] + "\n\n 아래 사항들을 참고하여 답변하세요. \n\n" + str(q_df.loc[i, "참고사항"] or "")
    answer_choices = q_df.loc[i, "choices"]

    # Q&A PROCESS
    try:
        answer, reranked_vector_df = process_question(SR_REPORT_CORPUS_VECTOR_PATH, SR_REPORT_IMAGE_PATH, question, answer_choices, grader_model="gpt-4o", answer_model="o1")
    except Exception as e:
        print(f"Exception occurred: {e}. Retrying after 5 minutes...")
        time.sleep(300)
        answer, reranked_vector_df = process_question(SR_REPORT_CORPUS_VECTOR_PATH, SR_REPORT_IMAGE_PATH, question, answer_choices, grader_model="gpt-4o", answer_model="o1")

    q_df.loc[i, "grade"] = answer["grade"]
    q_df.loc[i, "explanation"] = answer["explanation"]
    q_df.loc[i, "retrieved_page_numbers"] = str(answer["retrieved_page_numbers"])

    q_df.to_csv(SR_REPORT_PATH + "graded.csv", index=False)

    r_log_path= SR_REPORT_PATH + f"retrieved_logs/{i}.csv"
    os.makedirs(os.path.dirname(r_log_path), exist_ok=True)
    reranked_vector_df.drop(columns=["vector", "text"]).to_csv(r_log_path, index=False)

from esg_bot.grade_to_md import write_explanation

MD_WRITER_MODEL = 'gpt-4o'

g_df = pd.read_csv(SR_REPORT_PATH + "/graded.csv")

for i in range(len(g_df)):
    print(f"Question {i} / {len(g_df)} Rewriting Explnations")
    row = g_df.loc[i]
    md_content = write_explanation(row, SR_REPORT_IMAGE_PATH, model = MD_WRITER_MODEL)

    g_df.loc[i, "rewrited_explanation_md"] = md_content
    g_df.to_csv(SR_REPORT_PATH + "graded.csv", index=False)