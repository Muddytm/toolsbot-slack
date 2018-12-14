import config
import json
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

    counts =
    total = 0
    topten = ""

    for ip in data:
        total += data[ip]

    for i in range(10):
        name = ""
        count = 0
        for ip in data:
            total += data[ip]

            if data[ip] > count:
                name = ip
                count = data[ip]

        # Stuff for determining name of IP address owner
        url = "https://api.ipdata.co/{}?api-key={}".format(name,
                                                           config.ip_api_key)
        response = urllib2.urlopen(url)
        ip_data = response.read()
        info = json.loads(ip_data)

        org = "Unknown"
        if "organisation" in info:
            org = info["organisation"]

        percentage = float((count/total)*100.)

        # Appending stuff to the line
        topten += "\n{} ({}): {}%".format(org, name, str(percentage))
        del data[name]

    message.reply("```{}```".format(topten))


@respond_to("start", re.IGNORECASE)
def start(message):
    """Start process of periodically sending message."""
    pass
