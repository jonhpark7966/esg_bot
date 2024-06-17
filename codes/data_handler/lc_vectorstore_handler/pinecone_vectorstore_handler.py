from ..utils.krx_codes import KrxCodes
from .vectorstore_handler import VectorstoreHandler

from pinecone.grpc import PineconeGRPC as Pinecone
from pinecone import ServerlessSpec

from langchain_pinecone import PineconeVectorStore

import os
 


class PineconeVectorstoreHandler(VectorstoreHandler):
    # CHECK: os.envrion['PINECONE_API_KEY'] = "API_KEY"

    def connect(self):
        """
        tries to connect VectorDB

        Returns:
        vectorstore instance for langchain
        """
        raise NotImplementedError("TODO") 

    def load(self):
        """
        tries to load VectorDB
        Pinecone is cloud vector database, thus raise.

        Returns:
        vectorstore instance for langchain
        """
        print("Pinecone is Cloud based Vector Database, load opeartion Failed.")
        raise


    def create(self):
        """
        tries create to VectorDB

        Returns:
        vectorstore instance for langchain
        """
        api_key = os.getenv('PINECONE_API_KEY')
        pc = Pinecone(api_key=api_key)
        code = KrxCodes().convert_to_code(self.company_name)

        index_name = "krx"+code + "-" + str(self.year)

        if index_name not in pc.list_indexes().names():
            pc.create_index(
                name=index_name,
                dimension=self.dimension,
                metric=self.metric,
                spec=ServerlessSpec(
                cloud='aws',
                region='us-east-1'
            )
          )
            
        return PineconeVectorStore(
            index_name=index_name,
            embedding=self.lc_embeddingModel
        )