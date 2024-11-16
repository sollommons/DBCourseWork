import psycopg2
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QApplication, QMessageBox, QTableWidget, \
    QTableWidgetItem


class StudentProfileWindow(QWidget):
    def __init__(self, parent):
        super().__init__()

        self.setWindowTitle('Профиль Студента')
        self.setFixedSize(QApplication.primaryScreen().size().width(),QApplication.primaryScreen().size().height()-100)

        self.parent_window = parent

        self.setStyleSheet("""
                           QWidget {
                               background-color: #e0f7e7;  /* Бледно-зеленый цвет для фона всего окна */
                           }
                           QLabel {
                               color: #333;  /* Темный цвет для текста */
                           }
                           QLineEdit {
                               background-color: #ffffff;  /* Белый фон для полей ввода */
                               border-radius: 5px;
                               border: 1px solid #ccc;
                               padding: 8px;
                           }
                           QPushButton {
                               background-color: #66bb6a;  /* Зеленый фон для кнопок */
                               color: white;
                               font-size: 14px;
                               padding: 10px;
                               border-radius: 5px;
                               border: none;
                           }
                           QPushButton:hover {
                               background-color: #5cb85c;  /* При наведении кнопки темнеют */
                           }
                           QPushButton:pressed {
                               background-color: #4cae4c;  /* При нажатии кнопки */
                           }
                           QTableWidget {
                               background-color: #ffffff;  /* Белый фон для таблицы */
                               border: 1px solid #ddd;  /* Светлый бордер для таблицы */
                           }
                       """)

        layout = QVBoxLayout()

        button_style = """
                      QPushButton {
                          background-color: #4CAF50;
                          color: white;
                          font-size: 14px;
                          padding: 10px;
                          border-radius: 5px;
                          border: none;
                      }
                      QPushButton:hover {
                          background-color: #45a049;
                      }
                      """

        self.label = QLabel("Роль: Студент", self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("font-size: 20px; font-weight: bold; color: #333; padding: 10px;")
        self.permissions_label = QLabel(
            "Что может студент:\n"
            "- Посмотреть список студентов и преподавателей\n"
            "- Посмотреть статистику по периодам (подробнее внутри)",
            self
        )
        self.permissions_label.setAlignment(Qt.AlignCenter)
        self.permissions_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #333; padding: 10px;")

        self.view_students_button = QPushButton('Экран списка студентов', self)
        self.view_students_button.setStyleSheet(button_style)

        self.view_teacher_button = QPushButton('Экран списка преподавателей', self)
        self.view_teacher_button.setStyleSheet(button_style)

        self.statistics_button = QPushButton('Экран статистики', self)
        self.statistics_button.setStyleSheet(button_style)


        self.back_button = QPushButton('Выход', self)
        self.back_button.setStyleSheet("background-color: #f44336; color: white; font-size: 14px; padding: 10px; border-radius: 5px;")
        self.back_button.clicked.connect(self.back_to_profile)

        layout.addWidget(self.label)
        layout.addWidget(self.permissions_label)
        layout.addWidget(self.view_students_button)
        layout.addWidget(self.view_teacher_button)
        layout.addWidget(self.statistics_button)
        layout.addWidget(self.back_button)

        self.setLayout(layout)

        self.view_students_button.clicked.connect(self.get_all_students)
        self.view_teacher_button.clicked.connect(self.get_all_teachers)
        self.statistics_button.clicked.connect(self.open_statistics)

    def back_to_profile(self):
        """Возврат """
        self.parent_window.show()
        self.close()


    def open_statistics(self):
        """Открытие окна статистики"""
        from ui_and_logic.screens.statistic_screen import StatisticsWindow
        self.statistics_window = StatisticsWindow(self)  # Передаем родительское окно
        self.statistics_window.show()
        self.close()  # Закрываем текущее окно

    def get_all_students(self):
        """Возвращает всех студентов и их группы из базы данных."""
        try:
            # Подключение к базе данных
            connection = psycopg2.connect(
                dbname="university",
                user="postgres",
                password="s46825710",
                host="localhost",
                port="5432"
            )
            cursor = connection.cursor()

            select_query = """SELECT 
                 s.id,
                 s.first_name,
                 s.last_name,
                 s.father_name,
                 g.name
             FROM public.people s
             JOIN 
             public.group g ON g.id = s.group_id
             WHERE s.type = 'S'
             """
            cursor.execute(select_query)

            students = cursor.fetchall()

            if not students:
                QMessageBox.information(self, "Информация", "Студенты не найдены.")
                return

            self.show_students_in_table(students)

            cursor.close()
            connection.close()

        except Exception as e:
            import traceback
            traceback.print_exc()
            QMessageBox.critical(self, "Ошибка", f"Не удалось получить студентов: {str(e)}")
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    def show_students_in_table(self, students):
        """Отображает студентов в таблице."""
        table = QTableWidget(self)
        table.setRowCount(len(students))
        table.setColumnCount(5)
        table.setHorizontalHeaderLabels(['ID', 'Имя', 'Фамилия', 'Отчество', 'Группа'])
        table.setEditTriggers(QTableWidget.NoEditTriggers)

        for row, subject in enumerate(students):
            table.setItem(row, 0, QTableWidgetItem(str(subject[0])))
            table.setItem(row, 1, QTableWidgetItem(subject[1]))
            table.setItem(row, 2, QTableWidgetItem(subject[2]))
            table.setItem(row, 3, QTableWidgetItem(subject[3]))
            table.setItem(row, 4, QTableWidgetItem(subject[4]))

        table.setColumnWidth(0, QApplication.primaryScreen().size().width() // 5)
        table.setColumnWidth(1, QApplication.primaryScreen().size().width() // 5)
        table.setColumnWidth(2, QApplication.primaryScreen().size().width() // 5)
        table.setColumnWidth(3, QApplication.primaryScreen().size().width() // 5)
        table.setColumnWidth(4, QApplication.primaryScreen().size().width() // 5)

        close_button = QPushButton('Закрыть', table)
        close_button.clicked.connect(table.close)

        close_button.setFixedHeight(40)

        layout = QVBoxLayout(table)
        layout.addWidget(table)
        layout.addStretch(5)
        layout.addWidget(close_button)

        table.setLayout(layout)
        table.resize(QApplication.primaryScreen().size().width(), 600)
        table.show()

    def get_all_teachers(self):
        """Возвращает всех преподавателей и из базы данных."""
        try:
            connection = psycopg2.connect(
                dbname="university",
                user="postgres",
                password="s46825710",
                host="localhost",
                port="5432"
            )
            cursor = connection.cursor()

            select_query = """SELECT 
                s.id,
                s.first_name,
                s.last_name,
                s.father_name
            FROM public.people s
            WHERE s.type = 'T'
            """
            cursor.execute(select_query)

            teachers = cursor.fetchall()

            if not teachers:
                QMessageBox.information(self, "Информация", "Преподаватели не найдены.")
                return

            self.show_teachers_in_table(teachers)

            cursor.close()
            connection.close()

        except Exception as e:
            import traceback
            traceback.print_exc()
            QMessageBox.critical(self, "Ошибка", f"Не удалось получить преподавателей: {str(e)}")
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    def show_teachers_in_table(self, teachers):
        """Отображает преподавателей в таблице."""
        table = QTableWidget(self)
        table.setRowCount(len(teachers))
        table.setColumnCount(4)
        table.setHorizontalHeaderLabels(['ID', 'Имя', 'Фамилия', 'Отчество'])
        table.setEditTriggers(QTableWidget.NoEditTriggers)

        for row, subject in enumerate(teachers):
            table.setItem(row, 0, QTableWidgetItem(str(subject[0])))
            table.setItem(row, 1, QTableWidgetItem(subject[1]))
            table.setItem(row, 2, QTableWidgetItem(subject[2]))
            table.setItem(row, 3, QTableWidgetItem(subject[3]))

        table.setColumnWidth(0, QApplication.primaryScreen().size().width() // 4)
        table.setColumnWidth(1, QApplication.primaryScreen().size().width() // 4)
        table.setColumnWidth(2, QApplication.primaryScreen().size().width() // 4)
        table.setColumnWidth(3, QApplication.primaryScreen().size().width() // 4)

        close_button = QPushButton('Закрыть', table)
        close_button.clicked.connect(table.close)

        close_button.setFixedHeight(40)

        layout = QVBoxLayout(table)
        layout.addWidget(table)
        layout.addStretch(5)
        layout.addWidget(close_button)

        table.setLayout(layout)
        table.resize(QApplication.primaryScreen().size().width(), 600)
        table.show()