import sys
from PySide6.QtWidgets import QApplication
from ui_main import MainWindow, apply_dark_theme

app = QApplication(sys.argv)
apply_dark_theme(app)

window = MainWindow()
window.show()

sys.exit(app.exec())