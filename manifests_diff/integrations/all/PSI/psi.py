from manifestum_medicatus.models.integrations import ClustersConfig, Host, IngressWhiteListConfig, IntegrationConfig, KafkaConfig, MtlsConfig


def get_config():
    integration = IntegrationConfig(
        INGRESS_WHITELIST=[
            IngressWhiteListConfig(
                NAME='uvz-old',
                CN='.*CN=ci00448961-psi-ecm,.*',
                PATH='.*',
            ),
            IngressWhiteListConfig(
                NAME='uvz',
                CN='.*CN=ci00448961-psi-ai-hub,.*',
                PATH='.*',
            ),
            IngressWhiteListConfig(
                NAME='lboss',
                CN='.*CN=ci09708620-psi-lboss,.*',
                PATH='/health/.*',
            ),
        ],
        KAFKA=KafkaConfig(
            CLUSTERS=[
                ClustersConfig(
                    NAME='aef-istio-logs',
                    HOSTS=[
                        Host(
                            HOST='tvloq-btaaf0004.omega.sbrf.ru',
                            PORT=9093,
                        ),
                        Host(
                            HOST='tvloq-btaaf0003.omega.sbrf.ru',
                            PORT=9093,
                        ),
                        Host(
                            HOST='tvloq-btaaf0002.omega.sbrf.ru',
                            PORT=9093,
                        ),
                        Host(
                            HOST='tvloq-btaaf0001.omega.sbrf.ru',
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
                HOST='gigachat-psi.sberdevices.ca.sbrf.ru',
                PORT=443,
            ),
        ],
        MTLS_OTT=[
            MtlsConfig(
                NAME='mtls-uvz-external-api',
                HOST='uvz-external-api-psi.omega.sbrf.ru',
                PORT=8443,
            ),
        ],
    )

    return integration.model_dump(exclude_unset=True)
