from models.integrations import IntegrationConfig, MtlsConfig, KafkaConfig, IngressWhiteListConfig


def get_config():
    integration = IntegrationConfig(
        MTLS=[
            MtlsConfig(
                NAME="mtls-gigachat",
                HOST="gigachat-ift.sberdevices.delta.sbrf.ru",
                PORT= 443
            ),
            MtlsConfig(
                NAME="mtls-uvz-external-api",
                HOST="uvz-external-api.delta.sbrf.ru",
                PORT=8443
            )
        ],
        INGRESS_WHITELIST=[
            IngressWhiteListConfig(
                NAME="allow-all-dev",
                CN=".*",
                PATH=".*"
            )
        ]
    )

    return integration.model_dump(exclude_unset=True)

