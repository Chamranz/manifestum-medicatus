from models.agents import CpuMemory, Resources, Probe, ProbeConfig, AgentConfig
from src.reader import load_yaml


def get_config():
    env = {
        "GIGACHAT_BASE_URL": "http://gigachat-prom.sberdevices.ca.sbrf.ru:8080/v1",
        "AI_AGENT_DATA_BASE_URL": "http://uvz-external-api-prom.omega.sbrf.ru:8080/ai-agent/",
    }

    agents = AgentConfig(
        ENV=env,
    )

    return agents.model_dump(exclude_unset=True)



