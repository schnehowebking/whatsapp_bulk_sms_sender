import os

from PySide6.QtWidgets import *
from PySide6.QtCore import Qt, QThread, Signal

from database import add_contact, get_contacts, get_logs, init_db
from contact_manager import load_contacts_file
from bulk_worker import BulkSender
from whatsapp_web import WhatsAppWeb

import pandas as pd


class ImportPreview(QDialog):

    def __init__(self, df):

        super().__init__()

        self.setWindowTitle("Preview Contacts")

        layout = QVBoxLayout()

        table = QTableWidget()

        table.setColumnCount(3)

        table.setHorizontalHeaderLabels(["Name", "Phone", "Valid"])

        table.setRowCount(len(df))

        for i, row in df.iterrows():

            table.setItem(i, 0, QTableWidgetItem(str(row["name"])))
            table.setItem(i, 1, QTableWidgetItem(str(row["phone"])))

            valid = "YES" if row["valid"] else "INVALID"

            item = QTableWidgetItem(valid)

            if not row["valid"]:
                item.setBackground(Qt.red)

            table.setItem(i, 2, item)

        btn = QPushButton("Import Valid Contacts")

        btn.clicked.connect(self.accept)

        layout.addWidget(table)
        layout.addWidget(btn)

        self.setLayout(layout)


class ConnectWhatsAppWorker(QThread):

    connected = Signal(object)
    failed = Signal(str)

    def run(self):
        bot = None
        try:
            bot = WhatsAppWeb()
            bot.start()
            self.connected.emit(bot)
        except Exception as exc:
            if bot is not None:
                bot.stop()
            self.failed.emit(str(exc))


class MainWindow(QMainWindow):

    def __init__(self):

        super().__init__()

        self.setWindowTitle("WhatsApp Sender")

        init_db()

        self.bot = None
        self.connect_worker = None
        self.worker = None

        self.attachment = None

        self.progress = QProgressBar()

        self.contacts = QListWidget()

        self.contacts.setSelectionMode(QAbstractItemView.MultiSelection)

        self.message = QTextEdit()

        self.logs = QTextEdit()
        self.logs.setReadOnly(True)

        self.connect_btn = QPushButton("Connect WhatsApp")

        self.import_btn = QPushButton("Import Contacts")

        self.send_btn = QPushButton("Send")

        self.attach_btn = QPushButton("Attach File")

        self.export_btn = QPushButton("Export Logs")

        left = QVBoxLayout()

        right = QVBoxLayout()

        left.addWidget(self.connect_btn)

        left.addWidget(self.import_btn)

        left.addWidget(self.contacts)

        right.addWidget(self.message)

        right.addWidget(self.attach_btn)

        right.addWidget(self.send_btn)

        right.addWidget(self.progress)

        right.addWidget(self.export_btn)

        right.addWidget(self.logs)

        layout = QHBoxLayout()

        layout.addLayout(left)

        layout.addLayout(right)

        container = QWidget()

        container.setLayout(layout)

        self.setCentralWidget(container)

        self.connect_btn.clicked.connect(self.connect_whatsapp)

        self.import_btn.clicked.connect(self.import_contacts)

        self.send_btn.clicked.connect(self.send_messages)

        self.attach_btn.clicked.connect(self.attach_file)

        self.export_btn.clicked.connect(self.export_logs)

    def connect_whatsapp(self):
        if self.connect_worker is not None and self.connect_worker.isRunning():
            return

        self.connect_btn.setEnabled(False)
        self.logs.append("Connecting to WhatsApp Web...")

        self.connect_worker = ConnectWhatsAppWorker()
        self.connect_worker.connected.connect(self.on_whatsapp_connected)
        self.connect_worker.failed.connect(self.on_whatsapp_connect_failed)
        self.connect_worker.finished.connect(lambda: self.connect_btn.setEnabled(True))
        self.connect_worker.start()

    def on_whatsapp_connected(self, bot):
        self.bot = bot
        self.logs.append("Connected to WhatsApp Web.")
        self.load_contacts()

    def on_whatsapp_connect_failed(self, error):
        QMessageBox.critical(
            self,
            "Connection Error",
            f"Failed to connect WhatsApp Web:\n{error}"
        )
        self.logs.append(f"Connect failed: {error}")

    def import_contacts(self):

        file, _ = QFileDialog.getOpenFileName(
            self,
            "Select file",
            "",
            "Contacts (*.csv *.xls *.xlsx)"
        )

        if not file:
            return

        try:
            df = load_contacts_file(file)
        except Exception as exc:
            QMessageBox.warning(self, "Import Error", str(exc))
            return

        preview = ImportPreview(df)

        if preview.exec():

            for _, row in df.iterrows():

                if row["valid"]:

                    add_contact(row["name"], row["phone"])

        self.load_contacts()

    def load_contacts(self):

        self.contacts.clear()

        for _, name, phone in get_contacts():
            item = QListWidgetItem(f"{name} - {phone}")
            item.setData(Qt.UserRole, phone)
            self.contacts.addItem(item)

    def attach_file(self):

        file, _ = QFileDialog.getOpenFileName(self, "Select file")

        if file:
            self.attachment = file
            self.logs.append(f"Attachment selected: {file}")

    def send_messages(self):
        if self.bot is None:
            QMessageBox.warning(self, "Not Connected", "Connect WhatsApp first.")
            return

        items = self.contacts.selectedItems()
        if not items:
            QMessageBox.warning(self, "No Contacts", "Select at least one contact.")
            return

        phones = []

        for item in items:
            phone = item.data(Qt.UserRole)
            if not phone:
                text = item.text()
                if " - " in text:
                    phone = text.rsplit(" - ", 1)[1].strip()

            if phone:
                phones.append(phone)

        if not phones:
            QMessageBox.warning(self, "No Valid Contacts", "No valid phone selected.")
            return

        message = self.message.toPlainText().strip()
        if not message and not self.attachment:
            QMessageBox.warning(
                self,
                "Nothing To Send",
                "Write a message or select an attachment."
            )
            return

        if self.attachment and not os.path.isfile(self.attachment):
            QMessageBox.warning(
                self,
                "Attachment Missing",
                f"Attachment file not found:\n{self.attachment}"
            )
            return

        self.worker = BulkSender(self.bot, phones, message, self.attachment)

        self.worker.progress.connect(self.logs.append)

        self.worker.progress_bar.connect(self.progress.setValue)
        self.worker.finished.connect(lambda: self.send_btn.setEnabled(True))
        self.send_btn.setEnabled(False)
        self.progress.setValue(0)

        self.worker.start()

    def export_logs(self):

        file, _ = QFileDialog.getSaveFileName(
            self,
            "Save Logs",
            "",
            "CSV Files (*.csv)"
        )

        if not file:
            return

        logs = get_logs()

        df = pd.DataFrame(logs, columns=["Phone", "Message", "Status"])

        df.to_csv(file, index=False)

    def closeEvent(self, event):
        if self.worker is not None and self.worker.isRunning():
            self.worker.wait(2000)

        if self.connect_worker is not None and self.connect_worker.isRunning():
            self.connect_worker.wait(2000)

        if self.bot is not None:
            self.bot.stop()

        super().closeEvent(event)
