import glob
import json
import os
import urllib.request as urllib2

file_list = glob.glob("/mnt/TLS/*.txt")
latest = max(file_list, key=os.path.getctime)
#print (latest)
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
    url = "https://api.ipdata.co/{}?api-key={}".format(name,
                                                       config.ip_api_key)
    response = urllib2.urlopen(url)
    ip_data = response.read()
    info = json.loads(ip_data)

    org = "Unknown"
    if "organisation" in info:
        org = info["organisation"]

    if org not in cache:
        cache[org] = []

    if ip not in cache[org]:
        cache[org].append(ip)

with open("data/tls_cache.json", "w") as f:
    json.dump(cache, f)
