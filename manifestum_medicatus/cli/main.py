import os
import sys
import logging
from typing import List, Dict, Any
from pathlib import Path
import yaml

from ..core.merger import deep_merge
from ..core.validator import validate_manifest
from ..models.stub import StubConfig

# Слои по стендам (можно вынести в конфиг)
LAYER_CONFIG = {
    "DEV": ["general", "PREPROM", "DEV"],
    "IFT1": ["general", "PREPROM", "IFT", "IFT1"],
    "IFT2": ["general", "PREPROM", "IFT", "IFT2"],
    "PROM1": ["general", "PROM", "PROM1"],
    "PROM2": ["general", "PROM", "PROM2"],
    "PSI1": ["general", "PSI", "PSI1"],
    "PSI2": ["general", "PSI", "PSI2"],
}

MANIFEST_NAMES = ["agents", "common", "integrations", "namespace"]

def load_partial_config(config_dir: Path, manifest_type: str, layer: str) -> Dict[str, Any]:
    """Загрузка частичного конфига из Python-модуля."""
    if layer == "general":
        file_path = config_dir / manifest_type / "general.py"
    else:
        file_path = config_dir / manifest_type / layer / f"{layer.lower()}.py"

    if not file_path.exists():
        raise FileNotFoundError(f"Файл не найден: {file_path}")

    # Импорт модуля (без использования importlib — безопаснее через exec)
    namespace = {}
    with open(file_path, "r", encoding="utf-8") as f:
        code = compile(f.read(), file_path, "exec")
        exec(code, namespace)

    if "get_config" not in namespace:
        raise AttributeError(f"Модуль {file_path} не содержит функцию 'get_config'")

    try:
        return namespace["get_config"]()
    except Exception as e:
        logging.warning(f"Ошибка в {file_path}, используем заглушку: {e}")
        return StubConfig().model_dump()

def generate_manifests(config_dir: str, output_dir: str, stands: List[str] = None) -> None:
    """Генерация манифестов для указанных стендов."""
    config_path = Path(config_dir)
    output_path = Path(output_dir)
    stands = stands or list(LAYER_CONFIG.keys())

    for manifest_name in MANIFEST_NAMES:
        for stand in stands:
            if stand not in LAYER_CONFIG:
                logging.warning(f"Стенд {stand} не определён в LAYER_CONFIG")
                continue

            merged = {}
            for layer in LAYER_CONFIG[stand]:
                try:
                    layer_config = load_partial_config(config_path, manifest_name, layer)
                    merged = deep_merge(merged, layer_config, merge_lists=False)
                except Exception as e:
                    logging.error(f"Ошибка на слое {layer} для {stand}/{manifest_name}: {e}")
                    sys.exit(1)

            # Валидация
            validated = validate_manifest(manifest_name, merged)

            # Сохранение
            if manifest_name == "common":
                output_file = output_path / manifest_name / "COMMON.yaml"
            else:
                output_file = output_path / manifest_name / f"{stand}.yaml"

            output_file.parent.mkdir(parents=True, exist_ok=True)
            with open(output_file, "w", encoding="utf-8") as f:
                yaml.safe_dump(
                    validated.model_dump(),
                    f,
                    allow_unicode=True,
                    default_flow_style=False,
                    sort_keys=False,
                    indent=2,
                )
            logging.info(f"Сохранено: {output_file}")

def main() -> None:
    """Точка входа консольной утилиты."""
    import argparse

    parser = argparse.ArgumentParser(description="Генерация конфигураций Manifestum Medicatus")
    parser.add_argument("--config-dir", default="manifests_diff", help="Директория с исходными конфигами")
    parser.add_argument("--output-dir", default="./", help="Директория для результатов")
    parser.add_argument("--stands", nargs="+", default=None, help="Список стендов (по умолчанию все)")
    parser.add_argument("--verbose", action="store_true", help="Подробный вывод")

    args = parser.parse_args()
    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO)

    generate_manifests(
        config_dir=args.config_dir,
        output_dir=args.output_dir,
        stands=args.stands
    )

if __name__ == "__main__":
    main()