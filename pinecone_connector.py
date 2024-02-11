#! /usr/bin/env python3

import os

from dotenv import load_dotenv
from langchain_pinecone import Pinecone
from pinecone import Pinecone as PineconeClient
from pinecone import PodSpec, ServerlessSpec

load_dotenv()


class PineconeConnector(object):

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super(PineconeConnector, cls).__new__(cls)
        return cls._instance

    def __init__(self, embeddings):
        self.embeddings = embeddings
        self.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        self.PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
        self.PINECONE_ENV = os.getenv("PINECONE_ENV")
        if not hasattr(self, 'pc'):
            self.pc = PineconeClient(self.PINECONE_API_KEY)
            self.pinecone_env = self.PINECONE_ENV

    def create_index(self,
                     index_name: str,
                     dimension: int = 1536,
                     metric: str = "cosine",
                     cloud: str = "aws",
                     region: str = "None") -> None:
        """
        create_index Wrapper to create Pinecone Index

        Args:
            index_name (str): The name of the index to create.
            dimension (int, optional): The dimension of vectors that will be inserted in the index. Defaults to 1536.
            metric (str, optional): _description_. Defaults to "cosine".
            cloud (str, optional): _description_. Defaults to "aws".
            region (str, optional): _description_. Defaults to "None".
        """
        self.pc.create_index(
            index_name,
            dimension,
            metric,
            spec=ServerlessSpec(
                cloud,
                region,
                )
            )

    def desribe_index():
        pass

    def list_index():
        pass

    def add_index():
        Pinecone
        pass

    def delete_index():
        pass

    def __repr__():
        pass
