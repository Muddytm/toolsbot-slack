from slackbot.bot import respond_to
import re


@respond_to("test", re.IGNORECASE)
def test(message):
    """Send test message."""
    message.reply("Greetings!")


@respond_to("start", re.IGNORECASE)
def start(message):
    """Start process of periodically sending message."""
    pass
