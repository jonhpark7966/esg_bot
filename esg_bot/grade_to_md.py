from langchain_core.messages import SystemMessage, HumanMessage
from langchain_openai import ChatOpenAI
from esg_bot.utils import encode_image



explanation_write_instructions = f"""You are professional finantial and ESG report writer.
You will be given Questiona and Answer pair with explanation and retrieved page images from ESG report as a source data. 
Your task is to write a detailed explanation in markdown format based on the given information.
Detailed explanation should be based on the facts from the source data and explanation.
You should provide a clear and concise explanation that is easy to understand.

Detailed explanation you write will be used to for analysis reprort which will be used by the company's ESG team,
and be pulished in the web site's dashboard.

write the explanation in markdown format, like as follows.
write in Korean. Do NOT translate company names.

---

## 요약  
  - 등급: 나. 지역사회 상생 활동 공개  
  - 지역사회 상생 활동을 공개하고 있으나, 수혜자 중심의 구체적 성과지표(수혜자 수, 편익 규모 등)는 확인되지 않음  

## 상세 설명  
  
1. 활동 공개  
  - 보고서 17페이지, 66페이지 등에서 문화예술 후원(‘뷰티필마인드’ 협력), 학습활동 장려(장학금·연구 활동 지원), 전기차 충전소 설치 등 다양한 사회공헌 활동 및 지역사회 상생 활동을 소개하고 있음.  
  - 보고서 90페이지의 ESG Performance Data를 통해 기부금 내역과 임직원 봉사활동 현황을 구체적인 수치(금액·참여 인원·봉사시간 등)로 공개함.  

2. 성과 공개  
  - 현재 공개된 자료는 기업이 투입한 자원(기부금, 봉사시간 등)을 위주로 제시되어 있음.  
  - 수혜자 수, 편익 등을 계량화하여 보여주는 지표(예: 기부금 수혜 인원, 현물 기부 효과 등)는 확인되지 않음.  
  - 따라서 지역사회 상생 활동이 공개되어 있으나, 수혜자 중심의 성과 지표가 충분히 제시되지 않아 “활동 공개” 수준으로 판단됨.  

## 주요 근거 자료  

  - **17페이지**: 주요 이해관계자(지역사회 포함)에 대한 주요 관심 이슈와 대응 활동  
  - **66페이지**: 지역사회 문화예술 후원, 학습활동 장려, 전기차 충전소 설치 등 사회공헌 활동 사례  
  - **90페이지**: ESG Performance Data:  사회공헌(기부금, 임직원 자원봉사 등) 현황  
"""


def write_explanation(graded_row, SR_REPORT_IMAGE_PATH, model = "gpt-4o"):
    llm = ChatOpenAI(model=model, max_tokens=8192)

    messages = []
    messages.append(SystemMessage(content=explanation_write_instructions))

    graded_text = f"""
Qustion: {graded_row.loc["question"]}
---
Choices: {graded_row.loc[ "choices"]}
---
Grade: {graded_row.loc["grade"]}
---
Explanation: {graded_row.loc["explanation"]}
"""
    human_message_contents = []
    human_message_contents.append({"type": "text", "text": graded_text})

    page_numbers = eval(graded_row.loc["retrieved_page_numbers"])
    encoded_page_images = [encode_image(SR_REPORT_IMAGE_PATH + "/image_" + str(page_number) + ".jpg") for page_number in page_numbers]
    human_message_contents.extend(
        [
            {
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{encoded_image}"},
            }
            for encoded_image in encoded_page_images 
        ]
    )
    messages.append(HumanMessage(content=human_message_contents))

    msg = llm.invoke( messages )
    return msg.content



if __name__ == "__main__":
    import pandas as pd

    i = 92
    q_df = pd.read_csv("../data/reports/2024/서연이화/graded.csv")
    row = q_df.loc[i]

    SR_REPORT_PATH = "../data/reports/2024/서연이화/"
    SR_REPORT_IMAGE_PATH = SR_REPORT_PATH + "pages"

    content = write_explanation(row, SR_REPORT_IMAGE_PATH, model = "gpt-4o-mini")
    print(content)