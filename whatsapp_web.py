from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import os
import time
from config import SESSION_DIR


def normalize_phone(phone):

    phone = str(phone)

    if phone.startswith("880"):
        phone = phone[3:]

    if phone.startswith("0"):
        phone = phone[1:]

    return "880" + phone


class WhatsAppWeb:

    def __init__(self):

        options = Options()
        options.add_argument(f"--user-data-dir={SESSION_DIR}")

        self.options = options
        self.driver = None

    def _ensure_driver(self):
        if self.driver is None:
            self.driver = webdriver.Chrome(options=self.options)

    def stop(self):
        if self.driver is not None:
            self.driver.quit()
            self.driver = None

    def _wait_for_any_clickable(self, timeout, xpaths):
        wait = WebDriverWait(self.driver, timeout)
        for xpath in xpaths:
            try:
                return wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
            except TimeoutException:
                continue
        raise TimeoutException("Could not find a clickable element with known selectors.")

    def _wait_for_compose_box(self, timeout=30):
        wait = WebDriverWait(self.driver, timeout)
        xpaths = [
            '//footer//div[@contenteditable="true"]',
            '//div[@contenteditable="true"][@role="textbox"]',
            '//div[@contenteditable="true"][@data-tab]',
        ]
        for xpath in xpaths:
            try:
                return wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
            except TimeoutException:
                continue
        raise TimeoutException("Could not find message compose box.")

    def start(self):
        self._ensure_driver()

        self.driver.get("https://web.whatsapp.com")

        print("Scan QR if needed")

        wait = WebDriverWait(self.driver, 60)

        wait.until(
            EC.presence_of_element_located(
                (By.ID, "pane-side")
            )
        )

    def open_chat(self, phone):
        self._ensure_driver()

        phone = normalize_phone(phone)

        url = f"https://web.whatsapp.com/send?phone={phone}"

        self.driver.get(url)

        self._wait_for_compose_box(timeout=30)

    def send_text(self, message):
        self._ensure_driver()

        box = self._wait_for_compose_box(timeout=30)

        box.click()
        box.send_keys(message)

        send_btn = self._wait_for_any_clickable(30, [
            '//button[@aria-label="Send"]',
            '//span[@data-icon="send"]/ancestor::button[1]',
        ])

        send_btn.click()

    def send_file(self, file):
        self._ensure_driver()
        if not os.path.isfile(file):
            raise FileNotFoundError(f"Attachment file not found: {file}")

        attach = self._wait_for_any_clickable(20, [
            '//button[@title="Attach"]',
            '//span[@data-icon="clip"]/ancestor::button[1]',
        ])

        attach.click()

        wait = WebDriverWait(self.driver, 20)
        file_input = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, '//input[@type="file"]')
            )
        )

        file_input.send_keys(file)

        time.sleep(3)

        send_btn = self._wait_for_any_clickable(30, [
            '//button[@aria-label="Send"]',
            '//span[@data-icon="send"]/ancestor::button[1]',
        ])

        send_btn.click()
