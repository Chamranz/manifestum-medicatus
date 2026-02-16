from models.namespace import NamespaceConfig, SecManConfig, DynamicInventoryConfig, FluentBitConfig, IstioLogs, \
    IstioConfig, IngressConfig, NetworkingMtlsConfig, PatternsAgentConfig, GeoroutesConfig, GeoroutePatternsConfig, OttConfig, ResourceSpec, CpuMemoryResources

def get_config():
    namespace = NamespaceConfig(
        STAND_TYPE="PSI",
        PASS_CREDENTIAL_ID='sa-odvp00004006_AD_DOMAIN',
        STAND_ID='CI09889001',
        SECMAN=SecManConfig(
            HOST="ift.secrets.ca.sbrf.ru",
            NAMESPACE="CI08967393_CI09889001",
            CERT_KV_PATH="CI08967393_CI09889002/A/CI09708620/JEN/MAIN/KV/certs",
            SBER_CA_OTT_CN="CI09708620-CI10663014-OTTYUL",
            SBER_CA_KV_OTT_CLIENT_PATH="CI08967393_CI09889001/SBERCA/sberca-test2-int-ec/fetch/client_1y_APPLAYER_ec",
            SBER_CA_KV_SERVER_PATH="CI08967393_CI09889001/SBERCA/sberca-test-int-g2/fetch/server_3y_AS_rsa",
            SBER_CA_KV_CLIENT_PATH="CI08967393_CI09889001/SBERCA/sberca-test-int-g2/fetch/client_3y_AS_rsa",
            SBER_CA_CLIENT_CN="CI09708620-PSI-CI10663014-strategy-selection",
            INGRESS_GW_SAN="strategy-selection-kvaefdrpa-psi.omega.sbrf.ru,strategy-selection.ci09708620-strategy-selection.apps.a472facr.k8s.omega.sbrf.ru,strategy-selection.ci09708620-strategy-selection.apps.a47ow1gr.k8s.ca.sbrf.ru"
        ),
        ISTIO=IstioConfig(
            INGRESS=IngressConfig(
                NETWORKING_MTLS=NetworkingMtlsConfig(
                    strategy_selection=PatternsAgentConfig(
                        GEOROUTES=GeoroutesConfig(
                            georoute_strategy_selection=GeoroutePatternsConfig(
                                HOST="strategy-selection-kvaefdrpa-psi.omega.sbrf.ru",
                                PORT=2442
                            )
                        )
                    )
                )
            )
        ),
        FLUENT_BIT=FluentBitConfig(
            ISTIO_LOGS=IstioLogs(
                TOPIC='agentmetrics_BT_ALPHA',
                BROKERS="tvloq-btaaf0004.omega.sbrf.ru:9093,tvloq-btaaf0003.omega.sbrf.ru:9093,tvloq-btaaf0002.omega.sbrf.ru:9093,tvloq-btaaf0001.omega.sbrf.ru:9093"
            )
        ),
        OTT=OttConfig(
            HOST="otts.psi.pprb-ul.omega.sbrf.ru",
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
            ),
            OTT_OPER_MODE_INGRESS="provider_authz_local_pdp"
        ),
        DYNAMIC_INVENTORY=DynamicInventoryConfig(
            AUTH_TOKENS_URL="https://dyna.omega.sbrf.ru/api/v1/tokens/CI08967393",
            DEPLOYMENTS_URL="https://dyna.omega.sbrf.ru/api/v4/deployments/jenkins"
        )
    )

    return namespace.model_dump(exclude_unset=True)

