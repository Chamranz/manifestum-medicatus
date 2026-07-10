from manifestum_medicatus.models.integrations import IngressWhiteListConfig, IntegrationConfig


def get_config():
    integration = IntegrationConfig(
        INGRESS_WHITELIST=[
            IngressWhiteListConfig(
                NAME='allow-all-dev',
                CN='.*',
                PATH='.*',
            ),
            IngressWhiteListConfig(
                NAME='uvz-old',
                CN='.*CN=ci00448961-ift-ecm,.*',
                PATH='.*',
            ),
            IngressWhiteListConfig(
                NAME='uvz',
                CN='.*CN=ci00448961-ift-ai-hub,.*',
                PATH='.*',
            ),
            IngressWhiteListConfig(
                NAME='lboss',
                CN='.*CN=ci09708620-ift-lboss,.*',
                PATH='/health/.*',
            ),
        ],
    )

    return integration.model_dump(exclude_unset=True)
