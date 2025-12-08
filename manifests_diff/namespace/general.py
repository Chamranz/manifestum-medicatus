from models.namespace import NamespaceConfig, SecManConfig, FluentBitConfig, IstioLogs, ResourceSpec, CpuMemoryResources


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
                    MEMORY="100mi",
                ),
                REQUESTS=CpuMemoryResources(
                    CPU="50m",
                    MEMORY="100mi",
                )
            )
        ),
        INJECTEDISTIO=ResourceSpec(
            LIMITS=CpuMemoryResources(
                CPU="100m",
                MEMORY="100mi",
            ),
            REQUESTS=CpuMemoryResources(
                CPU="100m",
                MEMORY="50mi",
            )
        ),
        HASHICORP=ResourceSpec(
            LIMITS=CpuMemoryResources(
                CPU="100m",
                MEMORY="100mi",
            ),
            REQUESTS=CpuMemoryResources(
                CPU="100m",
                MEMORY="50mi",
            )
        ),
        INGRESS=ResourceSpec(
            REPLICAS=1,
            LIMITS=CpuMemoryResources(
                CPU="50m",
                MEMORY="100mi",
            ),
            REQUESTS=CpuMemoryResources(
                CPU="50m",
                MEMORY="100mi",
            )
        ),
        EGRESS=ResourceSpec(
            REPLICAS=1,
            LIMITS=CpuMemoryResources(
                CPU="50m",
                MEMORY="100mi",
            ),
            REQUESTS=CpuMemoryResources(
                CPU="50m",
                MEMORY="100mi",
            )
        ),
    )


    return namespace.model_dump(exclude_unset=True)

