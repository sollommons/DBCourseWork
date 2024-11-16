from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton

class StudentProfileWindow(QWidget):
    def __init__(self, parent):
        super().__init__()

        self.setWindowTitle('Профиль Студента')
        self.setGeometry(100, 100, 400, 300)

        self.parent_window = parent

        layout = QVBoxLayout()

        self.label = QLabel("Роль: Студент", self)
        self.permissions_label = QLabel(
            "Права:\n- Просмотр списка студентов\n- Просмотр статистики", self
        )

        self.view_students_button = QPushButton('Посмотреть Студентов', self)
        self.statistics_button = QPushButton('Посмотреть Статистику', self)

        self.back_button = QPushButton('Выход', self)
        self.back_button.clicked.connect(self.back_to_profile)

        layout.addWidget(self.label)
        layout.addWidget(self.permissions_label)
        layout.addWidget(self.view_students_button)
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
