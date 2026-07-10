from manifestum_medicatus.models.namespace import GeoroutesConfig, IngressConfig, IstioConfig, NamespaceConfig, OttConfig, PatternsAgentConfig, SecManConfig


def get_config():
    namespace = NamespaceConfig(
        ISTIO=IstioConfig(
            INGRESS=IngressConfig(
                NETWORKING_MTLS={
                    'document-classifier': PatternsAgentConfig(
                        PORT=5443,
                    ),
                },
                NETWORKING_OTT_MTLS={
                    'document-classifier': PatternsAgentConfig(
                        GEOROUTES={
                            'georoute-document-classifier': GeoroutesConfig(
                                HOST='document-classifier-kvaefdrpa.omega.sbrf.ru',
                                PORT=2446,
                            ),
                        },
                        PORT=5445,
                    ),
                },
            ),
        ),
        OTT=OttConfig(
            BILLING_ACCOUNT='CI09708620-CI10071809-OTTYUL',
        ),
        SECMAN=SecManConfig(
            SBER_CA_CLIENT_CN='CI09708620-CI10071809-document-classifier-prom',
            SBER_CA_OTT_CN='CI09708620-CI10071809-OTTYUL',
        ),
    )

    return namespace.model_dump(exclude_unset=True)
