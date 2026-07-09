from manifestum_medicatus.models.integrations import IntegrationConfig, IngressWhiteListConfig, KafkaConfig, PostgresConfig, ClustersConfig, Host

def get_config():
    integration = IntegrationConfig(
        INGRESS_WHITELIST=[
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
                CN=".*CN=ci09708620-ift-lboss,.*",
                PATH="/health/.*"
            )
        ],
        POSTGRES=[
            PostgresConfig(
                NAME="agent",
                HOST="tsled-kvaef0002.esrt.sber.ru",
                IP="10.134.16.50",
                PORT="6544",
                INNERPORT="8000"

            )
        ],
        KAFKA=KafkaConfig(
            CLUSTERS=[
                ClustersConfig(
                    NAME="agents-kafka-async",
                    HOSTS=[
                        Host(
                            HOST="tsleq-uvz000005.esrt.sber.ru",
                            PORT=9093
                        ),
                        Host(
                            HOST="tsleq-uvz000006.esrt.sber.ru",
                            PORT=9093
                        )
                    ],
                    MESH_PORT=19095,
                    PROTOCOL="kafka"
                )
            ],
        ),
    )

    return integration.model_dump(exclude_unset=True)