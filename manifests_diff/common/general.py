from models.common import CommonConfig, Hub, Aef, AgentsBuild, QualityGates, BuildCredentials, SonarQube


def get_config():
    hub = Hub(
        name="AI-HUB БТ",
        id="CI08967393",
    )

    aef = Aef(
        name="AI-HUB БТ.AEF Container ДРПА КВ Alpha",
        id="CI09708620",
        module_id="CI10663014"
    )

    agents = AgentsBuild(
        name="strategy-selection",
        git="ssh://git@stash.sigma.sbrf.ru:7999/kvaef/strategy-selection.git",
        path="./agents/strategy_selection/v0.1",
        baseImage="docker-internal.registry-ci.delta.sbrf.ru/ci04675739/ci04675739/python-3.11:9.6.2-se",
        compile=False,
        # (опционально) Ключ проекта sonar к которому привязывается агент
        sonar_key="strategy-selection",
        type="python",
    )

    sonarqube = SonarQube(
        jenkins_cred='sonar-token',
        installation_name='SonarQubeSigma',
    )

    qg = QualityGates(
        mus_code="00200044",
        # Имя команды
        mus_name="Models",
        mus_po_mail="Loshak.D.I@sberbank.ru",
        # КЭ агента
        sm_id="CI09708620",
        # Имя агента
        sm_name="AI-HUB БТ.AEF Container ДРПА КВ Alpha",
        jira_area="AAA",
    )

    buildCredentials = BuildCredentials(
        GIT_SSH_CREDENTIAL_ID='GIT_CONFIGS_CRED',
        # Секрет с ТУЗом в формате tuz@delta.sbrf.ru + паролем от AD движка SecMan
        PASS_CREDENTIAL_ID='cab-sa-dvo09991_AD_DOMAIN',
        # Секрет с OSC токеном для PyPi
        OSC_TOKEN_CREDENTIAL_ID='cab-sa-dvo09991_OSC_TOKEN',
    )

    common = CommonConfig(
        hub=hub,
        aef=aef,
        sonar_qube=sonarqube,
        agents=[agents],
        qg=qg,
        buildCredentials=buildCredentials
    )

    return common.model_dump(exclude_unset=True)
