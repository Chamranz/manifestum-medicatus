from models.namespace import NamespaceConfig, SecManConfig, DynamicInventoryConfig,FluentBitConfig,IstioLogs

def get_config():
    namespace = NamespaceConfig(
        STAND_TYPE="PSI",
        PASS_CREDENTIAL_ID='sa-odvp00004006_AD_DOMAIN',
        STAND_ID='CI09889001',
        SECMAN=SecManConfig(
            HOST="t.secrets.delta.sbrf.ru",
            SBER_CA_KV_SERVER_PATH="CI08967393_CI09889001/SBERCA/sberca-test-int-g2/fetch/server_3y_AS_rsa",
            SBER_CA_KV_CLIENT_PATH="CI08967393_CI09889001/SBERCA/sberca-test-int-g2/fetch/client_3y_AS_rsa",
            SBER_CA_CLIENT_CN="CI09708620-PSI-CI10663014-strategy-selection",
            INGRESS_GW_SAN="strategy-selection.ci09708620-strategy-selection.apps.a472facr.k8s.omega.sbrf.ru,strategy-selection.ci09708620-strategy-selection.apps.a47ow1gr.k8s.ca.sbrf.ru"
        ),
        FLUENT_BIT=FluentBitConfig(
            ISTIO_LOGS=IstioLogs(
                TOPIC='agentmetrics_BT_ALPHA',
                BROKERS="tvloq-btaaf0004.omega.sbrf.ru:9093,tvloq-btaaf0003.omega.sbrf.ru:9093,tvloq-btaaf0002.omega.sbrf.ru:9093,tvloq-btaaf0001.omega.sbrf.ru:9093"
            )
        ),
        DYNAMIC_INVENTORY=DynamicInventoryConfig(
            AUTH_TOKENS_URL="https://dyna.omega.sbrf.ru/api/v1/tokens/CI08967393",
            DEPLOYMENTS_URL="https://dyna.omega.sbrf.ru/api/v4/deployments/jenkins"
        )
    )

    return namespace.model_dump(exclude_unset=True)

