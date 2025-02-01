import cohere
import os
import pandas as pd


from langsmith import traceable

@traceable(name="Reranking")
def rerank(question, df, top_n=10):
    cohere_api_key = os.getenv("COHERE_API_KEY")
    co = cohere.ClientV2(cohere_api_key)

    docs = df["text"].tolist()

    reranked_df = df.copy().reset_index(drop=True)

    response = co.rerank(
        model="rerank-v3.5",
        query=question,
        documents=docs,
        top_n=top_n,
    )

    for result in response.results:
        reranked_df.loc[result.index,"rerank_relevance_score"] = result.relevance_score

    return reranked_df.sort_values("rerank_relevance_score", ascending=False)

 