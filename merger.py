import yaml
from typing import List, Optional, Any, Dict

import os
from dotenv import load_dotenv


load_dotenv()


def _detect_unique_key():
    ...


def deep_merge(base: Any, override: Any) -> Any:
    """Рекурсивно объединяем два словаря. override перетирает base.

        Args:
            base (Any):
                Базовый ямлик
            override (Any):
                Ямлик с delta параметрами

        Returns:
            dict: Итоговый ямлик."""
    if isinstance(base, dict) and isinstance(override, dict):
        result = base.copy()
        for key, value in override.items():
            if key in result:
                result[key] = deep_merge(result[key], value)
            else:
                result[key] = value
        return result

    elif isinstance(base, list) and isinstance(override, list):
        all_items = base + override
        if all(isinstance(x, dict) for x in all_items):
            unique_key = _detect_unique_key(all_items)
            if unique_key:
                base_map = {item[unique_key]: item for item in base if unique_key in item}
                override_map = {item[unique_key]: item for item in override if unique_key in item}

                merged = {}
