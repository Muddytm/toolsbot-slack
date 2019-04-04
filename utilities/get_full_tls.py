import glob
import json
import os
import time


file_list = glob.glob("/mnt/TLS/alltls/*.txt")
latest = max(file_list, key=os.path.getctime)

all_12_data = {}
all_10_11_data = {}
dfw_12_data = {}
sea_12_data = {}
dfw_10_11_data = {}
sea_10_11_data = {}

with open(latest) as f:
    for line in f:
        ip = line.split("ClientIP")[1].strip().split()[0]
        kurt = line.split("GMT")[1].strip().split()[0].split("-")[0] # Calling it this because idk what else to call it

        if "TLSv1.2" in line:
            if ip not in all_12_data:
                all_12_data[ip] = 1
            else:
                all_12_data[ip] += 1

            if kurt.lower() == "sea":
                if ip not in sea_12_data:
                    sea_12_data[ip] = 1
                else:
                    sea_12_data[ip] += 1
            elif kurt.lower() == "dfw":
                if ip not in dfw_12_data:
                    dfw_12_data[ip] = 1
                else:
                    dfw_12_data[ip] += 1
            else:
                print ("Was not able to get \"kurt\" variable?")

            print ("TLS 1.2: added {} ({})".format(ip, kurt))
        elif "TLSv1.0" in line or "TLSv1.1" in line:
            if ip not in all_10_11_data:
                all_10_11_data[ip] = 1
            else:
                all_10_11_data[ip] += 1

            if kurt.lower() == "sea":
                if ip not in sea_10_11_data:
                    sea_10_11_data[ip] = 1
                else:
                    sea_10_11_data[ip] += 1
            elif kurt.lower() == "dfw":
                if ip not in dfw_10_11_data:
                    dfw_10_11_data[ip] = 1
                else:
                    dfw_10_11_data[ip] += 1
            else:
                print ("Was not able to get \"kurt\" variable?")

            print ("TLS 1.0/1.1: added {} ({})".format(ip, kurt))

with open("data/alldata/all_12_data.json", "w") as f:
    json.dump(all_12_data, f)

with open("data/alldata/all_10_11_data.json", "w") as f:
    json.dump(all_10_11_data, f)

with open("data/alldata/dfw_12_data.json", "w") as f:
    json.dump(dfw_12_data, f)

with open("data/alldata/sea_12_data.json", "w") as f:
    json.dump(sea_12_data, f)

with open("data/alldata/dfw_10_11_data.json", "w") as f:
    json.dump(dfw_10_11_data, f)

with open("data/alldata/sea_10_11_data.json", "w") as f:
    json.dump(sea_10_11_data, f)
