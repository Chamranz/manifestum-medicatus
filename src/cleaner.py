import os
import yaml
from typing import Any, Dict, List, Set
# Корневые опциональные секции (удаляются целиком)
OPTIONAL_SECTIONS = {
    "MTLS_OTT",
    "KAFKA",
    "POSTGRES",
    "GRPC",
    "FLUENT_BIT",
    "OTT",
    "ISTIO",
    "REFLEX",
    "INJECTEDISTIO",
    "HASHICORP",
    "GR",
}


OPTIONAL_SCHEMA_PATH = os.path.join(os.path.dirname(__file__), "optional_fields.yaml")

_optional_schema_cache = None


def load_optional_schema():
    global _optional_schema_cache
    if _optional_schema_cache is None:
        with open(OPTIONAL_SCHEMA_PATH, "r", encoding="utf-8") as f:
            _optional_schema_cache = yaml.safe_load(f) or {}
    return _optional_schema_cache

def remove_optional_fields(data: Dict[str, Any], manifest_type: str) -> Dict[str, Any]:
    schema = load_optional_schema()
    manifest_schema = schema.get(manifest_type, {})

    if not isinstance(data, dict):
        return data

    cleaned = data.copy()

    root_optional = manifest_schema.get("__root_optional_fields__", [])
    for field in root_optional:
        print(f"Removing {field}")
        cleaned.pop(field, None)

    for block_key, optional_fields in manifest_schema.items():
        if block_key == "__root_optional_fields__":
            continue
        if block_key in cleaned and isinstance(cleaned[block_key], dict):
            inner = cleaned[block_key]
            for field in optional_fields:
                inner.pop(field, None)


    return cleaned

def remove_empty_lists(data: dict) -> dict:
    if not isinstance(data, dict):
        return data
    cleaned = {}
    for k, v in data.items():
        if isinstance(v, list) and len(v) == 0:
            continue  # пропускаем пустые списки
        elif isinstance(v, dict):
            cleaned[k] = remove_empty_lists(v)
        else:
            cleaned[k] = v
    return cleaned


def strip_optional_from_base(base: dict, optional_keys: set = OPTIONAL_SECTIONS) -> dict:
    if not isinstance(base, dict):
        return base
    cleaned = base.copy()
    for key in optional_keys:
        cleaned.pop(key, None)
    return cleaned
