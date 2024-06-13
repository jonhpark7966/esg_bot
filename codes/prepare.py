# Configuring
from codes.data_handler.lc_docstore_handler.in_memory_docstore_handler import InMemoryDocstoreHandler
from codes.data_handler.lc_retrieverHandler.retriever_handler import RetrieverHandler
from codes.data_handler.report_handler.pdf_image_report_handler import PdfImageReportHandler
from codes.data_handler.summary_handler.gpt_summary_handler import GPTSummaryHandler
from codes.data_handler.lc_vectorstore_handler.pinecone_vectorstore_handler import PineconeVectorstoreHandler

company = "SKT"
year = 2023
report_url = "...."

report_data_dir = "../data/reports/"
report_name = "report.pdf"

components = PdfImageReportHandler(
    company_name=company, year=year, report_url=report_url
    ).splitFile(report_data_dir, report_name)
summarized_components = GPTSummaryHandler().summary(components)


# USE LangChain from here.
vectorstore_handler = PineconeVectorstoreHandler(
    company_name=company, year=year, embeddingModel='text-embedding-3-large'
    ).getStore()
docstore_handler = InMemoryDocstoreHandler().getStore()

lc_retriever = RetrieverHandler(vectorstore_handler, docstore_handler)
lc_retriever.add(summarized_components)
docstore_handler.export()