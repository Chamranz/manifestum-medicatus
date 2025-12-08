from models.integrations import IntegrationConfig

def get_config():
    integration = IntegrationConfig()

    return integration.model_dump(exclude_unset=True)