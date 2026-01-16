from models.namespace import NamespaceConfig, SecManConfig, DynamicInventoryConfig, FluentBitConfig, IstioLogs, \
    IstioConfig, IngressConfig, NetworkingMtlsConfig, PatternsAgentConfig, GeoroutesConfig, GeoroutePatternsConfig, OttConfig, ResourceSpec, CpuMemoryResources

def get_config():
    namespace = NamespaceConfig(
        STAND_TYPE="PROM",
        PASS_CREDENTIAL_ID='sa-odvp00004007_AD_DOMAIN',
        STAND_ID='CI09889002',
        SECMAN=SecManConfig(
            HOST="p.secrets.ca.sbrf.ru",
            NAMESPACE="CI08967393_CI09889002",
            CERT_KV_PATH="CI08967393_CI09889002/A/CI09708620/JEN/MAIN/KV/certs",
            SBER_CA_OTT_CN="CI09708620-CI10663014-OTTYUL",
            SBER_CA_KV_OTT_CLIENT_PATH="CI08967393_CI09889002/SBERCA/sberca-int-ec/fetch/client_1y_APPLAYER_ec",
            SBER_CA_KV_SERVER_PATH="CI08967393_CI09889002/SBERCA/sberca-int/fetch/server_3y_AS_rsa",
            SBER_CA_KV_CLIENT_PATH="CI08967393_CI09889002/SBERCA/sberca-int/fetch/client_3y_AS_rsa",
            SBER_CA_CLIENT_CN="CI09708620-PROM-CI10663014-strategy-selection",
            INGRESS_GW_SAN="strategy-selection-kvaefdrpa.omega.sbrf.ru,strategy-selection.ci09708620-strategy-selection.apps.a4sxasyr.k8s.ca.sbrf.ru,strategy-selection.ci09708620-strategy-selection.apps.a4sujmd3.k8s.ca.sbrf.ru"
        ),
        ISTIO=IstioConfig(
            INGRESS=IngressConfig(
                NETWORKING_MTLS=NetworkingMtlsConfig(
                    strategy_selection=PatternsAgentConfig(
                        GEOROUTES=GeoroutesConfig(
                            georoute_strategy_selection=[GeoroutePatternsConfig(
                                HOST="strategy-selection-kvaefdrpa.omega.sbrf.ru",
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
                BROKERS="pvloq-btaaf0006.omega.sbrf.ru:9093,pvloq-btaaf0008.omega.sbrf.ru:9093,pvloq-btaaf0009.omega.sbrf.ru:9093,pvloq-btaaf0007.omega.sbrf.ru:9093"
            )
        ),
        OTT=OttConfig(
            HOST="otts.prom.pprb-ul.omega.sbrf.ru",
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
            AUTH_TOKENS_URL="https://dyna.omega.sbrf.ru/api/v1/tokens/CI08967393",
            DEPLOYMENTS_URL="https://dyna.sigma.sbrf.ru/api/v4/deployments/jenkins"
        )
    )

    return namespace.model_dump(exclude_unset=True)

