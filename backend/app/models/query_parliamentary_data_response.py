from pydantic import BaseModel
from langchain_core.documents import Document
from typing_extensions import List, TypedDict

class Query_Parliamentary_Data_Response(BaseModel):
    """
    A class to represent the response for querying parliamentary data.

    Attributes:
    entity (str): The entity that the user has queried.
    context (List[Document]): The context retrieved for the entity from parliamentary records.
    entity_summary_answer (str): The summary answer generated for the entity based on the context.
    """
    entity: str
    context: List[Document]
    entity_summary_answer: str