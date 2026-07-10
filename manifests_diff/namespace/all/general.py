from manifestum_medicatus.models.namespace import CpuMemoryResources, CpuMemoryResourcesMem, FluentBitConfig, NamespaceConfig, ResourceSpec, ServiceConfig, ServiceConfigWithResources


def get_config():
    namespace = NamespaceConfig(
        EGRESS=ServiceConfigWithResources(
            RESOURCES=ResourceSpec(
                LIMITS=CpuMemoryResources(
                    CPU='100m',
                    MEMORY='100Mi',
                ),
                REPLICAS=1,
                REQUESTS=CpuMemoryResources(
                    CPU='100m',
                    MEMORY='50Mi',
                ),
            ),
        ),
        FLUENT_BIT=FluentBitConfig(
            RESOURCES=ResourceSpec(
                LIMITS=CpuMemoryResources(
                    CPU='50m',
                    MEMORY='100Mi',
                ),
                REQUESTS=CpuMemoryResources(
                    CPU='50m',
                    MEMORY='100Mi',
                ),
            ),
        ),
        GIT_SSH_CREDENTIAL_ID='GIT_CONFIGS_CRED',
        HASHICORP=ServiceConfig(
            LIMITS=CpuMemoryResourcesMem(
                CPU='50m',
                MEM='100Mi',
            ),
            REQUESTS=CpuMemoryResourcesMem(
                CPU='50m',
                MEM='50Mi',
            ),
        ),
        INGRESS=ServiceConfigWithResources(
            RESOURCES=ResourceSpec(
                LIMITS=CpuMemoryResources(
                    CPU='100m',
                    MEMORY='100Mi',
                ),
                REPLICAS=1,
                REQUESTS=CpuMemoryResources(
                    CPU='100m',
                    MEMORY='50Mi',
                ),
            ),
        ),
        INJECTEDISTIO=ServiceConfig(
            LIMITS=CpuMemoryResourcesMem(
                CPU='100m',
                MEM='100Mi',
            ),
            REQUESTS=CpuMemoryResourcesMem(
                CPU='100m',
                MEM='50Mi',
            ),
        ),
    )

    return namespace.model_dump(exclude_unset=True)
