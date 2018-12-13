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

    topten = ""

    for i in range(10):
        name = ""
        count = 0
        for ip in data:
            if data[ip] > count:
                name = ip
                count = data[ip]

        url = "https://api.ipdata.co/{}?api-key={}".format(name,
                                                           config.ip_api_key)
        response = urllib2.urlopen(url)
        ip_data = response.read()
        info = json.loads(ip_data)

        org = ""
        if "organisation" in info:
            org = " ({})".format(info["organisation"])


        topten += "\n{}{}: {}".format(name, org, str(count))
        del data[name]

    message.reply("```{}```".format(topten))


@respond_to("start", re.IGNORECASE)
def start(message):
    """Start process of periodically sending message."""
    pass
