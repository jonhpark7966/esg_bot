from abc import ABC, abstractmethod


class DocstoreHandler(ABC):
    def getStore(self):
        return self.docstore

    @abstractmethod
    def load_from_file(self, path):
        """
        Abstract function
        tries to load DocStore

        Returns:
        docstore instance for langchain
        """
        pass

    @abstractmethod
    def export_to_file(self, path):
        """
        Abstract function
        export to file
        TODO - handle if stored data is too large.

        Returns:
        docstore instance for langchain
        """
        pass
