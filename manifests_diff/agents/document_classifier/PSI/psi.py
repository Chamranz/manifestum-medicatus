from manifestum_medicatus.models.agents import AgentConfig


def get_config():
    agent = AgentConfig(
        ENV={
            'DOCUMENT_READER_BASE_URL': 'http://uvz-external-api-psi.omega.sbrf.ru:8080/document-reader/',
            'GIGACHAT_BASE_URL': 'http://gigachat-psi.sberdevices.omega.sbrf.ru:8080/v1',
        },
    )

    return agent.model_dump(exclude_unset=True)
