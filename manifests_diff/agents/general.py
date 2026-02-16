from models.agents import AgentConfig, Resources, CpuMemory, ProbeConfig, Probe


def get_config():
    env = {
        "LOG_FILE": "/var/log/app/app.log",
        "AGENT_METRICS_LOG_FILE": "/var/log/app/app.log",
        "AGENT_ID": "CI10663014",
        "GIGACHAT_TIMEOUT": 60,
        "GIGACHAT_RETRY_LIMIT": 3,
        "GIGACHAT_RETRY_INCREMENT": 15,
        "GIGACHAT_ENABLE_PREVIEW": True,
        "GIGACHAT_PREVIEW_PROBABILITY": 0.05,
        "AI_AGENT_DATA_TIMEOUT": 60,
        "AI_AGENT_DATA_RETRY_LIMIT": 3,
        "AI_AGENT_DATA_RETRY_INCREMENT": 15,
        "LIVENESS_PROBE_PATH": "/health/liveness",
        "READINESS_PROBE_PATH": "/health/readiness"
    }

    agents = AgentConfig(
        AGENT_NAME="strategy-selection",
        RESOURCES=Resources(
            REPLICAS=2,
            LIMITS=CpuMemory(
                CPU="350m",
                MEMORY="512Mi"
            ),
            REQUESTS=CpuMemory(
                CPU="150m",
                MEMORY="256Mi"
            )
        ),
        PROBE=Probe(
            READINESS=ProbeConfig(
                INITIAL_DELAY_SECONDS=30,
                TIMEOUT_SECONDS=5,
                PERIOD_SECONDS=15,
                SUCCESS_THRESHOLD=1,
                FAILURE_THRESHOLD=3
            ),
            LIVENESS=ProbeConfig(
                INITIAL_DELAY_SECONDS=30,
                TIMEOUT_SECONDS=5,
                PERIOD_SECONDS=60,
                SUCCESS_THRESHOLD=1,
                FAILURE_THRESHOLD=3
            )
        ),
        ENV=env,
    )

    return agents.model_dump(exclude_unset=True)

