import os
import sys

# detect exe or script
if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

APP_DIR = os.path.join(BASE_DIR, "wbsstool")

SESSION_DIR = os.path.join(APP_DIR, "session")
LOG_DIR = os.path.join(APP_DIR, "logs")
DB_PATH = os.path.join(APP_DIR, "database.db")

# create folders if missing
os.makedirs(SESSION_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)