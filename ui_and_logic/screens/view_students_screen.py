from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QPushButton


class ViewStudentsWindow(QWidget):
    def __init__(self, parent):
        super().__init__()

        self.setWindowTitle('Список Студентов')
        self.setGeometry(100, 100, 600, 400)

        self.parent_window = parent  # Ссылка на родительское окно

        layout = QVBoxLayout()

        self.label = QLabel("Список студентов:", self)

        # Пример таблицы студентов
        self.students_table = QTableWidget(self)
        self.students_table.setColumnCount(3)
        self.students_table.setHorizontalHeaderLabels(["Имя", "Фамилия", "Группа"])

        # Пример данных
        self.students_table.setRowCount(3)
        self.students_table.setItem(0, 0, QTableWidgetItem("Иван"))
        self.students_table.setItem(0, 1, QTableWidgetItem("Иванов"))
        self.students_table.setItem(0, 2, QTableWidgetItem("Группа 1"))

        self.students_table.setItem(1, 0, QTableWidgetItem("Петр"))
        self.students_table.setItem(1, 1, QTableWidgetItem("Петров"))
        self.students_table.setItem(1, 2, QTableWidgetItem("Группа 2"))

        self.students_table.setItem(2, 0, QTableWidgetItem("Света"))
        self.students_table.setItem(2, 1, QTableWidgetItem("Светлова"))
        self.students_table.setItem(2, 2, QTableWidgetItem("Группа 3"))

        self.back_button = QPushButton('Назад', self)
        self.back_button.clicked.connect(self.back_to_profile)

        layout.addWidget(self.label)
        layout.addWidget(self.students_table)
        layout.addWidget(self.back_button)

        self.setLayout(layout)

    def back_to_profile(self):
        """Возврат в профиль преподавателя"""
        self.parent_window.show()  # Показываем окно профиля
        self.close()  # Закрываем текущее окно
