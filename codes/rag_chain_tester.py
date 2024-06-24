from chain.rag_chain import ESGReportRAGChain

from dotenv import load_dotenv
import pandas as pd
import os

# Load the .env file
load_dotenv()

file_list_df = pd.read_csv("./data/reports.csv")
target = "SK텔레콤"##"LG에너지솔루션"
row = file_list_df[file_list_df.company_name == target].iloc[0]
company_name = row["company_name"]
year = row["year"]
url = f"{os.getenv('logblack_url')}{company_name}_{year}.pdf"


chain = ESGReportRAGChain(company_name=company_name, year=year)

evaluate_sample_df = pd.read_csv("./data/evaluate/evaluate_sample.csv")

# Define a function to apply
def get_answer(x):
    answer = chain.invoke(x)
    return answer

# Apply the function to the '평가항목' column and create a new column 'Answer'
evaluate_sample_df['SKT RAG Answer'] = evaluate_sample_df['평가항목'].apply(get_answer)

# Save the updated DataFrame to a new CSV file
evaluate_sample_df.to_csv("./data/evaluate/evaluate_sample_with_answers.csv", index=False)

print("Answers added and CSV file saved.")