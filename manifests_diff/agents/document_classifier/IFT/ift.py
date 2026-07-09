from manifestum_medicatus.models.agents import AgentConfig

def get_config():
    env = {
        "KAFKA_BOOTSTRAP_SERVERS": '[egress-kafka-agents-kafka-async.ci09708620-document-classifier.svc.cluster.local:19095]',
        "KAFKA_INBOX_TOPIC": 'UVZ.CI09708620_DOCUMENT_CLASSIFIER_IN_EVENT',
        "KAFKA_OUTBOX_TOPIC": 'UVZ.CI09708620_DOCUMENT_CLASSIFIER_OUT_EVENT',
        "KAFKA_SECURITY_PROTOCOL": 'PLAINTEXT',
        "KAFKA_GROUP_ID": 'CI09708620-document-classifier',
        "TRACING_SERVICE_KAFKA_OUTBOX_TOPIC": 'tracingservice_BT_ALPHA',
    }

    agent = AgentConfig(ENV=env)

    return agent.model_dump(exclude_unset=True)