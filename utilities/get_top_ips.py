import glob
import json
import os

file_list = glob.glob("/mnt/TLS/*.txt")
latest = max(file_list, key=os.path.getctime)
print (latest)
lines = open("/mnt/TLS/" + latest).readlines()

data = {}

for line in lines:
    ip = line.split("ClientIP")[1].strip().split()[0]

    if ip not in data:
        data[ip] = 0
    else:
        data[ip] += 1

with open("data/tls.json", "w") as f:
    json.dump(data, f)
