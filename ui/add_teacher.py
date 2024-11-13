from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton

class AddTeacherWindow(QWidget):
    def __init__(self, parent):
        super().__init__()

        self.setWindowTitle('Добавить Преподавателя')
        self.setGeometry(100, 100, 400, 300)

        self.parent_window = parent  # Сохраняем ссылку на родительское окно (профиль администратора)

        layout = QVBoxLayout()

        # Поля для ввода данных преподавателя
        self.first_name_input = QLineEdit(self)
        self.first_name_input.setPlaceholderText('Имя')

        self.last_name_input = QLineEdit(self)
        self.last_name_input.setPlaceholderText('Фамилия')

        self.father_name_input = QLineEdit(self)
        self.father_name_input.setPlaceholderText('Отчество')

        self.role_input = QLineEdit(self)
        self.role_input.setPlaceholderText('Роль')

        # Кнопка добавления преподавателя
        self.add_button = QPushButton('Добавить', self)

        # Кнопка назад
        self.back_button = QPushButton('Назад', self)
        self.back_button.clicked.connect(self.back_to_profile)

        # Добавляем все элементы в layout
        layout.addWidget(self.first_name_input)
        layout.addWidget(self.last_name_input)
        layout.addWidget(self.father_name_input)
        layout.addWidget(self.role_input)
        layout.addWidget(self.add_button)
        layout.addWidget(self.back_button)

        self.setLayout(layout)

    def back_to_profile(self):
        """Возврат в профиль администратора"""
        self.parent_window.show()  # Показываем родительское окно (профиль администратора)
        self.close()  # Закрываем текущее окно
