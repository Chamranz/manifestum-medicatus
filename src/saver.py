import yaml
import os
def dump_yaml(data, output_name):
    filepath = os.path.join(f"{output_name}.yaml")
    with open(filepath, "w", encoding="utf-8") as f:
        yaml.dump(data, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
    print(f"Сохранено: {filepath}")

def save_yaml(merged_manifests, stand_names):
    for stand in stand_names:
        dump_yaml(merged_manifests[0], f"merged_manifests/agents/{stand}")
        dump_yaml(merged_manifests[1], f"merged_manifests/common/{stand}")
        dump_yaml(merged_manifests[2], f"merged_manifests/integrations/{stand}")
        dump_yaml(merged_manifests[3], f"merged_manifests/namespace/{stand}")