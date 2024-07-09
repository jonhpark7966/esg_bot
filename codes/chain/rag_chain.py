# Configuring
from langchain_openai import ChatOpenAI
from data_handler.utils.paths import build_store_path
from data_handler.utils.image_base64_utils import ImageBase64Utils
from data_handler.lc_docstore_handler.in_memory_docstore_handler import InMemoryDocstoreHandler
from data_handler.lc_retrieverHandler.retriever_handler import RetrieverHandler
from data_handler.lc_vectorstore_handler.pinecone_vectorstore_handler import PineconeVectorstoreHandler

from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage

from dotenv import load_dotenv
import pandas as pd
import os

# Load the .env file
load_dotenv()

file_list_df = pd.read_csv("./data/reports.csv")
target = "LG에너지솔루션"#SK텔레콤"
row = file_list_df[file_list_df.company_name == target].iloc[0]
company_name = row["company_name"]
year = row["year"]
url = f"{os.getenv('logblack_url')}{company_name}_{year}.pdf"


class RAGChain():
    def __init__(self):
        if False: #TODO, config LangSmith
            os.environ["LANGCHAIN_PROJECT"] = "LangSmithTracing"

    def invoke(self, query):
        return self.chain.invoke(query)


class ESGReportRAGChain(RAGChain):
    def __init__(self, company_name, year):
        self.vectorstore_handler = PineconeVectorstoreHandler(
            company_name=company_name, year=year, embeddingModel='text-embedding-3-large', postfix='kr'
            ).getStore()
        self.docstore_handler = InMemoryDocstoreHandler()
        self.docstore_handler.load_from_file(build_store_path(company_name,year))
        self.lc_docstore = self.docstore_handler.getStore()
        self.lc_retriever = RetrieverHandler(self.vectorstore_handler, self.lc_docstore)

        # 멀티모달 LLM
        model = ChatOpenAI(temperature=0, model="gpt-4o", max_tokens=2048)

        # RAG 파이프라인
        self.chain = (
            {
                "context": self.lc_retriever.retriever | RunnableLambda(ImageBase64Utils.split_image_text_types),
                "question": RunnablePassthrough(),
            }
            | RunnableLambda(self.img_prompt_func)
            | model
            | StrOutputParser()
        )

    def img_prompt_func(self, data_dict):
        """
        컨텍스트를 단일 문자열로 결합
        """
        formatted_texts = "\n".join(data_dict["context"]["texts"])
        messages = []
    
        # 이미지가 있으면 메시지에 추가
        if data_dict["context"]["images"]:
            for image in data_dict["context"]["images"]:
                image_message = {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{image}"},
                }
                messages.append(image_message)
    
        # 분석을 위한 텍스트 추가
        text_message = {
            "type": "text",
            "text": (
                "You are finantial and ESG report analysist tasking with providing investment advice.\n"
                "You will be given a image(s) which is some pages of company's ESG Report.\n"
                "Use this information to asnwer the following question.\n"
                "Answer 예 or 아니오 first, and explain the reason based on the provided pages of ESG report."
                "If possible, find the page number on the image and inform the page numbers for users to find the evidence easily."
                "Answer in Korean. Do NOT translate company names.\n"
                f"User-provided question: {data_dict['question']}\n\n"
            ),
        }
        messages.append(text_message)
        return [HumanMessage(content=messages)]

#ret = chain_multimodal_rag.invoke("이사회 내에서 기후변화 및 탄소중립 안건을 보고하거나 결의하였는가?")