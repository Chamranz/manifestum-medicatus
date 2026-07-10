from manifestum_medicatus.models.agents import AgentConfig, CpuMemory, Resources


def get_config():
    agent = AgentConfig(
        AGENT_NAME='document-classifier',
        ENV={
            'AGENT_ID': 'CI10071809',
            'DOCUMENT_READER_RETRY_INCREMENT': '30',
            'DOCUMENT_READER_RETRY_LIMIT': '3',
            'DOCUMENT_READER_TIMEOUT': '180',
            'MYSTEM_BIN': '/app/resources/mystem/mystem',
            'NLTK_DATA': '/app/resources/nltk_data',
            'POD_NAMESPACE': 'ci09708620-document-classifier',
            'TRACING_SERVICE_KAFKA_BOOTSTRAP_SERVERS': '[egress-kafka-aef-istio-logs.ci09708620-document-classifier.svc.cluster.local:19093]',
        },
        RESOURCES=Resources(
            LIMITS=CpuMemory(
                CPU='500m',
                MEMORY='800Mi',
            ),
            REQUESTS=CpuMemory(
                CPU='250m',
                MEMORY='400Mi',
            ),
        ),
    )

    return agent.model_dump(exclude_unset=True)
