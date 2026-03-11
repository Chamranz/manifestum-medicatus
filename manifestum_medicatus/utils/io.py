"""IO utilities for reading/writing YAML configurations."""
import os
import yaml
from pathlib import Path
from typing import Any, Dict, Union


def load_yaml(path: Union[str, Path]) -> Dict[str, Any]:
    """Загрузка YAML-файла."""
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Файл не найден: {path}")

    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def dump_yaml(data: Dict[str, Any], output_path: Union[str, Path], manifest_type: str) -> None:
    """Сохранение данных в YAML-файл."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if manifest_type == "agents":
        data = [data]
    with open(output_path, "w", encoding="utf-8") as f:
        yaml.safe_dump(
            data,
            f,
            allow_unicode=True,
            default_flow_style=False,
            sort_keys=False,
            indent=2,
            width=1000
        )
    print(f"Сохранено: {output_path}")


def save_manifests(
        manifests: Dict[str, Dict[str, Any]],
        stands: list[str]
) -> None:
    """
    Сохранение сгенерированных манифестов в файловую систему.

    Args:
        manifests: Словарь вида {manifest_type: {stand: config_dict}}
        stands: Список стендов для сохранения
        output_dir: Базовая директория для вывода
    """

    for manifest_type, stand_configs in manifests.items():
        for stand in stands:
            if stand not in stand_configs:
                continue

            # Особая обработка для common манифеста
            if manifest_type == "common":
                output_file = manifest_type / "COMMON.yaml"
            else:
                output_file = manifest_type / f"{stand}.yaml"

            dump_yaml(stand_configs[stand], output_file, manifest_type)