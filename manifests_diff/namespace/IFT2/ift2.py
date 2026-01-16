from models.namespace import NamespaceConfig, SecManConfig, DynamicInventoryConfig, FluentBitConfig, IstioLogs, \
    IstioConfig, IngressConfig, NetworkingMtlsConfig, PatternsAgentConfig, GeoroutesConfig, GeoroutePatternsConfig

def get_config():
    namespace = NamespaceConfig(
        DROPAPP_CLUSTER='a4x981tp.k8s.delta.sbrf.ru',
        DROPAPP_CREDENTIAL_ID='a4x981tp_k8s_delta_sbrf_ru_dropapp',
        SECMAN=SecManConfig(
            SBER_CA_SERVER_CN="strategy-selection.ci09708620-strategy-selection.apps.a4x981tp.k8s.delta.sbrf.ruu"
        ),
        ISTIO=IstioConfig(
            INGRESS=IngressConfig(
                NETWORKING_MTLS=NetworkingMtlsConfig(
                    strategy_selection=PatternsAgentConfig(
                        HOST="strategy-selection.ci09708620-strategy-selection.apps.a4x981tp.k8s.delta.sbrf.ru",
                        PORT=5443
                    )
                )
            )
        )
    )

    return namespace.model_dump(exclude_unset=True)

