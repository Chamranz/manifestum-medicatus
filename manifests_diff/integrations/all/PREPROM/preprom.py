from manifestum_medicatus.models.integrations import IntegrationConfig, MtlsConfig


def get_config():
    integration = IntegrationConfig(
        MTLS=[
            MtlsConfig(
                NAME='mtls-gigachat',
                HOST='gigachat-ift.sberdevices.delta.sbrf.ru',
                PORT=443,
            ),
        ],
        MTLS_OTT=[
            MtlsConfig(
                NAME='mtls-uvz-external-api',
                HOST='uvz-external-api.delta.sbrf.ru',
                PORT=8443,
            ),
        ],
    )

    return integration.model_dump(exclude_unset=True)
