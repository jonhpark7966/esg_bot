from pdf2image import convert_from_path
import os
import base64

from openai import OpenAI


from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI

# Function to extract images from a PDF and save them as JPG
def extract_images_from_pdf(pdf_path, output_folder):
    # Convert PDF to a list of images
    images = convert_from_path(pdf_path)

    # Ensure output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Iterate through each image and save as JPG
    for page_num, image in enumerate(images):
        image_output_path = os.path.join(output_folder, f"image_{page_num + 1}.jpg")
        image.save(image_output_path, "JPEG")
        print(f"Saved image: {image_output_path}")

def encode_image(image_path):
    # 이미지 파일을 base64 문자열로 인코딩합니다.
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def image_summarize(img_base64, prompt, model = "gpt-4o-mini"):
    # 이미지 요약을 생성합니다.
    chat = ChatOpenAI(model=model, max_tokens=8192)

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

def text_to_embeddings(text, model = "text-embedding-3-large"):
    client = OpenAI()
    response = client.embeddings.create(
      model=model,
      input=text,
      encoding_format="float"
    )
    return response.data[0].embedding