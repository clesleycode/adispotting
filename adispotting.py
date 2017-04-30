import os
import time
from slackclient import SlackClient

BOT_ID = os.environ.get("BOT_ID")
AT_BOT = "<@" + BOT_ID + ">"
EXAMPLE_COMMAND = "do"

slack_client = SlackClient(os.environ.get("SLACK_BOT_TOKEN"))

class ADISpotting(object):
    def __init__(self):
        self.winner = None
        self.users = {}

    def add_points(self, user, points):
        self.users[user] = self.users[user] += points


def handle_command(command, channel):
    # receives commands at bot and determines validity
    response = "Not sure what you mean."
    if command.startswith(EXAMPLE_COMMAND): 
        response = "Cool"
    print(response)
    slack_client.api_call("chat.postMessage", channel=channel, text=response, as_user=True)

def parse_slack_output(slack_rtm_output):
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                return(output['text'].split(AT_BOT)[1].strip().lower(), output['channel'])
    return(None,None)

if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1
    if slack_client.rtm_connect():
        print("ADISpotting connected and running!")
        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                handle_command(command,channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid slack token or bot ID")


