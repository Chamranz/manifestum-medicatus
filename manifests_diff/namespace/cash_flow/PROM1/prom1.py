from manifestum_medicatus.models.namespace import IngressConfig, IstioConfig, NamespaceConfig, PatternsAgentConfig, SecManConfig


def get_config():
    namespace = NamespaceConfig(
        ISTIO=IstioConfig(
            INGRESS=IngressConfig(
                NETWORKING_MTLS={
                    'cash-flow-compiler': PatternsAgentConfig(
                        HOST='cash-flow-compiler.ci09708620-cash-flow-compiler.apps.a4sxasyr.k8s.ca.sbrf.ru',
                    ),
                },
                NETWORKING_OTT_MTLS={
                    'cash-flow-compiler': PatternsAgentConfig(
                        HOST='cash-flow-compiler-ott.ci09708620-cash-flow-compiler.apps.a4sxasyr.k8s.ca.sbrf.ru',
                    ),
                },
            ),
        ),
        SECMAN=SecManConfig(
            INGRESS_GW_SAN='cash-flow-compiler-kvaefdrpa.omega.sbrf.ru,cash-flow-compiler-ott.ci09708620-cash-flow-compiler.apps.a4sxasyr.k8s.ca.sbrf.ru,cash-flow-compiler-ott.ci09708620-cash-flow-compiler.apps.a4sujmd3.k8s.ca.sbrf.ru,cash-flow-compiler.ci09708620-cash-flow-compiler.apps.a4sxasyr.k8s.ca.sbrf.ru',
            SBER_CA_SERVER_CN='cash-flow-compiler.ci09708620-cash-flow-compiler.apps.a4sxasyr.k8s.ca.sbrf.ru',
        ),
    )

    return namespace.model_dump(exclude_unset=True)
