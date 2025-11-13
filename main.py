import sys
import importlib.util
import os
from dotenv import load_dotenv
from src.merger import deep_merge
from src.reader import load_yaml
from src.saver import save_yaml
from src.cleaner import remove_empty_lists
import logging

logging.basicConfig(level=logging.DEBUG)
load_dotenv()

MANIFEST_NAMES = ["agents", "integrations", "namespace"]
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


def load_by_params(manifest_type: str, layer: str):
    var_name = f"{layer.lower()}_params"
    if layer == "general":
        file_path = f"manifests_diff/{manifest_type}/{layer.lower()}.py"
    else:
        file_path = f"manifests_diff/{manifest_type}/{layer}/{layer.lower()}.py"
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File {file_path} not found")

    spec = importlib.util.spec_from_file_location("mod", file_path)
    module =importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    print("ok")

    if not hasattr(module, var_name):
        raise AttributeError(f"Module {file_path} has no attribute {var_name}")
    return getattr(module, var_name)



def main():

    for manifest_name in MANIFEST_NAMES:
        base = load_yaml(f"base_manifests/{manifest_name}.yaml")

        for stand in STANDS:
            if stand not in LAYER:
                logging.warning(f"Stand {stand} is not defined")
                continue

            current = base.copy()

            for layer in LAYER[stand]:
                try:
                    layer_params = load_by_params(manifest_name, layer)
                    current = deep_merge(current, layer_params, merge_lists=True)
                except (FileNotFoundError, AttributeError) as e:
                    logging.warning(f"Could not load layer {layer}: {e}")
                    sys.exit(1)

            current = remove_empty_lists(current)

            output_path = f"merged_manifests/{manifest_name}/{stand}.yaml"
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, "w", encoding="utf-8") as f:
                import yaml
                yaml.dump(current, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
            logging.info(f"Сохранено: {output_path}")



if __name__ == "__main__":
    main()