from typing import Dict, Any
from ..models.agents import AgentConfig
from ..models.common import CommonConfig
from ..models.namespace import NamespaceConfig
from ..models.integrations import IntegrationConfig

_MANIFEST_TYPES = {
    "agents": AgentConfig,
    "common": CommonConfig,
    "namespace": NamespaceConfig,
    "integrations": IntegrationConfig,
}


def validate_manifest(manifest_type: str, data: Dict[str, Any]) -> Any:
    """Валидация словаря конфигурации через Pydantic-модели."""
    if manifest_type not in _MANIFEST_TYPES:
        raise ValueError(f"Неизвестный тип манифеста: {manifest_type}")

    model_class = _MANIFEST_TYPES[manifest_type]
    return model_class(**data)