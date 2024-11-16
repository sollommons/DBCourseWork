from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton

class AdminProfileWindow(QWidget):
    def __init__(self, parent):
        super().__init__()

        self.setWindowTitle('Профиль Администратора')
        self.setGeometry(100, 100, 400, 300)

        self.parent_window = parent

        layout = QVBoxLayout()

        self.label = QLabel("Роль: Администратор", self)
        self.permissions_label = QLabel(
            "Права:\n- Добавление студентов\n- Добавление преподавателей\n- Добавление групп\n- Управление оценками\n- Добавление предметов\n- Просмотр статистики", self
        )

        self.add_student_button = QPushButton('Добавить Студента', self)
        self.add_teacher_button = QPushButton('Добавить Преподавателя', self)
        self.add_group_button = QPushButton('Добавить Группу', self)
        self.add_sub_button = QPushButton('Добавить предмет', self)
        self.add_grade_button = QPushButton('Добавить Оценку', self)
        self.statistics_button = QPushButton('Посмотреть Статистику', self)

        self.back_button = QPushButton('Выход', self)
        self.back_button.clicked.connect(self.back_to_profile)

        layout.addWidget(self.label)
        layout.addWidget(self.permissions_label)
        layout.addWidget(self.add_student_button)
        layout.addWidget(self.add_teacher_button)
        layout.addWidget(self.add_group_button)
        layout.addWidget(self.add_grade_button)
        layout.addWidget(self.add_sub_button)
        layout.addWidget(self.statistics_button)
        layout.addWidget(self.back_button)

        self.setLayout(layout)

        self.add_student_button.clicked.connect(self.open_add_student)
        self.add_teacher_button.clicked.connect(self.open_add_teacher)
        self.add_group_button.clicked.connect(self.open_add_group)
        self.add_grade_button.clicked.connect(self.open_add_grade)
        self.add_sub_button.clicked.connect(self.open_add_sub)
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

    def open_add_teacher(self):
        """Открытие окна добавления преподавателя"""
        from ui.screens.teacher_screen import AddTeacherWindow
        self.add_teacher_window = AddTeacherWindow(self)
        self.add_teacher_window.show()
        self.close()

    def open_add_group(self):
        """Открытие окна добавления группы"""
        from ui.screens.group_screen import AddGroupWindow
        self.add_group_window = AddGroupWindow(self)
        self.add_group_window.show()
        self.close()

    def open_add_sub(self):
        """Открытие окна добавления оценки"""
        from ui.screens.subject_screen import AddSubWindow
        self.add_sub_window = AddSubWindow(self)
        self.add_sub_window.show()
        self.close()

    def open_add_grade(self):
        """Открытие окна добавления оценки"""
        from ui.screens.grade_screen import AddGradeWindow
        self.add_grade_window = AddGradeWindow(self)
        self.add_grade_window.show()
        self.close()

    def open_statistics(self):
        """Открытие окна статистики"""
        from ui.screens.statistic_screen import StatisticsWindow
        self.statistics_window = StatisticsWindow(self)
        self.statistics_window.show()
        self.close()
