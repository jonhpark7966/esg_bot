from collections.abc import Sequence
from typing import Any
from uuid import UUID

from langchain.callbacks.base import BaseCallbackHandler
from langchain_core.documents import Document


class RetrieveCallbackHandler(BaseCallbackHandler):
    def __init__(self):
        self.retrieved_docs = []

    def on_retriever_end(
        self, documents: Sequence[Document], *, run_id: UUID, parent_run_id: UUID | None = None, tags: list[str] | None = None, **kwargs: Any
    ) -> Any:
        """Run when Retriever ends."""
        self.retrieved_docs.clear()
        for doc in documents:
            self.retrieved_docs.append(doc)

        return
