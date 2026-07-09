from manifestum_medicatus.models.integrations import IntegrationConfig, MtlsConfig, KafkaConfig, IngressWhiteListConfig, ClustersConfig, Host


def get_config():
    integration = IntegrationConfig(
        MTLS=[
            MtlsConfig(
                NAME="mtls-gigachat",
                HOST="gigachat.sberdevices.omega.sbrf.ru",
                PORT=443
            ),
        ],
        MTLS_OTT=[
            MtlsConfig(
                NAME="mtls-uvz-external-api",
                HOST="uvz-external-api-prom.omega.sbrf.ru",
                PORT=8443
            )
        ],
        KAFKA=KafkaConfig(
            CLUSTERS=[
                ClustersConfig(
                    NAME="aef-istio-logs",
                    HOSTS=[
                        Host(
                            HOST="pvloq-btaaf0006.omega.sbrf.ru",
                            PORT=9093
                        ),
                        Host(
                            HOST="pvloq-btaaf0008.omega.sbrf.ru",
                            PORT=9093
                        ),
                        Host(
                            HOST="pvloq-btaaf0009.omega.sbrf.ru",
                            PORT=9093
                        ),
                        Host(
                            HOST="pvloq-btaaf0007.omega.sbrf.ru",
                            PORT=9093
                        )
                    ],
                    MESH_PORT=19093,
                    PROTOCOL="kafka"
                ),
                ClustersConfig(
                    NAME="agents-kafka-async",
                    HOSTS=[
                        Host(
                            HOST="psloq-uvz000001.cloud.omega.sbrf.ru",
                            PORT=9093
                        ),
                        Host(
                            HOST="psloq-uvz000002.cloud.omega.sbrf.ru",
                            PORT=9093
                        ),
                        Host(
                            HOST="psloq-uvz000003.cloud.omega.sbrf.ru",
                            PORT=9093
                        ),
                        Host(
                            HOST="psloq-uvz000004.cloud.omega.sbrf.ru",
                            PORT=9093
                        )
                    ],
                    MESH_PORT=19095,
                    PROTOCOL="kafka"
                )
            ]
        ),

        INGRESS_WHITELIST=[
            IngressWhiteListConfig(
                NAME="uvz-old",
                CN=".*CN=ci00448961-prom-ecm,.*",
                PATH=".*"
            ),
            IngressWhiteListConfig(
                NAME="uvz",
                CN=".*CN=ci00448961-prom-ai-hub,.*",
                PATH=".*"
            ),
            IngressWhiteListConfig(
                NAME="lboss",
                CN=".*CN=ci09708620-prom-lboss,.*",
                PATH= "/health/.*"
            )
        ]
    )

    return integration.model_dump(exclude_unset=True)

