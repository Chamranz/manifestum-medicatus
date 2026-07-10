from manifestum_medicatus.models.namespace import CpuMemoryResources, DynamicInventoryConfig, FluentBitConfig, IstioLogs, NamespaceConfig, OttConfig, ResourceSpec, SecManConfig


def get_config():
    namespace = NamespaceConfig(
        DYNAMIC_INVENTORY=DynamicInventoryConfig(
            AUTH_TOKENS_URL='https://dyna.omega.sbrf.ru/api/v1/tokens/CI08967393',
            DEPLOYMENTS_URL='https://dyna.omega.sbrf.ru/api/v4/deployments/jenkins',
        ),
        FLUENT_BIT=FluentBitConfig(
            ISTIO_LOGS=IstioLogs(
                KAFKA_CLUSTER_NAME='aef-istio-logs',
                TOPIC='agentmetrics_BT_ALPHA',
            ),
        ),
        OTT=OttConfig(
            HOST='otts.prom.pprb-ul.omega.sbrf.ru',
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
        PASS_CREDENTIAL_ID='sa-odvp00004007_AD_DOMAIN',
        SECMAN=SecManConfig(
            CERT_KV_PATH='CI08967393_CI09889002/A/CI09708620/JEN/MAIN/KV/certs',
            HOST='p.secrets.ca.sbrf.ru',
            NAMESPACE='CI08967393_CI09889002',
            SBER_CA_KV_CLIENT_PATH='CI08967393_CI09889002/SBERCA/sberca-int/fetch/client_1y_APPLAYER_rsa',
            SBER_CA_KV_OTT_CLIENT_PATH='CI08967393_CI09889002/SBERCA/sberca-int-ec/fetch/client_1y_APPLAYER_ec',
            SBER_CA_KV_SERVER_PATH='CI08967393_CI09889002/SBERCA/sberca-int/fetch/server_3y_AS_rsa',
        ),
        STAND_ID='CI09889002',
        STAND_TYPE='PROM',
    )

    return namespace.model_dump(exclude_unset=True)
