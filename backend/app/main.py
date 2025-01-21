import logging
from fastapi import FastAPI
from contextlib import asynccontextmanager
from pathlib import Path

from app.config.config_loader import Config
from app.services.start_up_service import load_model, load_data
from app.services.parliamentary_data_service import ParliamentaryGraph

from fastapi.middleware.cors import CORSMiddleware
import time

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("app")

# Initialize startup assets
start_up_assets = {}

# Load configuration
logger.info("Backend: Loading Config")
config_path = Path(__file__).parent / "config/config.yaml"
config = Config(config_path).config



@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Context manager for the lifespan of the FastAPI application.

    Parameters:
    app (FastAPI): The FastAPI application instance.

    Yields:
    None
    """
    logger.info("Waiting For All services to start")
    time.sleep(10)
    logger.info("Backend: Loading Data Into Memory")
    start_up_assets["model"], start_up_assets["vector_store"] = load_model(config['model']['model_name'],config['model']['model_url'])
    logger.info(start_up_assets)
    start_up_assets["document_ids"] = await load_data(start_up_assets["vector_store"], config['database']['connection_string'], config['database']['db_name'], config['database']['collection_name'], config['database']['field_names'])

    logger.info(f"Backend: Loaded {len(start_up_assets['document_ids'])} documents into the vector store.")
    yield
    start_up_assets.clear()
    logger.info("Backend: Data Loading Complete")

# Create FastAPI app instance
app = FastAPI(lifespan=lifespan)

# Allow CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


@app.get("/")
async def root():
    """
    Root endpoint.

    Returns:
    dict: A welcome message.
    """
    return {"message": "Hello World"}

@app.get("/query_parliamentary_data/{entity}")
def query_parliamentary_data(entity: str):
    """
    Endpoint to query parliamentary data for a given entity.

    Parameters:
    entity (str): The entity to query.

    Returns:
    Query_Parliamentary_Data_Response: The response object containing the entity, context, and generated answer.
    """
    parliamentary_graph = ParliamentaryGraph(model=start_up_assets["model"], vector_store=start_up_assets["vector_store"], document_ids=start_up_assets["document_ids"])
    return parliamentary_graph.query_parliamentary_data(entity)