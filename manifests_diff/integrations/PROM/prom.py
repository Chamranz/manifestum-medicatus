from models.integrations import IntegrationConfig, MtlsConfig, KafkaConfig, IngressWhiteListConfig


def get_config():
    integration = IntegrationConfig(
        MTLS=[
            MtlsConfig(
                NAME="mtls-gigachat",
                HOST="gigachat-prom.sberdevices.ca.sbrf.ru",
                PORT=443
            ),
            MtlsConfig(
                NAME="mtls-uvz-external-api",
                HOST="uvz-external-api-prom.omega.sbrf.ru",
                PORT=8443
            )
        ],
        KAFKA=[
            KafkaConfig(
                NAME="pvloq-btaaf0006",
                HOST="pvloq-btaaf0006.omega.sbrf.r",
                IP="10.70.73.48",
                PORT=9093
            ),
            KafkaConfig(
                NAME="pvloq-btaaf0008",
                HOST="pvloq-btaaf0008.omega.sbrf.ru",
                IP="10.110.86.120",
                PORT=9093
            ),
            KafkaConfig(
                NAME="pvloq-btaaf0009",
                HOST="pvloq-btaaf0009.omega.sbrf.ru",
                IP="10.70.72.36",
                PORT=9093
            ),
            KafkaConfig(
                NAME="pvloq-btaaf0007",
                HOST="pvloq-btaaf0007.omega.sbrf.ru",
                IP="10.110.86.38",
                PORT=9093
            )
        ],
        INGRESS_WHITE_LIST=[
            IngressWhiteListConfig(
                NAME="uvz-old",
                CN=".*CN=ci00448961-prom-ecm,.*",
                PATH=".*"
            ),
            IngressWhiteListConfig(
                NAME="uvz",
                CN=".*CN=ci00448961-prom-ai-hub,.*",
                PATH=".*"
            )
        ]
    )

    return integration.model_dump(exclude_unset=True)

