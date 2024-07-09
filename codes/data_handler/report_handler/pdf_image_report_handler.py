#from unstructured.partition.pdf import partition_pdf
import requests
import os
from pdf2image import convert_from_path
from PIL import Image

from .report_handler import ReportHandler

class PdfImageReportHandler(ReportHandler):
    def splitReport(self, save_dir, report_name):
        """
        Extract components of report.
        1. Extract tables from pdf files.
        2. Convert Pages to Images
        
        Returns:
        dictionary: dict contans the component type names and components.
        key : tables, page_images
        value : list of tables in text, list of page images in file path
        """

        try:
            components = {}
            components["source_url"] = self.report_url

            # get report file from url.
            save_path = save_dir + self.compnay_name + str(self.year) + "/" + report_name 
            self.download_file(self.report_url, save_path)

            # extract components from pdf.
            # TODO, table skipped
            #raw_pdf_elements = self.extract_pdf_elements(save_path)

            # 텍스트, 테이블, 이미지, 기타 정보 추출
            # texts, tables, images, others = self.categorize_elements(raw_pdf_elements)
            #components["tables"] = tables
            components["tables"] = []

            # Text 는 버리자. 보고서에서 무쓸모임.
            # text_splitter = CharacterTextSplitter.from_tiktoken_encoder(
            #     chunk_size=4000, chunk_overlap=0  # 텍스트를 4000 토큰 크기로 분할, 중복 없음
            # )
            # joined_texts = " ".join(texts)  # 텍스트 결합
            # texts_4k_token = text_splitter.split_text(joined_texts)  # 분할 실행

            page_image_dir = os.path.dirname(save_path)+"/page_images"
            image_paths = self.extract_images_from_pdf(save_path, page_image_dir)

            components["page_images_path"] = image_paths
            return components

        except Exception as e:
            print(f"Error on split reports: {e}")

        return {}
    

    def download_file(self, url, save_path):
        os.makedirs(os.path.dirname(save_path), exist_ok=True)

        response = requests.get(url)
        if response.status_code == 200:
            with open(save_path, 'wb') as file:
                file.write(response.content)
            print(f"File downloaded successfully and saved to {save_path}")
        else:
            print(f"Failed to download file. Status code: {response.status_code}")


    # PDF에서 요소 추출
    def extract_pdf_elements(self, filename):
        """
        PDF 파일에서 이미지, 테이블, 텍스트, 기타 정보를 추출합니다.
        path: 이미지(.jpg)를 저장할 파일 경로
        fname: 파일 이름
        """

        return partition_pdf(
            filename=filename,
            extract_images_in_pdf=True,  # PDF 내 이미지 추출 활성화
            infer_table_structure=True,  # 테이블 구조 추론 활성화
            chunking_strategy="by_title",  # 제목별로 텍스트 조각화
            max_characters=4000,  # 최대 문자 수
            new_after_n_chars=3800,  # 이 문자 수 이후에 새로운 조각 생성
            combine_text_under_n_chars=2000,  # 이 문자 수 이하의 텍스트는 결합
            image_output_dir_path=os.path.dirname(filename),  # 이미지 출력 디렉토리 경로
        )

    # 요소를 유형별로 분류
    def categorize_elements(self, raw_pdf_elements):
        """
        PDF에서 추출된 요소를 테이블, 텍스트, 이미지, 기타 정보로 분류합니다.
        raw_pdf_elements: unstructured.documents.elements의 리스트
        """
        tables = []  # 테이블 저장 리스트
        texts = []  # 텍스트 저장 리스트
        images = []  # 이미지 저장 리스트
        others = []  # 기타 정보 저장 리스트

        for element in raw_pdf_elements:
            element_type = str(type(element))
            if "unstructured.documents.elements.Table" in element_type:
                tables.append(str(element))  # 테이블 요소 추가
            elif "unstructured.documents.elements.CompositeElement" in element_type:
                texts.append(str(element))  # 텍스트 요소 추가
            elif "unstructured.documents.elements.Image" in element_type:
                images.append(str(element))  # 이미지 요소 추가
            else:
                others.append(str(element))  # 기타 정보 요소 추가

        return texts, tables, images, others

    # Function to extract images from a PDF and save them as JPG
    def extract_images_from_pdf(self, pdf_path, output_folder):
        # Convert PDF to a list of images
        images = convert_from_path(pdf_path, fmt='jpeg')

        # Ensure output folder exists
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # Iterate through each image and save as JPG
        paths = []
        for page_num, image in enumerate(images):
            image_output_path = os.path.join(output_folder, f"page_{page_num + 1:04}.jpg")
            image.save(image_output_path, "JPEG")
            paths.append(image_output_path)

        print(f"Saved image to {output_folder}, {len(images)} files")

        return paths 