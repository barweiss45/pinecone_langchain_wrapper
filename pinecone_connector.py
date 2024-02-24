#! /usr/bin/env python3

import json
import logging
import os
from typing import List, NewType, Optional, Dict, Any

from pinecone import Pinecone as PineconeClient
from pinecone import PodSpec, ServerlessSpec, exceptions

from schema import IndexModel, IndexList, IndexStatus, Pod, Severless, IndexesResponse

"""
Provides management features to Pinecone Vectorstore
Use Langchain for adding vectors and searches
"""

serverless = NewType("serverless", str)
pod = NewType("pod", str)


logger = logging.getLogger(__name__)


class PineconeConnector:

    """PineconeConnect"""

    def __init__(self, embeddings, index_names: Optional[List[str]] = None):
        self.embeddings = embeddings
        self.index_names = index_names
        self.PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

        if not hasattr(self, 'pc'):
            if self.PINECONE_API_KEY is None:
                raise ValueError("Issue with Pinecone API Key. Value is None.")
            self.pc = PineconeClient(self.PINECONE_API_KEY)

    def create_index(self, index: IndexModel) -> bool:
        """create_index Wrapper to create Pinecone Index"""

        if index.name in self.pc.list_indexes().names():
            return json.dumps({"success": False, "message": f"{index.name} already exists."})

        if index.server_type == "pod":
            spec = PodSpec(index.environment,
                           pod_type=index.pod_type,
                           pods=1,
                           metadata_config=index.metadata_config)
        elif index.server_type == "serverless":
            spec = ServerlessSpec(index.cloud, region=index.region)  # only availabe in us-west-2
        else:
            raise ValueError("Incorrect Server type. Choose either ServerlessSpec or PodSpec")

        self.pc.create_index(
            index.name,
            index.dimension,
            spec,
            index.metric,
            )
        return {"success": True, "message": f"{index.name} successfully."}

    def describe_index(self, index_name: str):
        """Describe a Specific index"""
        return self.pc.describe_index(index_name)

    def describe_index_stats(self, index_name: str):
        try:
            index = self.pc.Index(index_name)
            return index.describe_index_stats()
        except exceptions.NotFoundException as e:
            logger.warning("%s: %s index not found", e, index_name)

    def list_index(self):
        """Lists all Pinecone Indexes"""
        indexes = [index for index in self.pc.list_indexes()]
        return indexes


    def delete_index(self, index_name: str, time_out: int | None = None):
        try:
            return self.pc.delete_index(index_name, time_out)
        except TimeoutError as e:
            # Timeout in seconds
            raise f"{e}: Deleteing of {index_name} timed out."
