import os
import time
from slackclient import SlackClient

BOT_ID = os.environ.get("BOT_ID")
AT_BOT = "<@" + BOT_ID + ">"
EXAMPLE_COMMAND = "do"

slack_client = SlackClient(os.environ.get("SLACK_BOT_TOKEN"))
mems = slack_client.api_call(
  "channels.list",
   exclude_archived=1
)['channels'][71]['members']


class ADISpotting:
    def __init__(self):
        self.winner = "U56FWRC3D"
        self.users = {}

    def add_user(self, user):
        self.users[user] = 0

    def add_points(self, user, points):
        self.users[user] = self.users[user] + points
        if self.users[self.winner] < self.users[user]:
            self.winner = user

adispot = ADISpotting()
for i in mems:
    adispot.add_user(i)

def handle_command(command, channel):
    # receives commands at bot and determines validity
    response = "Not sure what you mean."
    if command.startswith(EXAMPLE_COMMAND): 
        response = "Cool"
    slack_client.api_call("chat.postMessage", channel=channel, text=response, as_user=True)

def parse_slack_output(slack_rtm_output):
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                return(output['user'],output['text'].split(AT_BOT)[1].strip().lower(), output['channel'])
    return(None,None,None)

if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1
    if slack_client.rtm_connect():
        print("ADISpotting connected and running!")
        while True:
            user, command, channel = parse_slack_output(slack_client.rtm_read())
            if user and command and channel:
                handle_command(command,channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid slack token or bot ID")


