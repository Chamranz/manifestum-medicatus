import yaml
import logging
from pathlib import Path
from typing import Any, List, Dict, Tuple

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message))")

class ConfigComporator:

    _MISSING = object()

    def __init__(self, agents: List[str], base_dir: str = "."):
        self.agents = agents
        self.base_dir = Path(base_dir)
        self.file_types = ["common", "namespace", "integrations"]
        self.stand_types = ["DEV", "IFT1", "IFT2", "PROM1", "PROM2", "PSI1", "PSI2"]
        self.output_dir = self.base_dir / "compare_res"
        self.output_dir.mkdir(exist_ok=True)

        if len(self.agents) < 2:
            raise ValueError("Для сравнения нужно более двух агентов")

    def load_config(self, agent: str, file_type: str, stand: str) -> Dict[str, Any]:
        if file_type == "common":
            file_path = self.base_dir / agent / file_type / f"{stand}.yaml"

        else:
            file_path = self.base_dir / agent / file_type / f"{stand}.yaml"

        if not file_path.exists():
            logging.warning(f"Файл не найден: {file_path}")
            return {}

        with open(file_path, "r", encoding='utf-8') as f:
            data = yaml.safe_load(f)
            return data if isinstance(data,dict) else {}

    def deep_compare(self, configs: List[Dict[str, Any]]) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:

        common: Dict[str, Any] = {}
        diffs: List[Dict[str, Any]] = [{} for _ in configs]

        if not configs:
            return common, diffs

        all_keys = sorted(set().union(*(d.keys() for d in configs)))

        for key in all_keys:
            values = [cfg.get(key, self._MISSING) for cfg in configs]
            is_present = [v is not self._MISSING for v in values]

            if not all(is_present):
                for i, v in enumerate(values):
                    if v is not self._MISSING:
                        diffs[i][key] = v
                continue

            if all(v == values[0] for v in values):
                if isinstance(values[0], dict):
                    sub_common, sub_diffs = self.deep_compare([v for v in values])
                    if sub_common:
                        common[key] = sub_common
                    for i, sd in enumerate(sub_diffs):
                        if sd:
                            diffs[i][key] = sd
                else:
                    common[key] = values[0]
            else:
                for i,v in enumerate(values):
                    diffs[i][key] = v
        return common, diffs




    def run(self):
        targets = []

        for file in self.file_types:
            if file == 'common':
                targets.append((file, "COMMON"))
            else:
                for stand in self.stand_types:
                    targets.append((file, stand))

        for file, stand in targets:
            # logging.info(f"Сравнение {stand} файла '{file}'...")

            agent_configs = [self.load_config(agent, file, stand) for agent in self.agents]

            common, agent_diffs = self.deep_compare(agent_configs)

            common_path = self.output_dir / f"same_{file}_{stand}.yaml"
            with open(common_path, "w", encoding="utf-8") as f:
                yaml.dump(common, f, default_flow_style=False, sort_keys=True, allow_unicode=True)

            for agent, diff in zip(self.agents, agent_diffs):
                if diff:
                    diff_path = self.output_dir / f"diff_{agent}_{file}_{stand}.yaml"
                    with open(diff_path, "w", encoding="utf-8") as f:
                        yaml.dump(diff, f, default_flow_style=False, sort_keys=True, allow_unicode=True)
                else:
                    logging.debug(f"Разлчий для agenta {agent} нет в {file}/{stand}")

