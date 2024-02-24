import logging
import os
import json

from dotenv import load_dotenv
from fastapi import FastAPI, Response, status, HTTPException
from langchain_openai import OpenAIEmbeddings

from pinecone_connector import PineconeConnector
from schema import IndexModel

app = FastAPI(debug=True)
logger = logging.getLogger(__name__)

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENV = os.getenv("PINECONE_ENV")

pc = PineconeConnector(embeddings=OpenAIEmbeddings(model="text-embedding-3-small"))


@app.post("/create_index", status_code=status.HTTP_201_CREATED)
def create_index(index: IndexModel) -> bool:
    try:
        message = pc.create_index(index)
        if message["success"]:
            return Response
    except ValueError as e:
        logging.exception("%s", e)
        raise HTTPException(status_code=400, detail={"success": False, "message": e})


@app.get("/list_index")
def list_index() -> Response:
    response = pc.list_index()
    logger.debug("%s", response)
    return response
