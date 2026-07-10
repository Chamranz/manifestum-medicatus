from manifestum_medicatus.models.common import CommonConfig


def get_config():
    common = CommonConfig()

    return common.model_dump(exclude_unset=True, exclude_none=True)
