from manifestum_medicatus.models.common import Aef, AgentsBuild, Assembly, CommonConfig, Pyinstaller, Sonar


def get_config():
    common = CommonConfig(
        aef=Aef(
            module_id='CI10663014',
        ),
        agents=[
            AgentsBuild(
                name='cash-flow-compiler',
                git='ssh://git@stash.sigma.sbrf.ru:7999/kvaef/cash-flow-compiler.git',
                path='./agents/cash_flow_compiler/v0.1',
                assembly=Assembly(
                    baseImage='docker-internal.registry-ci.delta.sbrf.ru/ci04675739/ci04675739/python-3.12:9.6.2-se',
                    aefsdk=True,
                    pyinstaller=Pyinstaller(
                        args='',
                    ),
                ),
                sonar=Sonar(
                    key='cash-flow-compiler',
                ),
                compile=False,
                type='python',
            ),
        ],
    )

    return common.model_dump(exclude_unset=True, exclude_none=True)
