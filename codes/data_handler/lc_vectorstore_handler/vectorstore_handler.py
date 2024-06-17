from abc import ABC, abstractmethod

from langchain_openai import OpenAIEmbeddings

class VectorstoreHandler(ABC):
    def getStore(self):
        return self.vectorstore

    def __init__(self, company_name, year, embeddingModel='text-embedding-3-large'):
        """
        Initialize the class with attributes.

        Parameters:
        companay_name (string): companay name
        year (int): year of report
        embeddingModel (str): default is openai's model
        """
        self.company_name = company_name
        self.year = year

        self.dimension = 1
        self.metric="cosine"
        self.lc_embeddingModel = None

        if embeddingModel == 'text-embedding-3-large':
            self.dimension = 3072
            self.metric="cosine"
            self.lc_embeddingModel = OpenAIEmbeddings(model=embeddingModel)

        self.vectorstore = None

        self.preinit()

        try:
            self.vectorstore = self.connect()
            return
        except:
            print("Vector Store Connection Failed, fallback to load.")

        try:
            self.vectorstore = self.load()
            return
        except:
            print("Vector Store Load Failed, fallback to create")

        try:
            self.vectorstore = self.create()
            return
        except Exception as e:
            print("Vector Store Creation Failed! ", e)

    def preinit(self):
        pass

    @abstractmethod
    def connect(self):
        """
        Abstract function
        tries to connect VectorDB

        Returns:
        vectorstore instance for langchain
        """
        pass

    @abstractmethod
    def load(self):
        """
        Abstract function
        tries to load VectorDB

        Returns:
        vectorstore instance for langchain
        """
        pass

    @abstractmethod
    def create(self):
        """
        Abstract function
        tries reate to VectorDB

        Returns:
        vectorstore instance for langchain
        """
        pass