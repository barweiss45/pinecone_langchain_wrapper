import os
from dotenv import load_dotenv
from typing import Dict, Any

from fastapi import FastAPI
import logging
from pinecone_connector import PineconeConnector, serverless, pod
from langchain_openai import OpenAIEmbeddings


app = FastAPI()
logger = logging.getLogger(__name__)

pc = PineconeConnector(embeddings=OpenAIEmbeddings(model="text-embedding-3-small"))

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENV = os.getenv("PINECONE_ENV")


@app.post("/create_index")
def create_index(index_name: str, *args, **kwargs) -> bool:
    return pc.create_index(index_name, *args, **kwargs)