from manifestum_medicatus.models.integrations import IntegrationConfig, MtlsConfig, KafkaConfig, IngressWhiteListConfig, ClustersConfig, Host


def get_config():
    integration = IntegrationConfig(
        MTLS=[
            MtlsConfig(
                NAME="mtls-gigachat",
                HOST="gigachat-psi.sberdevices.omega.sbrf.ru",
                PORT=443
            )
        ],
        MTLS_OTT=[
            MtlsConfig(
                NAME="mtls-uvz-external-api",
                HOST="uvz-external-api-psi.omega.sbrf.ru",
                PORT=8443
            )
        ],
        KAFKA=KafkaConfig(
            CLUSTERS=[
                ClustersConfig(
                    NAME="aef-istio-logs",
                    HOSTS=[
                        Host(
                            HOST="tvloq-btaaf0004.omega.sbrf.ru",
                            PORT=9093
                        ),
                        Host(
                            HOST="tvloq-btaaf0003.omega.sbrf.ru",
                            PORT=9093
                        ),
                        Host(
                            HOST="tvloq-btaaf0002.omega.sbrf.ru",
                            PORT=9093
                        ),
                        Host(
                            HOST="tvloq-btaaf0001.omega.sbrf.ru",
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
                            HOST="tsloq-uvz000001.cloud.omega.sbrf.ru",
                            PORT=9093
                        ),
                        Host(
                            HOST="tsloq-uvz000002.cloud.omega.sbrf.ru",
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
                CN=".*CN=ci00448961-psi-ecm,.*",
                PATH=".*"
            ),
            IngressWhiteListConfig(
                NAME="uvz",
                CN=".*CN=ci00448961-psi-ai-hub,.*",
                PATH=".*"
            ),
            IngressWhiteListConfig(
                NAME="lboss",
                CN=".*CN=ci09708620-psi-lboss,.*",
                PATH="/health/.*"
            )
        ]
    )

    return integration.model_dump(exclude_unset=True)

