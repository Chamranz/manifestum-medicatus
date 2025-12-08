from models.agents import AgentConfig

def get_config():
    agent = AgentConfig()

    return agent.model_dump(exclude_unset=True)