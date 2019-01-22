import utilities.config as config
import datetime
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
    """Get TLS stats."""
    date, top, status = utilities.sort_tls()

    if status == 0:
        message.reply("Something broke. Ask Caleb what happened.")
        return

    message.reply("TLS 1.0/1.1 summary for {}:\n```{}```".format(date, top))


@respond_to("weekly", re.IGNORECASE)
def weeklytls(message):
    """Get TLS stats for the past week."""
    date, top, status = utilities.sort_tls(1000, "weekly_stats")

    if status == 0:
        message.reply("Something broke. Ask Caleb what happened.")
        return

    message.reply("TLS 1.0/1.1 summary for the last 7 days:\n{}".format(date, top))



@respond_to("allstats", re.IGNORECASE)
def givemetls(message):
    """Get full TLS stats."""
    date, top, status = utilities.sort_tls(1000)

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

                    if datetime.datetime.today().weekday() > 4:
                        continue

                    if os.path.exists("data/tls_cache.json"):
                        with open("data/tls_cache.json") as f:
                            cache = json.load(f)
                    else:
                        #message.reply("No cache to read from. Contact Caleb Hawkins to get this fixed.")
                        continue

                    date, top, status = utilities.sort_tls()

                    if status == 0:
                        message.reply("Something broke. Ask Caleb what happened.")
                        continue

                    message._client.send_message(config.main_chan, "Top TLS 1.0/1.1 users for {}:\n```{}```".format(date, top))
                elif "PAGERDUTY" in jobs:
                    jobs.remove("PAGERDUTY")
                    with open("data/jobs.json", "w") as f:
                        json.dump(jobs, f)

                    name = utilities.get_oncall()

                    if name:
                        for channel in message._client.channels:
                            channel = config.main_chan_id # toolsbot: CCM0HCM6W
                            r = requests.get("https://slack.com/api/channels.info?token={}&channel={}".format(slackbot_settings.API_TOKEN, channel))
                            data = (json.loads(r.text))

                            cur_name = (data["channel"]["topic"]["value"]).split(": ")[1]
                            #print (cur_name)

                            if "channel" in data:
                                if "name" in data["channel"]:
                                    #print (config.main_chan + " " + data["channel"]["name"])
                                    if config.main_chan == data["channel"]["name"]:
                                        chan = data["channel"]["id"]
                                        #print (chan)
                                        break

                        if cur_name != name:
                            r = requests.post("https://slack.com/api/channels.setTopic?token={}&channel={}&topic=ON%2DCALL%3A%20{}".format(slackbot_settings.SCOPE_TOKEN, chan, name))
                        #print (r.text)
                else:
                    time.sleep(60)
                    continue
            else:
                time.sleep(60)
                continue
