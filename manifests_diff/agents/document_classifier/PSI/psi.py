from manifestum_medicatus.models.agents import CpuMemory, Resources, Probe, ProbeConfig, AgentConfig


def get_config():
    env = {
        "LOG_LEVEL": "DEBUG",
        "GIGACHAT_BASE_URL": 'http://gigachat-psi.sberdevices.omega.sbrf.ru:8080/v1',
        "DOCUMENT_READER_BASE_URL": 'http://uvz-external-api-psi.omega.sbrf.ru:8080/document-reader/',
        "TRACING_SERVICE_KAFKA_OUTBOX_TOPIC": 'tracingservice_BT_ALPHA',
        "KAFKA_BOOTSTRAP_SERVERS": '[egress-kafka-agents-kafka-async.ci09708620-document-classifier.svc.cluster.local:19095]',
        "KAFKA_INBOX_TOPIC": 'UVZ.CI09708620_DOCUMENT_CLASSIFIER_IN_EVENT',
        "KAFKA_OUTBOX_TOPIC": 'UVZ.CI09708620_DOCUMENT_CLASSIFIER_OUT_EVENT',
        "KAFKA_SECURITY_PROTOCOL": 'PLAINTEXT',
        "KAFKA_GROUP_ID": 'CI09708620-document-classifier',
    }

    agents = AgentConfig(
        ENV=env,
    )

    return agents.model_dump(exclude_unset=True)