from manifestum_medicatus.models.agents import AgentConfig


def get_config():
    agent = AgentConfig(
        ENV={
            'GIGACHAT_BASE_URL': 'http://gigachat-ift.sberdevices.delta.sbrf.ru:8080/v1',
            'LOG_LEVEL': 'DEBUG',
        },
    )

    return agent.model_dump(exclude_unset=True)
