from manifestum_medicatus.models.namespace import CpuMemoryResources, DynamicInventoryConfig, FluentBitConfig, IstioLogs, NamespaceConfig, OttConfig, ResourceSpec, SecManConfig


def get_config():
    namespace = NamespaceConfig(
        DYNAMIC_INVENTORY=DynamicInventoryConfig(
            AUTH_TOKENS_URL='https://dyna.sigma.sbrf.ru/api/v1/tokens/CI08967393',
            DEPLOYMENTS_URL='https://dyna.sigma.sbrf.ru/api/v4/deployments/jenkins',
        ),
        FLUENT_BIT=FluentBitConfig(
            ISTIO_LOGS=IstioLogs(
                KAFKA_CLUSTER_NAME='aef-istio-logs',
                TOPIC='agentmetrics_BT_ALPHA',
            ),
        ),
        OTT=OttConfig(
            HOST='otts.ift.pprb-ul.delta.sbrf.ru',
            OTT_OPER_MODE_INGRESS='provider_authz_local_pdp',
            RESOURCES=ResourceSpec(
                LIMITS=CpuMemoryResources(
                    CPU='300m',
                    MEMORY='500Mi',
                ),
                REQUESTS=CpuMemoryResources(
                    CPU='150m',
                    MEMORY='350Mi',
                ),
            ),
        ),
        PASS_CREDENTIAL_ID='cab-sa-dvo09990_AD_DOMAIN',
        SECMAN=SecManConfig(
            CERT_KV_PATH='CI08967393_CI09889000/A/CI09708620/JEN/MAIN/KV/certs',
            NAMESPACE='CI08967393_CI09889000',
            SBER_CA_KV_CLIENT_PATH='CI08967393_CI09889000/SBERCA/sberca-test-ext-g2/fetch/client_1y_APPLAYER_rsa',
            SBER_CA_KV_OTT_CLIENT_PATH='CI08967393_CI09889000/SBERCA/sberca-test1-ext-ec/fetch/client_1y_APPLAYER_ec',
            SBER_CA_KV_SERVER_PATH='CI08967393_CI09889000/SBERCA/sberca-test-ext-g2/fetch/server_3y_AS_rsa',
        ),
        STAND_ID='CI09889000',
    )

    return namespace.model_dump(exclude_unset=True)
