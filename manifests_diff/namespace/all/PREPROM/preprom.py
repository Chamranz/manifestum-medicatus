from manifestum_medicatus.models.namespace import NamespaceConfig, SecManConfig


def get_config():
    namespace = NamespaceConfig(
        SECMAN=SecManConfig(
            HOST='t.secrets.delta.sbrf.ru',
        ),
        STAND_TYPE='IFT',
    )

    return namespace.model_dump(exclude_unset=True)
