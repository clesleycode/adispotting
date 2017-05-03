import os
import time
import sched
from slackclient import SlackClient
import game

BOT_ID = os.environ.get("BOT_ID")
AT_BOT = "<@" + BOT_ID + ">"

slack_client = SlackClient(os.environ.get("SLACK_BOT_TOKEN"))

mems = slack_client.api_call(
  "channels.list",
   exclude_archived=1
)['channels']

# finds the correct channel (ADISpotting)
ind = 0
for i in mems: 
    if i['id'] == "C55UAGM3N":
        mems = mems[ind]['members']
        break
    else:
        ind += 1


# need to add: what if a new user joins the channel?
adispot = game.ADISpotting()
for i in mems:
    adispot.add_user(i)


# needs to be cleaned 
def parse_slack_output(slack_rtm_output):
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            # for general response when we @adispotting
            if output and 'text' in output and AT_BOT in output['text']:
                slack_client.api_call("chat.postMessage", text="What do you want?", channel="C55UAGM3N", as_user=True) # default message - need to add parsing so bot adds points
            # for when a picture is posted
            elif output and 'subtype' in output and 'file' in output:
                adispot.add_points(output['file']['user'], 5) 
                slack_client.api_call("chat.postMessage", channel="C55UAGM3N", text=output['username'] + " now has " + str(adispot.get_points(output['user'])) + " points!", as_user=True)


# keeps the server awake so it doesnt break every 30 mins
def wake_server(sc):
    slack_client.api_call("users.list")
    s.enter(300, 1, wake_server, (slack_client,))


if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1
    if slack_client.rtm_connect():
        s = sched.scheduler(time.time, time.sleep)
        print("ADISpotting connected and running!")
        while True:
            parse_slack_output(slack_client.rtm_read())
            s.enter(60,1, wake_server, (slack_client,))
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid slack token or bot ID")

 #output['text'].split(AT_BOT)[1].strip().lower()
