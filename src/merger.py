from typing import Any
import logging

logger = logging.getLogger(__name__)

def deep_merge(base: Any, override: Any, merge_lists: bool = False) -> Any:
    """
    Рекурсивно объединяет два объекта.
    
    - Если оба словари, то мерджим рекурсивно.
    - Если оба списки и `merge_lists=True` → конкатенируем.
    - Иначе override полностью заменяет base.
    
    Args:
        base: базовое значение
        override: переопределяющее значение
        merge_lists: если True и оба значения — списки, то объединить их; иначе override заменяет base.

    Returns:
        Итоговое значение.
    """
    if isinstance(base, dict) and isinstance(override, dict):
        result = base.copy()

        for key in base:
            if key not in override:
                #logger.debug("Сохранено из базового конфига (отсутствует в override): %s = %r", key, base[key])
                pass

        for key, value in override.items():
            if key in result:
                result[key] = deep_merge(result[key], value, merge_lists=merge_lists)
            else:
                result[key] = value
        return result

    elif merge_lists and isinstance(base, list) and isinstance(override, list):
        return base + override

    else:
        return override

