from manifestum_medicatus.models.namespace import AppLogconfig, FluentBitConfig, NamespaceConfig, SecManConfig


def get_config():
    namespace = NamespaceConfig(
        DROPAPP_NAMESPACE='ci09708620-document-classifier',
        EIGW_NAMESPACE='ci09708620-document-classifier',
        FLUENT_BIT=FluentBitConfig(
            APP_LOG=AppLogconfig(
                KAFKA_CLUSTER_NAME='agent-app-logs',
                MOUNT_FILE='app.log',
                MOUNT_PATH='/var/log/app',
                TOPIC='agentmetrics_BT_ALPHA',
            ),
        ),
        SECMAN=SecManConfig(
            ROLE_NAME='ci09708620-document-classifier',
        ),
    )

    return namespace.model_dump(exclude_unset=True)
