from manifestum_medicatus.models.namespace import DynamicInventoryConfig, NamespaceConfig, SecManConfig


def get_config():
    namespace = NamespaceConfig(
        DROPAPP_CLUSTER='a3q0odr0.k8s.delta.sbrf.ru',
        DROPAPP_CREDENTIAL_ID='a3q0odr0_k8s_delta_sbrf_ru_dropapp',
        DYNAMIC_INVENTORY=DynamicInventoryConfig(
            AUTH_TOKENS_URL='https://dyna.sber.ru/api/v1/tokens/CI08967393',
            DEPLOYMENTS_URL='https://dyna.apps.ift-efs1-dm.delta.sbrf.ru/api/v4/deployments/jenkins',
        ),
        PASS_CREDENTIAL_ID='cab-sa-dvo09991_AD_DOMAIN',
        SECMAN=SecManConfig(
            NAMESPACE='CI08967393_CI09888999',
            SBER_CA_KV_CLIENT_PATH='CI08967393_CI09888999/SBERCA/sberca-test-ext-g2/fetch/client_1y_APPLAYER_rsa',
            SBER_CA_KV_SERVER_PATH='CI08967393_CI09888999/SBERCA/sberca-test-ext-g2/fetch/server_3y_AS_rsa',
        ),
        STAND_ID='CI09888999',
    )

    return namespace.model_dump(exclude_unset=True)
