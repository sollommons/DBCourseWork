from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QFormLayout, QPushButton, QWidget, QLabel, QLineEdit, QApplication

from logic.auth_logic import AuthLogic


class AuthWindow(QWidget):
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

        self.label = QLabel('Введите логин и пароль:')
        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText('Логин')

        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText('Пароль')
        self.password_input.setEchoMode(QLineEdit.Password)

        self.login_button = QPushButton('Войти', self)
        self.login_button.setStyleSheet(button_style)
        self.login_button.clicked.connect(self.on_login_click)

        layout = QFormLayout()
        layout.addRow('Логин:', self.username_input)
        layout.addRow('Пароль:', self.password_input)

        button_layout = QHBoxLayout()
        button_layout.addStretch(1)
        button_layout.addWidget(self.login_button)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.label)
        main_layout.addLayout(layout)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

        self.db_config = {
            'dbname': 'university',
            'user': 'postgres',
            'password': 's46825710',
            'host': 'localhost',
            'port': '5432'
        }

        self.admin_profile_window = None
        self.teacher_profile_window = None
        self.student_profile_window = None

    def on_login_click(self):
        username = self.username_input.text()
        password = self.password_input.text()

        auth = AuthLogic(self.db_config)
        is_authenticated, role = auth.authenticate(username, password)

        if is_authenticated:
            self.label.setText(f"Успешная авторизация. Роль: {role}")
            self.username_input.clear()
            self.password_input.clear()

            if role == "admin":
                self.open_admin_profile()
            elif role == "student":
                self.open_student_profile()
            elif role == "teacher":
                self.open_teacher_profile()
        else:
            self.label.setText("Неверный логин или пароль")

    def open_admin_profile(self):
        """Открытие профиля администратора"""
        self.label.setText("Введите логин и пароль:")
        if self.admin_profile_window is None:
            from ui_and_logic.profiles.admin_profile import AdminProfileWindow
            self.admin_profile_window = AdminProfileWindow(self)
        self.close()
        self.admin_profile_window.show()

    def open_student_profile(self):
        """Открытие панели студента"""
        self.label.setText("Введите логин и пароль:")
        if self.student_profile_window is None:
            from ui_and_logic.profiles.student_profile import StudentProfileWindow
            self.student_profile_window = StudentProfileWindow(self)
        self.close()
        self.student_profile_window.show()

    def open_teacher_profile(self):
        """Открытие панели преподавателя"""
        self.label.setText("Введите логин и пароль:")
        if self.teacher_profile_window is None:
            from ui_and_logic.profiles.teacher_profile import TeacherProfileWindow
            self.teacher_profile_window = TeacherProfileWindow(self)
        self.close()
        self.teacher_profile_window.show()
