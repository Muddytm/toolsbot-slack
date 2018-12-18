import utilities.config as config
import glob
import json
import os
import time
import urllib.request as urllib2


def sort_tls(limit=10):
    """Sorting the TLS hits."""
    with open("data/tls.json") as f:
        data = json.load(f)

    if os.path.exists("data/tls_cache.json"):
        with open("data/tls_cache.json") as f:
            cache = json.load(f)
    else:
        return "", "", 0

    total = 0
    top_ip = ""
    top_ip_count = 0
    top = ""
    results = []

    for ip in data:
        total += data[ip]

    for i in range(limit):
        name = ""
        count = 0

        for ip in data:
            if data[ip] > count:
                name = ip
                count = data[ip]
                top_ip = name
                top_ip_count = count

        rename = False
        org = "Unknown"
        for set in cache:
            if name in cache[set]:
                org = set
                for other_ip in cache[set]:
                    if other_ip != name and other_ip in data:
                        if data[other_ip] > top_ip_count:
                            top_ip = other_ip
                            top_ip_count = data[other_ip]
                        rename = True
                        count += data[other_ip]
                        del data[other_ip]

                del cache[set]
                break

        del data[name]

        if rename:
            name = "<https://api.ipdata.co/{}?api-key={}|Multiple IPs>".format(top_ip,
                                                                               config.ip_api_key)
        else:
            name = "<https://api.ipdata.co/{}?api-key={}|{}>".format(name,
                                                                     config.ip_api_key,
                                                                     name)

        percentage = "%.2f" % float((count/total)*100.)
        top += "\n{} ({}): {}%".format(org, name, str(percentage))

    file_list = glob.glob("/mnt/TLS/*.txt")
    latest = max(file_list, key=os.path.getctime)
    latest_tokens = latest.replace(".txt", "").split("-")
    date = "{}/{}/{}".format(latest_tokens[2], latest_tokens[3], latest_tokens[1])

    return date, top, 1
