from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QPushButton


class StatisticsWindow(QWidget):
    def __init__(self, parent):
        super().__init__()

        self.setWindowTitle('Статистика')
        self.setGeometry(100, 100, 600, 400)

        self.parent_window = parent  # Ссылка на родительское окно

        layout = QVBoxLayout()

        self.label = QLabel("Просмотр статистики:", self)

        # Пример таблицы статистики
        self.statistics_table = QTableWidget(self)
        self.statistics_table.setColumnCount(4)
        self.statistics_table.setHorizontalHeaderLabels(["Предмет", "Средний балл", "Дата начала", "Дата окончания"])

        layout.addWidget(self.label)
        layout.addWidget(self.statistics_table)

        self.back_button = QPushButton('Назад', self)
        self.back_button.clicked.connect(self.back_to_profile)

        layout.addWidget(self.back_button)

        self.setLayout(layout)

    def back_to_profile(self):
        """Возврат в профиль преподавателя"""
        self.parent_window.show()  # Показываем окно профиля
        self.close()  # Закрываем текущее окно
