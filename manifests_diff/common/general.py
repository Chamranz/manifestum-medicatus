general_params = {
    "hub": {
        "name": "AI-HUB БТ",
        "id": "CI08967393"
    },
    "aef": {
        "name": "AI-HUB БТ.AEF Container ДРПА КВ Alpha",
        "id": "CI09708620",
        "module_id": "CI10663014"
    },
    "agents": [
        {
            "name": "strategy-selection",
            "git": "ssh://git@stash.sigma.sbrf.ru:7999/kvaef/strategy-selection.git",
            "path": "./agents/strategy_selection/v0.1",
            "baseImage": "docker-internal.registry-ci.delta.sbrf.ru/ci04675739/ci04675739/python3.11:8.9.1"
        }
    ],
    "qg": {
        "mus_code": "00200044",
        "mus_name": "Models",
        "mus_po_mail": "Loshak.D.I@sberbank.ru",
        "sm_id": "CI09708620",
        "sm_name": "AI-HUB БТ.AEF Container ДРПА КВ Alpha",
        "jira_area": "AAA"
    },
    "buildCredentials": {
        "GIT_SSH_CREDENTIAL_ID": "GIT_CONFIGS_CRED",
        "PASS_CREDENTIAL_ID": "cab-sa-dvo09991_AD_DOMAIN",
        "OSC_TOKEN_CREDENTIAL_ID": "cab-sa-dvo09991_OSC_TOKEN"
    }
}