from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QFormLayout, QPushButton, QWidget, QLabel, QLineEdit

from logic.auth_logic import AuthLogic
from ui.student_profile import StudentProfileWindow


class AuthWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Авторизация')
        self.setGeometry(100, 100, 300, 150)

        self.label = QLabel('Введите логин и пароль:')
        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText('Логин')

        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText('Пароль')
        self.password_input.setEchoMode(QLineEdit.Password)

        self.login_button = QPushButton('Войти', self)
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

        # Конфигурация подключения к БД
        self.db_config = {
            'dbname': 'university',
            'user': 'postgres',
            'password': 's46825710',
            'host': 'localhost',
            'port': '5432'
        }

        # Инициализируем переменную для окна профиля администратора
        self.admin_profile_window = None
        self.teacher_profile_window = None
        self.student_profile_window = None

    def on_login_click(self):
        username = self.username_input.text()
        password = self.password_input.text()

        # Логика аутентификации
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
        if self.admin_profile_window is None:  # Если окно профиля не открыто
            from ui.admin_profile import AdminProfileWindow
            self.admin_profile_window = AdminProfileWindow(self)  # Передаем ссылку на родительское окно
        self.close()  # Закрываем окно авторизации
        self.admin_profile_window.show()  # Показываем окно профиля

    def open_student_profile(self):
        """Открытие панели студента"""
        if self.student_profile_window is None:
            from ui.student_profile import StudentProfileWindow
            self.student_profile_window = StudentProfileWindow(self)
        self.close()  # Закрываем окно авторизации
        self.student_profile_window.show()



    def open_teacher_profile(self):
        """Открытие панели преподавателя"""
        if self.teacher_profile_window is None:
            from ui.teacher_profile import TeacherProfileWindow
            self.teacher_profile_window = TeacherProfileWindow(self)
        self.close()  # Закрываем окно авторизации
        self.teacher_profile_window.show()
