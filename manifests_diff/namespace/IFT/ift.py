from models.namespace import NamespaceConfig, SecManConfig, DynamicInventoryConfig, FluentBitConfig, IstioLogs, \
    IstioConfig, IngressConfig, NetworkingMtlsConfig, PatternsAgentConfig, GeoroutesConfig, GeoroutePatternsConfig, \
    OttConfig, ResourceSpec, CpuMemoryResources


def get_config():
    namespace = NamespaceConfig(
        PASS_CREDENTIAL_ID="cab-sa-dvo09990_AD_DOMAIN",
        STAND_ID='CI09889000',
        SECMAN=SecManConfig(
            NAMESPACE="CI08967393_CI09889000",
            CERT_KV_PATH="CI08967393_CI09889000/A/CI09708620/JEN/MAIN/KV/certs",
            SBER_CA_OTT_CN="CI09708620-CI10663014-OTTYUL",
            SBER_CA_KV_OTT_CLIENT_PATH="CI08967393_CI09889000/SBERCA/sberca-test1-ext-ec/fetch/client_1y_APPLAYER_ec",
            SBER_CA_KV_SERVER_PATH="CI08967393_CI09889000/SBERCA/sberca-test-ext-g2/fetch/server_3y_AS_rsa",
            SBER_CA_KV_CLIENT_PATH="CI08967393_CI09889000/SBERCA/sberca-test-ext-g2/fetch/client_3y_AS_rsa",
            SBER_CA_CLIENT_CN="CI09708620-IFT-CI10663014-strategy-selection",
            INGRESS_GW_SAN="strategy-selection-kvaefdrpa.delta.sbrf.ru,strategy-selection.ci09708620-strategy-selection.apps.a3q7cxy1.k8s.delta.sbrf.ru,strategy-selection.ci09708620-strategy-selection.apps.a4x981tp.k8s.delta.sbrf.ru"
        ),
        ISTIO=IstioConfig(
            INGRESS=IngressConfig(
                NETWORKING_MTLS=NetworkingMtlsConfig(
                    strategy_selection=PatternsAgentConfig(
                        GEOROUTES=GeoroutesConfig(
                            georoute_strategy_selection=[GeoroutePatternsConfig(
                                HOST="strategy-selection-kvaefdrpa.delta.sbrf.ru",
                                PORT=2442
                            )]
                        )
                    )
                )
            )
        ),
        FLUENT_BIT=FluentBitConfig(
            ISTIO_LOGS=IstioLogs(
                TOPIC="agentmetrics_BT_ALPHA",
                BROKERS="tvldq-btaaf0003.delta.sbrf.ru:9093,tvldq-btaaf0001.delta.sbrf.ru:9093,tvldq-btaaf0002.delta.sbrf.ru:9093,tvldq-btaaf0005.delta.sbrf.ru:9093"
            )
        ),
        OTT=OttConfig(
            HOST="otts.ift.pprb-ul.delta.sbrf.ru",
            BILLING_ACCOUNT="CI09708620-CI10663014-OTTYUL",
            RESOURCES=ResourceSpec(
                LIMITS=CpuMemoryResources(
                    CPU="300m",
                    MEMORY="500Mi",
                ),
                REQUESTS=CpuMemoryResources(
                    CPU="150m",
                    MEMORY="350Mi",
                )
            )
        ),
        DYNAMIC_INVENTORY=DynamicInventoryConfig(
            AUTH_TOKENS_URL="https://dyna.sigma.sbrf.ru/api/v1/tokens/CI08967393",
            DEPLOYMENTS_URL="https://dyna.sigma.sbrf.ru/api/v4/deployments/jenkins"
        )
    )

    return namespace.model_dump(exclude_unset=True)

