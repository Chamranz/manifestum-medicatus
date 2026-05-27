import os
import sys
import logging
from typing import List, Dict, Any, Optional
from pathlib import Path
import yaml

from ..core.merger import deep_merge
from ..core.validator import validate_manifest
from ..models.stub import StubConfig

# === КОНФИГУРАЦИЯ ===

# Слои по стендам (базовая иерархия)
STAND_LAYERS = {
    "DEV": ["general", "PREPROM", "DEV"],
    "IFT1": ["general", "PREPROM", "IFT", "IFT1"],
    "IFT2": ["general", "PREPROM", "IFT", "IFT2"],
    "PROM1": ["general", "PROM", "PROM1"],
    "PROM2": ["general", "PROM", "PROM2"],
    "PSI1": ["general", "PSI", "PSI1"],
    "PSI2": ["general", "PSI", "PSI2"],
}

# Типы манифестов
MANIFEST_NAMES = ["agents", "common", "integrations", "namespace"]

# Префиксы для "общих" и "агентных" слоёв
ALL_PREFIX = "all"  # general_all, PREPROM_all, ...
AGENT_PREFIX_TEMPLATE = "{agent}"  # general_classifier, PREPROM_classifier, ...


def load_partial_config(config_dir: Path, manifest_type: str, layer: str) -> Optional[Dict[str, Any]]:
    """
    Загрузка частичного конфига из Python-модуля.
    Возвращает None, если файл не найден (не ошибка — слой может отсутствовать).
    """
    # Определяем путь: general -> general.py, PREPROM -> PREPROM/preprom.py
    if layer.endswith("_all") or "_" not in layer:
        # Слой типа "general", "PREPROM_all"
        base_name = layer.replace("_all", "")
        if base_name == "general":
            file_path = config_dir / manifest_type / "general.py"
        else:
            file_path = config_dir / manifest_type / base_name / f"{base_name.lower()}.py"
    else:
        # Слой типа "general_classifier"
        parts = layer.split("_", 1)
        base_name, suffix = parts[0], parts[1] if len(parts) > 1 else ""
        if base_name == "general":
            file_path = config_dir / manifest_type / "general" / f"{suffix}.py"
        else:
            file_path = config_dir / manifest_type / base_name / suffix / f"{suffix.lower()}.py"

    if not file_path.exists():
        logging.debug(f"Слой не найден (пропускаем): {file_path}")
        return None

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


def _build_layer_names(base_layers: List[str], prefix: str, agent: Optional[str] = None) -> List[str]:
    """
    Генерирует имена слоёв по шаблону.
    Пример: base_layers=["general","PREPROM","DEV"], prefix="all"
            → ["general_all", "PREPROM_all", "DEV_all"]
    """
    result = []
    for layer in base_layers:
        if prefix == ALL_PREFIX:
            result.append(f"{layer}_{ALL_PREFIX}")
        elif agent:
            result.append(f"{layer}_{agent}")
        else:
            result.append(layer)
    return result


def merge_config_chain(
        config_dir: Path,
        manifest_type: str,
        base_layers: List[str],
        agent: Optional[str] = None,
        merge_lists: bool = True
) -> Dict[str, Any]:
    """
    Последовательно мерджит цепочку слоёв.
    Если агент указан — грузим агент-специфичные слои, иначе — "all"-слои.
    Пропущенные файлы не считаются ошибкой.
    """
    merged = {}
    layer_names = _build_layer_names(base_layers, prefix=ALL_PREFIX if agent is None else agent)

    for layer_name in layer_names:
        config = load_partial_config(config_dir, manifest_type, layer_name)
        if config is None:
            continue  # слой опционален
        merged = deep_merge(merged, config, manifest_type, merge_lists=merge_lists)

    return merged


def remove_none_values(data: Any) -> Any:
    """Рекурсивное удаление ключей со значением None."""
    if isinstance(data, dict):
        return {
            key: remove_none_values(value)
            for key, value in data.items()
            if value is not None
        }
    elif isinstance(data, list):
        return [remove_none_values(item) for item in data]
    return data


