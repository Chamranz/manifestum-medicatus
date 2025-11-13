psi_params = {
    "MTLS": [
        {
            "NAME": "mtls-gigachat",
            "HOST": "gigachat-psi.sberdevices.ca.sbrf.ru",
            "PORT": 443
        },
        {
            "NAME": "mtls-uvz-external-api",
            "HOST": "uvz-external-api-psi.omega.sbrf.ru",
            "PORT": 8443
        }
    ],
    "KAFKA": [
        {
            "NAME": "tvloq-btaaf0004",
            "HOST": "tvloq-btaaf0004.omega.sbrf.ru",
            "IP": "30.164.241.229",
            "PORT": 9093
        },
        {
            "NAME": "tvloq-btaaf0003",
            "HOST": "tvloq-btaaf0003.omega.sbrf.ru",
            "IP": "30.164.241.153",
            "PORT": 9093
        },
        {
            "NAME": "tvloq-btaaf0002",
            "HOST": "tvloq-btaaf0002.omega.sbrf.ru",
            "IP": "30.164.241.185",
            "PORT": 9093
        },
        {
            "NAME": "tvloq-btaaf0001",
            "HOST": "tvloq-btaaf0001.omega.sbrf.ru",
            "IP": "30.164.241.177",
            "PORT": 9093
        }
    ],
    "INGRESS_WHITELIST": [
        {
            "NAME": "uvz-old",
            "CN": ".*CN=ci00448961-psi-ecm,.*",
            "PATH": ".*"
        },
        {
            "NAME": "uvz",
            "CN": ".*CN=ci00448961-psi-ai-hub,.*",
            "PATH": ".*"
        }
    ]

}