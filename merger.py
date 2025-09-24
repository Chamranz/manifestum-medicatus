import yaml

from templates.agents_model import AgentsConfig, Agent

import os
from dotenv import load_dotenv

load_dotenv()


def deep_merge(base: dict, override: dict) -> dict:
    """Рекурсивно объединяем два словаря. override перетирает base.

        Args:
            base (dict):
                Базовый ямлик
            override (dict):
                Ямлик с delta параметрами

        Returns:
            dict: Итоговый ямлик/"""
    result = base.copy()
    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = value
    return result


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
