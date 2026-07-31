"""
Импорт уже готовых (руками сведённых) yaml-манифестов агента в централизованное
слоистое хранилище manifests_diff/.

Если параметр имеет одинаковое значение у нескольких импортируемых агентов на одной
и той же позиции иерархии стендов (см. STAND_LAYERS в cli/main.py), он автоматически
выносится в scope="all" — общий для всех агентов слой. Всё остальное остаётся
агент-специфичным.

Списки (MTLS, KAFKA.CLUSTERS, INGRESS_WHITELIST, POSTGRES, ...) сравниваются как единое
целое, а не поэлементно/подетально: движок merge_lists мерджит элементы списка по ключу
NAME, заменяя элемент целиком, поэтому "раздёргивание" отдельных полей одного элемента
по разным слоям привело бы к потере данных при последующей сборке.
"""
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import yaml

from ..models.agents import AgentConfig
from ..models.common import CommonConfig
from ..models.namespace import NamespaceConfig
from ..models.integrations import IntegrationConfig
from .codegen import render_module
from ..cli.main import _get_config_path

STANDS = ["DEV", "IFT1", "IFT2", "PROM1", "PROM2", "PSI1", "PSI2"]

STAND_GROUPS = {
    "PREPROM": ["DEV", "IFT1", "IFT2"],
    "IFT": ["IFT1", "IFT2"],
    "PROM": ["PROM1", "PROM2"],
    "PSI": ["PSI1", "PSI2"],
}

LAYER_KEYS = ["general", "PREPROM", "IFT", "PROM", "PSI", "DEV", "IFT1", "IFT2", "PROM1", "PROM2", "PSI1", "PSI2"]

MODEL_BY_MANIFEST = {
    "agents": AgentConfig,
    "common": CommonConfig,
    "namespace": NamespaceConfig,
    "integrations": IntegrationConfig,
}

_MISSING = object()


def _is_empty(value: Any) -> bool:
    if value is None or value is _MISSING:
        return True
    if isinstance(value, dict) and not value:
        return True
    if isinstance(value, list) and all(_is_empty(v) for v in value):
        return True
    return False


def _deep_compare(configs: List[Any]) -> Tuple[Any, List[Any]]:
    """N-way извлечение общей части и остатков. Списки сравниваются атомарно (см. модуль)."""
    if not configs:
        return None, []
    first_type = type(configs[0])
    if not all(type(c) == first_type for c in configs):
        return None, list(configs)

    if first_type is dict:
        common: Dict[str, Any] = {}
        diffs: List[Dict[str, Any]] = [{} for _ in configs]
        all_keys = sorted(set().union(*(d.keys() for d in configs)))
        for key in all_keys:
            values = [d.get(key, _MISSING) for d in configs]
            if not all(v is not _MISSING for v in values):
                for i, v in enumerate(values):
                    if v is not _MISSING:
                        diffs[i][key] = v
                continue
            sub_common, sub_diffs = _deep_compare(values)
            if sub_common is not None and not _is_empty(sub_common):
                common[key] = sub_common
            for i, sd in enumerate(sub_diffs):
                if not _is_empty(sd):
                    diffs[i][key] = sd
        return (common or None), diffs

    # Списки и примитивы — атомарное сравнение
    if all(c == configs[0] for c in configs):
        return configs[0], [None] * len(configs)
    return None, list(configs)


def _load_final_yaml(agent_dir: Path, manifest_type: str, stand: str) -> Dict[str, Any]:
    path = agent_dir / manifest_type / f"{stand}.yaml"
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if manifest_type == "agents" and isinstance(data, list):
        data = data[0] if data else {}
    return data


