from models.namespace import NamespaceConfig, SecManConfig, DynamicInventoryConfig,FluentBitConfig,IstioLogs

def get_config():
    namespace = NamespaceConfig(
        DROPAPP_CLUSTER='a47ow1gr.k8s.ca.sbrf.ru',
        DROPAPP_CREDENTIAL_ID='a47ow1gr_k8s_ca_sbrf_ru_dropapp',
        SECMAN=SecManConfig(
            SBER_CA_SERVER_CN="strategy-selection.ci09708620-strategy-selection.apps.a47ow1gr.k8s.ca.sbrf.ru"
        )
    )

    return namespace.model_dump(exclude_unset=True)

