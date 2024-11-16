from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QApplication


class StudentProfileWindow(QWidget):
    def __init__(self, parent):
        super().__init__()

        self.setWindowTitle('Профиль Студента')
        self.setFixedSize(QApplication.primaryScreen().size().width(),QApplication.primaryScreen().size().height()-100)

        self.parent_window = parent

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

        layout = QVBoxLayout()

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

        self.label = QLabel("Роль: Студент", self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("font-size: 20px; font-weight: bold; color: #333; padding: 10px;")
        self.permissions_label = QLabel(
            "Что может студент:\n"
            "- Посмотреть список студентов и преподавателей\n"
            "- Посмотреть статистику по периодам (подробнее внутри)",
            self
        )
        self.permissions_label.setAlignment(Qt.AlignCenter)
        self.permissions_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #333; padding: 10px;")

        self.view_students_button = QPushButton('Экран списка студентов', self)
        self.view_students_button.setStyleSheet(button_style)

        self.view_teacher_button = QPushButton('Экран списка преподавателей', self)
        self.view_teacher_button.setStyleSheet(button_style)

        self.statistics_button = QPushButton('Экран статистики', self)
        self.statistics_button.setStyleSheet(button_style)


        self.back_button = QPushButton('Выход', self)
        self.back_button.setStyleSheet("background-color: #f44336; color: white; font-size: 14px; padding: 10px; border-radius: 5px;")
        self.back_button.clicked.connect(self.back_to_profile)

        layout.addWidget(self.label)
        layout.addWidget(self.permissions_label)
        layout.addWidget(self.view_students_button)
        layout.addWidget(self.view_teacher_button)
        layout.addWidget(self.statistics_button)
        layout.addWidget(self.back_button)

        self.setLayout(layout)

        self.view_students_button.clicked.connect(self.open_view_students)
        self.statistics_button.clicked.connect(self.open_statistics)

    def back_to_profile(self):
        """Возврат в профиль """
        self.parent_window.show()
        self.close()


    def open_view_students(self):
        """Открытие окна для просмотра списка студентов"""
        from ui.screens.view_students_screen import ViewStudentsWindow
        self.view_students_window = ViewStudentsWindow(self)  # Передаем родительское окно
        self.view_students_window.show()
        self.close()  # Закрываем текущее окно

    def open_statistics(self):
        """Открытие окна статистики"""
        from ui.screens.statistic_screen import StatisticsWindow
        self.statistics_window = StatisticsWindow(self)  # Передаем родительское окно
        self.statistics_window.show()
        self.close()  # Закрываем текущее окно
