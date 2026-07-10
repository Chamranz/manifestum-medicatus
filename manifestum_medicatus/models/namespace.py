from pydantic import BaseModel, Field
from typing import Optional, List, Dict

class CpuMemoryResources(BaseModel):
    CPU: str = "Укажи меня"
    MEMORY: Optional[str] = None

class CpuMemoryResourcesMem(BaseModel):
    CPU: str = "Укажи меня"
    MEM: Optional[str] = None

class ResourceSpec(BaseModel):
    REPLICAS: Optional[int] = None
    LIMITS: Optional[CpuMemoryResources] = None
    REQUESTS: Optional[CpuMemoryResources] = None

class IstioLogs(BaseModel):
    TOPIC: str = "Укажи меня"
    KAFKA_CLUSTER_NAME: str = "Укажи меня"

class PGConfig(BaseModel):
    name: str = "Укажи меня",
    path: str = "Укажи меня",
    db_host: str = "Укажи меня",
    db_port: str = "Укажи меня",
    db_name: str = "Укажи меня",

    custom_string: str = None
    volume_path: str = None

class SecManConfig(BaseModel):
    HOST: str = "Укажи меня"
    ROLE_NAME: str = "Укажи меня"
    NAMESPACE: str = "Укажи меня"
    SBER_CA_KV_SERVER_PATH: str = "Укажи меня"
    SBER_CA_KV_CLIENT_PATH: str = "Укажи меня"
    SBER_CA_CLIENT_CN: str = "Укажи меня"
    SBER_CA_SERVER_CN: str = "Укажи меня"
    INGRESS_GW_SAN: str = "Укажи меня"

    # Опциональные поля
    CERT_KV_PATH: Optional[str] = None
    ENV_KV_PATH: Optional[str] = None
    SBER_CA_OTT_CN: Optional[str] = None
    SBER_CA_KV_OTT_CLIENT_PATH: Optional[str] = None
    SECRETS_KV_PATH: Optional[str] = None
    EGRESS_CUSTOM_CA_KV_PATH: Optional[str] = None
    INGRESS_CUSTOM_CA_KV_PATH: Optional[str] = None
    SECRET_FILES: Optional[List[str]] = None

    PG: Optional[List[PGConfig]] = None

class GeoroutesConfig(BaseModel):
    HOST: str = "Укажи меня"
    PORT: int = 2442

class PatternsAgentConfig(BaseModel):
    HOST: str = "Укажи меня"
    PORT: int = 5443
    GEOROUTES: Optional[Dict[str, GeoroutesConfig]] = None

class IngressConfig(BaseModel):
    CONNECT_TIMEOUT: Optional[str] = None
    READ_TIMEOUT: Optional[str] = None
    SEND_TIMEOUT: Optional[str] = None
    NETWORKING_MTLS: Optional[Dict[str, PatternsAgentConfig]] = "Укажи меня"
    NETWORKING_OTT_MTLS: Optional[Dict[str, PatternsAgentConfig]] = "Укажи меня"

class IstioConfig(BaseModel):
    INGRESS: IngressConfig = "Укажи меня"

class AppLogconfig(BaseModel):
    MOUNT_PATH: str = "/var/log/app"
    MOUNT_FILE: str = "app.log"
    KAFKA_CLUSTER_NAME: Optional[str] = None
    TOPIC: Optional[str] = None

class FluentBitConfig(BaseModel):
    RESOURCES: ResourceSpec = "Укажи меня"
    APP_LOG: Optional[AppLogconfig] = None
    IMAGE: Optional[str]  = None
    ISTIO_LOGS: Optional[IstioLogs] = None

class OttConfig(BaseModel):
    HOST: Optional[str] = None
    BILLING_ACCOUNT: Optional[str] = None
    RESOURCES: ResourceSpec = None
    OTT_OPER_MODE_INGRESS: str = "Укажи меня"

class DynamicInventoryConfig(BaseModel):
    AUTH_TOKENS_URL: str = "Укажи меня"
    DEPLOYMENTS_URL: str = "Укажи меня"

class ServiceConfigWithResources(BaseModel):
    RESOURCES: ResourceSpec

class ServiceConfig(BaseModel):
    LIMITS: Optional[CpuMemoryResourcesMem] = None
    REQUESTS: Optional[CpuMemoryResourcesMem] = None

class NamespaceConfig(BaseModel):
    # Обязательные корневые поля
    GIT_SSH_CREDENTIAL_ID: str = "Укажи меня"
    PASS_CREDENTIAL_ID: str = "Укажи меня"
    DROPAPP_CLUSTER: str = "Укажи меня"
    DROPAPP_CREDENTIAL_ID: str = "Укажи меня"
    DROPAPP_NAMESPACE: str = "Укажи меня"
    EIGW_NAMESPACE: str = "Укажи меня"
    STAND_ID: str = "Укажи меня"
    STAND_TYPE: str = "Укажи меня"

    # Опциональные корневые поля
    K8S_TYPE: Optional[str] = None
    SSM_CP: Optional[str] = None

    SECMAN: Optional[SecManConfig] = None
    ISTIO: Optional[IstioConfig] = None
    FLUENT_BIT: Optional[FluentBitConfig] = None
    OTT: Optional[OttConfig] = None

    DYNAMIC_INVENTORY: Optional[DynamicInventoryConfig] = None

    INJECTEDISTIO: Optional[ServiceConfig] = None
    HASHICORP: Optional[ServiceConfig] = None
    INGRESS: Optional[ServiceConfigWithResources] = None
    EGRESS: Optional[ServiceConfigWithResources] = None