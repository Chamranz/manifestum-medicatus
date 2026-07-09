from manifestum_medicatus.models.integrations import IntegrationConfig, MtlsConfig, KafkaConfig, IngressWhiteListConfig, \
    PostgresConfig


def get_config():
    integration = IntegrationConfig(
        INGRESS_WHITELIST=[
            IngressWhiteListConfig(
                NAME="allow-all-dev",
                CN=".*",
                PATH=".*"
            )
        ],
        POSTGRES=[
            PostgresConfig(
                NAME="agent",
                HOST="tsled-kvaef0001.esrt.sber.ru",
                IP="10.134.97.113",
                PORT="6544",
                INNERPORT="8000"
            )
        ],

    )

    return integration.model_dump(exclude_unset=True)

