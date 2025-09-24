from pydantic import BaseModel, Field
from typing import Optional, List, Dict


# БЛОК С РЕСУРСАМИ
class ResourceLimits(BaseModel):
    CPU: Optional[str] = None
    MEMORY: Optional[str] = None


class Resources(BaseModel):
    REPLICAS: Optional[int] = None
    LIMITS: Optional[ResourceLimits] = None
    REQUESTS: Optional[ResourceLimits] = None


# БЛОК ПРО PROBE
class ProbeConfig(BaseModel):
    # Время задержки (в секундах) перед первым выполнением. Optional
    INITIAL_DELAY_SECONDS: Optional[int] = None
    # Максимальное время ожидания ответа от приложения. Optional
    TIMEOUT_SECONDS: Optional[int] = None
    # Интервал между последовательными проверками. Optional
    PERIOD_SECONDS: Optional[int] = None
    # Количество подряд успешных проверок. Optional
    SUCCESS_THRESHOLD: Optional[int] = None
    # Количество подряд неудачных проверок. Optional
    FAILURE_THRESHOLD: Optional[int] = None


class Probe(BaseModel):
    READINESS: Optional[ProbeConfig] = None
    LIVENESS: Optional[ProbeConfig] = None


# ИНТЕГРАЛНЫЙ БЛОК ПРО КОНКРЕТНОГО АГЕНТА
class Agent(BaseModel):
    AGENT_NAME: str = None
    RESOURCES: Optional[Resources] = None
    PROBE: Optional[Probe] = None
    ENV: Optional[Dict[str, str]] = None
    SECRET_ENV: Optional[List[str]] = None


# ИНТЕГРАЛЬНЫЙ БЛОК СО ВСЕМИ АГЕНТАМИ
class AgentsConfig(BaseModel):
    agents: List[Agent]