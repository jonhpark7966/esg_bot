from langchain.callbacks.base import BaseCallbackHandler
from typing import Any, Dict, List, Optional, Sequence
from langchain_core.messages import BaseMessage
from langchain_core.documents import Document

class RetrieveCallbackHandler(BaseCallbackHandler):
    def __init__(self):
        self.retrieved_docs = []

    def on_retriever_end(self, documents: Sequence[Document], *, run_id, parent_run_id = None, **kwargs: Any) -> Any:
        """Run when Retriever ends."""
        self.retrieved_docs.clear()
        for doc in documents:
            self.retrieved_docs.append(doc)

        return  



