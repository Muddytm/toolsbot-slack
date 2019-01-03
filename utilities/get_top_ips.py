try:
    import utilities.config as config
except ModuleNotFoundError:
    import config
import glob
import json
import os
import urllib.request as urllib2

file_list = glob.glob("/mnt/TLS/*.txt")
latest = max(file_list, key=os.path.getctime)
print ("Getting info from..." + latest)
lines = open(latest).readlines()

data = {}

for line in lines:
    ip = line.split("ClientIP")[1].strip().split()[0]

    if ip not in data:
        data[ip] = 1
    else:
        data[ip] += 1

with open("data/tls.json", "w") as f:
    json.dump(data, f)

# Assigning orgs and making cache
if os.path.exists("data/tls_cache.json"):
    with open("data/tls_cache.json") as f:
        cache = json.load(f)
else:
    cache = {}

for ip in data:
    url = "http://ip-api.com/json/{}".format(ip)
    #url = "https://api.ipdata.co/{}?api-key={}".format(ip,
    #                                                   config.ip_api_key)
    try:
        response = urllib2.urlopen(url)
        ip_data = response.read()
        info = json.loads(ip_data)
    except Exception as e: #placeholder since the specified exception was apparently not defined...?
        print (e)
        info = {}

    org = "Unknown/Private"
    if "org" in info: # used to be "organisation"
        org = info["org"]

    if org not in cache:
        cache[org] = []

    if ip not in cache[org]:
        cache[org].append(ip)

with open("data/tls_cache.json", "w") as f:
    json.dump(cache, f)

if os.path.exists("data/jobs.json"):
    with open("data/jobs.json") as f:
        jobs = json.load(f)
else:
    jobs = []

jobs.append("TLS")

with open("data/jobs.json", "w") as f:
    json.dump(jobs, f)
