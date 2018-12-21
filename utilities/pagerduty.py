try:
    import utilities.config as config
except ModuleNotFoundError:
    import config
import json
import os
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


if __name__ == '__main__':
    if os.path.exists("data/jobs.json"):
        with open("data/jobs.json") as f:
            jobs = json.load(f)
    else:
        jobs = []

    jobs.append("PAGERDUTY")

    with open("data/jobs.json", "w") as f:
        json.dump(jobs, f)
