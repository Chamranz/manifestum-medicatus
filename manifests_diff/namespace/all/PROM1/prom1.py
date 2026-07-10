from manifestum_medicatus.models.namespace import NamespaceConfig


def get_config():
    namespace = NamespaceConfig(
        DROPAPP_CLUSTER='a4sxasyr.k8s.ca.sbrf.ru',
        DROPAPP_CREDENTIAL_ID='a4sxasyr_k8s_ca_sbrf_ru_dropapp',
    )

    return namespace.model_dump(exclude_unset=True)
