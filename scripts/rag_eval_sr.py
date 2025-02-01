from dotenv import load_dotenv
import pandas as pd

from esg_bot.retriever import HybridRetriever
from esg_bot.reranker import rerank
from esg_bot.grader import retrieval_relevance

from esg_bot.choice_answer import get_answer_rag
from esg_bot.utils import encode_image

from langsmith import traceable


@traceable(name="Process Question", project_name="[KCGS] Report Analysis")
def process_question(SR_REPORT_CORPUS_VECTOR_PATH, SR_REPORT_IMAGE_PATH, question, answer_choices,
                     relevance_score_threshold=0.5, max_relevant_pages=5, min_relevant_pages=3,
                     grader_model="gpt-4o", answer_model="o1"):
    df = pd.read_csv(SR_REPORT_CORPUS_VECTOR_PATH + "corpus_vector_sr.csv")
    df["vector"] = df["vector"].apply(lambda x: eval(x))
    h_retriever = HybridRetriever(df)

    vector_retreived_df = h_retriever.retrieve_df_vectors(question)
    bm25_retreived_df = h_retriever.retrieve_df_bm25(question)

    reranked_vector_df = rerank(question, pd.concat([bm25_retreived_df, vector_retreived_df]).drop_duplicates(['page_number']))

    reranked_vector_df[["explanation", "relevant"]] = reranked_vector_df["text"].apply(
        lambda x: pd.Series(retrieval_relevance(question, [x], grader_model))
    )

    # get pages with relevance score above threshold, also consider min/max relevant pages
    if reranked_vector_df[reranked_vector_df["relevant"] == True].shape[0] < min_relevant_pages:
        retrieved_pages = reranked_vector_df.head(min_relevant_pages)
    else:
        retrieved_pages = reranked_vector_df[reranked_vector_df["relevant"] == True]

    if retrieved_pages[retrieved_pages["rerank_relevance_score"] > relevance_score_threshold].shape[0] > max_relevant_pages:
        retrieved_pages = retrieved_pages[retrieved_pages["rerank_relevance_score"] > relevance_score_threshold].head(max_relevant_pages)
    elif retrieved_pages[retrieved_pages["rerank_relevance_score"] > relevance_score_threshold].shape[0] < min_relevant_pages:
        retrieved_pages = retrieved_pages.head(min_relevant_pages)
    else:
        retrieved_pages = retrieved_pages[retrieved_pages["rerank_relevance_score"] > relevance_score_threshold]

    page_numbers = retrieved_pages["page_number"].tolist()
    encoded_page_images = [encode_image(SR_REPORT_IMAGE_PATH + "/image_" + str(page_number) + ".jpg") for page_number in page_numbers]

    answer = get_answer_rag(question, answer_choices, encoded_page_images, model=answer_model)
    answer["retrieved_page_numbers"] = page_numbers
    return answer, reranked_vector_df

if __name__ == "__main__":
    # Load .env file
    load_dotenv()

    # Example test function
    SR_REPORT_CORPUS_VECTOR_PATH = "./data/reports/2024/현대차/"
    SR_REPORT_IMAGE_PATH = SR_REPORT_CORPUS_VECTOR_PATH + "./pages"

    question = """이사회 내에서 기후변화 및 탄소중립 안건을 보고하거나 결의하였는가?

 아래 항목들을 참고하여 답변하세요.

 (정의)
 기후변화 및 탄소중립 이슈: 온실가스 및 에너지 등 기후변화와 직접적 관련성이 높은 이슈

 (확인사항)
 이사회 개최 일시, 안건명, 결의 여부

 (시점)
 평가대상연도(FY)~평가실시연도(FY+1) 내의 안건 보고 및 결의사항만 반영 가능

 (불인정 사례)
 1. 안건명, 보고 및 결의사항 내 기후변화 및 탄소중립과 관련된 “실제 활동” 내역이 확인되지 않는 경우
 (ex. ESG 위원회 설치, ESG규정 제/개정, 지속가능경영보고서 발간 보고 등)
 2. 'ESG 중대성 평가 결과 보고의 건'은 반영 불가
"""

    answer_choices =  """
가. 아니오
나. 안건보고
다. 안건결의"""

    answer, reranked_vector_df = process_question(SR_REPORT_CORPUS_VECTOR_PATH, SR_REPORT_IMAGE_PATH, question, answer_choices)
    print("Answer:", answer)
