"""
<meta http-equiv="refresh" content="3; URL=https://www.youtube.com/watch?v=dQw4w9WgXcQ" />
dndgen wbz ttttest mafia123
"""



from classes import Agent, WebServer

import re
import requests
import sys
from time import sleep
from threading import Thread
from random import randint
from flask import request

agents = {}
main = WebServer(__name__)

index_page = " ".join([(lambda font: f'<h{font}>{"James Curran"}</h{font}>')(str(randint(1, 4))) for x in range(100)])
@main.route("/")
def index():
    return index_page

@main.post('/chat')
def chat():
    message = request.json

    message_room = message['room']
    message_author = message['author']

    # Check for room
    if message_room not in agents:
        print("yes")
        agents[message_room] = Agent(f"Timothy [{len(agents.keys()) + 1}]", message_room)

    if "form_data" in message:
        agent = agents[message_room]
        data = message["form_data"]

        response = agent.call("Please fix this code, then return it. Remember to put all code blocks in markdown code formatting. Do not include the programming language within the code quotes.: " + data["text"])
        return {
                    "author": agent.name,
                    "text": response,
                    "css": "/static/default.css"
                }

    return process_message(agents[message_room], message)

def process_message(agent, message):
    message_text = message['text']

    if re.search("meow", message_text, re.IGNORECASE):
        return {
            "author": agent.name,
            "text": f"Meow<br>I'm {agent.name}"
        }

    elif re.search("print agents", message_text, re.IGNORECASE):
        for key in agents:
            return {
                "author": agent.name,
                "text": str({
                    "name": agents[key].name,
                    "room": agents[key].room,
                    "timer": agents[key].timer
                })
            }

    elif re.search("clear room", message_text, re.IGNORECASE):
        data = {
            "room": agent.room
        }
        requests.post("https://chat.ncss.cloud/api/actions/clear-room-messages", json=data)
        return {
            "author": agent.name,
            "text": "Cleared room."
        }

    elif re.search("help (me with my|with my|me) code", message_text, re.IGNORECASE):
        form = f"""
        <form method="post">
            <p>What code do you need help with?</p>
            <input type="hidden" name="agent_name" value="{agent.name}" />
            <textarea name="text" cols="40" rows="5"></textarea><br>
            <input type="submit" value="Submit">
        </form>
        """
        return {
            "author": agent.name,
            "text": form
        }

    elif re.search("del", message_text, re.IGNORECASE):
        return {
            "author": agent.name,
            "text": "test",
            "js": "/static/delete_last_msg.js"
        }

    elif re.search(r"Timothy|yeah|yes|ye|yea|yup", message_text, re.IGNORECASE):
        response = agent.call(message_text)
        
        return {
            "author": agent.name,
            "text": response,
            "css": "/static/default.css"
        }

    else:
        
        return {
            "author": agent.name,
            "text": "I don't understand, please say that again."
        }


def main_loop():
    main.run()

def event_loop():
    while True:
        for key in agents.copy():
            if key in agents:
                agents[key].timer += 1

                if agents[key].timer >= 180: # Delete conversation history after three minutes
                    del agents[key]

        sleep(1)

    print("Application closed.")
    sys.exit()

if __name__ == "__main__":

    #threads = [
    #    Thread(target=main_loop),
    #    Thread(target=event_loop)
    #]

    #try:
    #    for thread in threads:
    #        thread.start()

    #except KeyboardInterrupt:
    #    pass
    main_loop()