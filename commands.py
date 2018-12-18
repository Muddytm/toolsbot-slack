import utilities.config as config
import glob
import json
import os
from slackbot.bot import respond_to
from slackbot.bot import listen_to
import re
import time
import utilities.tls as tls
import urllib.request as urllib2

tls_check = False

@respond_to("test", re.IGNORECASE)
def test(message):
    """Send test message."""
    message.reply("Greetings!")


@respond_to("tls", re.IGNORECASE)
def tls(message):
    """Send test tls message."""
    date, top, status = tls.sort_tls()

    if status == 0:
        message.reply("Something broke. Ask Caleb what happened.")
        return

    message.reply("TLS 1.0/1.1 summary for {}:\n```{}```".format(date, top))


@listen_to("starttls", re.IGNORECASE)
def starttls(message):
    """Start TLS loop."""
    if tls_check:
        return
    else:
        message._client.send_message(config.main_chan, "Posting TLS stats daily at 8 AM! (Unless I break. Fingers crossed.)")
        while True:
            if os.path.exists("data/jobs.json"):
                with open("data/jobs.json") as f:
                    jobs = json.load(f)

                if "TLS" in jobs:
                    print (jobs)
                    jobs.remove("TLS")
                    print (jobs)
                    with open("data/jobs.json", "w") as f:
                        json.dump(jobs, f)
                else:
                    time.sleep(60)
                    continue
            else:
                time.sleep(60)
                continue

            with open("data/tls.json") as f:
                data = json.load(f)

            if os.path.exists("data/tls_cache.json"):
                with open("data/tls_cache.json") as f:
                    cache = json.load(f)
            else:
                #message.reply("No cache to read from. Contact Caleb Hawkins to get this fixed.")
                return

            date, top, status = tls.sort_tls()

            if status == 0:
                message.reply("Something broke. Ask Caleb what happened.")
                return

            message._client.send_message(config.main_chan, "TLS 1.0/1.1 summary for {}:\n```{}```".format(date, topten))


@respond_to("start", re.IGNORECASE)
def start(message):
    """Start process of periodically sending message."""
    pass
