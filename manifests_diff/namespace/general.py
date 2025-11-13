general_params = {
    "GIT_SSH_CREDENTIAL_ID": 'GIT_CONFIGS_CRED',
    "DROPAPP_NAMESPACE": 'ci09708620-strategy-selection',
    "EIGW_NAMESPACE": 'ci09708620-strategy-selection',
    "SECMAN": {
        "ROLE_NAME": "ci09708620-strategy-selection"
    },
    "FLUENT_BIT": {
        "RESOURCES": {
            "LIMITS": {
                  "CPU": "50m",
                  "MEMORY": "100Mi"
                        },
            "REQUESTS": {
                  "CPU": "50m",
                  "MEMORY": "100Mi"
                        }
        }
    },
    "INJECTEDISTIO": {
            "LIMITS": {
                  "CPU": "100m",
                  "MEMORY": "100Mi"
                        },
            "REQUESTS": {
                  "CPU": "100m",
                  "MEMORY": "50Mi"
                        }
        },
    "HASHICORP": {
                "LIMITS": {
                      "CPU": "100m",
                      "MEMORY": "100Mi"
                            },
                "REQUESTS": {
                      "CPU": "100m",
                      "MEMORY": "50Mi"
                            }
            },
    "INGRESS": {
        "RESOURCES": {
            "REPLICAS": 1,
            "LIMITS": {
                  "CPU": "50m",
                  "MEMORY": "100Mi"
                        },
            "REQUESTS": {
                  "CPU": "50m",
                  "MEMORY": "100Mi"
                        }
            }
        },
    "EGRESS": {
        "RESOURCES": {
            "REPLICAS": 1,
            "LIMITS": {
                  "CPU": "50m",
                  "MEMORY": "100Mi"
                        },
            "REQUESTS": {
                  "CPU": "50m",
                  "MEMORY": "100Mi"
                        }
        }
    },
}