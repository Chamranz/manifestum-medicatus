"""
Онбординг нового агента "с нуля" — без готовых yaml, только по КЭ модуля агента и его имени.

Заполняет в manifests_diff только те поля, которые механически выводятся из
(agent_name, ci) + уже существующих общих констант (hub.id/aef.id из common/all,
DROPAPP_CLUSTER конкретных стендов из namespace/all): идентификаторы namespace,
переменные окружения, вычисляемые из имени и КЭ, и CN для mTLS-сертификатов.

Всё, что требует бизнес-решения (sizing ресурсов, ISTIO/OTT/GEOROUTES, кастомные ENV,
Kafka-топики, git/sonar/docker-образ в common) сознательно НЕ генерируется: неверная
догадка здесь хуже отсутствия значения. Такие поля остаются непроставленными и, если
модель считает их обязательными, сами всплывут в итоговом YAML как "Укажи меня" —
это и есть сигнал, что нужно доделать руками (см. models/*.py).
"""
from pathlib import Path
from typing import Any, Dict, List

from ..cli.main import STAND_LAYERS, load_partial_config, merge_layer_chain
from .importer import LAYER_KEYS, STANDS, _write_layer_file

# Суффикс для SBER_CA_CLIENT_CN: слой, на который он ставится (DEV — свой лист,
# IFT1/IFT2 делят один "ift", PROM1/PROM2 — "prom", PSI1/PSI2 — "psi").
CLIENT_CN_LAYER_SUFFIX = {"DEV": "dev", "IFT": "ift", "PROM": "prom", "PSI": "psi"}


def _read_container_constants(config_dir: Path) -> Dict[str, str]:
    common_all = load_partial_config(config_dir, "common", "all", "general") or {}
    hub_id = (common_all.get("hub") or {}).get("id")
    aef_id = (common_all.get("aef") or {}).get("id")
    if not hub_id or not aef_id:
        raise RuntimeError(
            "common/all/general.py не содержит hub.id/aef.id — сначала опишите общий "
            "AEF-контейнер (см. core.importer.bootstrap_common), онбординг агента "
            "полагается на эти константы."
        )
    return {"hub_id": hub_id, "aef_id": aef_id}


def scaffold_agent(config_dir: Path, agent_scope: str, agent_name: str, ci: str) -> Dict[str, List[str]]:
    """
    Создаёt заготовку нового агента в manifests_diff.

    agent_scope: имя папки-слоя (Python-модуль), например "claim_terms".
    agent_name:  имя агента как в k8s/AEF (через дефис), например "claim-terms".
    ci:          КЭ модуля агента, например "CI10071234".

    Возвращает {manifest_type: [список записанных файлов]}.
    """
    config_dir = Path(config_dir)
    consts = _read_container_constants(config_dir)
    hub_id, aef_id = consts["hub_id"], consts["aef_id"]
    # k8s-идентификаторы (namespace, hostname) — всегда lowercase (DNS label); в CN-строках
    # (SBER_CA_CLIENT_CN и т.п.) КЭ/aef.id остаются как в CMDB, т.е. uppercase "CI...".
    aef_id_lc = aef_id.lower()

    written: Dict[str, List[str]] = {"agents": [], "common": [], "namespace": []}

    # --- agents/{scope}/general.py ---
    agents_general = {
        "AGENT_NAME": agent_name,
        "ENV": {
            "AGENT_ID": ci,
            "POD_NAMESPACE": f"{aef_id_lc}-{agent_name}",
            "TRACING_SERVICE_KAFKA_BOOTSTRAP_SERVERS":
                f"[egress-kafka-aef-istio-logs.{aef_id_lc}-{agent_name}.svc.cluster.local:19093]",
        },
    }
    p = _write_layer_file(config_dir, "agents", agent_scope, "general", agents_general)
    written["agents"].append(str(p))

    # --- common/{scope}/general.py: module_id и agents[] для этого агента ---
    common_general = {
        "aef": {
            "module_id": ci,
        },
        "agents": [
            {
                "name": agent_name,
                "git": f"ssh://git@stash.sigma.sbrf.ru:7999/kvaef/{agent_name}.git",
                "path": f"./agents/{agent_scope}/v0.1",
                "assembly": {
                    "baseImage": "docker-internal.registry-ci.delta.sbrf.ru/ci04675739/ci04675739/python-3.12:9.6.2-se",
                    "aefsdk": True,
                    "pyinstaller": {"args": ""},
                },
                "sonar": {
                    "key": agent_name,
                },
                "compile": False,
                "type": "python",
            },
        ],
    }
    p = _write_layer_file(config_dir, "common", agent_scope, "general", common_general)
    written["common"].append(str(p))

    # --- namespace/{scope}/*: собираем по каждому слою, чтобы не перезаписать друг друга ---
    ns_layers: Dict[str, Dict[str, Any]] = {layer: {} for layer in LAYER_KEYS}
    ns_layers["general"] = {
        "DROPAPP_NAMESPACE": f"{aef_id_lc}-{agent_name}",
        "EIGW_NAMESPACE": f"{aef_id_lc}-{agent_name}",
    }

    # SBER_CA_SERVER_CN — свой на каждый физический стенд (нужен DROPAPP_CLUSTER из namespace/all)
    for stand in STANDS:
        all_ns = merge_layer_chain(config_dir, "namespace", "all", STAND_LAYERS[stand])
        dropapp_cluster = all_ns.get("DROPAPP_CLUSTER")
        if dropapp_cluster:
            ns_layers[stand]["SECMAN"] = {
                "SBER_CA_SERVER_CN": f"{agent_name}.{aef_id_lc}-{agent_name}.apps.{dropapp_cluster}",
            }

    # SBER_CA_CLIENT_CN — один на группу стендов одного типа (DEV — сам себе группа)
    for group_layer, suffix in CLIENT_CN_LAYER_SUFFIX.items():
        ns_layers[group_layer].setdefault("SECMAN", {})["SBER_CA_CLIENT_CN"] = \
            f"{aef_id}-{ci}-{agent_name}-{suffix}"

    for layer, data in ns_layers.items():
        p = _write_layer_file(config_dir, "namespace", agent_scope, layer, data)
        written["namespace"].append(str(p))

    return written
