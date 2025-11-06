# main.py
import sys
import os
import yaml
from dotenv import load_dotenv
from src.merger import deep_merge
from src.reader import load_yaml
from src.saver import save_yaml
import logging
logging.basicConfig(level=logging.DEBUG)

load_dotenv()



# ... (deep_merge и _detect_unique_key — как выше)

def main():
    if sys.argv.__len__() < 2:
        print("После python main.py нужно ввести название стендов/стенда: python main.py DEV IFT1 IFT2")
        sys.exit(1)

    base_manifests = [load_yaml("base_manifests/agents.yaml")[0], load_yaml("base_manifests/common.yaml"),
                      load_yaml("base_manifests/integration.yaml"), load_yaml("base_manifests/namespace.yaml"),]
    current_manifests = [(load_yaml("current_manifests/agents.yaml"))[0], load_yaml("current_manifests/common.yaml"),
                     load_yaml("current_manifests/integration.yaml"), load_yaml("current_manifests/namespace.yaml"), ]
    stand_names = [sys.argv[i] for i in range(1, sys.argv.__len__())]
    merged_manifests = [deep_merge(b, o) for b, o in zip(base_manifests, current_manifests)]
    save_yaml(merged_manifests, stand_names)

if __name__ == "__main__":
    main()