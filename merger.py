import yaml
from typing import List, Optional, Any, Dict

import os
from dotenv import load_dotenv


load_dotenv()


def deep_merge(base: Any, override: Any) -> Any:
    """Склеивам два ямлика

        Args:
            base (Any):
                базовый ямлик
            override (Any):
    :param base:
    :param override:
    :return:
    """
