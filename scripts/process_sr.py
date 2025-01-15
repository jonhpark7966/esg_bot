from scripts.prepare_sr import process_sr_report
from scripts.rag_eval_sr import process_question

from dotenv import load_dotenv

# Load .env file
load_dotenv()

SR_REPORT_PATH = "../data/reports/2024/삼성전자/"
SR_REPORT_IMAGE_PATH = SR_REPORT_PATH + "pages"
SR_REPORT_CORPUS_VECTOR_PATH = SR_REPORT_PATH 
PREPROCESS_MODEL = "o1"

process_sr_report(SR_REPORT_PATH+"sr.pdf",
                  SR_REPORT_IMAGE_PATH,
                  SR_REPORT_CORPUS_VECTOR_PATH, PREPROCESS_MODEL)



import pandas as pd
import os
import time

#q_df = pd.read_csv("./data/questions.csv")
#
#for i in range(len(q_df)):
#    print(f"Question {i} / {len(q_df)} processing...")
#
#    question = q_df.loc[i, "question"]
#    answer_choices = q_df.loc[i, "choices"]
#
#    # Q&A PROCESS
#    try:
#        answer, reranked_vector_df = process_question(SR_REPORT_CORPUS_VECTOR_PATH, SR_REPORT_IMAGE_PATH, question, answer_choices, grader_model="gpt-4o", answer_model="o1")
#    except Exception as e:
#        print(f"Exception occurred: {e}. Retrying after 5 minutes...")
#        time.sleep(300)
#        answer, reranked_vector_df = process_question(SR_REPORT_CORPUS_VECTOR_PATH, SR_REPORT_IMAGE_PATH, question, answer_choices, grader_model="gpt-4o", answer_model="o1")
#
#    q_df.loc[i, "grade"] = answer["grade"]
#    q_df.loc[i, "explanation"] = answer["explanation"]
#    q_df.loc[i, "retrieved_page_numbers"] = str(answer["retrieved_page_numbers"])
#
#    q_df.to_csv(SR_REPORT_PATH + "graded.csv", index=False)
#
#    r_log_path= SR_REPORT_PATH + f"retrieved_logs/{i}.csv"
#    os.makedirs(os.path.dirname(r_log_path), exist_ok=True)
#    reranked_vector_df.drop(columns=["vector", "text"]).to_csv(r_log_path, index=False)
#
#
#from esg_bot.grade_to_md import write_explanation
#
#MD_WRITER_MODEL = 'gpt-4o'
#
#q_df = pd.read_csv(SR_REPORT_PATH + "/graded.csv")
#
#for i in range(len(q_df)):
#    row = q_df.loc[i]
#    md_content = write_explanation(row, SR_REPORT_IMAGE_PATH, model = MD_WRITER_MODEL)
#    # save markdown file
#    os.makedirs(SR_REPORT_PATH + "explanations", exist_ok=True)
#    with open(SR_REPORT_PATH + f"explanations/{i}.md", "w") as f:
#        f.write(md_content)
