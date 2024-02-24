from typing import Any, Dict, NewType, Optional, Union, List
from typing_extensions import Annotated

from pydantic import BaseModel, Field

serverless = NewType("serverless", str)
pod = NewType("pod", str)


class IndexModel(BaseModel):

    """
    Name:
        IndexModel

    Summary:
        The index args needed to create Index Vector Store
    """

    name: str = Field(...,
                      description="Name of Index. Required.")
    dimension: int = Field(default=1536,
                           description="The dimension of vectors that will be inserted in the index. Defaults to 1536.")
    metric: str = Field(default="cosine",
                        description="Values are 'euclidean','cosine', and 'dotproduct.' Defaults to 'cosine")
    server_type: Union[serverless, pod] = Field(default="pod",
                                                description="Choose between 'serverless' or 'pod' instance.")
    cloud: str = Field(default="aws", 
                       description="Used for Serverless instances. Defaults to 'aws'.")
    region: str = Field(default="us-west-2", 
                        description="Location for ServerlessSpec. Defaults to 'us-west-2'. Note: Current 'us-west-2' is only region.")
    environment: str = Field(default=None, 
                             description="Used in PodSpec same as region is Serverless Spec. Defaults to 'None'.")
    pod_type: str = Field(default="p1.x1", 
                          description="For PodSpec, used see documentation for specifics. Defaults to 'p1.x1'")
    metadata_config: Optional[Dict[str, Any]] = Field(default=None,
                                                      description="Metadata Schema, Defaults to empty dictionary.")


class IndexStatus(BaseModel):
    ready: bool = Field(..., required=True)
    state: str = Field(..., required=True)


class IndexMetadataConfig(BaseModel):
    indexed: Optional[List[str]] = Field(...)


class Pod(BaseModel):
    environment: str = Field(..., required=True)
    replicas: int = Field(..., required=True)
    shards: int = Field(...)
    pod_type: str = Field(..., require=True)
    pods: int = Field(..., required=True)
    metadata_config: Optional[IndexMetadataConfig] = Field(default=None)
    source_collection: Optional[str] = Field(default=None)


class Severless(BaseModel):
    cloud: str
    region: str


class IndexList(BaseModel):
    name: str = Field(..., required=True)
    dimension: int = Field(..., required=True)
    metric: str = Field(..., required=True)
    host: str
    spec: Union[Pod, Severless] = Field(..., required=True)
    status: IndexStatus


class IndexesResponse(BaseModel):
    indexes: List[IndexList]
