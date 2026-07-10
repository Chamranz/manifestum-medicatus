from manifestum_medicatus.models.namespace import IngressConfig, IstioConfig, NamespaceConfig, PatternsAgentConfig, SecManConfig


def get_config():
    namespace = NamespaceConfig(
        ISTIO=IstioConfig(
            INGRESS=IngressConfig(
                NETWORKING_MTLS={
                    'cash-flow-compiler': PatternsAgentConfig(
                        HOST='cash-flow-compiler.ci09708620-cash-flow-compiler.apps.a472facr.k8s.omega.sbrf.ru',
                    ),
                },
                NETWORKING_OTT_MTLS={
                    'cash-flow-compiler': PatternsAgentConfig(
                        HOST='cash-flow-compiler-ott.ci09708620-cash-flow-compiler.apps.a472facr.k8s.omega.sbrf.ru',
                    ),
                },
            ),
        ),
        SECMAN=SecManConfig(
            INGRESS_GW_SAN='cash-flow-compiler-kvaefdrpa-psi.omega.sbrf.ru,cash-flow-compiler-ott.ci09708620-cash-flow-compiler.apps.a472facr.k8s.omega.sbrf.ru,cash-flow-compiler-ott.ci09708620-cash-flow-compiler.apps.a47ow1gr.k8s.ca.sbrf.ru,cash-flow-compiler.ci09708620-cash-flow-compiler.apps.a472facr.k8s.omega.sbrf.ru',
            SBER_CA_SERVER_CN='cash-flow-compiler.ci09708620-cash-flow-compiler.apps.a472facr.k8s.omega.sbrf.ru',
        ),
    )

    return namespace.model_dump(exclude_unset=True)
