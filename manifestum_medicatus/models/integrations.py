from pydantic import BaseModel, Field
from typing import List, Optional, Union

class MtlsConfig(BaseModel):
    NAME: str = "Укажи меня"
    HOST: str = "Укажи меня"
    PORT: int = "Укажи меня"

class Host(BaseModel):
    HOST: str = "Укажи меня"
    PORT: int = "Укажи меня"

class ClustersConfig(BaseModel):
    NAME: str = "Укажи меня"
    HOSTS: List[Host] = "Укажи меня"
    MESH_PORT: int = "Укажи меня"
    PROTOCOL: str = "Укажи меня"

class KafkaConfig(BaseModel):
    CLUSTERS: List[ClustersConfig] = "Укажи меня"

class IngressWhiteListConfig(BaseModel):
    NAME: str = "Укажи меня"
    CN: str = "Укажи меня"
    PATH: str = "Укажи меня"

class MtlsOttConfig(BaseModel):  # переименовано для PEP8
    NAME: str = "Укажи меня"
    HOST: str = "Укажи меня"
    PORT: int = "Укажи меня"
    INNERPORT: int = "Укажи меня"

class IntegrationConfig(BaseModel):
    MTLS: List[MtlsConfig] = "Укажи меня"
    KAFKA: KafkaConfig = "Укажи меня"
    INGRESS_WHITELIST: List[IngressWhiteListConfig] = "Укажи меня"
    MTLS_OTT: Optional[List[Union[MtlsOttConfig, MtlsConfig]]] = Field(default_factory=list)