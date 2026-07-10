from manifestum_medicatus.models.namespace import NamespaceConfig, SecManConfig


def get_config():
    namespace = NamespaceConfig(
        DROPAPP_NAMESPACE='ci09708620-cash-flow-compiler',
        EIGW_NAMESPACE='ci09708620-cash-flow-compiler',
        SECMAN=SecManConfig(
            ROLE_NAME='ci09708620-cash-flow-compiler',
        ),
    )

    return namespace.model_dump(exclude_unset=True)
