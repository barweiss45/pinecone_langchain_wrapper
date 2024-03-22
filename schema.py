from typing import Any, Dict, List, NewType, Optional, Union

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

    name: str = Field(..., description="Name of Index. Required.")
    dimension: int = Field(
        default=1536,
        description="Dimension of vectors inserted into index. Default 1536.",
    )
    metric: str = Field(
        default="cosine",
        description="'euclidean','cosine', or 'dotproduct.' Default 'cosine",
    )
    server_type: Union[serverless, pod] = Field(
        default="pod",
        description="Choose 'serverless' or 'pod' instance. Default 'pod'.",
    )
    cloud: str = Field(
        default="aws", description="Used for Serverless instances. Default 'aws'."
    )
    region: str = Field(
        default="us-west-2",
        description="Location for ServerlessSpec. Default 'us-west-2'.b",
    )
    environment: str = Field(
        default=None,
        description="Used for PodSpec. Default 'None'.",
    )
    pod_type: str = Field(
        default="p1.x1",
        description="Used for PodSpec. Defaults 'p1.x1'",
    )
    metadata_config: Optional[Dict[str, Any]] = Field(
        default=None, description="Metadata Schema. Default {}."
    )


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


class ResponseMessage(BaseModel):
    success: bool = Field(...)
    # Leav as Any for now
    message: Any = Field(...)
