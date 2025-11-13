prom_params = {
    "MTLS": [
        {
            "NAME": "mtls-gigachat",
            "HOST": "gigachat-prom.sberdevices.ca.sbrf.ru",
            "PORT": 443
        },
        {
            "NAME": "mtls-uvz-external-api",
            "HOST": "uvz-external-api-prom.omega.sbrf.ru",
            "PORT": 8443
        }
    ],
    "KAFKA": [
        {
            "NAME": "pvloq-btaaf0006",
            "HOST": "pvloq-btaaf0006.omega.sbrf.r",
            "IP": "10.70.73.48",
            "PORT": 9093
        },
        {
            "NAME": "pvloq-btaaf0008",
            "HOST": "pvloq-btaaf0008.omega.sbrf.ru",
            "IP": "10.110.86.120",
            "PORT": 9093
        },
        {
            "NAME": "pvloq-btaaf0009",
            "HOST": "pvloq-btaaf0009.omega.sbrf.ru",
            "IP": "10.70.72.36",
            "PORT": 9093
        },
        {
            "NAME": "pvloq-btaaf0007",
            "HOST": "pvloq-btaaf0007.omega.sbrf.ru",
            "IP": "10.110.86.38",
            "PORT": 9093
        }
    ],
    "INGRESS_WHITELIST": [
        {
            "NAME": "uvz-old",
            "CN": ".*CN=ci00448961-prom-ecm,.*",
            "PATH": ".*"
        },
        {
            "NAME": "uvz",
            "CN": ".*CN=ci00448961-prom-ai-hub,.*",
            "PATH": ".*"
        }
    ]

}