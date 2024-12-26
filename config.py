import os
from dotenv import load_dotenv

# Load enviorment variables
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
INACTIVITY_THRESHOLD = 5 # time in seconds