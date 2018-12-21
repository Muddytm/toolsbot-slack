import utilities.config as config
import glob
import json
import os
import time
import urllib.request as urllib2


def fetch_tls(name):
    """Print IPs that apply to whatever org name is given."""
    with open("data/tls_cache.json") as f:
        cache = json.load(f)

    with open("data/tls.json") as f:
        data = json.load(f)

    total = 0
    all_ips = ""
    for org in cache:
        if name in org.lower():
            for ip in cache[org]:
                if ip in data:
                    total += data[ip]

            for ip in cache[org]:
                if ip in data:
                    all_ips += "{} - {}\n".format(ip,
                                                  "%.2f" % float((data[ip]/total)*100.))
            break

    print (all_ips)


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

    orgs = {}

    for org in cache:
        org_count = 0
        ip_name = ""
        ip_count = 0
        rename = False

        for ip in cache[org]:
            if ip in data:
                if data[ip] > ip_count:
                    if ip_count > 0:
                        rename = True
                    ip_count = data[ip]
                    ip_name = ip
                org_count += data[ip]
            #del data[ip]

        orgs[org] = {}
        orgs[org]["count"] = org_count

        if rename:
            orgs[org]["url"] = "<https://api.ipdata.co/{}?api-key={}|Multiple IPs>".format(ip_name,
                                                                                           config.ip_api_key)
        else:
            orgs[org]["url"] = "<https://api.ipdata.co/{}?api-key={}|{}>".format(ip_name,
                                                                                 config.ip_api_key,
                                                                                 ip_name)

    for i in range(limit):
        org_name = ""
        org_count = 0
        for org in orgs:
            if orgs[org]["count"] > org_count:
                org_name = org
                org_count = orgs[org]["count"]
                org_url = orgs[org]["url"]

        percentage = "%.2f" % float((org_count/total)*100.)
        top += "\n{} ({}): {}%".format(org_name, org_url, str(percentage))
        del orgs[org_name]


    file_list = glob.glob("/mnt/TLS/*.txt")
    latest = max(file_list, key=os.path.getctime)
    latest_tokens = latest.replace(".txt", "").split("-")
    date = "{}/{}/{}".format(latest_tokens[2], latest_tokens[3], latest_tokens[1])

    return date, top, 1


if __name__ == '__main__':
    fetch_tls("placeholder")
