from manifestum_medicatus.models.namespace import NamespaceConfig, SecManConfig, DynamicInventoryConfig, FluentBitConfig, IstioLogs, \
    IstioConfig, IngressConfig, PatternsAgentConfig, GeoroutesConfig, \
    OttConfig, ResourceSpec, CpuMemoryResources, PGConfig


def get_config():
    namespace = NamespaceConfig(
        PASS_CREDENTIAL_ID="cab-sa-dvo09990_AD_DOMAIN",
        STAND_ID='CI09889000',
        SECMAN=SecManConfig(
            NAMESPACE="CI08967393_CI09889000",
            CERT_KV_PATH="CI08967393_CI09889000/A/CI09708620/JEN/MAIN/KV/certs",
            SBER_CA_OTT_CN="CI09708620-CI10071809-OTTYUL",
            SBER_CA_KV_OTT_CLIENT_PATH="CI08967393_CI09889000/SBERCA/sberca-test-ext-ec/fetch/client_1y_APPLAYER_ec",
            SBER_CA_KV_SERVER_PATH="CI08967393_CI09889000/SBERCA/sberca-test-ext-g2/fetch/server_3y_AS_rsa",
            SBER_CA_KV_CLIENT_PATH="CI08967393_CI09889000/SBERCA/sberca-test-ext-g2/fetch/client_1y_APPLAYER_rsa",
            SBER_CA_CLIENT_CN="CI09708620-CI10071809-document-classifier-ift",
            INGRESS_GW_SAN="document-classifier-kvaefdrpa.delta.sbrf.ru,strategy-selection.ci09708620-strategy-selection.apps.a3q7cxy1.k8s.delta.sbrf.ru,strategy-selection.ci09708620-strategy-selection.apps.a4x981tp.k8s.delta.sbrf.ru",
            PG = [
                PGConfig(
                    name="pg_1",
                    path="CI08967393_CI09889000/A/CI09708620/JEN/MAIN/KV/PANGOLIN/document_classifier",
                    db_host="tsled-kvaef0002.esrt.sber.ru",
                    db_port="8000",
                    db_name="kvaef",
                    volume_path="/vault/secrets/postgres"
                )
            ]
        ),
        ISTIO=IstioConfig(
            INGRESS=IngressConfig(
                NETWORKING_OTT_MTLS={
                    "document-classifier": PatternsAgentConfig(
                        GEOROUTES={
                            "georoute-document-classifier": GeoroutesConfig(
                                HOST="document-classifier-kvaefdrpa.delta.sbrf.ru",
                                PORT=2446
                            ),
                        }
                    )
                }
            ),
        ),
        FLUENT_BIT=FluentBitConfig(
            ISTIO_LOGS=IstioLogs(
                KAFKA_CLUSTER_NAME='aef-istio-logs',
                TOPIC="agentmetrics_BT_ALPHA"
            )
        ),
        OTT=OttConfig(
            HOST="otts.ift-a.pprb-esrt.sigma.sbrf.ru",
            BILLING_ACCOUNT="CI09708620-CI10071809-OTTYUL",
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
            AUTH_TOKENS_URL="https://dyna.sigma.sbrf.ru/api/v1/tokens/CI08967393",
            DEPLOYMENTS_URL="https://dyna.sigma.sbrf.ru/api/v4/deployments/jenkins"
        )
    )

    return namespace.model_dump(exclude_unset=True)