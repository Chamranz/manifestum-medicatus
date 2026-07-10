from manifestum_medicatus.models.namespace import NamespaceConfig, SecManConfig


def get_config():
    namespace = NamespaceConfig(
        SECMAN=SecManConfig(
            INGRESS_GW_SAN='cash-flow-compiler.ci09708620-cash-flow-compiler.apps.a3q0odr0.k8s.delta.sbrf.ru',
            SBER_CA_CLIENT_CN='CI09708620-CI10663014-cash-flow-compiler-dev',
            SBER_CA_SERVER_CN='cash-flow-compiler.ci09708620-cash-flow-compiler.apps.a3q0odr0.k8s.delta.sbrf.ru',
        ),
    )

    return namespace.model_dump(exclude_unset=True)
