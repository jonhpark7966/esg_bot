from langchain.retrievers.multi_vector import MultiVectorRetriever
from langchain_core.documents import Document

import uuid

class RetrieverHandler():

    def __init__(self, vectorstore, docstore):
        self.id_key = "doc_id"

        self.retriever = MultiVectorRetriever(
            vectorstore=vectorstore,
            docstore=docstore,
            id_key=self.id_key,
        )


    def add(self, components, company_name, year):
        """
        add components to retreiver
        also, automatically addeding them to vectorstore, docsotre

        Returns:
        True on Success 
        """

        self.add_documents(
            components["page_images_summaries"], components["page_images_b64"], components['source_url'],
            company_name, year
            )

        return True
    
    # 문서를 벡터 저장소와 문서 저장소에 추가하는 헬퍼 함수
    def add_documents(self, doc_summaries, doc_contents, source, company_name, year):
        doc_ids = [
            str(uuid.uuid4()) for _ in doc_contents
        ]  # 문서 내용마다 고유 ID 생성
        summary_docs = [
            Document(page_content=s, metadata={
                 self.id_key: doc_ids[i],
                  "source_url": source,
                  "company_name": company_name,
                  "year": year
                  })
            for i, s in enumerate(doc_summaries)
        ]
        self.retriever.vectorstore.add_documents(
            summary_docs
        )  # 요약 문서를 벡터 저장소에 추가
        self.retriever.docstore.mset(
            list(zip(doc_ids, doc_contents))
        )  # 문서 내용을 문서 저장소에 추가
