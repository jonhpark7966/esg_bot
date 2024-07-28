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
            components["page_images_summaries"], components["page_images_b64"], components['source_url'], components['page_num'],
            company_name, year
            )

        return True
    
    # 문서를 벡터 저장소와 문서 저장소에 추가하는 헬퍼 함수
    def add_documents(self, doc_summaries, doc_contents, source, page_nums, company_name, year):
        doc_ids = [
            str(uuid.uuid4()) for _ in doc_contents
        ]  # 문서 내용마다 고유 ID 생성
        summary_docs = [
            Document(page_content=s, metadata={
                 self.id_key: doc_ids[i],
                  "page_num":page_nums[i],
                  "source_url": source,
                  "company_name": company_name,
                  "year": str(year), # to string
                  })
            for i, s in enumerate(doc_summaries)
        ]
        self.retriever.vectorstore.add_documents(
            summary_docs
        )  # 요약 문서를 벡터 저장소에 추가

        docs = [
            Document(page_content=s, metadata={
                self.id_key: doc_ids[i],
                "page_num": page_nums[i],
                "source_url": source,
                "company_name": company_name,
                "year": str(year) # to string
                })
            for i, s in enumerate(doc_contents)
        ]

        #TODO: doc_contents 를 docs 로 묶어 넣었으니까 뒤에서 가져가는 파트도 수정이 되어야함.
        self.retriever.docstore.mset(
            list(zip(doc_ids,  docs))
        )  # 문서 내용을 문서 저장소에 추가
