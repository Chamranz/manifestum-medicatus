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

# Слои по стендам (иерархия наследования)
STAND_LAYERS = {
    "DEV": ["general", "PREPROM", "DEV"],
    "IFT1": ["general", "PREPROM", "IFT", "IFT1"],
    "IFT2": ["general", "PREPROM", "IFT", "IFT2"],
    "PROM1": ["general", "PROM", "PROM1"],
    "PROM2": ["general", "PROM", "PROM2"],
    "PSI1": ["general", "PSI", "PSI1"],
    "PSI2": ["general", "PSI", "PSI2"],
}

MANIFEST_NAMES = ["agents", "common", "integrations", "namespace"]

# Манифесты, которые НЕ имеют агент-специфичных конфигов
NO_AGENT_MANIFESTS = {"common"}


def _get_config_path(config_dir: Path, manifest_type: str, scope: str, layer: str) -> Path:
    """
    Возвращает путь к файлу конфига.

    scope: "all" или имя агента (например, "classifier")
    layer: имя слоя (general, PREPROM, IFT, IFT1, ...)

    Примеры:
    - manifest=agents, scope=all, layer=general
      → manifests_diff/agents/all/general.py
    - manifest=agents, scope=classifier, layer=PREPROM
      → manifests_diff/agents/classifier/PREPROM/classifier/classifier.py
    - manifest=common, scope=all, layer=general
      → manifests_diff/common/all/general.py
    """
    # special case: general всегда лежит прямо в scope/
    if layer == "general":
        return config_dir / manifest_type / scope / "general.py"

    # остальные слои: scope/layer/{agent_or_layer}.py
    # для all: PREPROM/preprom.py
    # для agent: PREPROM/classifier/classifier.py
    suffix = scope if scope != "all" else layer.lower()
    return config_dir / manifest_type / scope / layer / f"{suffix}.py"


def load_partial_config(config_dir: Path, manifest_type: str, scope: str, layer: str) -> Optional[Dict[str, Any]]:
    """
    Загрузка конфига из Python-модуля.
    Возвращает None, если файл не найден (слой опционален).
    """
    file_path = _get_config_path(config_dir, manifest_type, scope, layer)

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


def merge_layer_chain(
        config_dir: Path,
        manifest_type: str,
        scope: str,  # "all" или имя агента
        base_layers: List[str],
        merge_lists: bool = True
) -> Dict[str, Any]:
    """
    Последовательно мерджит цепочку слоёв для заданного scope.
    Пропущенные файлы не считаются ошибкой.
    """
    merged = {}

    for layer in base_layers:
        config = load_partial_config(config_dir, manifest_type, scope, layer)
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


def _save_manifest(
        config: Dict[str, Any],
        manifest_name: str,
        stand: str,
        agent: Optional[str],
        output_path: Path
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

    # Формирование пути сохранения
    if manifest_name == "common":
        # common не зависит ни от стенда, ни от агента
        output_file = output_path / "common" / "COMMON.yaml"
    elif agent:
        # агент-специфичный конфиг
        output_file = output_path / manifest_name / agent / f"{stand}.yaml"
    else:
        # только _all конфиг (без агента)
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


def generate_manifests(
        config_dir: str,
        output_dir: str,
        stands: Optional[List[str]] = None,
        agents: Optional[List[str]] = None
) -> None:
    """
    Генерация манифестов с двухуровневым мерджем:

    1. Сначала грузим и мерджим слои из scope="all" (общие для всех агентов)
    2. Если указан агент — грузим и мерджим слои из scope={agent} поверх общих
    3. Для манифеста "common" шаг 2 пропускается
    """
    config_path = Path(config_dir)
    output_path = Path(output_dir)
    stands = stands or list(STAND_LAYERS.keys())

    for manifest_name in MANIFEST_NAMES:
        merge_lists = (manifest_name == "integrations")
        has_agent_scope = manifest_name not in NO_AGENT_MANIFESTS

        for stand in stands:
            if stand not in STAND_LAYERS:
                logging.warning(f"Стенд {stand} не определён в STAND_LAYERS")
                continue

            base_layers = STAND_LAYERS[stand]

            # === ШАГ 1: Мердж общих слоёв (scope="all") ===
            logging.info(f"[{manifest_name}/{stand}] Загрузка общих слоёв (all)")
            base_config = merge_layer_chain(
                config_path, manifest_name, scope="all",
                base_layers=base_layers, merge_lists=merge_lists
            )

            # === ШАГ 2: Если манифест поддерживает агентов — мерджим агент-специфичные ===
            if has_agent_scope and agents:
                for agent in agents:
                    logging.info(f"[{manifest_name}/{stand}/{agent}] Наложение агент-слоёв")

                    agent_config = merge_layer_chain(
                        config_path, manifest_name, scope=agent,
                        base_layers=base_layers, merge_lists=merge_lists
                    )

                    # Финальный мердж: all + agent (agent переопределяет all)
                    final_config = deep_merge(
                        base_config, agent_config, manifest_name, merge_lists=merge_lists
                    )

                    _save_manifest(final_config, manifest_name, stand, agent, output_path)

            elif not has_agent_scope:
                # === Для common: сохраняем только all-конфиг ===
                _save_manifest(base_config, manifest_name, stand, None, output_path)

            elif has_agent_scope and not agents:
                # === Если агенты не указаны, но манифест их поддерживает — сохраняем только all ===
                logging.info(f"[{manifest_name}/{stand}] Сохраняем только all-конфиг (агенты не указаны)")
                _save_manifest(base_config, manifest_name, stand, None, output_path)


def main() -> None:
    """Точка входа консольной утилиты."""
    import argparse

    parser = argparse.ArgumentParser(description="Генерация конфигураций Manifestum Medicatus")
    parser.add_argument("--config-dir", default="manifests_diff", help="Директория с исходными конфигами")
    parser.add_argument("--output-dir", default="./output", help="Директория для результатов")
    parser.add_argument("--stands", nargs="+", default=None, help="Список стендов (по умолчанию все)")
    parser.add_argument("--agents", nargs="+", default=None, help="Список агентов для генерации")
    parser.add_argument("--verbose", action="store_true", help="Подробный вывод")

    args = parser.parse_args()
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(levelname)s: %(message)s"
    )

    generate_manifests(
        config_dir=args.config_dir,
        output_dir=args.output_dir,
        stands=args.stands,
        agents=args.agents
    )


if __name__ == "__main__":
    main()