from manifestum_medicatus.models.common import Aef, BuildCredentials, CommonConfig, Hub, QualityGates, SonarQube


def get_config():
    common = CommonConfig(
        aef=Aef(
            id='CI09708620',
            name='AI-HUB БТ.AEF Container ДРПА КВ Alpha',
        ),
        buildCredentials=BuildCredentials(
            GIT_SSH_CREDENTIAL_ID='GIT_CONFIGS_CRED',
            OSC_TOKEN_CREDENTIAL_ID='cab-sa-dvo09991_OSC_TOKEN',
            PASS_CREDENTIAL_ID='cab-sa-dvo09991_AD_DOMAIN',
        ),
        hub=Hub(
            id='CI08967393',
            name='AI-HUB БТ',
        ),
        qg=QualityGates(
            jira_area='AAA',
            mus_code='00200044',
            mus_name='Models',
            mus_po_mail='Loshak.D.I@sberbank.ru',
            sm_id='CI09708620',
            sm_name='AI-HUB БТ.AEF Container ДРПА КВ Alpha',
        ),
        sonar_qube=SonarQube(
            installation_name='SonarQubeSigma',
            jenkins_cred='sonar-supertoken',
        ),
    )

    return common.model_dump(exclude_unset=True, exclude_none=True)
