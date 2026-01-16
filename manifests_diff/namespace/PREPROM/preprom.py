from models.namespace import NamespaceConfig, SecManConfig


def get_config():
    namespace = NamespaceConfig(
        STAND_TYPE="IFT",
        SECMAN=SecManConfig(
            HOST="t.secrets.delta.sbrf.ru"
        )
    )

    return namespace.model_dump(exclude_unset=True)
