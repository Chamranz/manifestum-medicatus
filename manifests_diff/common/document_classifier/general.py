from manifestum_medicatus.models.common import Aef, AgentsBuild, Assembly, CommonConfig, Pyinstaller, Sonar


def get_config():
    common = CommonConfig(
        aef=Aef(
            module_id='CI10071809',
        ),
        agents=[
            AgentsBuild(
                name='document-classifier',
                git='ssh://git@stash.sigma.sbrf.ru:7999/kvaef/document-classifier.git',
                path='./agents/document_classifier/v0.1',
                assembly=Assembly(
                    baseImage='docker-internal.registry-ci.delta.sbrf.ru/ci04675739/ci04675739/python-3.12:9.6.2-se',
                    aefsdk=True,
                    pyinstaller=Pyinstaller(
                        args='',
                    ),
                ),
                sonar=Sonar(
                    key='document-classifier',
                ),
                compile=False,
                type='python',
            ),
        ],
    )

    return common.model_dump(exclude_unset=True, exclude_none=True)
