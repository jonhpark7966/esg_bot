import os

import pandas as pd
from dotenv import load_dotenv

from esg_bot.chain.rag_chain import ESGReportRAGChain
from esg_bot.data_handler.utils.lc_callback_handler import RetrieveCallbackHandler

# Load the .env file
load_dotenv()

company_name = "현대차"
year = 2024

cb = RetrieveCallbackHandler()
chain = ESGReportRAGChain(company_name=company_name, year=year)

evaluate_sample_df = pd.read_csv("./data/evaluate/evaluate_sample.csv")


# Define a function to apply
def get_answer(x):
    answer = chain.invoke(x, callbacks=[cb])
    return answer


# Apply the function to the '평가항목' column and create a new column 'Answer'
evaluate_sample_df["SKT RAG Answer - 2"] = evaluate_sample_df["평가항목"].apply(get_answer)

# Save the updated DataFrame to a new CSV file
evaluate_sample_df.to_csv("./data/evaluate/evaluate_sample_with_answers.csv", index=False)

print("Answers added and CSV file saved.")
