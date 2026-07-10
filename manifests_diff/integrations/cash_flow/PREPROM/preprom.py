from manifestum_medicatus.models.integrations import ClustersConfig, Host, IntegrationConfig, KafkaConfig


def get_config():
    integration = IntegrationConfig(
        KAFKA=KafkaConfig(
            CLUSTERS=[
                ClustersConfig(
                    NAME='aef-istio-logs',
                    HOSTS=[
                        Host(
                            HOST='tvldq-btaaf0003.delta.sbrf.ru',
                            PORT=9093,
                        ),
                        Host(
                            HOST='tvldq-btaaf0001.delta.sbrf.ru',
                            PORT=9093,
                        ),
                        Host(
                            HOST='tvldq-btaaf0002.delta.sbrf.ru',
                            PORT=9093,
                        ),
                        Host(
                            HOST='tvldq-btaaf0005.delta.sbrf.ru',
                            PORT=9093,
                        ),
                    ],
                    MESH_PORT=19093,
                    PROTOCOL='kafka',
                ),
            ],
        ),
    )

    return integration.model_dump(exclude_unset=True)
