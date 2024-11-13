from PyQt5.QtWidgets import QApplication
import sys
from ui.auth_window import AuthWindow

def main():
    app = QApplication(sys.argv)
    auth_window = AuthWindow()  # Создаем окно авторизации
    auth_window.show()  # Показываем окно авторизации
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
