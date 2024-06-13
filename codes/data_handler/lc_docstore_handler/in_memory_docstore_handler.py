from codes.data_handler.lc_docstore_handler.docstore_handler import DocstoreHandler
from langchain.storage import InMemoryStore

import json

class InMemoryDocstoreHandler(DocstoreHandler):
    def __init__(self):
        self.docstore = InMemoryStore() 

    def load_from_file(self, path):
        """
        Abstract function
        tries to load DocStore

        Returns:
        docstore instance for langchain
        """
        raise NotImplementedError() 

    def export_to_file(self, path="store_data.json"):
        """
        Abstract function
        export to file
        TODO - handle if stored data is too large.

        Returns:
        docstore instance for langchain
        """

        # 데이터를 dictionary로 변환
        store_data = dict(self.docstore.store.items())

        # JSON 파일로 저장
        with open(path, "w") as json_file:
            json.dump(store_data, json_file)