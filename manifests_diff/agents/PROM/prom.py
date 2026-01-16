from models.agents import CpuMemory, Resources, Probe, ProbeConfig, AgentConfig
from src.reader import load_yaml


def get_config():
    env = {
        "GIGACHAT_BASE_URL": 'http://gigachat.sberdevices.omega.sbrf.ru:8080/v1',
        "AI_AGENT_DATA_BASE_URL": "http://uvz-external-api-prom.omega.sbrf.ru:8080/ai-agent/",
        "TRACING_SERVICE_KAFKA_OUTBOX_TOPIC": 'tracingservice_BT_ALPHA',
        "TRACING_SERVICE_KAFKA_BOOTSTRAP_SERVERS": '[pvloq-btaaf0006.omega.sbrf.ru:9093,pvloq-btaaf0008.omega.sbrf.ru:9093,'
                                                   'pvloq-btaaf0009.omega.sbrf.ru:9093,pvloq-btaaf0007.omega.sbrf.ru:9093]',
        "POD_NAMESPACE": 'ci09708620-strategy-selection'
    }

    agents = AgentConfig(
        ENV=env,
    )

    return agents.model_dump(exclude_unset=True)



