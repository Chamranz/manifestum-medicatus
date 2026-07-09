from manifestum_medicatus.models.namespace import NamespaceConfig, SecManConfig, DynamicInventoryConfig, FluentBitConfig, IstioLogs, \
    IstioConfig, IngressConfig, PatternsAgentConfig, GeoroutesConfig

def get_config():
    namespace = NamespaceConfig(
        DROPAPP_CLUSTER='a4x981tp.k8s.delta.sbrf.ru',
        DROPAPP_CREDENTIAL_ID='a4x981tp_k8s_delta_sbrf_ru_dropapp',
        SECMAN=SecManConfig(
            SBER_CA_SERVER_CN="document-classifier.ci09708620-document-classifier.apps.a4x981tp.k8s.delta.sbrf.ru",
            INGRESS_GW_SAN="document-classifier-kvaefdrpa.delta.sbrf.ru,document-classifier-ott.ci09708620-document-classifier.apps.a3q7cxy1.k8s.delta.sbrf.ru,document-classifier-ott.ci09708620-document-classifier.apps.a4x981tp.k8s.delta.sbrf.ru,document-classifier.ci09708620-document-classifier.apps.a4x981tp.k8s.delta.sbrf.ru"
        ),
        ISTIO=IstioConfig(
            INGRESS=IngressConfig(
                NETWORKING_MTLS={
                    "document-classifier": PatternsAgentConfig(
                        HOST="document-classifier.ci09708620-document-classifier.apps.a4x981tp.k8s.delta.sbrf.ru",
                        PORT=5443
                    )
                },
                NETWORKING_OTT_MTLS={
                    "document-classifier": PatternsAgentConfig(
                        HOST="document-classifier-ott.ci09708620-document-classifier.apps.a4x981tp.k8s.delta.sbrf.ru",
                        PORT=5445
                    )
                }
            ),
        ),
    )

    return namespace.model_dump(exclude_unset=True)

