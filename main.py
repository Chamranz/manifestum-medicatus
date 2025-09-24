# main.py
import sys
import os
import yaml
from dotenv import load_dotenv
from merger import deep_merge

load_dotenv()

def load_yaml(path):
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}

def save_yaml(data, output_name):
    output_path = os.getenv("OUTPUT_PATH", ".")
    os.makedirs(output_path, exist_ok=True)
    filepath = os.path.join(output_path, f"{output_name}.yaml")
    with open(filepath, "w", encoding="utf-8") as f:
        yaml.dump(data, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
    print(f"✅ Сохранено: {filepath}")

# ... (deep_merge и _detect_unique_key — как выше)

def main():
    if len(sys.argv) != 4:
        print("Использование: python main.py <base.yaml> <override.yaml> <output_name>")
        sys.exit(1)

    base = load_yaml(sys.argv[1])
    override = load_yaml(sys.argv[2])
    output_name = sys.argv[3]

    result = deep_merge(base, override)
    save_yaml(result, output_name)

if __name__ == "__main__":
    main()