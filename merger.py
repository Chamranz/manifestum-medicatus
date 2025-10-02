import yaml
from typing import List, Optional, Any, Dict

import os
from dotenv import load_dotenv


load_dotenv()


def _detect_unique_key(items: List[Dict]) -> Optional[str]:
    """Рекурсивно объединяем два словаря. override перетирает base.

        Args:
            items (List[Dict]):
                Базовый ямлик
            Optional (str:
                Ямлик с delta параметрами

        Returns:
            dict: Итоговый ямлик."""
    if not items:
        return None
    # Получаем пересечение ключей всех элементов
    common_keys = set(items[0].keys())
    for item in items[1:]:
        if not isinstance(item, dict):
            return None
        common_keys &= set(item.keys())
        if not common_keys:
            return None
    # Ищем уникальный ключ
    typical_keys = {"name", "id", "NAME", "AGENT_NAME", "branch"}
    for key in typical_keys:
        if key in common_keys:
            return key
    # Если нет стандартных — пробуем первый общий ключ
    if common_keys:
        return next(iter(common_keys))
    return None


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
            print(f"all_items: {all_items}, unique_key: {unique_key}")
            if unique_key:
                base_map = {item[unique_key]: item for item in base if unique_key in item}
                print(f"base_map: {base_map}")
                override_map = {item[unique_key]: item for item in override if unique_key in item}
                print(f"override_map: {override_map}")
                merged = {}

                for key, item in base_map.items():
                    merged[key] = item.copy()

                for key, item in override_map.items():
                    if key in merged:
                        merged[key] = deep_merge(merged[key], item)
                    else:
                        merged[key] = item

                result = []
                seen = set()
                for item in base:
                    if unique_key in item:
                        k = item[unique_key]
                        if k in merged:
                            result.append(merged[k])
                            seen.add(k)
                for item in override:
                    if unique_key in item and item[unique_key] not in seen:
                        result.append(item)
                        seen.add(item[unique_key])
                return result

        return override

    else:
        return override