def generate_manifests(
        config_dir: str,
        output_dir: str,
        stands: Optional[List[str]] = None,
        agents: Optional[List[str]] = None
    ) -> None:
    """
    Генерация манифестов с двухуровневым мерджем:
    1. Сначала "all"-слои (общие для всех агентов)
    2. Затем агент-специфичные слои поверх
    """
    config_path = Path(config_dir)
    output_path = Path(output_dir)
    stands = stands or list(STAND_LAYERS.keys())
    agents = agents or []  # если пустой — генерируем только "all"-конфиги

    for manifest_name in MANIFEST_NAMES:
        merge_lists = (manifest_name == "integrations")

        for stand in stands:
            if stand not in STAND_LAYERS:
                logging.warning(f"Стенд {stand} не определён в STAND_LAYERS")
                continue

            base_layers = STAND_LAYERS[stand]

            # === ШАГ 1: Мердж "all"-слоёв (агент-агностичные) ===
            logging.info(f"[{manifest_name}/{stand}] Загрузка общих слоёв (_all)")
            common_config = merge_config_chain(
                config_path, manifest_name, base_layers,
                agent=None, merge_lists=merge_lists
            )

            # === ШАГ 2: Если есть агенты — мерджим агент-специфичные поверх ===
            if agents:
                for agent in agents:
                    logging.info(f"[{manifest_name}/{stand}/{agent}] Наложение агент-слоёв")

                    agent_config = merge_config_chain(
                        config_path, manifest_name, base_layers,
                        agent=agent, merge_lists=merge_lists
                    )

                    # Финальный мердж: all + agent
                    final_config = deep_merge(
                        common_config, agent_config, manifest_name, merge_lists=merge_lists
                    )

                    # Валидация и сохранение
                    _save_manifest(
                        final_config, manifest_name, stand, agent,
                        output_path, merge_lists
                    )
            else:
                # === Только "all"-конфиги (без привязки к агенту) ===
                _save_manifest(
                    common_config, manifest_name, stand, None, output_path, merge_lists
                    )


def _save_manifest(
        config: Dict[str, Any],
        manifest_name: str,
        stand: str,
        agent: Optional[str],
        output_path: Path,
        merge_lists: bool
) -> None:
    """Валидация, очистка и сохранение манифеста."""
    # Валидация через Pydantic
    validated = validate_manifest(manifest_name, config)

    # Специальная обработка для agents (возвращает список)
    if manifest_name == "agents":
        validated = [validated.model_dump()]
    else:
        validated = validated.model_dump()

    # Удаление None-значений
    validated = remove_none_values(validated)

    # Формирование пути
    if manifest_name == "common":
        # common не зависит от стенда и агента
        output_file = output_path / "common" / "COMMON.yaml"
    elif agent:
        output_file = output_path / manifest_name / agent / f"{stand}.yaml"
    else:
        output_file = output_path / manifest_name / f"{stand}_all.yaml"

    output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, "w", encoding="utf-8") as f:
        yaml.dump(
            validated,
            f,
            Dumper=yaml.Dumper,
            allow_unicode=True,
            default_flow_style=False,
            sort_keys=False,
            indent=2,
        )
    logging.info(f"✓ Сохранено: {output_file}")


def main() -> None:
    """Точка входа консольной утилиты."""
    import argparse

    parser = argparse.ArgumentParser(description="Генерация конфигураций Manifestum Medicatus")
    parser.add_argument("--config-dir", default="manifests_diff", help="Директория с исходными конфигами")
    parser.add_argument("--output-dir", default="./output", help="Директория для результатов")
    parser.add_argument("--stands", nargs="+", default=None, help="Список стендов (по умолчанию все)")
    parser.add_argument("--agents", nargs="+", default=None, help="Список агентов для генерации")
    parser.add_argument("--all-only", action="store_true", help="Генерировать только _all конфиги (без агентов)")
    parser.add_argument("--verbose", action="store_true", help="Подробный вывод")

    args = parser.parse_args()
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(levelname)s: %(message)s"
    )

    agents = None if args.all_only else args.agents

    generate_manifests(
        config_dir=args.config_dir,
        output_dir=args.output_dir,
        stands=args.stands,
        agents=agents
    )


if __name__ == "__main__":
    main()