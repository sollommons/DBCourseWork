from PyQt5.QtWidgets import QApplication, QDialog, QLabel
import sys

from logic.data import Role
from logic.login_dialog import LoginDialog


class MainWindow(QDialog):
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

        self.label = QLabel("Введите логин и пароль:", self)
        self.label.move(50, 50)

        self.admin_profile_window = None
        self.teacher_profile_window = None
        self.student_profile_window = None

    def open_admin_profile(self):
        """Открытие профиля администратора"""
        self.label.setText("Вы вышли из приложения!")
        if self.admin_profile_window is None:
            from ui_and_logic.profiles.admin_profile import AdminProfileWindow
            self.admin_profile_window = AdminProfileWindow(self)
        self.close()
        self.admin_profile_window.show()

    def open_student_profile(self):
        """Открытие панели студента"""
        self.label.setText("Вы вышли из приложения!")
        if self.student_profile_window is None:
            from ui_and_logic.profiles.student_profile import StudentProfileWindow
            self.student_profile_window = StudentProfileWindow(self)
        self.close()
        self.student_profile_window.show()

    def open_teacher_profile(self):
        """Открытие панели преподавателя"""
        self.label.setText("Вы вышли из приложения!")
        if self.teacher_profile_window is None:
            from ui_and_logic.profiles.teacher_profile import TeacherProfileWindow
            self.teacher_profile_window = TeacherProfileWindow(self)
        self.close()
        self.teacher_profile_window.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Создание главного окна
    main_window = MainWindow()

    # Логика входа
    role = Role()
    login_dialog = LoginDialog()
    if login_dialog.exec_() == QDialog.Accepted:
        role.set_role(login_dialog.credentials[0])
        role.set_password(login_dialog.credentials[1])

        # Открытие профиля в зависимости от роли
        if login_dialog.credentials[0] == "admin":
            main_window.open_admin_profile()
        elif login_dialog.credentials[0] == "student":
            main_window.open_student_profile()
        elif login_dialog.credentials[0] == "teacher":
            main_window.open_teacher_profile()
        else:
            main_window.label.setText("Неверный логин или пароль")

    sys.exit(app.exec_())
