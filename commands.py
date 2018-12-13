import json
from slackbot.bot import respond_to
import re


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

        topten += "\n{}: {}".format(name, str(count))
        del data[name]

    message.reply("```{}```".format(topten))


@respond_to("start", re.IGNORECASE)
def start(message):
    """Start process of periodically sending message."""
    pass
