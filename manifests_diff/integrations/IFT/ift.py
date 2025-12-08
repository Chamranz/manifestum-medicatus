from models.integrations import IntegrationConfig, IngressWhiteListConfig

def get_config():
    integration = IntegrationConfig(
        INGRESS_WHITE_LIST=[
            IngressWhiteListConfig(
                NAME="uvz-old",
                CN=".*CN=ci00448961-ift-ecm,.*",
                PATH=".*"
            ),
            IngressWhiteListConfig(
                NAME="uvz",
                CN=".*CN=ci00448961-ift-ai-hub,.*",
                PATH=".*"
            ),
            IngressWhiteListConfig(
                NAME="lboss",
                CN=".*CN=CI09708620-IFT-LBOSS,.*",
                PATH=".*"
            )
        ]
    )

    return integration.model_dump(exclude_unset=True)