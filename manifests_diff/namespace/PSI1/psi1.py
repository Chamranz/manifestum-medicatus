from models.namespace import NamespaceConfig, SecManConfig, DynamicInventoryConfig,FluentBitConfig,IstioLogs

def get_config():
    namespace = NamespaceConfig(
        DROPAPP_CLUSTER='a472facr.k8s.omega.sbrf.ru',
        DROPAPP_CREDENTIAL_ID='a472facr_k8s_omega_sbrf_ru_dropapp',
        SECMAN=SecManConfig(
            SBER_CA_SERVER_CN="strategy-selection.ci09708620-strategy-selection.apps.a472facr.k8s.omega.sbrf.ru"
        )
    )

    return namespace.model_dump(exclude_unset=True)

