# esg_bot





## History

- Try 1. Pages -> Images -> Summary -> Vector -> Multimodal RAG
  - Results
    - Vector Retriever has some problems
    - Some pages are not founded
  - Failure Analysis
    - Problem: 6 환경경영방침을 공개하고 있는가? -> 51 page should be retrieved, but not.
    - Threshold 로는 해결이 불가함. 왜냐하면 ranking 순으로 보았을때 51 페이지가 나오지 않음.
    - 왜 51 페이지는 검색이 안되는가?
    - summary 에는 "환경 경영" 이라는 내용이 충분히 잘 나온 것 같긴한데?
  - TODO
    - summary 형식을 통일 하거나, Prompting  -> Try2 완
    - Summary 를 한국어로 하거나? "환경 경영" 키워드가 벡터에 반영이 잘 안됐나? -> Try2 완
    - 하이브리드 서칭 (+키워드 서칭) 을 하거나. LangGraph를 만들어야 하나? 
    - 자동 평가 머신을 만들어야 할까?
     
- Try 2. Images -> Summary 개선
  - 2024.07.09
  - Results
    - Success!
    - Similarity search로 충분하다. SKT 보고서만으로 우선 평가한 결과임
  - 첨언
    - "중장기 목표" 에 대한 정의가 없어서 틀렸음. 이를 정의하도록 질문지를 잘 만들어주면 올바르게 수행함.
    - 당해년도(2023년), 보고서에 맞게 2022년으로 수정해주면 올바르게 대답함.
  -  TODO
     - 다양한 보고서와 다양한 질문에 대해 전문가의 평가가 필요함.
  
- User feedback 수집 창구
  - 2024.07.09
  - Streamlit 으로 UI 구성.
  - Langsmith Feedback 연결.
  - 사용자가 챗봇을 통해 질문지를 수정하거나, 결과를 관찰하며 피드백을 남겨 기록하고 나중에 추적해서 개선하도록 함.
  
- Dataset & Evaluation
  - prompt 를 바꾸거나, LLM을 바꾸거나, 여러가지 요소들에 의해서 차이가 발생할 수 있는데, 자동 evaluation 도구가 필요함
  - Retreival 이 잘 된건지. 혹은 대답이 잘못되었는지 등 여러가지 시도와 정량적인 평가를 위한 파이프라인을 만들자.

- Pinecone Vector Database metadata추가, namespace 는 바꾸지는 않음


- Chain callback to get Retrived Images
  - 근거 이미지를 streamlit chatbot에 추가함.
  - Evalution 로직으로 들어감.

- Evaluation
  - 온라인
    - 쓸데 없는 것을 들고 왔나.
    - 답변 퀄리티를 정의해야 함... 이건 못해. 이건 유저 피드백으로 받아야 함.
  - 평가 항목을 구성한다. --> 손으로 누가 잡아줘야 함. 
  - 데이터셋을 만들어야 하고
  - 사람이 잡아준 정답 output 이랑 비교를 하는 평가를 만들어야함.
  - 리트라이브가 잘 되었는지 봐야한다. 
  - 데이터셋을 구성한 후 모델을 바꿔가며 a/b 테스트를 한다. 