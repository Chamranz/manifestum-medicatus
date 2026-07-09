from manifestum_medicatus.models.agents import AgentConfig


def get_config():
    env = {
        "LOG_LEVEL": "DEBUG",
        "GIGACHAT_BASE_URL": "http://gigachat-ift.sberdevices.delta.sbrf.ru:8080/v1",
        "DOCUMENT_READER_BASE_URL": 'http://uvz-external-api.delta.sbrf.ru:8080/document-reader/'
    }

    return AgentConfig(
        ENV=env,
    ).model_dump(exclude_unset=True)
