from manifestum_medicatus.models.integrations import IngressWhiteListConfig, IntegrationConfig


def get_config():
    integration = IntegrationConfig(
        INGRESS_WHITELIST=[
            IngressWhiteListConfig(
                NAME='allow-all-dev',
                CN='.*',
                PATH='.*',
            ),
        ],
    )

    return integration.model_dump(exclude_unset=True)
