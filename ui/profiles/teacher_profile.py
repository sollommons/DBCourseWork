from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton

class TeacherProfileWindow(QWidget):
    def __init__(self, parent):
        super().__init__()

        self.setWindowTitle('Профиль Преподавателя')
        self.setGeometry(100, 100, 400, 300)

        self.parent_window = parent

        layout = QVBoxLayout()

        self.label = QLabel("Роль: Преподаватель", self)
        self.permissions_label = QLabel(
            "Права:\n- Добавление студентов\n- Добавление оценок\n- Просмотр списка людей\n- Просмотр статистики", self
        )

        self.add_student_button = QPushButton('Добавить Студента', self)
        self.add_grade_button = QPushButton('Добавить Оценку', self)
        self.view_people_button = QPushButton('Посмотреть Студентов и Преподаваталей', self)
        self.statistics_button = QPushButton('Посмотреть Статистику', self)

        self.back_button = QPushButton('Выход', self)
        self.back_button.clicked.connect(self.back_to_profile)

        layout.addWidget(self.label)
        layout.addWidget(self.permissions_label)
        layout.addWidget(self.add_student_button)
        layout.addWidget(self.add_grade_button)
        layout.addWidget(self.view_people_button)
        layout.addWidget(self.statistics_button)
        layout.addWidget(self.back_button)

        self.setLayout(layout)

        self.add_student_button.clicked.connect(self.open_add_student)
        self.add_grade_button.clicked.connect(self.open_add_grade)
        self.view_people_button.clicked.connect(self.open_people)
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
        from ui.view_people import ViewPeopleWindow
        self.view_people = ViewPeopleWindow(self)
        self.view_people.show()
        self.close()

    def open_statistics(self):
        """Открытие окна статистики"""
        from ui.statistics import StatisticsWindow
        self.statistics_window = StatisticsWindow(self)
        self.statistics_window.show()
        self.close()