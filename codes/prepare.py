# Configuring
from data_handler.lc_docstore_handler.in_memory_docstore_handler import InMemoryDocstoreHandler
from data_handler.lc_retrieverHandler.retriever_handler import RetrieverHandler
from data_handler.report_handler.pdf_image_report_handler import PdfImageReportHandler
from data_handler.summary_handler.gpt_summary_handler import GPTSummaryHandler
from data_handler.lc_vectorstore_handler.pinecone_vectorstore_handler import PineconeVectorstoreHandler

from dotenv import load_dotenv
import pandas as pd
import os

# Load the .env file
load_dotenv()

report_data_dir = "./data/reports/"
report_name = "report.pdf"
file_list_df = pd.read_csv("./data/reports.csv")

target = "SK텔레콤"#"LG에너지솔루션"#
row = file_list_df[file_list_df.company_name == target].iloc[0]

company_name = row["company_name"]
year = row["year"]
url = f"{os.getenv('logblack_url')}{company_name}_{year}.pdf"

# FIXME: TESTING.
#url = "https://pdfobject.com/pdf/sample.pdf"


def report_prepare(company, year, report_url, report_data_dir, report_name):
    # pdf to components.
    components = PdfImageReportHandler(
        company_name=company, year=year, report_url=report_url
        ).splitReport(report_data_dir, report_name)
    summarized_components = GPTSummaryHandler().summary(components)

    # USE LangChain from here.
    vectorstore_handler = PineconeVectorstoreHandler(
        company_name=company, year=year, embeddingModel='text-embedding-3-large', postfix="kr"
        ).getStore()
    docstore_handler = InMemoryDocstoreHandler()
    lc_docstore = docstore_handler.getStore()

    lc_retriever = RetrieverHandler(vectorstore_handler, lc_docstore)
    lc_retriever.add(summarized_components, company_name = company, year = year)
    docstore_handler.export_to_file(report_data_dir+company_name+str(year)+"/store_data.json")

report_prepare(company_name, year, url, report_data_dir, report_name)
print("SUCCESS!")

