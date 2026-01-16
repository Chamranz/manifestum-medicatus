from models.agents import AgentConfig

def get_config():
    env = { "TRACING_SERVICE_KAFKA_OUTBOX_TOPIC": 'tracingservice_BT_ALPHA',
    "TRACING_SERVICE_KAFKA_BOOTSTRAP_SERVERS": '[tvldq-btaaf0003.delta.sbrf.ru:9093,tvldq-btaaf0001.delta.sbrf.ru:9093,'
                                               'tvldq-btaaf0002.delta.sbrf.ru:9093,tvldq-btaaf0005.delta.sbrf.ru:9093]',
    "POD_NAMESPACE": 'ci09708620-strategy-selection'}

    agent = AgentConfig(ENV=env)

    return agent.model_dump(exclude_unset=True)