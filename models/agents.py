from pydantic import BaseModel
from typing import Dict, Optional, Union


class CpuMemory(BaseModel):
    CPU: str = "Укажи меня"
    MEMORY: str = "Укажи меня"

class Resources(BaseModel):
    REPLICAS: int = 2
    LIMITS: CpuMemory = CpuMemory(CPU="350m", MEMORY="512Mi")
    REQUESTS: CpuMemory = CpuMemory(CPU="150m", MEMORY="256Mi")

class ProbeConfig(BaseModel):
    INITIAL_DELAY_SECONDS: int = "Укажи меня"
    TIMEOUT_SECONDS: int = "Укажи меня"
    PERIOD_SECONDS: int = "Укажи меня"
    SUCCESS_THRESHOLD: int = "Укажи меня"
    FAILURE_THRESHOLD: int = "Укажи меня"

class Probe(BaseModel):
    READINESS: ProbeConfig = ProbeConfig(
        INITIAL_DELAY_SECONDS=30,
        TIMEOUT_SECONDS=5,
        PERIOD_SECONDS=60,
        SUCCESS_THRESHOLD=1,
        FAILURE_THRESHOLD=3
    )
    LIVENESS: ProbeConfig = ProbeConfig(
        INITIAL_DELAY_SECONDS=30,
        TIMEOUT_SECONDS=5,
        PERIOD_SECONDS=15,
        SUCCESS_THRESHOLD=1,
        FAILURE_THRESHOLD=3
    )

class AgentConfig(BaseModel):
    AGENT_NAME: str = "Укажи меня братка"
    RESOURCES: Resources = "Укажи меня братка"
    PROBE: Probe = "Укажи меня братка"
    ENV: Dict[str, Union[str,int]] = "Укажи меня"