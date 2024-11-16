from PyQt5.QtWidgets import QApplication
import sys
from ui_and_logic.screens.auth_screen import AuthWindow

def main():
    app = QApplication(sys.argv)
    auth_window = AuthWindow()
    auth_window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
