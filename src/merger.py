from typing import Any
import logging

logger = logging.getLogger(__name__)

def deep_merge(base: Any, override: Any) -> Any:
    """Рекурсивно объединяем два словаря. override перетирает base.

    Если оба аргумента — словари, происходит рекурсивное слияние. Если список - то просто вставляется значение из override
    Значения из override имеют приоритет.

        Args:
            base (Any):
                Базовый ямлик
            override (Any):
                Текущий ямлик

        Returns:
            dict: Итоговый ямлик."""
    if isinstance(base, dict) and isinstance(override, dict):
        result = base.copy()

        for key in base:
            if key not in override:
                logger.debug("Сохранено из базового конфига (отсутствует в override): %s = %r", key, base[key])

        for key, value in override.items():
            if key in result:
                result[key] = deep_merge(result[key], value)
            else:
                #print(value)
                result[key] = value
        return result

    else:
        #print(override)
        return override

