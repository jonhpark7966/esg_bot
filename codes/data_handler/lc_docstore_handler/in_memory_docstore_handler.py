from .docstore_handler import DocstoreHandler
from langchain.storage import InMemoryStore
from langchain.schema import Document
import json

class InMemoryDocstoreHandler(DocstoreHandler):
    def __init__(self):
        self.docstore = InMemoryStore()

    def load_from_file(self, path="store_data.json"):
        """
        Loads the DocStore from a JSON file.

        Args:
        path (str): The path to the JSON file.

        Returns:
        None
        """
        with open(path, "r") as json_file:
            loaded_data = json.load(json_file)
            
            # Deserialize the loaded data into Document objects
            deserialized_data = [
                Document(page_content=value['page_content'], metadata=value['metadata'])
                for key, value in loaded_data.items()
            ]
            
            self.docstore.mset(zip(list(loaded_data.keys()), deserialized_data))

    def export_to_file(self, path="store_data.json"):
        """
        Exports the DocStore to a JSON file.

        Args:
        path (str): The path to the JSON file.

        Returns:
        None
        """
        store_data = dict(self.docstore.store.items())

        # Convert Document objects to a serializable format (dict)
        serializable_data = {
            key: {
                'page_content': value.page_content,
                'metadata': value.metadata
            }
            for key, value in store_data.items()
        }
       
        with open(path, "w") as json_file:
            json.dump(serializable_data, json_file, indent=4)

# Example usage
# handler = InMemoryDocstoreHandler()
# handler.export_to_file('store_data.json')
# handler.load_from_file('store_data.json')