def decompose_stand_layers(agent_dir: Path, manifest_type: str) -> Dict[str, Dict[str, Any]]:
    """Раскладывает 7 готовых yaml одного агента на иерархию слоёв STAND_LAYERS."""
    finals = {s: _load_final_yaml(agent_dir, manifest_type, s) for s in STANDS}

    general, diffs = _deep_compare([finals[s] for s in STANDS])
    layers: Dict[str, Dict[str, Any]] = {"general": general or {}}
    residual = dict(zip(STANDS, diffs))

    preprom_common, preprom_diffs = _deep_compare([residual[s] for s in STAND_GROUPS["PREPROM"]])
    layers["PREPROM"] = preprom_common or {}
    residual_after_preprom = dict(zip(STAND_GROUPS["PREPROM"], preprom_diffs))

    ift_common, ift_diffs = _deep_compare([residual_after_preprom["IFT1"], residual_after_preprom["IFT2"]])
    layers["IFT"] = ift_common or {}
    residual_after_ift = dict(zip(["IFT1", "IFT2"], ift_diffs))

    prom_common, prom_diffs = _deep_compare([residual["PROM1"], residual["PROM2"]])
    layers["PROM"] = prom_common or {}
    residual_after_prom = dict(zip(["PROM1", "PROM2"], prom_diffs))

    psi_common, psi_diffs = _deep_compare([residual["PSI1"], residual["PSI2"]])
    layers["PSI"] = psi_common or {}
    residual_after_psi = dict(zip(["PSI1", "PSI2"], psi_diffs))

    layers["DEV"] = residual_after_preprom["DEV"]
    layers["IFT1"] = residual_after_ift["IFT1"]
    layers["IFT2"] = residual_after_ift["IFT2"]
    layers["PROM1"] = residual_after_prom["PROM1"]
    layers["PROM2"] = residual_after_prom["PROM2"]
    layers["PSI1"] = residual_after_psi["PSI1"]
    layers["PSI2"] = residual_after_psi["PSI2"]
    return layers


def _write_layer_file(
        config_dir: Path, manifest_type: str, scope: str, layer: str,
        data: Dict[str, Any], exclude_none: bool = False
) -> Path:
    model_class = MODEL_BY_MANIFEST[manifest_type]
    path = _get_config_path(config_dir, manifest_type, scope, layer)
    path.parent.mkdir(parents=True, exist_ok=True)
    if layer != "general":
        init_file = path.parent / "__init__.py"
        if not init_file.exists():
            init_file.write_text("", encoding="utf-8")
    source = render_module(model_class, data, exclude_none=exclude_none)
    path.write_text(source, encoding="utf-8")
    return path


def bootstrap_agents(
        config_dir: Path,
        sources: Dict[str, Path],
        manifest_types: Optional[List[str]] = None,
) -> Dict[str, List[str]]:
    """
    Импортирует уже готовые yaml-манифесты нескольких агентов в manifests_diff.

    sources: {agent_scope: путь_к_папке_с_готовыми_yaml} (папки вида cash-flow/, classifier/,
             с подпапками agents/common/integrations/namespace и файлами {STAND}.yaml).

    Возвращает список записанных файлов по scope ("all" и каждый agent_scope).
    """
    manifest_types = manifest_types or ["agents", "namespace", "integrations"]
    written: Dict[str, List[str]] = {"all": [], **{name: [] for name in sources}}
    agent_names = list(sources.keys())

    for manifest_type in manifest_types:
        per_agent_layers = {
            agent: decompose_stand_layers(path, manifest_type)
            for agent, path in sources.items()
        }

        for layer in LAYER_KEYS:
            configs = [per_agent_layers[agent][layer] for agent in agent_names]
            common, diffs = _deep_compare(configs)
            common = common or {}

            # Слой всегда материализуется валидным (пусть и пустым) get_config(), даже если
            # общих параметров на этой позиции иерархии нет: файл может уже существовать как
            # заглушка, и пустой файл без get_config() ломает load_partial_config() при загрузке.
            p = _write_layer_file(config_dir, manifest_type, "all", layer, common)
            written["all"].append(str(p))

            for agent, diff in zip(agent_names, diffs):
                p = _write_layer_file(config_dir, manifest_type, agent, layer, diff or {})
                written[agent].append(str(p))

    return written


def bootstrap_common(config_dir: Path, sources: Dict[str, Path]) -> Dict[str, List[str]]:
    """
    Выносит в common/all/general.py параметры, одинаковые у всех переданных агентов в COMMON.yaml
    (hub, aef.name/id, sonar_qube, qg, buildCredentials), а агент-специфичные поля (aef.module_id,
    agents[]) записывает в common/{scope}/general.py для каждого агента.
    """
    finals = []
    for agent, path in sources.items():
        data = yaml.safe_load((path / "common" / "COMMON.yaml").read_text(encoding="utf-8")) or {}
        finals.append(data)

    common, diffs = _deep_compare(finals)
    written: Dict[str, List[str]] = {"all": [], **{name: [] for name in sources}}

    # Общая часть — в common/all/general.py
    common = common or {}
    if common:
        p = _write_layer_file(config_dir, "common", "all", "general", common, exclude_none=True)
        written["all"].append(str(p))

    # Агент-специфичные остатки — в common/{scope}/general.py
    for agent, diff in zip(sources.keys(), diffs):
        diff = diff or {}
        if diff:
            p = _write_layer_file(config_dir, "common", agent, "general", diff, exclude_none=True)
            written[agent].append(str(p))

    return written
