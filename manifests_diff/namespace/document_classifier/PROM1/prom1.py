from manifestum_medicatus.models.namespace import NamespaceConfig, SecManConfig, DynamicInventoryConfig, FluentBitConfig, IstioLogs, \
    IstioConfig, IngressConfig, PatternsAgentConfig, GeoroutesConfig

def get_config():
    namespace = NamespaceConfig(
        DROPAPP_CLUSTER='a4sxasyr.k8s.ca.sbrf.ru',
        DROPAPP_CREDENTIAL_ID='a4sxasyr_k8s_ca_sbrf_ru_dropapp',
        SECMAN=SecManConfig(
            SBER_CA_SERVER_CN="document-classifier.ci09708620-document-classifier.apps.a4sxasyr.k8s.ca.sbrf.ru",
            INGRESS_GW_SAN="document-classifier-kvaefdrpa.omega.sbrf.ru,document-classifier-ott.ci09708620-document-classifier.apps.a4sxasyr.k8s.ca.sbrf.ru,document-classifier-ott.ci09708620-document-classifier.apps.a4sujmd3.k8s.ca.sbrf.ru,document-classifier.ci09708620-document-classifier.apps.a4sxasyr.k8s.ca.sbrf.ru"
        ),
        ISTIO=IstioConfig(
            INGRESS=IngressConfig(
                NETWORKING_MTLS={
                    "document-classifier": PatternsAgentConfig(
                        HOST="document-classifier.ci09708620-document-classifier.apps.a4sxasyr.k8s.ca.sbrf.ru",
                        PORT=5443
                    )
                },
                NETWORKING_OTT_MTLS={
                    "document-classifier": PatternsAgentConfig(
                        HOST="document-classifier-ott.ci09708620-document-classifier.apps.a4sxasyr.k8s.ca.sbrf.ru",
                        PORT=5445
                    )
                }
            ),
        ),
    )

    return namespace.model_dump(exclude_unset=True)

