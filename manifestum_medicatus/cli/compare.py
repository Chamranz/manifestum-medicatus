import yaml
import logging
from pathlib import Path
from typing import Any, List, Dict, Tuple

# Исправлена опечатка в format
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


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
        file_path = self.base_dir / agent / file_type / f"{stand}.yaml"

        if not file_path.exists():
            logging.warning(f"Файл не найден: {file_path}")
            return {}

        with open(file_path, "r", encoding='utf-8') as f:
            data = yaml.safe_load(f)
            return data if isinstance(data, dict) else {}

    def _is_empty_diff(self, val: Any) -> bool:
        """Проверяет, является ли значение 'пустым' диффом (None, {} или [])."""
        if val is None or val is self._MISSING:
            return True
        if isinstance(val, dict) and not val:
            return True
        if isinstance(val, list) and all(self._is_empty_diff(v) for v in val):
            return True
        return False

    def deep_compare(self, configs: List[Any]) -> Tuple[Any, List[Any]]:
        """
        Универсальное глубокое сравнение.
        Умеет работать со словарями, списками и примитивами.
        """
        if not configs:
            return None, []

        first_type = type(configs[0])

        # Если типы элементов различаются (например, int и str),
        # то общего ничего нет, всё уходит в дифф
        if not all(type(item) == first_type for item in configs):
            return None, configs

        # --- 1. Если это СЛОВАРИ ---
        if first_type == dict:
            common = {}
            diffs = [{} for _ in configs]
            all_keys = sorted(set().union(*(d.keys() for d in configs)))

            for key in all_keys:
                values = [d.get(key, self._MISSING) for d in configs]
                is_present = [v is not self._MISSING for v in values]

                # Если ключ есть не во всех конфигах, он не может быть общим
                if not all(is_present):
                    for i, v in enumerate(values):
                        if v is not self._MISSING:
                            diffs[i][key] = v
                    continue

                # Рекурсивно сравниваем значения
                sub_common, sub_diffs = self.deep_compare(values)

                if sub_common is not None:
                    common[key] = sub_common

                # Добавляем в дифф только те значения, которые не являются "пустыми"
                for i, sd in enumerate(sub_diffs):
                    if not self._is_empty_diff(sd):
                        diffs[i][key] = sd

            if not common:
                return None, diffs
            return common, diffs

        # --- 2. Если это СПИСКИ ---
        elif first_type == list:
            lengths = set(len(item) for item in configs)
            # Если списки разной длины, мы не можем сравнивать их поэлементно
            if len(lengths) > 1:
                if all(item == configs[0] for item in configs):
                    return configs[0], [[] for _ in configs]
                else:
                    return None, configs

            common_list = []
            diffs_list = [[] for _ in configs]

            # Сравниваем списки поэлементно (по индексам)
            for j in range(len(configs[0])):
                col_values = [item[j] for item in configs]
                sub_common, sub_diffs = self.deep_compare(col_values)

                # Если для какого-то индекса нет общего значения,
                # то и весь список не может иметь общей части
                if sub_common is None:
                    return None, configs

                common_list.append(sub_common)

                for i in range(len(configs)):
                    diffs_list[i].append(sub_diffs[i])

            # Формируем итоговые диффы, заменяя полностью пустые списки на []
            final_diffs = []
            for i in range(len(configs)):
                if self._is_empty_diff(diffs_list[i]):
                    final_diffs.append([])
                else:
                    final_diffs.append(diffs_list[i])

            return common_list, final_diffs

        # --- 3. Если это ПРИМИТИВЫ (строки, числа, булевы) ---
        else:
            if all(item == configs[0] for item in configs):
                return configs[0], [None] * len(configs)
            else:
                return None, configs

    def run(self):
        targets = []

        for file in self.file_types:
            if file == 'common':
                targets.append((file, "COMMON"))
            else:
                for stand in self.stand_types:
                    targets.append((file, stand))

        for file, stand in targets:
            agent_configs = [self.load_config(agent, file, stand) for agent in self.agents]

            common, agent_diffs = self.deep_compare(agent_configs)

            common_path = self.output_dir / f"same_{file}_{stand}.yaml"
            with open(common_path, "w", encoding="utf-8") as f:
                # Если common оказался None (нет вообще ни одного общего поля), пишем пустой словарь
                yaml.dump(common if common else {}, f, default_flow_style=False, sort_keys=True, allow_unicode=True)

            for agent, diff in zip(self.agents, agent_diffs):
                if diff:
                    diff_path = self.output_dir / f"diff_{agent}_{file}_{stand}.yaml"
                    with open(diff_path, "w", encoding="utf-8") as f:
                        yaml.dump(diff, f, default_flow_style=False, sort_keys=True, allow_unicode=True)
                else:
                    logging.debug(f"Различий для агента {agent} нет в {file}/{stand}")