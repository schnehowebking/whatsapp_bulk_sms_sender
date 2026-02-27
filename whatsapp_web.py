from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import urllib.parse


class WhatsAppWeb:

    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--window-size=420,620")
        chrome_options.add_argument("--disable-notifications")

        # 🔥 REMOVE webdriver-manager
        self.driver = webdriver.Chrome(options=chrome_options)

    def start_session(self):
        self.driver.get("https://web.whatsapp.com/")
        print("Scan QR Code...")

        while True:
            try:
                self.driver.find_element("id", "pane-side")
                break
            except:
                time.sleep(2)

        print("Connected!")

    def send_message(self, phone, message):
        try:
            encoded = urllib.parse.quote(message)
            url = f"https://web.whatsapp.com/send?phone={phone}&text={encoded}"
            self.driver.get(url)

            time.sleep(6)

            send_btn = self.driver.find_element(
                "xpath", '//span[@data-icon="send"]'
            )
            send_btn.click()

            return "sent"

        except Exception as e:
            return f"failed: {str(e)}"