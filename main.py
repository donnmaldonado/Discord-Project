import discord
import csv
import hashlib
import os
from dotenv import load_dotenv, dotenv_values

# loading in ENV variable: Discord Token
load_dotenv()
bot_token = os.getenv("DISCORD_BOT_TOKEN")

# generates unique id by hashing user's discord id
def generate_unique_id(discord_user_id):
    id = f"{discord_user_id}".encode('utf-8')
    hashed_id = hashlib.sha256(id).hexdigest()
    return hashed_id


class Client(discord.Client):
    # called when bot has finished logging in and setting up
    async def on_ready(self):
        print(f'Logged on as {self.user}!')
    
    # Records all messages along with a unique ID representing user
    async def on_message(self, message):
        # ignore messages from self(bot)
        if message.author == self.user:
            return

        # generate hash from user id
        unique_id = generate_unique_id(message.author)

        # write message and hashed id to file
        with open('data.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerows([[unique_id ,message.content]])
            file.close()

# FIXME: Mechanism for sending message after some inactivity

# intents allow bot to subscribe to specific bucket of events
intents = discord.Intents.default() 
# enables app to recieve actual content of newly created messages
intents.message_content = True      


client = Client(intents=intents)
client.run(bot_token)