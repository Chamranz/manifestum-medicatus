from manifestum_medicatus.models.namespace import GeoroutesConfig, IngressConfig, IstioConfig, NamespaceConfig, OttConfig, PatternsAgentConfig, SecManConfig


def get_config():
    namespace = NamespaceConfig(
        ISTIO=IstioConfig(
            INGRESS=IngressConfig(
                NETWORKING_MTLS={
                    'cash-flow-compiler': PatternsAgentConfig(
                        PORT=5443,
                    ),
                },
                NETWORKING_OTT_MTLS={
                    'cash-flow-compiler': PatternsAgentConfig(
                        GEOROUTES={
                            'georoute-cash-flow-compiler': GeoroutesConfig(
                                HOST='cash-flow-compiler-kvaefdrpa.delta.sbrf.ru',
                                PORT=2446,
                            ),
                        },
                        PORT=5445,
                    ),
                },
            ),
        ),
        OTT=OttConfig(
            BILLING_ACCOUNT='CI09708620-CI10663014-OTTYUL',
        ),
        SECMAN=SecManConfig(
            SBER_CA_CLIENT_CN='CI09708620-CI10663014-cash-flow-compiler-ift',
            SBER_CA_OTT_CN='CI09708620-CI10663014-OTTYUL',
        ),
    )

    return namespace.model_dump(exclude_unset=True)
