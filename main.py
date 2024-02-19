import os
from dotenv import load_dotenv

from fastapi import FastAPI
import logging
from pinecone_connector import PineconeConnector
from langchain_openai import OpenAIEmbeddings


app = FastAPI()
logger = logging.getLogger(__name__)

pc = PineconeConnector(embeddings=OpenAIEmbeddings(model="text-embedding-3-small"))

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENV = os.getenv("PINECONE_ENV")

def 