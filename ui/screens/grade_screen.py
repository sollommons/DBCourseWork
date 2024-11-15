from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel

class AddGradeWindow(QWidget):
    def __init__(self, parent):
        super().__init__()

        self.setWindowTitle('Добавить Оценку')
        self.setGeometry(100, 100, 400, 300)

        self.parent_window = parent  # Ссылка на родительское окно

        layout = QVBoxLayout()

        self.label = QLabel("Введите данные оценки:", self)

        self.student_name_input = QLineEdit(self)
        self.student_name_input.setPlaceholderText('Имя студента')

        self.student_surname_input = QLineEdit(self)
        self.student_surname_input.setPlaceholderText('Фамилия студента')

        self.subject_input = QLineEdit(self)
        self.subject_input.setPlaceholderText('Предмет')

        self.teacher_name_input = QLineEdit(self)
        self.teacher_name_input.setPlaceholderText('Имя преподавателя')

        self.teacher_surname_input = QLineEdit(self)
        self.teacher_surname_input.setPlaceholderText('Фамилия преподавателя')

        self.grade_input = QLineEdit(self)
        self.grade_input.setPlaceholderText('Оценка')

        self.add_button = QPushButton('Добавить', self)

        self.back_button = QPushButton('Назад', self)
        self.back_button.clicked.connect(self.back_to_profile)

        layout.addWidget(self.label)
        layout.addWidget(self.student_name_input)
        layout.addWidget(self.student_surname_input)
        layout.addWidget(self.subject_input)
        layout.addWidget(self.teacher_name_input)
        layout.addWidget(self.teacher_surname_input)
        layout.addWidget(self.grade_input)
        layout.addWidget(self.add_button)
        layout.addWidget(self.back_button)

        self.setLayout(layout)

    def back_to_profile(self):
        """Возврат в профиль преподавателя"""
        self.parent_window.show()  # Показываем окно профиля
        self.close()  # Закрываем текущее окно
