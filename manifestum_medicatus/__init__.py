"""Manifestum Medicatus — библиотека для генерации конфигураций."""

# Экспортируем основные компоненты для удобного импорта
from .core.merger import deep_merge
from .core.validator import validate_manifest
from .core.cleaner import remove_optional_fields
from .models.agents import AgentConfig
from .models.common import CommonConfig
from .models.namespace import NamespaceConfig
from .models.integrations import IntegrationConfig
from .models.stub import StubConfig

__version__ = "0.1.0"
__all__ = [
    "deep_merge",
    "validate_manifest",
    "remove_optional_fields",
    "AgentConfig",
    "CommonConfig",
    "NamespaceConfig",
    "IntegrationConfig",
    "StubConfig",
]