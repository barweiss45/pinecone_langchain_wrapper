import logging
import os

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Response, status
from langchain_openai import OpenAIEmbeddings
from schema import ResponseMessage, IndexModel

from pinecone_connector import PineconeConnector

app = FastAPI(debug=True)
logger = logging.getLogger(__name__)
consoleHandler = logging.StreamHandler()
logger.addHandler(consoleHandler)

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENV = os.getenv("PINECONE_ENV")

pc = PineconeConnector(embeddings=OpenAIEmbeddings(model="text-embedding-3-small"))


@app.post("/index/", status_code=status.HTTP_201_CREATED)
def create_index(index: IndexModel) -> bool:
    try:
        message = pc.create_index(index)
        if message["success"]:
            logger.info("main.create_index: %s", message)
            return Response
    except ValueError as e:
        logging.exception("%s", e)
        raise HTTPException(status_code=400, detail={"success": False, "message": e})


@app.get("/index/")
def list_index() -> ResponseMessage:
    """Lists all Pinecone Indexes"""
    response = pc.list_index()
    logger.debug("main.list_index: %s", response)
    return response
