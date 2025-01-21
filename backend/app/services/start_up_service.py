import time
import logging
from langchain_ollama.llms import OllamaLLM
from langchain_community.llms import Ollama
from langchain_ollama import OllamaEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_community.document_loaders.mongodb import MongodbLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

logger = logging.getLogger("app")

def load_model(model_name, model_url):
    """
    Load the model and initialize the vector store with embeddings.

    Parameters:
    model_name (str): The name of the model to load.

    Returns:
    Tuple[OllamaLLM, InMemoryVectorStore]: The loaded model and initialized vector store.
    """
    model = OllamaLLM(model=model_name, base_url=model_url)
    embeddings = OllamaEmbeddings(model=model_name, base_url=model_url)
    vector_store = InMemoryVectorStore(embeddings)
    return model, vector_store

async def load_data(vector_store, connection_string, db_name, collection_name, field_names):
    """
    Load data from MongoDB, split the documents, and add them to the vector store.

    Parameters:
    vector_store (InMemoryVectorStore): The vector store to add documents to.
    connection_string (str): The connection string for MongoDB.
    db_name (str): The name of the database.
    collection_name (str): The name of the collection.
    field_names (List[str]): The list of field names to retrieve from the collection.

    Returns:
    List[str]: List of document IDs added to the vector store.
    """
    start_time = time.time()
    logger.info("Loading data from MongoDB...")
    loader = MongodbLoader(
        connection_string=connection_string,
        db_name=db_name,
        collection_name=collection_name,
        field_names=field_names,
    )
    parliament_data = await loader.aload()  # Ensure this is awaited
    logger.info(f"Loaded {len(parliament_data)} documents from MongoDB in {time.time() - start_time:.2f} seconds")

    logger.info("Splitting documents...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        add_start_index=True,
    )
    all_splits = text_splitter.split_documents(parliament_data)
    logger.info(f"Split documents into {len(all_splits)} chunks in {time.time() - start_time:.2f} seconds")

    document_ids = vector_store.add_documents(documents=all_splits)

    return document_ids