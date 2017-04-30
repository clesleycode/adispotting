import os
import time
from slackclient import SlackClient

BOT_ID = os.environ.get("BOT_ID")
AT_BOT = "<@" + BOT_ID + ">"

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
    
    def get_points(self, user):
        return(self.users[user])


adispot = ADISpotting()
for i in mems:
    adispot.add_user(i)


def parse_slack_output(slack_rtm_output):
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                slack_client.api_call("chat.postMessage", text="What do you want?", channel= output['channel'], as_user=True)
            elif output and 'user_id' in output and output['type'] == 'file_shared':
                adispot.add_points(output['user_id'], 5)
                slack_client.api_call("chat.postMessage", channel="C57D2GXM4", text=output['user_id'] + " now has " + str(adispot.get_points(output['user_id'])) + " points!", as_user=True)


if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1
    if slack_client.rtm_connect():
        print("ADISpotting connected and running!")
        while True:
            parse_slack_output(slack_client.rtm_read())
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid slack token or bot ID")


