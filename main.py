import sys
import importlib.util
import os
from dotenv import load_dotenv
from src.validator import validate
from models.agents import AgentConfig
from src.merger import deep_merge
from src.reader import load_yaml
from src.saver import save_yaml
from src.cleaner import remove_empty_lists
import logging

from manifests_diff import agents
from manifests_diff.agents.PSI import psi
from models.stub import StubConfig
logging.basicConfig(level=logging.DEBUG)
load_dotenv()

MANIFEST_NAMES = ["agents", "common", "integrations", "namespace"]
STANDS = ["DEV", "IFT1", "IFT2", "PROM1", "PROM2", "PSI1", "PSI2"]

LAYER = {
    "DEV": ["general", "PREPROM", "DEV"],
    "IFT1": ["general", "PREPROM", "IFT", "IFT1"],
    "IFT2": ["general", "PREPROM", "IFT", "IFT2"],
    "PROM1": ["general", "PROM", "PROM1"],
    "PROM2": ["general", "PROM", "PROM2"],
    "PSI1": ["general", "PSI", "PSI1"],
    "PSI2": ["general", "PSI", "PSI2"],
}


def load_partial_config(manifest_type: str, layer: str):
    if layer == "general":
        file_path = f"manifests_diff/{manifest_type}/general.py"
    else:
        file_path = f"manifests_diff/{manifest_type}/{layer}/{layer.lower()}.py"
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    spec = importlib.util.spec_from_file_location("mod", file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    if not hasattr(module, "get_config"):
        raise AttributeError(f"Module {file_path} has no function 'get_config'")

    try:
        partial_obj = module.get_config()
    except Exception as e:
        print(f"STUUUUUUB {e}")
        partial_obj = StubConfig()

    # Преобразуем в словарь для слияния
    return partial_obj



def main():
    for manifest_name in MANIFEST_NAMES:
        for stand in STANDS:
            if stand not in LAYER:
                logging.warning(f"Stand {stand} is not defined")
                continue

            merged_dict = {} # Инициализация дикта с конфигами
            for layer in LAYER[stand]:
                try:
                    print(f' start with layer {layer} and stand {stand}, manifest {manifest_name}')
                    layer_dict = load_partial_config(manifest_name, layer)
                    merged_dict = deep_merge(merged_dict, layer_dict, merge_lists=False)
                except Exception as e:
                    logging.error(f"Ошибка на слое {layer} и стенде {stand}: {e}")
                    sys.exit(1)

            final_obj = validate(manifest_name, merged_dict)

            output_path = f"merged_manifests/{manifest_name}/{stand}.yaml"

            if manifest_name == "common":
                output_path = f"merged_manifests/{manifest_name}/COMMON.yaml"

            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, "w", encoding="utf-8") as f:
                import yaml
                data_dict = final_obj.model_dump()
                yaml.safe_dump(
                    data_dict,
                    f,
                    allow_unicode=True,
                    default_flow_style=False,
                    sort_keys=False,
                    indent=2,  # для красивых отступов
                    width=1000  # предотвращает разрыв длинных строк
                )


if __name__ == "__main__":
    main()