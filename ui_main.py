from PySide6.QtWidgets import *
from database import *
from contact_manager import import_csv
from bulk_worker import BulkSender
from whatsapp_web import WhatsAppWeb


def apply_dark_theme(app):
    app.setStyleSheet("""
        QWidget { background-color: #ffffff; color: black; }
        QPushButton { background-color: #ffffff; padding:8px; border-radius:5px; }
        QPushButton:hover { background-color: #ffffff; }
        QTextEdit, QListWidget {
            background-color:#ffffff;
            border:1px solid #444;
        }
    """)


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("WhatsApp Desktop Tool")
        self.setGeometry(200,200,900,600)

        init_db()

        self.bot = WhatsAppWeb()

        self.status_label = QLabel("Status: Not Connected")
        self.connect_btn = QPushButton("Connect WhatsApp")
        self.connect_btn.clicked.connect(self.connect_whatsapp)

        self.import_btn = QPushButton("Import CSV")
        self.import_btn.setEnabled(False)

        self.send_btn = QPushButton("Send Selected")
        self.send_btn.setEnabled(False)

        self.contact_list = QListWidget()
        self.message_box = QTextEdit()
        self.log_view = QTextEdit()

        self.import_btn.clicked.connect(self.import_contacts)
        self.send_btn.clicked.connect(self.send_selected)

        layout = QVBoxLayout()
        layout.addWidget(self.status_label)
        layout.addWidget(self.connect_btn)
        layout.addWidget(self.contact_list)
        layout.addWidget(self.import_btn)
        layout.addWidget(QLabel("Message"))
        layout.addWidget(self.message_box)
        layout.addWidget(self.send_btn)
        layout.addWidget(self.log_view)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def connect_whatsapp(self):
        self.bot.start_session()
        self.status_label.setText("Status: Connected")
        self.import_btn.setEnabled(True)
        self.send_btn.setEnabled(True)

    def import_contacts(self):
        file,_ = QFileDialog.getOpenFileName(self,"Select CSV","","CSV Files (*.csv)")
        if file:
            import_csv(file)
            self.load_contacts()

    def load_contacts(self):
        self.contact_list.clear()
        for id,name,phone in get_contacts():
            self.contact_list.addItem(f"{name} - {phone}")

    def send_selected(self):
        selected = self.contact_list.currentItem()
        if not selected:
            QMessageBox.warning(self, "Warning", "Select a contact first")
            return

        phone = selected.text().split("-")[1].strip()
        message = self.message_box.toPlainText()

        self.worker = BulkSender(self.bot, [phone], message)
        self.worker.progress.connect(self.log_view.append)
        self.worker.start()