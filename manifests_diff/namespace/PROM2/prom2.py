from models.namespace import NamespaceConfig, SecManConfig, DynamicInventoryConfig, FluentBitConfig, IstioLogs, \
    IstioConfig, IngressConfig, NetworkingMtlsConfig, PatternsAgentConfig, GeoroutesConfig, GeoroutePatternsConfig

def get_config():
    namespace = NamespaceConfig(
        DROPAPP_CLUSTER='a4sujmd3.k8s.ca.sbrf.ru',
        DROPAPP_CREDENTIAL_ID='a4sujmd3_k8s_ca_sbrf_ru_dropapp',
        SECMAN=SecManConfig(
            SBER_CA_SERVER_CN="strategy-selection.ci09708620-strategy-selection.apps.a4sujmd3.k8s.ca.sbrf.ru"
        ),
        ISTIO=IstioConfig(
            INGRESS=IngressConfig(
                NETWORKING_MTLS=NetworkingMtlsConfig(
                    strategy_selection=PatternsAgentConfig(
                        HOST="strategy-selection.ci09708620-strategy-selection.apps.a4sujmd3.k8s.ca.sbrf.ru",
                        PORT=5443
                    )
                )
            )
        )
    )

    return namespace.model_dump(exclude_unset=True)

