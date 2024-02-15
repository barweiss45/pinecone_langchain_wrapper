#! /usr/bin/env python3

import os
from typing import Any, Dict, NewType, Union

from dotenv import load_dotenv
from langchain_pinecone import Pinecone
from pinecone import IndexDescription, IndexList, DescribeIndexStatsResponse
from pinecone import Pinecone as PineconeClient
from pinecone import PodSpec, ServerlessSpec

serverless = NewType("serverless", str)
pod = NewType("pod", str)

load_dotenv()


class PineconeConnector(object):

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
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
                     server_type: Union[serverless, pod] = "pod",
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

        if server_type == "pod":
            spec = PodSpec(environment,
                           pod_type=pod_type,
                           pods=1,
                           metadata_config=metadata_config)
        elif server_type == "serverless":
            spec = ServerlessSpec(cloud, region="us-west-2")  # only availabe in us-west-2
        else:
            raise ValueError("Incorrect Server type. Choose either ServerlessSpec or PodSpec")

        self.pc.create_index(
            index_name,
            dimension,
            spec,
            metric,
            )
        return True

    def describe_index(self, index_name: str) -> IndexDescription:
        """Describe a Specific index"""
        return self.pc.describe_index(index_name)

    def describe_index_stats(self, index_name: str) -> DescribeIndexStatsResponse:
        index = self.pc.Index(index_name)
        return index.describe_index_stats()

    def list_index(self) -> IndexList:
        """Lists all Pinecone Indexes"""
        return [index for index in self.pc.list_indexes()]

    def add_index():
        pass

    def delete_index(self, index_name: str, time_out: int | None = None):
        try:
            return self.pc.delete_index(index_name, time_out)
        except TimeoutError as e:
            # Timeout in seconds
            raise f"{e}: Deleteing of {index_name} timed out."

    def __repr__(self):
        return "Pinceconnector(embeddings={self.embeddings!r}, OPENAI_API_KEY={self.OPENAI_API_KEY!r}, PINECONE_API_KEY={self.PINECONE_API_KEY!r}, PINECONE_ENV={self.PINECONE_ENV!r})"
