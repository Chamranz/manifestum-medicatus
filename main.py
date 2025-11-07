# main.py
import sys
import argparse
from dotenv import load_dotenv
from src.merger import deep_merge
from src.reader import load_yaml
from src.saver import save_yaml
from src.cleaner import remove_empty_lists, strip_optional_from_base, remove_optional_fields
from src.cleaner import OPTIONAL_SECTIONS
import logging
logging.basicConfig(level=logging.DEBUG)

load_dotenv()


MANIFEST_NAMES = ["agents", "common", "integration", "namespace"]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-st", "--stand", nargs='+', required=True)
    parser.add_argument("-tp", "--type", choices=["update", "reconf"], default="reconf")
    args = parser.parse_args()

    base_manifests = [
        load_yaml(f"base_manifests/{name}.yaml") for name in MANIFEST_NAMES
    ]
    current_manifests = [
        load_yaml(f"current_manifests/{name}.yaml") for name in MANIFEST_NAMES
    ]

    if args.type == "update":
        cleaned_base = []
        for base, name in zip(base_manifests, MANIFEST_NAMES):
            # Удаляем корневые опциональные секции (MTLS_OTT, KAFKA и т.д.)
            base_no_root_opt = strip_optional_from_base(base, OPTIONAL_SECTIONS)
            #Удаляем опциональные поля внутри блоков (например, в SECMAN)
            base_final = remove_optional_fields(base_no_root_opt, name)
            cleaned_base.append(base_final)
        base_manifests = cleaned_base

    merged_manifests = [deep_merge(b, c) for b, c in zip(base_manifests, current_manifests)]
    cleaned_manifests = [remove_empty_lists(m) for m in merged_manifests]

    save_yaml(cleaned_manifests, args.stand)

if __name__ == "__main__":
    main()