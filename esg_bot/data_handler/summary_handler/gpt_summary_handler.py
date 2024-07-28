from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

import base64

from langchain_core.messages import HumanMessage
from .summary_handler import SummaryHandler

class GPTSummaryHandler(SummaryHandler):
    def summary(self, components, model="gpt-4o"):
        """
        Generate Summary of components of report.
          - Try to handler all of the components
          - MultiModal Model or not may occurs error
        
        Returns:
        dictionary: dict contans the component type names and components.
        key : add keys named "$key_summary"
        value : list of summaries for each compoenents
        """

        try:
            for key in list(components.keys()):
                value = components[key]
                # value might be a list.
                if key == "texts" or key == "tables":
                    # 텍스트, 테이블 요약 가져오기
                    summaries = self.generate_text_summaries(value, model)
                    components[key+"_summaries"] = summaries
                elif key == "page_images_path":
                    # 이미지 요약 실행
                    img_base64_list, image_summaries, page_nums = self.generate_img_summaries(value, model)
                    components["page_images_b64"] = img_base64_list
                    components["page_images_summaries"] = image_summaries
                    components["page_num"] = page_nums

                    # remove paths.
                    del components["page_images_path"]
                
                print(f"{key} summary generated")

            return components

        except Exception as e:
            print(f"Error on summary generation: {e}")

        return {}
    

    # 텍스트 요소의 요약 생성
    def generate_text_summaries(self, inputs, model):
        """
        텍스트 요소 요약
        texts: 문자열 리스트
        tables: 문자열 리스트
        summarize_texts: 텍스트 요약 여부를 결정. True/False
        """

        # 프롬프트 설정
        prompt_text = """You are an assistant tasked with summarizing tables and text for retrieval. \
        These summaries will be embedded and used to retrieve the raw text or table elements. \
        Give a concise summary of the table or text that is well optimized for retrieval. Table or text: {element} """
        prompt = ChatPromptTemplate.from_template(prompt_text)

        # 텍스트 요약 체인
        model = ChatOpenAI(temperature=0, model=model)
        summarize_chain = {"element": lambda x: x} | prompt | model | StrOutputParser()

        # 요약을 위한 빈 리스트 초기화
        summaries = []
        summaries = summarize_chain.batch(inputs, {"max_concurrency": 5})

        return summaries
    


    def encode_image(self, image_path):
        # 이미지 파일을 base64 문자열로 인코딩합니다.
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")
    
    def image_summarize(self, img_base64, prompt, model):
        # 이미지 요약을 생성합니다.
        chat = ChatOpenAI(model=model, max_tokens=2048)

        msg = chat.invoke(
            [
                HumanMessage(
                    content=[
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/jpeg;base64,{img_base64}"},
                        },
                    ]
                )
            ]
        )
        return msg.content


    def generate_img_summaries(self, paths, model):
        """
        이미지에 대한 요약과 base64 인코딩된 문자열을 생성합니다.
        path: .jpg 파일 목록의 경로
        """

        # base64로 인코딩된 이미지를 저장할 리스트
        img_base64_list = []

        # 이미지 요약을 저장할 리스트
        image_summaries = []

        # number of pages
        page_nums = []

        # 요약을 위한 프롬프트
        prompt = """You are an assistant tasked with summarizing images for retrieval. \
        These summaries will be embedded and used to retrieve the raw image. \
        Give a concise summary of the image that is well optimized for retrieval."""

        # 이미지 요약 프롬프트 추가
        prompt = prompt + """
        Summary should be in Korean.
        Output format is like this.

        예시:

        페이지 제목: 준법 경영 및 주요 추진 성과
        키워드: 환경 경영, 중장기 목표, 인권
        패이지 번호 : 42
        핵심 내용:
	    - 주요 내용
          - 컴플라이언스: 시장과 사회로 부터 요구되는 법적 규제 및 윤리적 기준을 준수
          - 컴플라이언스 체계 가이드라인을 바탕으로 공정 거래 채계를 구축
          - 추진 과제: 준법 경영 문화 확산, 대외 신뢰도 제고
	    - 주요 데이터/통계:
	      - 정책관련 지출 현황
	      -	유관 기관 협회 협회비 총액 609백만원
          - 상위 5개 지출 협회명: A협회, B협회, C협회, D협회, E협회
        - 주요 이미지 설명
            - 중장기 추진 목표의 달성을 위한 도식
            - 환경 경영 성과에 대한 그래프
        """

        # 이미지에 적용
        for img_path in paths:
                try:
                    base64_image = self.encode_image(img_path)
                    summary = self.image_summarize(base64_image, prompt, model)
                    img_base64_list.append(base64_image)
                    image_summaries.append(summary)
                    page_nums.append(int(img_path.split("/")[-1].split("_")[-1].split(".")[0]))
                except:
                    print(f"FAIL! {img_path}")

        return img_base64_list, image_summaries, page_nums


