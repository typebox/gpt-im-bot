
import os
import openai
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack import WebClient
from slack_bolt import App

def main(args):
    # Get the Home Assistant instance URL, bearer token, and sensors from environment variables
    SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")
    SLACK_APP_TOKEN = os.environ.get("SLACK_APP_TOKEN")
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

    print(f"Received args:\n{args}")
    
    # send_text_response(event)
    
    return "200 OK"

def send_text_response(event):
    print("Messaging Slack...")
    SLACK_URL = "https://slack.com/api/chat.postMessage"
    channel_id = event.get("event").get("channel")
    
    body = event.get("body")

    # Log message
    print(str(body["event"]["text"]).split(">")[1])
    
    # Create prompt for ChatGPT
    prompt = str(body["event"]["text"]).split(">")[1]
    
    # Check ChatGPT
    openai.api_key = OPENAI_API_KEY
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5).choices[0].text

    data = urllib.parse.urlencode(
        (
            ("token", SLACK_BOT_TOKEN),
            ("channel", channel_id),
            ("text", response)
        )
    )
    data = data.encode("ascii")
    
    request = urllib.request.Request(SLACK_URL, data=data, method="POST")
    request.add_header( "Content-Type", "application/x-www-form-urlencoded" )
    
    # Fire off the request!
    x = urllib.request.urlopen(request).read()