from manifestum_medicatus.models.agents import AgentConfig


def get_config():
    agent = AgentConfig(
        ENV={
            'DOCUMENT_READER_BASE_URL': 'http://uvz-external-api-prom.omega.sbrf.ru:8080/document-reader/',
        },
    )

    return agent.model_dump(exclude_unset=True)
