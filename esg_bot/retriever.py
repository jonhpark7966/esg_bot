from kiwipiepy import Kiwi
from scipy.spatial.distance import cosine
from rank_bm25 import BM25Okapi

import pandas as pd

from langsmith import traceable

from esg_bot.utils import text_to_embeddings

class HybridRetriever:
    def __init__(self, df, model="text-embedding-3-large"):
        self.df = df.copy()
        self.model = model
        self.kiwi = Kiwi()

        # Tokenize documents for BM25
        tokenized_docs = []
        for doc in self.df["text"]:
            if pd.isna(doc):
                tokenized_docs.append([])
                continue
            tokens = [t.form for t in self.kiwi.tokenize(doc)]
            tokenized_docs.append(tokens)

        # Build BM25
        self.bm25 = BM25Okapi(tokenized_docs)

    @traceable(name="Retrieve BM25")
    def retrieve_df_bm25(self, query, top_k=10):
        q_tokens = [t.form for t in self.kiwi.tokenize(query)]
        scores = self.bm25.get_scores(q_tokens)
        self.df["bm25_score"] = scores
        return self.df.sort_values("bm25_score", ascending=False).head(top_k)

    @traceable(name="Retrieve Cosine Similarity")
    def retrieve_df_vectors(self, query, top_k=10):
        q_vector = text_to_embeddings(query, model=self.model)
        # Assuming df["vector"] already contains precomputed embeddings
        self.df["distance"] = self.df["vector"].apply(lambda x: cosine(q_vector, x))
        return self.df.sort_values("distance").head(top_k)