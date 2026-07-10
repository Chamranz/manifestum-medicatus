from manifestum_medicatus.models.agents import AgentConfig, Probe, ProbeConfig, Resources


def get_config():
    agent = AgentConfig(
        ENV={
            'GIGACHAT_ENABLE_PREVIEW': 'true',
            'GIGACHAT_PREVIEW_PROBABILITY': '0.05',
            'GIGACHAT_RETRY_INCREMENT': '15',
            'GIGACHAT_RETRY_LIMIT': '3',
            'GIGACHAT_TIMEOUT': '60',
            'LIVENESS_PROBE_PATH': '/health/liveness',
            'LOG_FILE': '/var/log/app/app.log',
            'READINESS_PROBE_PATH': '/health/readiness',
            'REST_PROBE_PATH': '/rest/health',
        },
        PROBE=Probe(
            LIVENESS=ProbeConfig(
                FAILURE_THRESHOLD=3,
                INITIAL_DELAY_SECONDS=30,
                PERIOD_SECONDS=60,
                SUCCESS_THRESHOLD=1,
                TIMEOUT_SECONDS=5,
            ),
            READINESS=ProbeConfig(
                FAILURE_THRESHOLD=3,
                INITIAL_DELAY_SECONDS=30,
                PERIOD_SECONDS=60,
                SUCCESS_THRESHOLD=1,
                TIMEOUT_SECONDS=5,
            ),
        ),
        RESOURCES=Resources(
            REPLICAS=2,
        ),
    )

    return agent.model_dump(exclude_unset=True)
