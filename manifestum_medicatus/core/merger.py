from typing import Any, Dict, List


def deep_merge(base: Any, override: Any, merge_lists: bool = True) -> Any:
    # Случай 1: оба — словари
    if isinstance(base, dict) and isinstance(override, dict):
        result = base.copy()
        for key, value in override.items():
            # Случай 1.1: оба значения — списки → объединяем
            if key in result and isinstance(result[key], list) and isinstance(value, list) and merge_lists:
                result[key] = deep_merge(result[key], value, merge_lists)
            # Случай 1.2: оба значения — словари → рекурсивный мердж
            elif key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = deep_merge(result[key], value, merge_lists)
            # Случай 1.3: иначе — заменяем
            else:
                result[key] = value
        return result

    # Случай 2: оба — списки → объединяем по уникальному ключу NAME
    elif isinstance(base, list) and isinstance(override, list) and merge_lists:
        key_field = "NAME"

        # Собираем все элементы из base в словарь для быстрого поиска
        merged_dict = {
            item[key_field]: item
            for item in base
            if isinstance(item, dict) and key_field in item
        }

        # Добавляем/заменяем элементы из override
        for item in override:
            if isinstance(item, dict) and key_field in item:
                merged_dict[item[key_field]] = item

        # Восстанавливаем порядок: сначала элементы из base, потом новые из override
        result = []
        seen = set()

        # Сохраняем порядок из base
        for item in base:
            if isinstance(item, dict) and key_field in item:
                key = item[key_field]
                if key not in seen:
                    result.append(merged_dict[key])
                    seen.add(key)

        # Добавляем новые элементы из override (которых не было в base)
        for item in override:
            if isinstance(item, dict) and key_field in item:
                key = item[key_field]
                if key not in seen:
                    result.append(item)
                    seen.add(key)

        return result

    # Случай 3: любые другие типы → заменяем base на override
    else:
        return override