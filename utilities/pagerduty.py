import utilities.config as config
import json
import requests

token = config.pd_token

headers = {"Authorization": "Token token=" + token,
           "Accept": "application/vnd.pagerduty+json;version=2"}
r = requests.get("https://api.pagerduty.com/oncalls", headers=headers)

oncalls = json.loads(r.text)

#print (oncalls)

for oncall in oncalls["oncalls"]:
    if "schedule" in oncall and oncall["schedule"]:
        if "summary" in oncall["schedule"]:
            if oncall["schedule"]["summary"] == "Ops Primary Contact":
                print (oncall["user"]["summary"])
