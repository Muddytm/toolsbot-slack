import json
import os

ip_info = {}

for file in os.listdir("data/"):
    print (file)
    if file.endswith("day.json"): # Get daily files
        with open("data/{}".format(file)) as f:
            data = json.loads(f.read())

        for ip in data:
            if ip not in ip_info:
                ip_info[ip] = 0

            ip_info[ip] += data[ip]

with open("data/weekly_stats.json", "w") as f:
    json.dump(ip_info, f)
