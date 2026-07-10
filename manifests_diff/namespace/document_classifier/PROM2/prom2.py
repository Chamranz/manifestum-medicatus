from manifestum_medicatus.models.namespace import IngressConfig, IstioConfig, NamespaceConfig, PatternsAgentConfig, SecManConfig


def get_config():
    namespace = NamespaceConfig(
        ISTIO=IstioConfig(
            INGRESS=IngressConfig(
                NETWORKING_MTLS={
                    'document-classifier': PatternsAgentConfig(
                        HOST='document-classifier.ci09708620-document-classifier.apps.a4sujmd3.k8s.ca.sbrf.ru',
                    ),
                },
                NETWORKING_OTT_MTLS={
                    'document-classifier': PatternsAgentConfig(
                        HOST='document-classifier-ott.ci09708620-document-classifier.apps.a4sujmd3.k8s.ca.sbrf.ru',
                    ),
                },
            ),
        ),
        SECMAN=SecManConfig(
            INGRESS_GW_SAN='document-classifier-kvaefdrpa.omega.sbrf.ru,document-classifier-ott.ci09708620-document-classifier.apps.a4sxasyr.k8s.ca.sbrf.ru,document-classifier-ott.ci09708620-document-classifier.apps.a4sujmd3.k8s.ca.sbrf.ru,document-classifier.ci09708620-document-classifier.apps.a4sujmd3.k8s.ca.sbrf.ru',
            SBER_CA_SERVER_CN='document-classifier.ci09708620-document-classifier.apps.a4sujmd3.k8s.ca.sbrf.ru',
        ),
    )

    return namespace.model_dump(exclude_unset=True)
