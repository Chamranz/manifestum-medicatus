from manifestum_medicatus.models.namespace import NamespaceConfig


def get_config():
    namespace = NamespaceConfig(
        DROPAPP_CLUSTER='a3q7cxy1.k8s.delta.sbrf.ru',
        DROPAPP_CREDENTIAL_ID='a3q7cxy1_k8s_delta_sbrf_ru_dropapp',
    )

    return namespace.model_dump(exclude_unset=True)
