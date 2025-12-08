from models.namespace import NamespaceConfig, SecManConfig, DynamicInventoryConfig,FluentBitConfig,IstioLogs

def get_config():
    namespace = NamespaceConfig(
        DROPAPP_CLUSTER='a3q7cxy1.k8s.delta.sbrf.ru',
        DROPAPP_CREDENTIAL_ID='a3q7cxy1_k8s_delta_sbrf_ru_dropapp',
        SECMAN=SecManConfig(
            SBER_CA_SERVER_CN="strategy-selection.ci09708620-strategy-selection.apps.a3q7cxy1.k8s.delta.sbrf.ru"
        )
    )

    return namespace.model_dump(exclude_unset=True)

