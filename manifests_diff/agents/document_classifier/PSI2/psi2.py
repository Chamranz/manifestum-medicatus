from manifestum_medicatus.models.agents import AgentConfig

def get_config():
    env = {
        "CLUSTER_ID": 'console.a472facr.k8s.omega.sbrf.ru'
    }

    agent = AgentConfig(ENV=env)

    return agent.model_dump(exclude_unset=True)