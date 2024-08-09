# Configuring
import os

import pandas as pd
from dotenv import load_dotenv

from esg_bot.data_handler.lc_docstore_handler.in_memory_docstore_handler import InMemoryDocstoreHandler
from esg_bot.data_handler.lc_retrieverHandler.retriever_handler import RetrieverHandler
from esg_bot.data_handler.lc_vectorstore_handler.pinecone_vectorstore_handler import PineconeVectorstoreHandler
from esg_bot.data_handler.report_handler.pdf_image_report_handler import PdfImageReportHandler
from esg_bot.data_handler.summary_handler.gpt_summary_handler import GPTSummaryHandler


def report_prepare(company, year, report_url, report_data_dir, report_name):
    # pdf to components.
    components = PdfImageReportHandler(company_name=company, year=year, report_url=report_url).splitReport(report_data_dir, report_name)

    #FIXME: filter components.
    #paths = components["page_images_path"]
    #components["page_images_path"] = [path for path in paths if "0061" in path]

    summarized_components = GPTSummaryHandler().summary(components)

    # USE LangChain from here.
    vectorstore_handler = PineconeVectorstoreHandler(company_name=company, year=year, embeddingModel="text-embedding-3-large", postfix="kr").getStore()
    docstore_handler = InMemoryDocstoreHandler()
    lc_docstore = docstore_handler.getStore()

    lc_retriever = RetrieverHandler(vectorstore_handler, lc_docstore)
    lc_retriever.add(summarized_components, company_name=company, year=year)
    docstore_handler.export_to_file(report_data_dir + company_name + str(year) + "/store_data.json")


if __name__ == "__main__":
    # Load the .env file
    load_dotenv()

    report_data_dir = "./data/reports/"
    report_name = "report.pdf"
    file_list_df = pd.read_csv("./data/reports.csv")

    target = "현대비앤지스틸" #"현대차" #"SK텔레콤"  # "LG에너지솔루션"#
    #row = file_list_df[file_list_df.company_name == target].iloc[0]

    company_name = target #row["company_name"]
    year = 2024 #row["year"]
    #url = f"{os.getenv('LOGBLACK_URL')}{company_name}_{year}.pdf"
    #url = "https://www.hyundai.com/content/dam/hyundai/kr/ko/images/company-intro/sustain-manage/2024/hmc-sr-kor-2024.pdf"
    url = "https://www.bngsteel.com/kr/pds/file/pdf/Sustainability_Report.pdf"

    # FIXME: TESTING.
    # url = "https://www.clickdimensions.com/links/TestPDFfile.pdf"


    report_prepare(company_name, year, url, report_data_dir, report_name)
    print("SUCCESS!")