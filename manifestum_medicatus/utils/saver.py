"""
Utility functions for saving YAML files.
"""
from typing import Any
import os
import yaml

def save_yaml(data: Any, file_path: str) -> None:
    """
    Save data to a YAML file.
    
    Args:
        data: Data to save
        file_path: Path to the output file
    """
    # Ensure directory exists
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    with open(file_path, "w", encoding="utf-8") as f:
        yaml.safe_dump(
            data,
            f,
            allow_unicode=True,
            default_flow_style=False,
            sort_keys=False,
            indent=2,
            width=1000
        )