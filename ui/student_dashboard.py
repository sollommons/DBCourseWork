# ui/student_dashboard.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton

class StudentDashboardWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Панель студента')
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        self.label = QLabel("Добро пожаловать, Студент!", self)
        layout.addWidget(self.label)

        self.view_grades_button = QPushButton("Посмотреть оценки", self)
        layout.addWidget(self.view_grades_button)

        self.view_profile_button = QPushButton("Посмотреть профиль", self)
        layout.addWidget(self.view_profile_button)

        self.setLayout(layout)  # Убедись, что этот метод есть
