from manifestum_medicatus.models.namespace import IngressConfig, IstioConfig, NamespaceConfig, PatternsAgentConfig, SecManConfig


def get_config():
    namespace = NamespaceConfig(
        ISTIO=IstioConfig(
            INGRESS=IngressConfig(
                NETWORKING_MTLS={
                    'document-classifier': PatternsAgentConfig(
                        HOST='document-classifier.ci09708620-document-classifier.apps.a4x981tp.k8s.delta.sbrf.ru',
                    ),
                },
                NETWORKING_OTT_MTLS={
                    'document-classifier': PatternsAgentConfig(
                        HOST='document-classifier-ott.ci09708620-document-classifier.apps.a4x981tp.k8s.delta.sbrf.ru',
                    ),
                },
            ),
        ),
        SECMAN=SecManConfig(
            INGRESS_GW_SAN='document-classifier-kvaefdrpa.delta.sbrf.ru,document-classifier-ott.ci09708620-document-classifier.apps.a3q7cxy1.k8s.delta.sbrf.ru,document-classifier-ott.ci09708620-document-classifier.apps.a4x981tp.k8s.delta.sbrf.ru,document-classifier.ci09708620-document-classifier.apps.a4x981tp.k8s.delta.sbrf.ru',
            SBER_CA_SERVER_CN='document-classifier.ci09708620-document-classifier.apps.a4x981tp.k8s.delta.sbrf.ru',
        ),
    )

    return namespace.model_dump(exclude_unset=True)
