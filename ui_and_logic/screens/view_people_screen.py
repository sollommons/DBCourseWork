from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QPushButton


class ViewPeopleWindow(QWidget):
    def __init__(self, parent):
        super().__init__()

        self.setWindowTitle('Студенты и преподаватели')
        self.setGeometry(100, 100, 600, 400)

        self.parent_window = parent  # Ссылка на родительское окно

        layout = QVBoxLayout()

        self.label = QLabel("Просмотр списка студентов и преподаваталей:", self)

        # Пример таблицы статистики
        self.people_table = QTableWidget(self)
        self.people_table.setColumnCount(5)
        self.people_table.setHorizontalHeaderLabels(["Имя", "Фамилия", "Отчество", "Группа","Роль" ])

        layout.addWidget(self.label)
        layout.addWidget(self.people_table)

        self.back_button = QPushButton('Назад', self)
        self.back_button.clicked.connect(self.back_to_profile)

        layout.addWidget(self.back_button)

        self.setLayout(layout)

    def back_to_profile(self):
        """Возврат в профиль преподавателя"""
        self.parent_window.show()  # Показываем окно профиля
        self.close()  # Закрываем текущее окно
