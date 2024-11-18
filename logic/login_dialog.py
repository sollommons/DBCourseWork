from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
import psycopg2

class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Авторизация')
        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()

        window_width = 300
        window_height = 150
        center_x = (screen_geometry.width() - window_width) // 2
        center_y = (screen_geometry.height() - window_height) // 2

        self.setGeometry(center_x, center_y, window_width, window_height)

        self.setStyleSheet("""
                             QWidget {
                                 background-color: #e0f7e7;  /* Бледно-зеленый цвет для фона всего окна */
                             }
                             QLabel {
                                 color: #333;  /* Темный цвет для текста */
                             }
                             QLineEdit {
                                 background-color: #ffffff;  /* Белый фон для полей ввода */
                                 border-radius: 5px;
                                 border: 1px solid #ccc;
                                 padding: 8px;
                             }
                             QPushButton {
                                 background-color: #66bb6a;  /* Зеленый фон для кнопок */
                                 color: white;
                                 font-size: 14px;
                                 padding: 10px;
                                 border-radius: 5px;
                                 border: none;
                             }
                             QPushButton:hover {
                                 background-color: #5cb85c;  /* При наведении кнопки темнеют */
                             }
                             QPushButton:pressed {
                                 background-color: #4cae4c;  /* При нажатии кнопки */
                             }
                             QTableWidget {
                                 background-color: #ffffff;  /* Белый фон для таблицы */
                                 border: 1px solid #ddd;  /* Светлый бордер для таблицы */
                             }
                         """)


        button_style = """
                               QPushButton {
                                   background-color: #4CAF50;
                                   color: white;
                                   font-size: 14px;
                                   padding: 10px;
                                   border-radius: 5px;
                                   border: none;
                               }
                               QPushButton:hover {
                                   background-color: #45a049;
                               }
                               """

        layout = QVBoxLayout()

        self.label_login = QLabel("Логин:")
        self.input_login = QLineEdit()

        self.label_password = QLabel("Пароль:")
        self.input_password = QLineEdit()
        self.input_password.setEchoMode(QLineEdit.Password)

        self.button_login = QPushButton("Войти")
        self.button_login.clicked.connect(self.on_login)
        self.button_login.setStyleSheet(button_style)

        layout.addWidget(self.label_login)
        layout.addWidget(self.input_login)
        layout.addWidget(self.label_password)
        layout.addWidget(self.input_password)
        layout.addWidget(self.button_login)

        self.setLayout(layout)

        self.credentials = None

    def on_login(self):
        login = self.input_login.text()
        password = self.input_password.text()
        try:
            connection = psycopg2.connect(
                dbname='university',
                user=login,
                password=self.input_password.text(),
                host='localhost',
                port='5432'
            )
            cursor = connection.cursor()

            cursor.close()
            connection.close()
            self.credentials = (login, password)
            self.accept()

        except Exception as error:
            print("Неверный логин или пароль", error)
            self.message_wrong = QMessageBox(QMessageBox.Warning, "Ошибка", "Неверный логин или пароль")
            self.message_wrong.exec_()
