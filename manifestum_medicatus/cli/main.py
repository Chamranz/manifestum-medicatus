import os
import sys
import logging
from typing import List, Dict, Any, Optional, Set
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

# Директории, которые НЕ являются агентами (служебные)
_NON_AGENT_SCOPES = {"all", "__pycache__"}


def _get_config_path(config_dir: Path, manifest_type: str, scope: str, layer: str) -> Path:
    """
    Возвращает путь к файлу конфига.

    scope: "all" или имя агента (например, "classifier")
    layer: имя слоя (general, PREPROM, IFT, IFT1, ...)

    Примеры:
    - manifest=agents, scope=all, layer=general
      → manifests_diff/agents/all/general.py
    - manifest=agents, scope=classifier, layer=PREPROM
      → manifests_diff/agents/classifier/PREPROM/preprom.py
    - manifest=common, scope=all, layer=general
      → manifests_diff/common/all/general.py
    """
    # special case: general всегда лежит прямо в scope/
    if layer == "general":
        return config_dir / manifest_type / scope / "general.py"

    # остальные слои: scope/layer/{layer}.py, независимо от scope (all или агент)
    return config_dir / manifest_type / scope / layer / f"{layer.lower()}.py"


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


def _detect_agent_scopes(config_dir: Path, manifest_type: str) -> List[str]:
    """
    Авто-определение всех существующих агентов в manifests_diff.

    Сканирует директорию manifests_diff/<manifest_type>/ и возвращает имена
    поддиректорий, которые не являются служебными (all, __pycache__).
    Агентом считается scope, у которого есть хотя бы general.py.
    """
    manifest_path = config_dir / manifest_type
    if not manifest_path.exists():
        return []

    scopes: List[str] = []
    for entry in sorted(manifest_path.iterdir()):
        if not entry.is_dir():
            continue
        if entry.name in _NON_AGENT_SCOPES:
            continue
        # Считаем директорию агентом, если в ней есть general.py
        if (entry / "general.py").exists():
            scopes.append(entry.name)

    return scopes


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

    Если --agents не указан, автоматически определяются все существующие агенты
    в manifests_diff и генерация происходит для каждого из них.
    """
    config_path = Path(config_dir)
    output_path = Path(output_dir)
    stands = stands or list(STAND_LAYERS.keys())

    for manifest_name in MANIFEST_NAMES:
        merge_lists = (manifest_name == "integrations")
        has_agent_scope = manifest_name not in NO_AGENT_MANIFESTS

        # Если агенты не указаны явно — авто-определяем для этого типа манифеста
        effective_agents: Optional[List[str]] = agents
        if has_agent_scope and effective_agents is None:
            effective_agents = _detect_agent_scopes(config_path, manifest_name)
            if effective_agents:
                logging.info(
                    f"[{manifest_name}] Агенты не указаны, авто-определено: {effective_agents}"
                )

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
            if has_agent_scope and effective_agents:
                for agent in effective_agents:
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

            elif has_agent_scope and not effective_agents:
                # === Если агентов нет ни указанных, ни авто-определённых — сохраняем только all ===
                logging.info(f"[{manifest_name}/{stand}] Агенты не найдены, сохраняем только all-конфиг")
                _save_manifest(base_config, manifest_name, stand, None, output_path)


def main() -> None:
    """Точка входа консольной утилиты."""
    import argparse

    parser = argparse.ArgumentParser(description="Генерация конфигураций Manifestum Medicatus")
    subparsers = parser.add_subparsers(dest="command")

    gen = subparsers.add_parser("generate", help="Сгенерировать YAML-манифесты из manifests_diff")
    gen.add_argument("--config-dir", default="manifests_diff", help="Директория с исходными конфигами")
    gen.add_argument("--output-dir", default="./output", help="Директория для результатов")
    gen.add_argument("--stands", nargs="+", default=None, help="Список стендов (по умолчанию все)")
    gen.add_argument("--agents", nargs="+", default=None, help="Список агентов для генерации")
    gen.add_argument("--verbose", action="store_true", help="Подробный вывод")

    imp = subparsers.add_parser(
        "import-agent",
        help="Импортировать уже готовые yaml-манифесты агента(ов) в manifests_diff",
    )
    imp.add_argument("--config-dir", default="manifests_diff", help="Директория с manifests_diff")
    imp.add_argument(
        "--agent", action="append", required=True, metavar="SCOPE=PATH",
        help="scope=путь_к_папке_с_готовыми_yaml; можно указывать несколько раз "
             "(--agent cash_flow=cash-flow --agent document_classifier=classifier). "
             "Общее для всех переданных агентов автоматически выносится в scope=all.",
    )
    imp.add_argument("--verbose", action="store_true", help="Подробный вывод")

    onboard = subparsers.add_parser(
        "onboard-agent",
        help="Создать заготовку нового агента в manifests_diff по КЭ и имени агента",
    )
    onboard.add_argument("--config-dir", default="manifests_diff", help="Директория с manifests_diff")
    onboard.add_argument("--agent-scope", required=True, help="Имя папки-слоя, например claim_terms")
    onboard.add_argument("--agent-name", required=True, help="Имя агента в k8s/AEF, например claim-terms")
    onboard.add_argument("--ci", required=True, help="КЭ модуля агента, например CI10071234")
    onboard.add_argument("--verbose", action="store_true", help="Подробный вывод")

    args = parser.parse_args()
    command = args.command or "generate"
    logging.basicConfig(
        level=logging.DEBUG if getattr(args, "verbose", False) else logging.INFO,
        format="%(levelname)s: %(message)s"
    )

    if command == "generate":
        generate_manifests(
            config_dir=args.config_dir,
            output_dir=args.output_dir,
            stands=args.stands,
            agents=args.agents
        )
    elif command == "import-agent":
        from pathlib import Path
        from ..core.importer import bootstrap_agents, bootstrap_common

        sources = {}
        for item in args.agent:
            scope, _, path = item.partition("=")
            if not scope or not path:
                parser.error(f"--agent должен быть в формате scope=путь, получено: {item!r}")
            sources[scope] = Path(path)

        written = bootstrap_agents(Path(args.config_dir), sources)
        common_file = bootstrap_common(Path(args.config_dir), sources)
        for scope, files in written.items():
            logging.info(f"[{scope}] записано файлов: {len(files)}")
        if common_file:
            logging.info(f"[common/all] записано: {common_file}")
    elif command == "onboard-agent":
        from pathlib import Path
        from ..core.onboarding import scaffold_agent

        written = scaffold_agent(
            Path(args.config_dir), args.agent_scope, args.agent_name, args.ci
        )
        for manifest_type, files in written.items():
            logging.info(f"[{manifest_type}] записано файлов: {len(files)}")
    else:
        parser.error(f"Неизвестная команда: {command}")


if __name__ == "__main__":
    main()