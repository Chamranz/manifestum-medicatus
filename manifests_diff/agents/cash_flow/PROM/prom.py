from manifestum_medicatus.models.agents import AgentConfig


def get_config():
    agent = AgentConfig(
        ENV={
            'AI_AGENT_DATA_BASE_URL': 'http://uvz-external-api-prom.omega.sbrf.ru:8080/ai-agent/',
        },
    )

    return agent.model_dump(exclude_unset=True)
