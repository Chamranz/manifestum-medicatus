from manifestum_medicatus.models.namespace import NamespaceConfig


def get_config():
    namespace = NamespaceConfig(
        DROPAPP_CLUSTER='a472facr.k8s.omega.sbrf.ru',
        DROPAPP_CREDENTIAL_ID='a472facr_k8s_omega_sbrf_ru_dropapp',
    )

    return namespace.model_dump(exclude_unset=True)
