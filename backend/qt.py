import sys
from PySide6.QtWidgets import QApplication
from src.qt.windows import LoginWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow(app=app, host="http://localhost:8000")
    window.show()
    sys.exit(app.exec())
