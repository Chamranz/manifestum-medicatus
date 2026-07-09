from manifestum_medicatus.models.integrations import IntegrationConfig, MtlsConfig, KafkaConfig, IngressWhiteListConfig, \
    ClustersConfig, Host


def get_config():
    integration = IntegrationConfig(
        MTLS=[
            MtlsConfig(
                NAME="mtls-gigachat",
                HOST="gigachat-ift.sberdevices.delta.sbrf.ru",
                PORT= 443
            )
        ],
        MTLS_OTT=[
            MtlsConfig(
                NAME="mtls-uvz-external-api",
                HOST="uvz-external-api.delta.sbrf.ru",
                PORT=8443
            )
        ],
        KAFKA=KafkaConfig(
            CLUSTERS=[
                ClustersConfig(
                    NAME="aef-istio-logs",
                    HOSTS=[
                        Host(
                            HOST="tvldq-btaaf0003.delta.sbrf.ru",
                            PORT=9093
                        ),
                        Host(
                            HOST="tvldq-btaaf0001.delta.sbrf.ru",
                            PORT=9093
                        ),
                        Host(
                            HOST="tvldq-btaaf0002.delta.sbrf.ru",
                            PORT=9093
                        ),
                        Host(
                            HOST="tvldq-btaaf0005.delta.sbrf.ru",
                            PORT=9093
                        )
                    ],
                    MESH_PORT = 19093,
                    PROTOCOL = "kafka"
                )
            ],
        ),

        INGRESS_WHITELIST=[
            IngressWhiteListConfig(
                NAME="allow-all-dev",
                CN=".*",
                PATH=".*"
            )
        ]
    )

    return integration.model_dump(exclude_unset=True)

