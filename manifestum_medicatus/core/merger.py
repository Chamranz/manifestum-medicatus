from typing import Any, Dict, List


def deep_merge(base: Any, override: Any, merge_lists: bool = False) -> Any:
    """Рекурсивное слияние конфигураций."""
    if isinstance(base, dict) and isinstance(override, dict):
        result = base.copy()
        for key, value in override.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = deep_merge(result[key], value, merge_lists)
            else:
                result[key] = value
        return result

    elif isinstance(base, list) and isinstance(override, list) and merge_lists:
        # Специальная логика для агентов (слияние по полю NAME)
        base_names = {item.get("NAME") for item in base if isinstance(item, dict) and "NAME" in item}
        result = base.copy()
        for item in override:
            if isinstance(item, dict) and item.get("NAME") not in base_names:
                result.append(item)
        return result

    else:
        return override