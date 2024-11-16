import psycopg2
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QPushButton, QMessageBox, QLineEdit


class StatisticsWindow(QWidget):
    def __init__(self, parent):
        super().__init__()

        self.setWindowTitle('Статистика')
        self.setGeometry(100, 100, 600, 400)

        self.parent_window = parent

        # Создание компоновки
        layout = QVBoxLayout()

        self.label = QLabel("Просмотр статистики", self)

        self.start_date = QLineEdit(self)
        self.start_date.setPlaceholderText('Начальный год')

        self.end_date = QLineEdit(self)
        self.end_date.setPlaceholderText('Последний год')

        self.get_sub_button = QPushButton('Посмотреть средний балл по предметам за период', self)
        self.get_sub_button.clicked.connect(self.get_sub_with_date)

        self.get_stud_button = QPushButton('Посмотреть средний балл по студентам за период', self)
        self.get_stud_button.clicked.connect(self.get_stud_with_date)

        self.get_all_button = QPushButton('Посмотреть средний балл студентов по предметам за период', self)
        self.get_all_button.clicked.connect(self.get_all_with_date)

        self.back_button = QPushButton('Назад', self)
        self.back_button.clicked.connect(self.back_to_profile)

        layout.addWidget(self.label)
        layout.addWidget(self.start_date)
        layout.addWidget(self.end_date)
        layout.addWidget(self.get_sub_button)
        layout.addWidget(self.get_stud_button)
        layout.addWidget(self.get_all_button)
        layout.addWidget(self.back_button)

        self.setLayout(layout)

    def back_to_profile(self):
        """Возврат в профиль преподавателя"""
        self.parent_window.show()  # Показываем окно профиля
        self.close()  # Закрываем текущее окно

    def get_sub_with_date(self):
        """Получить средний балл по предметам за интервал лет"""
        self._get_data_about_subj_from_db('public.get_avg_marks_by_subject_for_course_interval')

    def get_stud_with_date(self):
        """Получить средний балл по студентам за интервал лет"""
        self._get_data_about_stud_from_db('public.get_avg_marks_by_student_for_course_interval')

    def get_all_with_date(self):
        """Получить средний балл студентов по предметам за интервал лет"""
        self._get_data_about_all_from_db('public.get_avg_marks_by_student_and_subject_for_period')

    def _get_data_about_subj_from_db(self, procedure_name):
        """Общий метод для получения данных о предметах из базы данных"""
        start_date = self.start_date.text().strip()
        end_date = self.end_date.text().strip()

        # Проверка на корректность введенных данных
        if not start_date.isdigit() or not end_date.isdigit():
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, введите корректные года.")
            return

        start_year = int(start_date)
        end_year = int(end_date)

        if start_year > end_year:
            QMessageBox.warning(self, "Ошибка", "Начальный год не может быть больше конечного!")
            return

        try:
            # Подключение к базе данных
            connection = psycopg2.connect(
                dbname="university",
                user="postgres",
                password="s46825710",  # Замените на ваш пароль
                host="localhost",
                port="5432"
            )
            cursor = connection.cursor()

            # Выполнение вызова функции с параметрами
            cursor.execute(f"SELECT * FROM {procedure_name}(%s, %s);", (start_year, end_year))

            result = cursor.fetchall()

            if not result:
                QMessageBox.information(self, "Информация", "Ничего не найдено.")
                return

            # Отображаем результат в таблице
            self.show_subj_result_in_table(result)

        except Exception as e:
            import traceback
            traceback.print_exc()
            QMessageBox.critical(self, "Ошибка", f"Не удалось получить данные: {str(e)}")
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    def show_subj_result_in_table(self, res):
        """Отображает результаты по предметам в таблице"""
        table = QTableWidget(self)
        table.setRowCount(len(res))
        table.setColumnCount(2)  # Столбцы: 'Предмет' и 'Средний балл'
        table.setHorizontalHeaderLabels(['Предмет', 'Средний балл'])
        table.setEditTriggers(QTableWidget.NoEditTriggers)

        # Заполняем таблицу результатами
        for row, row_data in enumerate(res):
            for col, item in enumerate(row_data):
                if isinstance(item, float):  # Если это число с плавающей запятой
                    # Форматируем число до 2 знаков после запятой
                    table.setItem(row, col, QTableWidgetItem(f"{item:.2f}"))
                else:
                    # Преобразуем другие данные в строковый формат
                    table.setItem(row, col, QTableWidgetItem(str(item)))

        # Создаем кнопку для закрытия таблицы
        close_button = QPushButton('Закрыть', table)
        close_button.clicked.connect(table.close)

        # Добавляем таблицу и кнопку на layout
        layout = QVBoxLayout(table)
        layout.addWidget(table)
        layout.addWidget(close_button)

        # Устанавливаем layout для таблицы
        table.setLayout(layout)
        table.resize(400, 300)
        table.show()

    def _get_data_about_stud_from_db(self, procedure_name):
        """Общий метод для получения данных о студентах из базы данных"""
        start_date = self.start_date.text().strip()
        end_date = self.end_date.text().strip()

        # Проверка на корректность введенных данных
        if not start_date.isdigit() or not end_date.isdigit():
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, введите корректные года.")
            return

        start_year = int(start_date)
        end_year = int(end_date)

        if start_year > end_year:
            QMessageBox.warning(self, "Ошибка", "Начальный год не может быть больше конечного!")
            return

        try:
            # Подключение к базе данных
            connection = psycopg2.connect(
                dbname="university",
                user="postgres",
                password="s46825710",  # Замените на ваш пароль
                host="localhost",
                port="5432"
            )
            cursor = connection.cursor()

            # Выполнение вызова функции с параметрами
            cursor.execute(f"SELECT * FROM {procedure_name}(%s, %s);", (start_year, end_year))

            result = cursor.fetchall()

            if not result:
                QMessageBox.information(self, "Информация", "Ничего не найдено.")
                return

            # Отображаем результат в таблице
            self.show_stud_result_in_table(result)

        except Exception as e:
            import traceback
            traceback.print_exc()
            QMessageBox.critical(self, "Ошибка", f"Не удалось получить данные: {str(e)}")
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    def show_stud_result_in_table(self, res):
        """Отображает результаты по студентам в таблице"""
        table = QTableWidget(self)
        table.setRowCount(len(res))
        table.setColumnCount(3)  # Столбцы: 'Имя', 'Фамилия', 'Средний балл'
        table.setHorizontalHeaderLabels(['Имя', 'Фамилия', 'Средний балл'])
        table.setEditTriggers(QTableWidget.NoEditTriggers)

        # Заполняем таблицу результатами
        for row, row_data in enumerate(res):
            for col, item in enumerate(row_data):
                if isinstance(item, float):  # Если это число с плавающей запятой
                    # Форматируем число до 2 знаков после запятой
                    table.setItem(row, col, QTableWidgetItem(f"{item:.2f}"))
                else:
                    # Преобразуем другие данные в строковый формат
                    table.setItem(row, col, QTableWidgetItem(str(item)))

        # Создаем кнопку для закрытия таблицы
        close_button = QPushButton('Закрыть', table)
        close_button.clicked.connect(table.close)

        # Добавляем таблицу и кнопку на layout
        layout = QVBoxLayout(table)
        layout.addWidget(table)
        layout.addWidget(close_button)

        # Устанавливаем layout для таблицы
        table.setLayout(layout)
        table.resize(600, 400)
        table.show()

    def _get_data_about_all_from_db(self, procedure_name):
        """Общий метод для получения данных о студентах и предметах из базы данных"""
        start_date = self.start_date.text().strip()
        end_date = self.end_date.text().strip()

        # Проверка на корректность введенных данных
        if not start_date.isdigit() or not end_date.isdigit():
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, введите корректные года.")
            return

        start_year = int(start_date)
        end_year = int(end_date)

        if start_year > end_year:
            QMessageBox.warning(self, "Ошибка", "Начальный год не может быть больше конечного!")
            return

        try:
            # Подключение к базе данных
            connection = psycopg2.connect(
                dbname="university",
                user="postgres",
                password="s46825710",  # Замените на ваш пароль
                host="localhost",
                port="5432"
            )
            cursor = connection.cursor()

            # Выполнение вызова функции с параметрами
            cursor.execute(f"SELECT * FROM {procedure_name}(%s, %s);", (start_year, end_year))

            result = cursor.fetchall()

            if not result:
                QMessageBox.information(self, "Информация", "Ничего не найдено.")
                return

            # Отображаем результат в таблице
            self.show_all_result_in_table(result)

        except Exception as e:
            import traceback
            traceback.print_exc()
            QMessageBox.critical(self, "Ошибка", f"Не удалось получить данные: {str(e)}")
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    def show_all_result_in_table(self, res):
        """Отображает данные студентов и предметов в таблице"""
        table = QTableWidget(self)
        table.setRowCount(len(res))
        table.setColumnCount(4)  # Столбцы: 'Имя', 'Фамилия', 'Предмет', 'Средний балл'
        table.setHorizontalHeaderLabels(['Имя', 'Фамилия', 'Предмет', 'Средний балл'])
        table.setEditTriggers(QTableWidget.NoEditTriggers)

        # Заполняем таблицу результатами
        for row, row_data in enumerate(res):
            for col, item in enumerate(row_data):
                if isinstance(item, float):  # Если это число с плавающей запятой
                    # Форматируем число до 2 знаков после запятой
                    table.setItem(row, col, QTableWidgetItem(f"{item:.2f}"))
                else:
                    # Преобразуем другие данные в строковый формат
                    table.setItem(row, col, QTableWidgetItem(str(item)))

        # Создаем кнопку для закрытия таблицы
        close_button = QPushButton('Закрыть', table)
        close_button.clicked.connect(table.close)

        # Добавляем таблицу и кнопку на layout
        layout = QVBoxLayout(table)
        layout.addWidget(table)
        layout.addWidget(close_button)

        # Устанавливаем layout для таблицы
        table.setLayout(layout)
        table.resize(600, 400)
        table.show()
