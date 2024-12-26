import os
from dotenv import load_dotenv

# Load enviorment variables
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
SHEET_ID = os.getenv("SHEETS_TOKEN")
WORKSHEET_NAME = os.getenv("WORKSHEET_NAME")
INACTIVITY_THRESHOLD = 3600 # time in seconds (1 hr)
INACTIVITY_LOOP_TIME = 60   # time in seconds (1 min)