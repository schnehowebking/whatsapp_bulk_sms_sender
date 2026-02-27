from PySide6.QtCore import QThread, Signal
from database import add_log
import random
import time

class BulkSender(QThread):
    progress = Signal(str)

    def __init__(self, bot, contacts, message):
        super().__init__()
        self.bot = bot
        self.contacts = contacts
        self.message = message

    def run(self):
        for phone in self.contacts:
            status = self.bot.send_message(phone, self.message)
            add_log(phone, self.message, status)

            self.progress.emit(f"{phone}: {status}")

            time.sleep(random.randint(8, 15))