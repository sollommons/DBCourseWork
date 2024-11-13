from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel

class AddStudentWindow(QWidget):
    def __init__(self, parent):
        super().__init__()

        self.setWindowTitle('Добавить Студента')
        self.setGeometry(100, 100, 400, 300)

        self.parent_window = parent  # Ссылка на родительское окно

        layout = QVBoxLayout()

        self.label = QLabel("Введите данные студента:", self)

        self.first_name_input = QLineEdit(self)
        self.first_name_input.setPlaceholderText('Имя')

        self.last_name_input = QLineEdit(self)
        self.last_name_input.setPlaceholderText('Фамилия')

        self.group_input = QLineEdit(self)
        self.group_input.setPlaceholderText('Группа')

        self.add_button = QPushButton('Добавить', self)

        self.back_button = QPushButton('Назад', self)
        self.back_button.clicked.connect(self.back_to_profile)

        layout.addWidget(self.label)
        layout.addWidget(self.first_name_input)
        layout.addWidget(self.last_name_input)
        layout.addWidget(self.group_input)
        layout.addWidget(self.add_button)
        layout.addWidget(self.back_button)

        self.setLayout(layout)

    def back_to_profile(self):
        """Возврат в профиль преподавателя"""
        self.parent_window.show()  # Показываем окно профиля
        self.close()  # Закрываем текущее окно
