from ..models.query_parliamentary_data_response import Query_Parliamentary_Data_Response

from langchain_ollama.llms import OllamaLLM
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_core.prompts import PromptTemplate
from langchain_core.documents import Document
from typing_extensions import List

from fastapi.responses import JSONResponse

class ParliamentaryGraph:
    def __init__(self, model: OllamaLLM, vector_store: InMemoryVectorStore, document_ids: List[Document]):
        """
        Initialize the ParliamentaryGraph with the given model, vector store, and document IDs.

        Parameters:
        model (OllamaLLM): The language model to use for generating answers.
        vector_store (InMemoryVectorStore): The vector store to use for similarity search.
        document_ids (List[Document]): The list of document IDs.
        """
        self.model = model
        self.vector_store = vector_store
        self.document_ids = document_ids

    def retrieve(self, state: Query_Parliamentary_Data_Response, k: int = 15) -> List[Document]:
        """
        Retrieve the context (RAG) for the entity that the user has entered.

        Parameters:
        state (Query_Parliamentary_Data_Response): Response object which contains the entity and context + answer both of which are empty
        k (int): The number of similar documents to retrieve (default is 15)

        Returns:
        List[Document]: List of retrieved documents
        """
        retrieved_docs = self.vector_store.similarity_search(state.entity, k=k)
        return retrieved_docs

    def create_entity_summary_prompt(self) -> str:
        """
        Create a prompt that asks the model to generate a summary of the entity with context to help with response.

        Returns:
        template_prompt_string: generated prompt with entity and context as input variables
        """
        template_prompt_string = """
        You are a service that allows users to query parliamentary meeting records by an entity that can be a name, topic or anything else the user types.

        You will be given context which is from the parliamentary meeting records that are relevant to the entity, use this context to help you.

        The user has entered the entity: '{entity}'
        Below is the context that you can use to generate the answer: '{context}'

        You have now been given all the context

        1) A summary that will give insight into what the entity is and how it relates to the context that the user has entered.
        2) List all key events within the context that are relevant to the entity that the user has entered.
        3) List all contributions and names within the context that are relevant to the entity that the user has entered.
        4) List all times and dates within the context that are relevant to the entity that the user has entered.
        
        You response must follow this template:
         1) summary
         2) key events
         3) contributions/names
         4) times/dates
        """
        return template_prompt_string

    def generate(self, state: Query_Parliamentary_Data_Response, entity_summary_prompt: PromptTemplate, model: OllamaLLM) -> dict:
        """
        Generate an answer based on the retrieved context for the entity that the user has entered.

        Parameters:
        state (Query_Parliamentary_Data_Response): Response object which contains the entity, context, and an empty answer.
        entity_summary_prompt (PromptTemplate): The prompt template to use for generating the answer.
        model (OllamaLLM): The model to use for generating the answer.

        Returns:
        dict: A dictionary containing the generated answer.
        """
        docs_content = "\n\n".join(doc.page_content for doc in state.context)
        messages = entity_summary_prompt.invoke({"entity": state.entity, "context": docs_content})
        return {"entity_summary_answer": model.invoke(messages)}

    def query_parliamentary_data(self, entity: str) -> Query_Parliamentary_Data_Response:
        """
        Query parliamentary data for a given entity.

        Parameters:
        entity (str): The entity to query.

        Returns:
        Query_Parliamentary_Data_Response: The response object containing the entity, context, and generated answer.
        """
        response = Query_Parliamentary_Data_Response(entity=entity, context=[], entity_summary_answer="")
        response.context = self.retrieve(response)
        response.entity_summary_answer = self.generate(response, PromptTemplate(input_variables=["entity", "context"], template=self.create_entity_summary_prompt()), self.model)
        return JSONResponse(content={"entity_response": response.entity_summary_answer})