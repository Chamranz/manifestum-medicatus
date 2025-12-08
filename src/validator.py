from models.agents import AgentConfig
from models.common import CommonConfig
from models.namespace import NamespaceConfig
from models.integrations import IntegrationConfig
import sys

conf = {
    "agents": AgentConfig,
    "common": CommonConfig,
    "namespace": NamespaceConfig,
    "integrations": IntegrationConfig,
}

def validate(manifests_type, merged_dict):
    try:
        print("start final validate")
        final_obj = conf[f"{manifests_type}"](**merged_dict)
        print("end final validate")
    except Exception as e:
        print(f"Финальная версия манифеста не вышла:{e}")
        sys.exit(1)
    return final_obj