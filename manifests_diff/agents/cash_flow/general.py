from manifestum_medicatus.models.agents import AgentConfig, CpuMemory, Resources


def get_config():
    agent = AgentConfig(
        AGENT_NAME='cash-flow-compiler',
        ENV={
            'AGENT_ID': 'CI10663014',
            'AGENT_METRICS_LOG_FILE': '/var/log/app/app.log',
            'AI_AGENT_DATA_RETRY_INCREMENT': '15',
            'AI_AGENT_DATA_RETRY_LIMIT': '3',
            'AI_AGENT_DATA_TIMEOUT': '60',
            'POD_NAMESPACE': 'ci09708620-cash-flow-compiler',
            'TRACING_SERVICE_KAFKA_BOOTSTRAP_SERVERS': '[egress-kafka-aef-istio-logs.ci09708620-cash-flow-compiler.svc.cluster.local:19093]',
        },
        RESOURCES=Resources(
            LIMITS=CpuMemory(
                CPU='350m',
                MEMORY='512Mi',
            ),
            REQUESTS=CpuMemory(
                CPU='150m',
                MEMORY='256Mi',
            ),
        ),
    )

    return agent.model_dump(exclude_unset=True)
