preprom_params = {
    "MTLS": [
        {
            "NAME": "mtls-gigachat",
            "HOST": "gigachat-ift.sberdevices.delta.sbrf.ru",
            "PORT": 443
        },
        {
            "NAME": "mtls-uvz-external-api",
            "HOST": "uvz-external-api.delta.sbrf.ru",
            "PORT": 8443
        }
    ],
    "KAFKA": [
        {
            "NAME": "tvldq-btaaf0003",
            "HOST": "tvldq-btaaf0003.delta.sbrf.ru",
            "IP": "10.26.118.66",
            "PORT": 9093
        },
        {
            "NAME": "tvldq-btaaf0001",
            "HOST": "tvldq-btaaf0003.delta.sbrf.ru",
            "IP": "10.26.118.42",
            "PORT": 9093
        },
        {
            "NAME": "tvldq-btaaf0002",
            "HOST": "tvldq-btaaf0003.delta.sbrf.ru",
            "IP": "10.26.118.196",
            "PORT": 9093
        },
        {
            "NAME": "tvldq-btaaf0005",
            "HOST": "tvldq-btaaf0003.delta.sbrf.ru",
            "IP": "10.26.118.89",
            "PORT": 9093
        }
    ],
    "INGRESS_WHITELIST": [
        {
            "NAME": "allow-all-dev",
            "CN": ".*",
            "PATH": ".*"
        }
    ]

}