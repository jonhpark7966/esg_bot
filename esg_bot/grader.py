# Relavence Score
# Grade output schema
# (2) relavant -> irrelevant changed for better filtering
# refer - https://docs.smith.langchain.com/evaluation/tutorials/rag
from typing import Annotated, TypedDict
from langchain_openai import ChatOpenAI

class RetrievalRelevanceGrade(TypedDict):
    explanation: Annotated[str, ..., "Explain your reasoning for the score"]
    relevant: Annotated[bool, ..., "True if the retrieved documents are relevant to the question, False otherwise"]

# Grade prompt
retrieval_relevance_instructions = """You are a teacher grading a quiz. 

You will be given a QUESTION and a set of FACTS provided by the student. 

Here is the grade criteria to follow:
(1) You goal is to identify FACTS that are completely unrelated to the QUESTION
(2) If the facts does not contains ANY keywords or semantic meaning to answer the question, consider them irrelevant
(3) It is OK if the facts have SOME information that is unrelated to the question as long as (2) is met

Relevance:
A relevance value of True means that the FACTS contain ANY keywords or semantic meaning related to the QUESTION and are therefore relevant.
A relevance value of False means that the FACTS are completely unrelated to the QUESTION.

Explain your reasoning in a step-by-step manner to ensure your reasoning and conclusion are correct. 

Avoid simply stating the correct answer at the outset."""

def retrieval_relevance(question, docs, model="gpt-4o") -> bool:
    retrieval_relevance_llm = ChatOpenAI(model=model).with_structured_output(RetrievalRelevanceGrade, method="json_schema", strict=True)

    """An evaluator for document relevance"""
    doc_string = """

""".join(doc for doc in docs)
    answer = f"""      FACTS: {doc_string}
QUESTION: {question}"""

    # Run evaluator
    grade = retrieval_relevance_llm.invoke([{"role": "system", "content": retrieval_relevance_instructions}, {"role": "user", "content": answer}])
    return grade
 