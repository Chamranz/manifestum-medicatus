from manifestum_medicatus.models.agents import AgentConfig


def get_config():
    agent = AgentConfig(
        ENV={
            'GIGACHAT_BASE_URL': 'http://gigachat.sberdevices.omega.sbrf.ru:8080/v1',
            'TRACING_SERVICE_KAFKA_OUTBOX_TOPIC': 'tracingservice_BT_ALPHA',
        },
    )

    return agent.model_dump(exclude_unset=True)
