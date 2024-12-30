import os

import pandas as pd
from dotenv import load_dotenv

from esg_bot.chain.rag_chain import ESGReportRAGChain
from esg_bot.data_handler.utils.lc_callback_handler import RetrieveCallbackHandler

# Load the .env file
load_dotenv()

os.environ["LANGCHAIN_PROJECT"] = "LogBlack Evaluation Test"

company_name = "현대비앤지스틸"
year = 2024

cb = RetrieveCallbackHandler()
chain = ESGReportRAGChain(company_name=company_name, year=year)

evaluate_sample_df = pd.read_csv("./data/evaluate/2024_KCGS_Template.csv")
print(evaluate_sample_df.columns)

# Define a function to apply
def get_answer(x):
    answer = chain.invoke(x, callbacks=[cb])
    return answer


df_to_write = pd.DataFrame(columns=['항목번호', 'Query', 'Answer', 'Retreived Page Number'])

# loop rows
for index, row in evaluate_sample_df.iterrows():
    question_number = row['항목번호']
    query = row['항목명'] + "\n\n아래 항목들을 참고하여 답변하세요.\n" + row['정의 및 확인사항 + 참고사례 및 제출 시 유의사항']
    answer = chain.invoke(query, callbacks=[cb])
    page_nums = [doc.metadata['page_num'] for doc in cb.retrieved_docs]

    row_to_append = pd.DataFrame({
        '항목번호': question_number, 'Query': query, 'Answer': answer, 'Retreived Page Number': str(page_nums)}, index=[0])
    df_to_write = pd.concat([df_to_write,row_to_append], ignore_index=True)
    
df_to_write.to_csv(f"./data/evaluate/{company_name}_{year}.csv", index=False)

# Apply the function to the '평가항목' column and create a new column 'Answer'
#evaluate_sample_df["SKT RAG Answer - 2"] = evaluate_sample_df["평가항목"].apply(get_answer)
# Save the updated DataFrame to a new CSV file
#evaluate_sample_df.to_csv("./data/evaluate/evaluate_sample_with_answers.csv", index=False)

print("Answers added and CSV file saved.")
