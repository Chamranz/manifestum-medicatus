from manifestum_medicatus.models.namespace import NamespaceConfig


def get_config():
    namespace = NamespaceConfig()

    return namespace.model_dump(exclude_unset=True)
