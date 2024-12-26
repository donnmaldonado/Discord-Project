import discord
from discord.ext import tasks
import csv
import hashlib
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv, dotenv_values
import json
import random
from utils.file_utils import load_last_message_times, load_questions

from config import BOT_TOKEN

INACTIVITY_THRESHOLD = 5 # time in seconds
last_message_times = load_last_message_times("data/channels.json")
questions = load_questions("data/questions.json")


# generates unique id by hashing user's discord id
def generate_unique_id(discord_user_id):
    id = f"{discord_user_id}".encode('utf-8')
    hashed_id = hashlib.sha256(id).hexdigest()
    return hashed_id

# checks inactivity of channels, sends message if inactive
@tasks.loop(seconds=5)
async def check_inactivity(self):
    print(f"checking inactivity {datetime.utcnow()}")
    for key in last_message_times:
        if last_message_times[key] != None:
            inactivity_duration = datetime.utcnow() - last_message_times[key]
            if inactivity_duration.total_seconds() > INACTIVITY_THRESHOLD:
                print(f"{key} has been inactive for {inactivity_duration}")
                channel = self.get_channel(key)
                question = random.choice(questions[key])
                await channel.send(question)
                last_message_times[key] = datetime.utcnow()


class Client(discord.Client):
    # called when bot has finished logging in and setting up
    async def on_ready(self):
        print(f'Logged on as {self.user}!')
        check_inactivity.start(self)
    

    # Records all messages along with a unique ID representing user
    async def on_message(self, message):
        # ignore messages from self(bot)
        if message.author == self.user:
            return

        # create unique id for given user
        unique_id = generate_unique_id(message.author)
        
        # update time of last message in specific channel
        last_message_times[message.channel.id] = datetime.utcnow()
        # print(last_message_times)

        # write message and hashed id to file
        with open('data/messages.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerows([[unique_id ,message.content]])
            file.close()


# intents allow bot to subscribe to specific bucket of events
intents = discord.Intents.default() 
# enables app to recieve actual content of newly created messages
intents.message_content = True      


client = Client(intents=intents)
client.run(BOT_TOKEN)