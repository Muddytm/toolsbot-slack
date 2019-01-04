import utilities.config as config
import glob
import json
import os
from slackbot.bot import respond_to
from slackbot.bot import listen_to
import re
import requests
import slackbot_settings
import time
import utilities
import urllib.request as urllib2

tls_check = False

@respond_to("test", re.IGNORECASE)
def test(message):
    """Send test message."""
    message.reply("Greetings!")


@respond_to("tls", re.IGNORECASE)
def tls(message):
    """Send test tls message."""
    date, top, status = utilities.sort_tls()

    if status == 0:
        message.reply("Something broke. Ask Caleb what happened.")
        return

    message.reply("TLS 1.0/1.1 summary for {}:\n```{}```".format(date, top))


@listen_to("start", re.IGNORECASE)
def starttls(message):
    """Start TLS loop."""
    global tls_check

    if tls_check:
        return
    else:
        #message._client.send_message(config.main_chan, "Posting TLS stats daily at 8 AM! (Unless I break. Fingers crossed.)")
        tls_check = True
        while True:
            if os.path.exists("data/jobs.json"):
                with open("data/jobs.json") as f:
                    jobs = json.load(f)

                if "TLS" in jobs:
                    jobs.remove("TLS")
                    with open("data/jobs.json", "w") as f:
                        json.dump(jobs, f)

                    with open("data/tls.json") as f:
                        data = json.load(f)

                    if os.path.exists("data/tls_cache.json"):
                        with open("data/tls_cache.json") as f:
                            cache = json.load(f)
                    else:
                        #message.reply("No cache to read from. Contact Caleb Hawkins to get this fixed.")
                        return

                    date, top, status = utilities.sort_tls()

                    if status == 0:
                        message.reply("Something broke. Ask Caleb what happened.")
                        return

                    message._client.send_message(config.main_chan, "TLS 1.0/1.1 summary for {}:\n```{}```".format(date, top))
                elif "PAGERDUTY" in jobs:
                    jobs.remove("PAGERDUTY")
                    with open("data/jobs.json", "w") as f:
                        json.dump(jobs, f)

                    name = utilities.get_oncall()

                    if name:
                        for channel in message._client.channels:
                            if channel["name"] == config.main_chan:
                                chan = channel["id"]

                        body = {"token": slackbot_settings.SCOPE_TOKEN,
                                "channel": chan,
                                "topic": "ONCALL: " + name}

                        r = requests.post("https://slack.com/api/channels.setTopic",
                                          data=body)
                else:
                    time.sleep(60)
                    continue
            else:
                time.sleep(60)
                continue
