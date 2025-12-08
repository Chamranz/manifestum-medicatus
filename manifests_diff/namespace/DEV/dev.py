from models.namespace import NamespaceConfig, SecManConfig, DynamicInventoryConfig

def get_config():
    namespace = NamespaceConfig(
        PASS_CREDENTIAL_ID="cab-sa-dvo09991_AD_DOMAIN",
        DROPAPP_CLUSTER='a3q0odr0.k8s.delta.sbrf.ru',
        DROPAPP_CREDENTIAL_ID='a3q0odr0_k8s_delta_sbrf_ru_dropapp',
        STAND_ID='CI09888999',
        SECMAN=SecManConfig(
            NAMESPACE="CI08967393_CI09888999",
            SBER_CA_KV_SERVER_PATH="CI08967393_CI09888999/SBERCA/sberca-test-ext-g2/fetch/server_3y_AS_rsa",
            SBER_CA_KV_CLIENT_PATH="CI08967393_CI09888999/SBERCA/sberca-test-ext-g2/fetch/client_3y_AS_rsa",
            SBER_CA_CLIENT_CN="CI09708620-DEV-CI10663014-strategy-selection",
            SBER_CA_SERVER_CN="strategy-selection.ci09708620-strategy-selection.apps.a3q0odr0.k8s.delta.sbrf.ru",
            INGRESS_GW_SAN="strategy-selection.ci09708620-strategy-selection.apps.a3q0odr0.k8s.delta.sbrf.ru"
        ),
        DYNAMIC_INVENTORY=DynamicInventoryConfig(
            AUTH_TOKENS_URL="https://dyna.sber.ru/api/v1/tokens/CI08967393",
            DEPLOYMENTS_URL="https://dyna.apps.ift-efs1-dm.delta.sbrf.ru/api/v4/deployments/jenkins"
        )
    )

    return namespace.model_dump(exclude_unset=True)

