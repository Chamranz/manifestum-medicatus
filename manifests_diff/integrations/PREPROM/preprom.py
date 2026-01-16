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
        KAFKA=[
            KafkaConfig(
                NAME="tvldq-btaaf0003",
                HOST="tvldq-btaaf0003.delta.sbrf.ru",
                IP="10.26.118.66",
                PORT=9093
            ),
            KafkaConfig(
                NAME="tvldq-btaaf0001",
                HOST="tvldq-btaaf0001.delta.sbrf.ru",
                IP="10.26.118.42",
                PORT=9093
            ),
            KafkaConfig(
                NAME="tvldq-btaaf0002",
                HOST="tvldq-btaaf0002.delta.sbrf.ru",
                IP="10.26.118.196",
                PORT=9093
            ),
            KafkaConfig(
                NAME="tvldq-btaaf0005",
                HOST="tvldq-btaaf0005.delta.sbrf.ru",
                IP="10.26.118.89",
                PORT=9093
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

