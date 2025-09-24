import yaml
from typing import List, Optional, Any, Dict

from templates.agents_model import AgentsConfig, Agent

import os
from dotenv import load_dotenv

load_dotenv()


def _detect_unique_key(items: List[Dict]) -> Optional[str]:
    """Определяет, есть ли общий уникальный ключ во всех элементах списка."""
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
    # Ищем кандидатов на уникальный ключ (часто: name, id, AGENT_NAME, NAME и т.д.)
    candidates = {"name", "id", "NAME", "AGENT_NAME", "branch", "HOST", "CN"}
    for key in candidates:
        if key in common_keys:
            return key
    # Если нет стандартных — пробуем первый общий ключ
    if common_keys:
        return next(iter(common_keys))
    return None

def deep_merge(base: Any, override: Any) -> Any:
    """Универсальный рекурсивный merge для любых структур."""
    # Случай 1: оба — словари
    if isinstance(base, dict) and isinstance(override, dict):
        result = base.copy()
        for key, value in override.items():
            if key in result:
                result[key] = deep_merge(result[key], value)
            else:
                result[key] = value
        return result

    # Случай 2: оба — списки
    elif isinstance(base, list) and isinstance(override, list):
        # Попробуем определить, есть ли уникальный ключ
        all_items = base + override
        if all(isinstance(x, dict) for x in all_items):
            unique_key = _detect_unique_key(all_items)
            if unique_key:
                # Сливаем по уникальному ключу
                base_map = {item[unique_key]: item for item in base if unique_key in item}
                override_map = {item[unique_key]: item for item in override if unique_key in item}
                merged = base_map.copy()
                merged.update(override_map)  # override перетирает base
                # Сохраняем порядок: сначала base (в исходном порядке), потом новые из override
                result = []
                seen = set()
                for item in base:
                    if unique_key in item:
                        key_val = item[unique_key]
                        if key_val in merged:
                            result.append(merged[key_val])
                            seen.add(key_val)
                for item in override:
                    if unique_key in item and item[unique_key] not in seen:
                        result.append(item)
                        seen.add(item[unique_key])
                return result

        # Если не смогли определить уникальный ключ — заменяем весь список
        return override

    # Случай 3: простые значения — override побеждает
    else:
        return override


def merge_agents(base: AgentsConfig, override: AgentsConfig) -> AgentsConfig:
    """Та же самя функция только работа теперь с моделями пайдентик.

        Args:
            base (AgentsConfig):
                Базовый ямлик в виде пайдентик модели
            override (AgentsConfig):
                Ямлик с delta параметрами в виде пайдентик модели

        Returns:
            AgentsConfig: Итоговый ямлик в виде пайдентик модели."""
    merged_agents = []
    override_map = {agent.AGENT_NAME: agent for agent in override.agents}

    for base_agent in base.agents:
        agent_name = base_agent.AGENT_NAME
        if agent_name in override_map:
            override_agent = override_map[agent_name]

            # Конвертация модели в словари
            base_dict = base_agent.dict(exclude_unset=True)
            override_dict = override_agent.dict(exclude_unset=True)

            # Сливаем
            merged_dict = deep_merge(base_dict, override_dict)

            # Создаем новую модель
            merged_agent = Agent(**merged_dict)
            merged_agents.append(merged_agent)
        else:
            # Если агента нет в override — оставляем как есть
            merged_agents.append(base_agent)

    return AgentsConfig(agents=merged_agents)


def save_model_to_yaml(config: AgentsConfig, output_file: str) -> None:
    """Извлекаем список агентов.

            Args:
                config (AgentsConfig):
                    Базовый ямлик в виде пайдентик модели
                output_path (str):
                    Куда сохраняем - считывается с .env."""

    agents_list = [agent.dict(exclude_none=True, by_alias=True) for agent in config.agents]
    output_path = os.getenv("OUTPUT_PATH")
    result_file = os.path.join(output_path, f"{output_file}.yaml")
    with open(result_file, "w", encoding="utf-8") as f:
        yaml.dump(agents_list, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
