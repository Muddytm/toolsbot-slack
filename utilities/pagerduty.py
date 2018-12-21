import config
import json
import requests


def get_oncall():
    """Get currently oncall from Pagerduty."""
    token = config.pd_token

    headers = {"Authorization": "Token token=" + token,
               "Accept": "application/vnd.pagerduty+json;version=2"}

    r = requests.get("https://api.pagerduty.com/oncalls", headers=headers)

    oncalls = json.loads(r.text)

    name = ""
    for oncall in oncalls["oncalls"]:
        if "schedule" in oncall and oncall["schedule"]:
            if "summary" in oncall["schedule"]:
                if oncall["schedule"]["summary"] == "Ops Primary Contact":
                    name = oncall["user"]["summary"]
                    break

    return name
