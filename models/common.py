from pydantic import BaseModel
from typing import List, Optional

class Hub(BaseModel):
    name: str = "Укажи меня"
    id: str = "Укажи меня"

class Aef(BaseModel):
    name: str = "Укажи меня"
    id: str = "Укажи меня"
    module_id: str = "Укажи меня"

class AgentsBuild(BaseModel):
    name: str = "Укажи меня"
    git: str = "Укажи меня"
    path: str = "Укажи меня"
    baseImage: str = "Укажи меня"
    compile: bool = False
    sonar_key: str = "Укажи меня",
    type: str = "pyhon",


class SonarQube(BaseModel):
    # Наименование jenkins credentials в котором содержится токен для авторизации
    jenkins_cred: str = 'sonar-token'
    # Сегмент SonarQube
    installation_name: str = 'SonarQubeSigma'


class QualityGates(BaseModel):
    mus_code: str = "Укажи меня"
    mus_name: str = "Укажи меня"
    mus_po_mail: str = "Укажи меня"
    sm_id: str = "Укажи меня"
    sm_name: str = "Укажи меня"
    jira_area: str = "Укажи меня"

class BuildCredentials(BaseModel):
    GIT_SSH_CREDENTIAL_ID: str = "Укажи меня"
    # Секрет с ТУЗом в формате tuz@delta.sbrf.ru + паролем от AD движка SecMan
    PASS_CREDENTIAL_ID: str = "Укажи меня"
    # Секрет с OSC токеном для PyPi
    OSC_TOKEN_CREDENTIAL_ID: str = "Укажи меня"

class CommonConfig(BaseModel):
    hub: Hub = "Укажи меня"
    aef: Aef = "Укажи меня"
    sonar_qube: SonarQube = "Укажи меня"
    agents: List[AgentsBuild] = "Укажи меня"
    qg: QualityGates = "Укажи меня"
    buildCredentials: BuildCredentials = "Укажи меня"