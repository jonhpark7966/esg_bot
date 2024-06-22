import base64
from IPython.display import HTML, display
import io
import re
from PIL import Image
from langchain_core.documents import Document


class ImageBase64Utils():
    @staticmethod
    def plt_img_base64(img_base64):
        """base64 인코딩된 문자열을 이미지로 표시"""
        # base64 문자열을 소스로 사용하는 HTML img 태그 생성
        image_html = f'<img src="data:image/jpeg;base64,{img_base64}" />'
        # HTML을 렌더링하여 이미지 표시
        display(HTML(image_html))

    @staticmethod
    def looks_like_base64(sb):
        """문자열이 base64로 보이는지 확인"""
        return re.match("^[A-Za-z0-9+/]+[=]{0,2}$", sb) is not None

    @staticmethod
    def is_image_data(b64data):
        """
        base64 데이터가 이미지인지 시작 부분을 보고 확인
        """
        image_signatures = {
            b"\xff\xd8\xff": "jpg",
            b"\x89\x50\x4e\x47\x0d\x0a\x1a\x0a": "png",
            b"\x47\x49\x46\x38": "gif",
            b"\x52\x49\x46\x46": "webp",
        }
        try:
            header = base64.b64decode(b64data)[:8]  # 처음 8바이트를 디코드하여 가져옴
            for sig, format in image_signatures.items():
                if header.startswith(sig):
                    return True
            return False
        except Exception:
            return False

    @staticmethod
    def resize_base64_image(base64_string, size=(128, 128)):
        """
        Base64 문자열로 인코딩된 이미지의 크기 조정
        """
        # Base64 문자열 디코드
        img_data = base64.b64decode(base64_string)
        img = Image.open(io.BytesIO(img_data))

        # 이미지 크기 조정
        resized_img = img.resize(size, Image.LANCZOS)

        # 조정된 이미지를 바이트 버퍼에 저장
        buffered = io.BytesIO()
        resized_img.save(buffered, format=img.format)

        # 조정된 이미지를 Base64로 인코딩
        return base64.b64encode(buffered.getvalue()).decode("utf-8")

    @staticmethod
    def split_image_text_types(docs):
        """
        base64로 인코딩된 이미지와 텍스트 분리
        """
        b64_images = []
        texts = []
        for doc in docs:
            # 문서가 Document 타입인 경우 page_content 추출
            if isinstance(doc, Document):
                doc = doc.page_content
            if ImageBase64Utils.looks_like_base64(doc) and ImageBase64Utils.is_image_data(doc):
                doc = ImageBase64Utils.resize_base64_image(doc, size=(1280, 720))
                b64_images.append(doc)
            else:
                texts.append(doc)
        return {"images": b64_images, "texts": texts}


