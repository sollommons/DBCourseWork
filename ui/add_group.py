from PyQt5.QtWidgets import QPushButton, QLineEdit, QLabel, QVBoxLayout, QWidget


class AddGroupWindow(QWidget):
    def __init__(self, parent):
        super().__init__()

        self.setWindowTitle('Добавить Группу')
        self.setGeometry(100, 100, 400, 300)

        self.parent_window = parent  # Ссылка на родительское окно

        layout = QVBoxLayout()

        self.label = QLabel("Введите данные группы:", self)

        self.group_name_input = QLineEdit(self)
        self.group_name_input.setPlaceholderText('Название группы')

        self.add_button = QPushButton('Добавить', self)

        self.back_button = QPushButton('Назад', self)
        self.back_button.clicked.connect(self.back_to_profile)

        layout.addWidget(self.label)
        layout.addWidget(self.group_name_input)
        layout.addWidget(self.add_button)
        layout.addWidget(self.back_button)

        self.setLayout(layout)

    def back_to_profile(self):
        """Возврат в профиль администратора"""
        self.parent_window.show()  # Показываем окно профиля
        self.close()  # Закрываем текущее окно
