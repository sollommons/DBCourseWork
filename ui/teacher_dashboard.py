# ui/teacher_dashboard.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import Qt


class TeacherDashboardWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Панель преподавателя')
        self.setGeometry(100, 100, 600, 400)

        layout = QVBoxLayout()

        # Заголовок
        self.label = QLabel("Добро пожаловать, Преподаватель!", self)
        layout.addWidget(self.label)

        # Кнопки для просмотра студентов и оценок
        self.view_students_button = QPushButton("Посмотреть студентов", self)
        layout.addWidget(self.view_students_button)

        self.add_grades_button = QPushButton("Добавить оценки", self)
        layout.addWidget(self.add_grades_button)

        # Таблица с оценками (пока пустая, можно заполнять)
        self.grades_table = QTableWidget(self)
        self.grades_table.setColumnCount(4)
        self.grades_table.setHorizontalHeaderLabels(["Студент", "Предмет", "Оценка", "Дата"])
        self.grades_table.setRowCount(0)  # Пока пустая
        layout.addWidget(self.grades_table)

        self.setLayout(layout)

        # Обработчик кнопки "Посмотреть студентов"
        self.view_students_button.clicked.connect(self.on_view_students)

        # Обработчик кнопки "Добавить оценки"
        self.add_grades_button.clicked.connect(self.on_add_grades)

    def on_view_students(self):
        # Здесь будет код для отображения списка студентов
        print("Открыть список студентов")

    def on_add_grades(self):
        # Здесь будет код для добавления оценок студентам
        print("Открыть форму для добавления оценок")
