try:
    import utilities.config as config
except ModuleNotFoundError:
    import config
import datetime
import glob
import json
import os
import time
import urllib.request as urllib2


def match_ip(ip, start, end):
    """Check if ip lies between start and end."""
    ip_tokens = ip.split(".")
    start_tokens = start.split(".")
    end_tokens = end.split(".")

    if int(ip_tokens[2]) >= int(start_tokens[2]) and int(ip_tokens[2]) <= int(end_tokens[2]):
        if int(ip_tokens[3]) >= int(start_tokens[3]) and int(ip_tokens[3]) <= int(end_tokens[3]):
            return True

file_list = glob.glob("/mnt/TLS/*.txt")
latest = max(file_list, key=os.path.getctime)
#print ("Getting info from..." + latest)
lines = open(latest).readlines()

data = {}
dfw_data = {}
sea_data = {}

for line in lines:
    ip = line.split("ClientIP")[1].strip().split()[0]
    kurt = line.split("GMT")[1].strip().split()[0].split("-")[0] # Calling it this because idk what else to call it

    if ip not in data:
        data[ip] = 1
    else:
        data[ip] += 1

    if kurt.lower() == "dfw":
        if ip not in dfw_data:
            dfw_data[ip] = 1
        else:
            dfw_data[ip] += 1
    elif kurt.lower() == "sea":
        if ip not in sea_data:
            sea_data[ip] = 1
        else:
            sea_data[ip] += 1

    print ("TLS 1.0/1.1: added {} ({})".format(ip, kurt))

with open("data/tls.json", "w") as f:
    json.dump(data, f)

with open("data/tls_dfw.json", "w") as f:
    json.dump(dfw_data, f)

with open("data/tls_sea.json", "w") as f:
    json.dump(sea_data, f)

# Record the daily TLS information.
day_int = datetime.datetime.today().weekday()
days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
with open("data/tls_{}.json".format(days[day_int]), "w") as f:
    json.dump(data, f)

# Assigning orgs and making cache
if os.path.exists("data/tls_cache.json"):
    with open("data/tls_cache.json") as f:
        cache = json.load(f)
else:
    cache = {}

for ip in data:

    with open("data/aliases.json") as f:
        aliases = json.load(f)

    cont = False
    for alias in aliases:
        if match_ip(ip, aliases[alias]["start"], aliases[alias]["end"]):
            cache[alias] = []
            cache[alias].append(ip)
            cont = True
            break

    if cont:
        continue

    #url = "http://ip-api.com/json/{}".format(ip)
    url = "https://api.ipdata.co/{}?api-key={}".format(ip,
                                                       config.ip_api_key)

    for i in range(3):
        try:
            response = urllib2.urlopen(url)
            ip_data = response.read()
            info = json.loads(ip_data)
        except Exception as e: #placeholder since the specified exception was apparently not defined...?
            #print (e)
            info = {}

        if "organisation" in info:
            break

        time.sleep(1)

    org = "Unknown/Private"
    if "organisation" in info: # used to be "organisation"
        org = info["organisation"]

    if org not in cache:
        cache[org] = []

    if ip not in cache[org]:
        cache[org].append(ip)

with open("data/tls_cache.json", "w") as f:
    json.dump(cache, f)

# if os.path.exists("data/jobs.json"):
#     with open("data/jobs.json") as f:
#         jobs = json.load(f)
# else:
#     jobs = []
#
# jobs.append("TLS")
#
# with open("data/jobs.json", "w") as f:
#     json.dump(jobs, f)
