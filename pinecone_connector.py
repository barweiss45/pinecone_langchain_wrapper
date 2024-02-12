#! /usr/bin/env python3

import os
from typing import Union, Dict, Any, List, TypeVar,

from dotenv import load_dotenv
from langchain_pinecone import Pinecone
from pinecone import Pinecone as PineconeClient
from pinecone import PodSpec, ServerlessSpec

IndexDescription = TypeVar('IndexDescription', str, int)
IndexList = TypeVar('IndexList', List)

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
                     server_type: Union[ServerlessSpec, PodSpec] = PodSpec,
                     cloud: str = "aws",
                     environment: str = None,
                     pod_type: str = "p1.x1",
                     metadata_config: Dict[str, Any] = {},) -> bool:
        """
        create_index Wrapper to create Pinecone Index

        Args:
            index_name (str): The name of the index to create.
            dimension (int, optional): The dimension of vectors that will be inserted in the index. Defaults to 1536.
            metric (str, optional): _description_. Defaults to "cosine".
            cloud (str, optional): _description_. Defaults to "aws".
            region (str, optional): _description_. Defaults to "None".
        """
        if index_name in self.pc.list_indexes().names():
            return False
        if self.PINECONE_ENV is not None:
            environment = self.PINECONE_API_KEY
        if server_type == PodSpec:
            spec = PodSpec(environment,
                           pod_type,
                           pods=1,
                           metadata_config=metadata_config)
        elif server_type == ServerlessSpec:
            spec = ServerlessSpec(cloud, region="us-west-2")  # only availabe in us-west-2
        else:
            raise ValueError("Incorrect Server type. Choose either ServerlessSpec or PodSpec")
        
        self.pc.create_index(
            index_name,
            dimension,
            metric,
            spec=spec,
            )
        return True

    def desribe_index():
        pass

    def list_index(self) -> IndexList[IndexDescription]:
        """Lists all Pinecone Indexes"""
        return [index for index in self.pc.list_indexes()]

    def add_index():
        Pinecone
        pass

    def delete_index():
        pass

    def __repr__():
        pass
