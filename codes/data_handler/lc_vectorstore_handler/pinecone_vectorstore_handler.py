from ..utils.krx_codes import KrxCodes
from .vectorstore_handler import VectorstoreHandler

from pinecone.grpc import PineconeGRPC as Pinecone
from pinecone import ServerlessSpec

from langchain_pinecone import PineconeVectorStore

import os
 


class PineconeVectorstoreHandler(VectorstoreHandler):

    def preinit(self):
        self.api_key = os.getenv('PINECONE_API_KEY')
        self.pc = Pinecone(api_key=self.api_key)
        self.code = KrxCodes().convert_to_code(self.company_name)
        self.index_name = "krx"+self.code + "-" + str(self.year)

    def connect(self):
        """
        tries to connect VectorDB

        Returns:
        vectorstore instance for langchain
        """

        if self.index_name not in self.pc.list_indexes().names():
            raise ValueError("Index does not exist in the Pinecone Project")
            
        return PineconeVectorStore(
            index_name=self.index_name,
            embedding=self.lc_embeddingModel
        )

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

        if self.index_name not in self.pc.list_indexes().names():
            self.pc.create_index(
                name=self.index_name,
                dimension=self.dimension,
                metric=self.metric,
                spec=ServerlessSpec(
                cloud='aws',
                region='us-east-1'
            )
          )
            
        return PineconeVectorStore(
            index_name=self.index_name,
            embedding=self.lc_embeddingModel
        )