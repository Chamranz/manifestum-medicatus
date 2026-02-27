"""
Utility functions for merging dictionaries.
"""
from typing import Any, Dict

def deep_merge(dict1: Dict[str, Any], dict2: Dict[str, Any], merge_lists: bool = False) -> Dict[str, Any]:
    """
    Recursively merge two dictionaries.
    
    If both values are dictionaries, they are merged recursively.
    Otherwise, the value from dict2 replaces the value from dict1.
    Lists are replaced entirely unless merge_lists is True.
    
    Args:
        dict1: First dictionary
        dict2: Second dictionary
        merge_lists: Whether to merge lists instead of replacing them
    
    Returns:
        Merged dictionary
    """
    result = dict1.copy()
    
    for key, value in dict2.items():
        if key in result:
            if isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = deep_merge(result[key], value, merge_lists)
            elif isinstance(result[key], list) and isinstance(value, list) and merge_lists:
                result[key] = result[key] + value
            else:
                result[key] = value
        else:
            result[key] = value
            
    return result