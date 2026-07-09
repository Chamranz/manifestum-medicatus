from manifestum_medicatus.models.agents import AgentConfig

def get_config():
    env = {
        "CLUSTER_ID": 'console.a47ow1gr.k8s.ca.sbrf.ru'
    }

    agent = AgentConfig(ENV=env)

    return agent.model_dump(exclude_unset=True)