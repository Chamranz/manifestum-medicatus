import yaml
from templates.agents_model import AgentsConfig


def load_yaml_to_models(yaml_file: str) -> AgentsConfig:
    """Загружает и возвращает дыямлик.

            Args:
                yaml_file (str):
                    Назваине файла, из которого нужно взять изменения.

            Returns:
                AgentsConfig: Модель пайдентик с параметрами из файлика"""
    with open(yaml_file, "r", encoding="utf-8") as f:
        raw_data = yaml.safe_load(f)
    print(raw_data)
    return AgentsConfig(agents=raw_data)