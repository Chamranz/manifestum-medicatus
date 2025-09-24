import sys
from pathlib import Path
from templates.agents_model import AgentsConfig
from reader import load_yaml_to_models
from merger import merge_agents, save_model_to_yaml


def main():
    if len(sys.argv) < 4:
        print("Использование: python main.py <base.yaml> <override.yaml> <output.yaml>")
        sys.exit(1)

    base_path = sys.argv[1]
    override_path = sys.argv[2]
    output_file = sys.argv[3]
    print(override_path)
    # Загружаем базовый и переопределяющие манифесты
    base_config = load_yaml_to_models(base_path)
    override_config = load_yaml_to_models(override_path)

    # Сливание 🚰
    merged_config = merge_agents(base_config, override_config)

    # Сохранеине
    save_model_to_yaml(merged_config, output_file)
    print(f"Done: {output_file}")


if __name__ == "__main__":
    main()