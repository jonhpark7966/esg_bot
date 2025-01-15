from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

from typing import Annotated, TypedDict

class ReportEvaluationGrade(TypedDict):
    explanation: Annotated[str, ..., "Explain your reasoning for the score"]
    grade: Annotated[str, ..., "Select the answer choice for the question"]


report_eval_instructions = f"""You are finantial and ESG report analysist tasking with providing investment advice.
                You will be given a image(s) which is some pages of company's ESG Report.
                Use this information to asnwer the following question.

                Select the answer choices.

                Also, explain your resoning in a step-by-step manner.
                If possible, find the page number on the image and inform the page numbers for users to find the evidence easily.

                Answer in Korean. Do NOT translate company names."""


def get_answer_rag(question, answer_choices, retrieved_pages_encoded, model="o1"):
    report_eval_llm = ChatOpenAI(model=model).with_structured_output(ReportEvaluationGrade, method="json_schema", strict=True)

    messages = []

    messages.append(SystemMessage(content=report_eval_instructions))

    human_message_contents = []
    human_message_contents.append({"type": "text", "text": f"""Question: {question}
                                   Answer Choices:{answer_choices}"""})
    human_message_contents.extend(
        [
            {
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{encoded_image}"},
            }
            for encoded_image in retrieved_pages_encoded
        ]
    )
    messages.append(HumanMessage(content=human_message_contents))

    msg = report_eval_llm.invoke( messages )
    return msg
