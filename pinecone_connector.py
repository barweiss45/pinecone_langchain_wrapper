#! /usr/bin/env python3

import os
from typing import Any, Dict, List, NewType, Optional, Union

from dotenv import load_dotenv
from pinecone import DescribeIndexStatsResponse, IndexDescription, IndexList
from pinecone import Pinecone as PineconeClient
from pinecone import PodSpec, ServerlessSpec

"""
Provides management features to Pinecone Vectorstore
Use Langchain for adding vectors and searches
"""

serverless = NewType("serverless", str)
pod = NewType("pod", str)

load_dotenv()


class PineconeConnector(object):
    # Note may not need Singleton
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(PineconeConnector, cls).__new__(cls)
        return cls._instance

    def __init__(self, embeddings, index_names: Optional[List[str]] = None):
        self.embeddings = embeddings
        self.index_names = index_names
        self.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        self.PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

        if not hasattr(self, 'pc'):
            if self.OPENAI_API_KEY is None:
                raise ValueError("Issue with Pinecone API Key. Value is None.")
            self.pc = PineconeClient(self.PINECONE_API_KEY)

    def create_index(self,
                     index_name: str,
                     dimension: int = 1536,
                     metric: str = "cosine",
                     server_type: Union[serverless, pod] = "pod",
                     cloud: str = "aws",
                     region: str = "us-west-2",
                     environment: str = None,
                     pod_type: str = "p1.x1",
                     metadata_config: Dict[str, Any] = {},) -> bool:
        """
        create_index Wrapper to create Pinecone Index

        Args:
            index_name (str): The name of the index to create.
            dimension (int, optional): The dimension of vectors that will be inserted in the index. Defaults to 1536.
            metric (str, optional): Distance calculation used. Values may be "euclidean",
                                    "cosine", and "dotproduct." Defaults to "cosine".
            cloud (str, optional): Used for Serverless instances. Defaults to "aws".
            region (str, optional): Location for ServerlessSpec. Defaults to "us-west-2". Note: Current us-west-2 is only available region.
            environment (str, optional): Used in PodSpec same as region is Serverless Spec. Defaults to "None".
            pod_type (str, optional): Used in PodSpec, Pod type and size used see documentation for specifics. Defaults to "p1.x1"
            metadata_config (Dict[str, Any]): Metat Data Schema, Defaults to empty dictionary.)
        """
        if index_name in self.pc.list_indexes().names():
            return False

        if server_type == "pod":
            spec = PodSpec(environment,
                           pod_type=pod_type,
                           pods=1,
                           metadata_config=metadata_config)
        elif server_type == "serverless":
            spec = ServerlessSpec(cloud, region=region)  # only availabe in us-west-2
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

    def delete_index(self, index_name: str, time_out: int | None = None):
        try:
            return self.pc.delete_index(index_name, time_out)
        except TimeoutError as e:
            # Timeout in seconds
            raise f"{e}: Deleteing of {index_name} timed out."

    def __repr__(self):
        return "Pinceconnector(embeddings={self.embeddings!r}, OPENAI_API_KEY={self.OPENAI_API_KEY!r}, PINECONE_API_KEY={self.PINECONE_API_KEY!r}, PINECONE_ENV={self.PINECONE_ENV!r})"
