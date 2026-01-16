from models.namespace import NamespaceConfig, SecManConfig, FluentBitConfig, IstioLogs, ResourceSpec, \
    CpuMemoryResources, ServiceConfig, ServiceConfigWithResources


def get_config():
    namespace = NamespaceConfig(
        GIT_SSH_CREDENTIAL_ID='GIT_CONFIGS_CRED',
        DROPAPP_NAMESPACE='ci09708620-strategy-selection',
        EIGW_NAMESPACE='ci09708620-strategy-selection',
        SECMAN=SecManConfig(
            ROLE_NAME="ci09708620-strategy-selection"
        ),
        FLUENT_BIT=FluentBitConfig(
            RESOURCES=ResourceSpec(
                LIMITS=CpuMemoryResources(
                    CPU="50m",
                    MEMORY="100Mi",
                ),
                REQUESTS=CpuMemoryResources(
                    CPU="50m",
                    MEMORY="100Mi",
                )
            )
        ),
        INJECTEDISTIO=ServiceConfig(
                LIMITS=CpuMemoryResources(
                    CPU="100m",
                    MEMORY="100Mi",
                ),
                REQUESTS=CpuMemoryResources(
                    CPU="100m",
                    MEMORY="50Mi",
                )
            ),

        HASHICORP=ServiceConfig(
                LIMITS=CpuMemoryResources(
                    CPU="50m",
                    MEMORY="100Mi",
                ),
                REQUESTS=CpuMemoryResources(
                    CPU="50m",
                    MEMORY="50Mi",
                )
        ),
        INGRESS=ServiceConfigWithResources(
            RESOURCES=ResourceSpec(
                REPLICAS=1,
                LIMITS=CpuMemoryResources(
                    CPU="100m",
                    MEMORY="100Mi",
                ),
                REQUESTS=CpuMemoryResources(
                    CPU="100m",
                    MEMORY="50Mi",
                )
            )
        ),
        EGRESS=ServiceConfigWithResources(
            RESOURCES=ResourceSpec(
                REPLICAS=1,
                LIMITS=CpuMemoryResources(
                    CPU="100m",
                    MEMORY="100Mi",
                ),
                REQUESTS=CpuMemoryResources(
                    CPU="100m",
                    MEMORY="50Mi",
                )
            )
        ),
    )


    return namespace.model_dump(exclude_unset=True)

