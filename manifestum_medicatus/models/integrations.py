from pydantic import BaseModel, Field
from typing import List, Optional

class MtlsConfig(BaseModel):
    NAME: str = "Укажи меня"
    HOST: str = "Укажи меня"
    PORT: int = "Укажи меня"

class KafkaConfig(BaseModel):
    NAME: str = "Укажи меня"
    HOST: str = "Укажи меня"
    IP: str = "Укажи меня"
    PORT: int = "Укажи меня"

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
    KAFKA: List[KafkaConfig] = "Укажи меня"
    INGRESS_WHITELIST: List[IngressWhiteListConfig] = "Укажи меня"
    MTLS_OTT: Optional[List[MtlsOttConfig]] = Field(default_factory=list)