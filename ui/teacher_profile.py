from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton

class TeacherProfileWindow(QWidget):
    def __init__(self, parent):
        super().__init__()

        self.setWindowTitle('Профиль Преподавателя')
        self.setGeometry(100, 100, 400, 300)

        self.parent_window = parent  # Ссылка на родительское окно

        layout = QVBoxLayout()

        self.label = QLabel("Роль: Преподаватель", self)
        self.permissions_label = QLabel(
            "Права:\n- Добавление студентов\n- Добавление оценок\n- Просмотр списка студентов\n- Просмотр статистики", self
        )

        # Кнопки для перехода в другие окна
        self.add_student_button = QPushButton('Добавить Студента', self)
        self.add_grade_button = QPushButton('Добавить Оценку', self)
        self.view_students_button = QPushButton('Посмотреть Студентов', self)
        self.statistics_button = QPushButton('Посмотреть Статистику', self)

        # Кнопка "Назад"
        self.back_button = QPushButton('Назад', self)
        self.back_button.clicked.connect(self.back_to_profile)

        layout.addWidget(self.label)
        layout.addWidget(self.permissions_label)
        layout.addWidget(self.add_student_button)
        layout.addWidget(self.add_grade_button)
        layout.addWidget(self.view_students_button)
        layout.addWidget(self.statistics_button)
        layout.addWidget(self.back_button)

        self.setLayout(layout)

        # Обработчики кнопок
        self.add_student_button.clicked.connect(self.open_add_student)
        self.add_grade_button.clicked.connect(self.open_add_grade)
        self.view_students_button.clicked.connect(self.open_view_students)
        self.statistics_button.clicked.connect(self.open_statistics)

    def back_to_profile(self):
        """Возврат в профиль преподавателя"""
        self.parent_window.show()  # Показываем родительское окно (профиль преподавателя)
        self.close()  # Закрываем текущее окно

    def open_add_student(self):
        """Открытие окна добавления студента"""
        from ui.add_student import AddStudentWindow
        self.add_student_window = AddStudentWindow(self)  # Передаем родительское окно
        self.add_student_window.show()
        self.close()  # Закрываем текущее окно

    def open_add_grade(self):
        """Открытие окна добавления оценки"""
        from ui.add_grade import AddGradeWindow
        self.add_grade_window = AddGradeWindow(self)  # Передаем родительское окно
        self.add_grade_window.show()
        self.close()  # Закрываем текущее окно

    def open_view_students(self):
        """Открытие окна для просмотра списка студентов"""
        from ui.view_students import ViewStudentsWindow
        self.view_students_window = ViewStudentsWindow(self)  # Передаем родительское окно
        self.view_students_window.show()
        self.close()  # Закрываем текущее окно

    def open_statistics(self):
        """Открытие окна статистики"""
        from ui.statistics import StatisticsWindow
        self.statistics_window = StatisticsWindow(self)  # Передаем родительское окно
        self.statistics_window.show()
        self.close()  # Закрываем текущее окно
