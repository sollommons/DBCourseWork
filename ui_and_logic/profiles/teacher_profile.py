from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QApplication


class TeacherProfileWindow(QWidget):
    def __init__(self, parent):
        super().__init__()

        self.setWindowTitle('Профиль Преподавателя')
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

        self.label = QLabel("Роль: Преподаватель", self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("font-size: 20px; font-weight: bold; color: #333; padding: 10px;")
        self.permissions_label = QLabel(
            "Что может преподаватель:\n"
            "- Добавлять, удалять, редактировать студентов, а также просмотреть их полный список\n"
            "- Посмотреть список преподавателей\n"
            "- Добавлять, удалять, редактировать оценк, а также посмотреть их полнгый список\n"
            "- Посмотреть статистику по периодам (подробнее внутри)",
            self
        )
        self.permissions_label.setAlignment(Qt.AlignCenter)
        self.permissions_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #333; padding: 10px;")

        self.add_student_button = QPushButton('Экран студента', self)
        self.add_student_button.setStyleSheet(button_style)

        self.add_grade_button = QPushButton('Экран оценки', self)
        self.add_grade_button.setStyleSheet(button_style)

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
        layout.addWidget(self.add_student_button)
        layout.addWidget(self.add_grade_button)
        layout.addWidget(self.view_students_button)
        layout.addWidget(self.view_teacher_button)
        layout.addWidget(self.statistics_button)
        layout.addWidget(self.back_button)

        self.setLayout(layout)

        self.add_student_button.clicked.connect(self.open_add_student)
        self.add_grade_button.clicked.connect(self.open_add_grade)
        self.view_students_button.clicked.connect(self.open_people)
        self.statistics_button.clicked.connect(self.open_statistics)

    def back_to_profile(self):
        """Возврат в профиль """
        self.parent_window.show()
        self.close()

    def open_add_student(self):
        """Открытие окна добавления студента"""
        from ui.screens.student_screen import AddStudentWindow
        self.add_student_window = AddStudentWindow(self)
        self.add_student_window.show()
        self.close()

    def open_add_grade(self):
        """Открытие окна добавления оценки"""
        from ui.screens.grade_screen import AddGradeWindow
        self.add_grade_window = AddGradeWindow(self)
        self.add_grade_window.show()
        self.close()

    def open_people(self):
        """Открытие окна добавления студента"""
        from ui.screens.view_people_screen import ViewPeopleWindow
        self.view_people = ViewPeopleWindow(self)
        self.view_people.show()
        self.close()

    def open_statistics(self):
        """Открытие окна статистики"""
        from ui.screens.statistic_screen import StatisticsWindow
        self.statistics_window = StatisticsWindow(self)
        self.statistics_window.show()
        self.close()
