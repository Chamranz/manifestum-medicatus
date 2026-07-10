from manifestum_medicatus.models.agents import AgentConfig


def get_config():
    agent = AgentConfig(
        ENV={
            'AI_AGENT_DATA_BASE_URL': 'http://uvz-external-api-psi.omega.sbrf.ru:8080/ai-agent/',
            'GIGACHAT_BASE_URL': 'http://gigachat-psi.sberdevices.ca.sbrf.ru:8080/v1',
        },
    )

    return agent.model_dump(exclude_unset=True)
