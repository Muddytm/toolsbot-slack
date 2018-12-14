import utilities.config as config
import glob
import json
import os
from slackbot.bot import respond_to
import re
import urllib.request as urllib2


@respond_to("test", re.IGNORECASE)
def test(message):
    """Send test message."""
    message.reply("Greetings!")


@respond_to("tls", re.IGNORECASE)
def tls(message):
    """Send test tls message."""
    with open("data/tls.json") as f:
        data = json.load(f)

    if os.path.exists("data/tls_cache.json"):
        with open("data/tls_cache.json") as f:
            cache = json.load(f)
    else:
        message.reply("No cache to read from. Contact Caleb Hawkins to get this fixed.")
        return

    total = 0
    topten = ""
    results = []

    for ip in data:
        total += data[ip]

    for i in range(10):
        name = ""
        count = 0

        for ip in data:
            if data[ip] > count:
                name = ip
                count = data[ip]

        rename = False
        org = "Unknown"
        for set in cache:
            if name in cache[set]:
                org = set
                for other_ip in cache[set]:
                    if other_ip != name:
                        rename = True
                        count += data[other_ip]
                        del data[other_ip]

                del cache[set]
                break

        del data[name]

        if rename:
            name = "Multiple IPs"
        else:
            name = "<https://api.ipdata.co/{}?api-key={}|{}>".format(name,
                                                                     config.ip_api_key,
                                                                     name)

        percentage = "%.2f" % float((count/total)*100.)
        topten += "\n{} ({}): {}%".format(org, name, str(percentage))

    file_list = glob.glob("/mnt/TLS/*.txt")
    latest = max(file_list, key=os.path.getctime)
    latest_tokens = latest.replace(".txt", "").split("-")
    date = "{}/{}/{}".format(latest_tokens[2], latest_tokens[3], latest_tokens[1])

    message.reply("TLS 1.0/1.1 summary for {}:\n```{}```".format(date, topten))


@respond_to("start", re.IGNORECASE)
def start(message):
    """Start process of periodically sending message."""
    pass
