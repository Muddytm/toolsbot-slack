import config
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

        org = "Unknown"
        for set in cache:
            if name in cache[set]:
                org = set
                for other_ip in cache[set]:
                    if other_ip != name:
                        count += data[other_ip]
                        del data[other_ip]
                break

        percentage = "%.2f" % float((count/total)*100.)
        topten += "\n{} ({}): {}%".format(org, name, str(percentage))

    # for i in range(10):
    #     name = ""
    #     count = 0
    #     for ip in data:
    #         if data[ip] > count:
    #             name = ip
    #             count = data[ip]
    #
    #     # Stuff for determining name of IP address owner
    #     org = None
    #     for orgname in cache:
    #         if name in cache[orgname]:
    #             org = orgname
    #
    #     if not org:
    #         url = "https://api.ipdata.co/{}?api-key={}".format(name,
    #                                                            config.ip_api_key)
    #         response = urllib2.urlopen(url)
    #         ip_data = response.read()
    #         info = json.loads(ip_data)
    #
    #         org = "Unknown"
    #         if "organisation" in info:
    #             org = info["organisation"]
    #
    #         if org not in cache:
    #             cache[org] = []
    #
    #         if name not in cache[org]:
    #             cache[org].append(name)
    #
    #     changed = False
    #     for result in results:
    #         if result[0] == org:
    #             result[1] = "Multiple IPs"
    #             result[2] += count
    #             changed = True
    #             break
    #
    #     if not changed:
    #         results.append([org, name, count])
    #
    #     del data[name]
    #
    # for result in results:
    #     percentage = "%.2f" % float((result[2]/total)*100.)
    #     topten += "\n{} ({}): {}%".format(result[0], result[1], str(percentage))


    message.reply("TLS 1.0/1.1 summary:\n```{}```".format(topten))


@respond_to("start", re.IGNORECASE)
def start(message):
    """Start process of periodically sending message."""
    pass
