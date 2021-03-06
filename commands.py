import utilities.config as config
import csv
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


@respond_to("fulltlsreport", re.IGNORECASE)
def fulltlsreport(message):
    """Get full tls report"""

    output=open("data/alldata/tls_report.txt", "w")

    with open("data/alldata/tls_report.csv", "rt", encoding="ascii") as f:
        for row in f:
            output.write(row)

    with open("data/alldata/tls_report.txt") as f:
        data = f.read()

    message.reply(data)


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

    message.reply("TLS 1.0/1.1 summary for the last 7 days:\n{}".format(top))


@respond_to("dfwstats", re.IGNORECASE)
def dfwstats(message):
    """Get DFW stats for the past week."""
    date, top, status = utilities.sort_tls(1000, "tls_dfw")

    if status == 0:
        message.reply("Something broke. Ask Caleb what happened.")
        return

    message.reply("DFW TLS 1.0/1.1 summary for {}:\n{}".format(date, top))


@respond_to("seastats", re.IGNORECASE)
def seastats(message):
    """Get SEA stats for the past week."""
    date, top, status = utilities.sort_tls(1000, "tls_sea")

    if status == 0:
        message.reply("Something broke. Ask Caleb what happened.")
        return

    message.reply("SEA TLS 1.0/1.1 summary for {}:\n{}".format(date, top))


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
        tls_check = True
        while True:
            if os.path.exists("data/jobs.json"):
                with open("data/jobs.json") as f:
                    jobs = json.load(f)

                if "PAGERDUTY" in jobs:
                    jobs.remove("PAGERDUTY")
                    with open("data/jobs.json", "w") as f:
                        json.dump(jobs, f)

                    try:
                        name = utilities.get_oncall()
                    except JSONDecodeError:
                        with open("most_recent_error.log", "w") as f:
                            f.write(str(datetime.datetime.now()))
                        continue

                    if name:
                        for channel in message._client.channels:
                            channel = config.main_chan_id
                            r = requests.get("https://slack.com/api/channels.info?token={}&channel={}".format(slackbot_settings.API_TOKEN, channel))
                            data = (json.loads(r.text))

                            cur_name = (data["channel"]["topic"]["value"]).split(": ")[1]

                            if "channel" in data:
                                if "name" in data["channel"]:
                                    if config.main_chan == data["channel"]["name"]:
                                        chan = data["channel"]["id"]
                                        break

                        if cur_name != name:
                            r = requests.post("https://slack.com/api/channels.setTopic?token={}&channel={}&topic=ON%2DCALL%3A%20{}".format(slackbot_settings.SCOPE_TOKEN, chan, name))
                else:
                    time.sleep(60)
                    continue
            else:
                time.sleep(60)
                continue
