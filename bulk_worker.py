from PySide6.QtCore import QThread, Signal
import random
import time
from database import add_log



class BulkSender(QThread):

    progress = Signal(str)
    progress_bar = Signal(int)

    def __init__(self, bot, phones, message, attachment=None):

        super().__init__()

        self.bot = bot
        self.phones = phones
        self.message = message
        self.attachment = attachment

    def run(self):

        total = len(self.phones)
        if total == 0:
            self.progress.emit("No contacts selected.")
            self.progress_bar.emit(0)
            return

        for i, phone in enumerate(self.phones):

            try:

                self.bot.open_chat(phone)

                self.bot.send_text(self.message)

                if self.attachment:
                    self.bot.send_file(self.attachment)

                status = "sent"

            except Exception as e:

                status = str(e)

            add_log(phone, self.message, status)

            self.progress.emit(f"{phone} : {status}")

            percent = int((i + 1) / total * 100)

            self.progress_bar.emit(percent)

            time.sleep(random.randint(8, 15))
