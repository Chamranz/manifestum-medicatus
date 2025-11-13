prom_params = {
    "STAND_TYPE": "PROM",
    "PASS_CREDENTIAL_ID": 'sa-odvp00004007_AD_DOMAIN',
    "STAND_ID": 'CI09889002',
    "SECMAN": {
        "HOST": "p.secrets.ca.sbrf.ru",
        "SBER_CA_KV_SERVER_PATH": "CI08967393_CI09889002/SBERCA/sberca-int/fetch/server_3y_AS_rsa",
        "SBER_CA_KV_CLIENT_PATH": "CI08967393_CI09889002/SBERCA/sberca-int/fetch/client_3y_AS_rsa",
        "SBER_CA_CLIENT_CN": "CI09708620-PROM-CI10663014-strategy-selection",
        "INGRESS_GW_SAN": "strategy-selection.ci09708620-strategy-selection.apps.a4sxasyr.k8s.ca.sbrf.ru,strategy-selection.ci09708620-strategy-selection.apps.a4sujmd3.k8s.ca.sbrf.ru"
    },
    "ISTIO_LOGS":{
        "TOPIC": 'agentmetrics_BT_ALPHA',
        "BROKERS": "pvloq-btaaf0006.omega.sbrf.ru:9093,pvloq-btaaf0008.omega.sbrf.ru:9093,pvloq-btaaf0009.omega.sbrf.ru:9093,pvloq-btaaf0007.omega.sbrf.ru:9093"
    },
    "DYNAMIC_INVENTORY": {
      "AUTH_TOKENS_URL": "https://dyna.omega.sbrf.ru/api/v1/tokens/CI08967393",
      "DEPLOYMENTS_URL": "https://dyna.omega.sbrf.ru/api/v4/deployments/jenkins"
    }
}