from models.agents import CpuMemory, Resources, Probe, ProbeConfig, AgentConfig
from src.reader import load_yaml


def get_config():
    env = {
        "LOG_LEVEL": "DEBUG",
        "GIGACHAT_BASE_URL": 'http://gigachat-psi.sberdevices.ca.sbrf.ru:8080/v1',
        "AI_AGENT_DATA_BASE_URL": "http://uvz-external-api-psi.omega.sbrf.ru:8080/ai-agent/",
        "TRACING_SERVICE_KAFKA_OUTBOX_TOPIC": 'tracingservice_BT_ALPHA',
        "TRACING_SERVICE_KAFKA_BOOTSTRAP_SERVERS": '[tvloq-btaaf0004.omega.sbrf.ru:9093,tvloq-btaaf0003.omega.sbrf.ru:9093,tvloq-btaaf0002.omega.sbrf.ru:9093,tvloq-btaaf0001.omega.sbrf.ru:9093]',
        "POD_NAMESPACE": 'ci09708620-strategy-selection'
    }

    agents = AgentConfig(
        ENV=env,
    )

    return agents.model_dump(exclude_unset=True)