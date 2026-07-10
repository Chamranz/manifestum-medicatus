from manifestum_medicatus.models.integrations import ClustersConfig, Host, IngressWhiteListConfig, IntegrationConfig, KafkaConfig, MtlsConfig


def get_config():
    integration = IntegrationConfig(
        INGRESS_WHITELIST=[
            IngressWhiteListConfig(
                NAME='uvz-old',
                CN='.*CN=ci00448961-prom-ecm,.*',
                PATH='.*',
            ),
            IngressWhiteListConfig(
                NAME='uvz',
                CN='.*CN=ci00448961-prom-ai-hub,.*',
                PATH='.*',
            ),
            IngressWhiteListConfig(
                NAME='lboss',
                CN='.*CN=ci09708620-prom-lboss,.*',
                PATH='/health/.*',
            ),
        ],
        KAFKA=KafkaConfig(
            CLUSTERS=[
                ClustersConfig(
                    NAME='aef-istio-logs',
                    HOSTS=[
                        Host(
                            HOST='pvloq-btaaf0006.omega.sbrf.ru',
                            PORT=9093,
                        ),
                        Host(
                            HOST='pvloq-btaaf0008.omega.sbrf.ru',
                            PORT=9093,
                        ),
                        Host(
                            HOST='pvloq-btaaf0009.omega.sbrf.ru',
                            PORT=9093,
                        ),
                        Host(
                            HOST='pvloq-btaaf0007.omega.sbrf.ru',
                            PORT=9093,
                        ),
                    ],
                    MESH_PORT=19093,
                    PROTOCOL='kafka',
                ),
            ],
        ),
        MTLS=[
            MtlsConfig(
                NAME='mtls-gigachat',
                HOST='gigachat.sberdevices.omega.sbrf.ru',
                PORT=443,
            ),
        ],
        MTLS_OTT=[
            MtlsConfig(
                NAME='mtls-uvz-external-api',
                HOST='uvz-external-api-prom.omega.sbrf.ru',
                PORT=8443,
            ),
        ],
    )

    return integration.model_dump(exclude_unset=True)
