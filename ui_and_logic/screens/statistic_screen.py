import psycopg2
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QPushButton, QMessageBox, \
    QLineEdit, QApplication


class StatisticsWindow(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.setWindowTitle('Статистика')
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

        # Создание компоновки
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

        self.label = QLabel("Просмотр статистики", self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("font-size: 20px; font-weight: bold; color: #333; padding: 10px;")

        self.start_date = QLineEdit(self)
        self.start_date.setPlaceholderText('Начальный год')

        self.end_date = QLineEdit(self)
        self.end_date.setPlaceholderText('Последний год')

        self.get_sub_button = QPushButton('Посмотреть средний балл по предметам за период', self)
        self.get_sub_button.setStyleSheet(button_style)
        self.get_sub_button.clicked.connect(self.get_sub_with_date)

        self.get_stud_button = QPushButton('Посмотреть средний балл по студентам за период', self)
        self.get_stud_button.setStyleSheet(button_style)
        self.get_stud_button.clicked.connect(self.get_stud_with_date)

        self.get_all_button = QPushButton('Посмотреть средний балл студентов по предметам за период', self)
        self.get_all_button.setStyleSheet(button_style)
        self.get_all_button.clicked.connect(self.get_all_with_date)

        self.get_teacher_button = QPushButton('Посмотреть средний балл по преподавателям и предметам за период', self)
        self.get_teacher_button.setStyleSheet(button_style)
        self.get_teacher_button.clicked.connect(self.get_avg_marks_by_subject_and_teacher)

        self.get_group_button = QPushButton('Посмотреть средний балл по группам за период', self)
        self.get_group_button.setStyleSheet(button_style)
        self.get_group_button.clicked.connect(self.get_group_with_date)

        self.back_button = QPushButton('Назад', self)
        self.back_button.setStyleSheet("background-color: #f44336; color: white; font-size: 14px; padding: 10px; border-radius: 5px;")
        self.back_button.clicked.connect(self.back_to_profile)

        layout.addWidget(self.label)
        layout.addWidget(self.start_date)
        layout.addWidget(self.end_date)
        layout.addWidget(self.get_sub_button)
        layout.addWidget(self.get_stud_button)
        layout.addWidget(self.get_all_button)
        layout.addWidget(self.get_teacher_button)
        layout.addWidget(self.get_group_button)
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

        table.setColumnWidth(0, QApplication.primaryScreen().size().width() // 2)
        table.setColumnWidth(1, QApplication.primaryScreen().size().width() // 2)

        # Создаем кнопку для закрытия таблицы
        close_button = QPushButton('Закрыть', table)
        close_button.clicked.connect(table.close)

        close_button.setFixedHeight(40)  # Например, фиксируем высоту кнопки в 40 пикселей

        # Добавляем таблицу и кнопку на layout
        layout = QVBoxLayout(table)
        layout.addWidget(table)
        layout.addStretch(5)  # Это растягиваемое пространство
        layout.addWidget(close_button)

        # Устанавливаем layout для таблицы
        table.setLayout(layout)
        table.resize(QApplication.primaryScreen().size().width(), 600)
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

        table.setColumnWidth(0, QApplication.primaryScreen().size().width() // 3)
        table.setColumnWidth(1, QApplication.primaryScreen().size().width() // 3)
        table.setColumnWidth(2, QApplication.primaryScreen().size().width() // 3)

        # Создаем кнопку для закрытия таблицы
        close_button = QPushButton('Закрыть', table)
        close_button.clicked.connect(table.close)

        close_button.setFixedHeight(40)  # Например, фиксируем высоту кнопки в 40 пикселей

        # Добавляем таблицу и кнопку на layout
        layout = QVBoxLayout(table)
        layout.addWidget(table)
        layout.addStretch(5)  # Это растягиваемое пространство
        layout.addWidget(close_button)

        # Устанавливаем layout для таблицы
        table.setLayout(layout)
        table.resize(QApplication.primaryScreen().size().width(), 600)
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

        table.setColumnWidth(0, QApplication.primaryScreen().size().width() // 4)
        table.setColumnWidth(1, QApplication.primaryScreen().size().width() // 4)
        table.setColumnWidth(2, QApplication.primaryScreen().size().width() // 4)
        table.setColumnWidth(3, QApplication.primaryScreen().size().width() // 4)
        # Создаем кнопку для закрытия таблицы
        close_button = QPushButton('Закрыть', table)
        close_button.clicked.connect(table.close)

        close_button.setFixedHeight(40)  # Например, фиксируем высоту кнопки в 40 пикселей

        # Добавляем таблицу и кнопку на layout
        layout = QVBoxLayout(table)
        layout.addWidget(table)
        layout.addStretch(5)  # Это растягиваемое пространство
        layout.addWidget(close_button)

        # Устанавливаем layout для таблицы
        table.setLayout(layout)
        table.resize(QApplication.primaryScreen().size().width(), 600)
        table.show()

    def get_avg_marks_by_subject_and_teacher(self):
        """Получить средний балл по предметам и преподавателям за интервал лет"""
        self._get_avg_marks_by_subject_and_teacher_from_db()

    def _get_avg_marks_by_subject_and_teacher_from_db(self):
        """Метод для получения данных о среднем балле по предметам и преподавателям из базы данных"""
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
                password="s46825710",
                host="localhost",
                port="5432"
            )
            cursor = connection.cursor()

            # Выполнение вызова функции с параметрами
            cursor.execute(
                "SELECT * FROM public.get_avg_marks_by_subject_and_teacher_for_period(%s, %s);",
                (start_year, end_year)
            )

            result = cursor.fetchall()

            if not result:
                QMessageBox.information(self, "Информация", "Ничего не найдено.")
                return

            # Отображаем результат в таблице
            self.show_avg_marks_result_in_table(result)

        except Exception as e:
            import traceback
            traceback.print_exc()
            QMessageBox.critical(self, "Ошибка", f"Не удалось получить данные: {str(e)}")
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    def show_avg_marks_result_in_table(self, res):
        """Отображает результаты по предметам и преподавателям в таблице"""
        table = QTableWidget(self)
        table.setRowCount(len(res))
        table.setColumnCount(4)  # Столбцы: 'Имя преподавателя', 'Фамилия преподавателя', 'Предмет', 'Средний балл'
        table.setHorizontalHeaderLabels(['Имя преподавателя', 'Фамилия преподавателя', 'Предмет', 'Средний балл'])
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

        table.setColumnWidth(0, QApplication.primaryScreen().size().width() // 4)
        table.setColumnWidth(1, QApplication.primaryScreen().size().width() // 4)
        table.setColumnWidth(2, QApplication.primaryScreen().size().width() // 4)
        table.setColumnWidth(3, QApplication.primaryScreen().size().width() // 4)

        # Создаем кнопку для закрытия таблицы
        close_button = QPushButton('Закрыть', table)
        close_button.clicked.connect(table.close)

        close_button.setFixedHeight(40)  # Например, фиксируем высоту кнопки в 40 пикселей

        # Добавляем таблицу и кнопку на layout
        layout = QVBoxLayout(table)
        layout.addWidget(table)
        layout.addStretch(5)  # Это растягиваемое пространство
        layout.addWidget(close_button)

        # Устанавливаем layout для таблицы
        table.setLayout(layout)
        table.resize(QApplication.primaryScreen().size().width(), 600)
        table.show()

    def get_group_with_date(self):
        """Получить средний балл по группам за интервал лет"""
        self._get_data_about_group_from_db('public.get_avg_marks_by_group_for_period')

    def _get_data_about_group_from_db(self, procedure_name):
        """Общий метод для получения данных о группах из базы данных"""
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
            self.show_group_result_in_table(result)

        except Exception as e:
            import traceback
            traceback.print_exc()
            QMessageBox.critical(self, "Ошибка", f"Не удалось получить данные: {str(e)}")
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    def show_group_result_in_table(self, res):
        """Отображает данные о группах в таблице"""
        table = QTableWidget(self)
        table.setRowCount(len(res))
        table.setColumnCount(2)  # Столбцы: 'Группа' и 'Средний балл'
        table.setHorizontalHeaderLabels(['Группа', 'Средний балл'])
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

        table.setColumnWidth(0, QApplication.primaryScreen().size().width()//2)
        table.setColumnWidth(1, QApplication.primaryScreen().size().width()//2)

        # Создаем кнопку для закрытия таблицы
        close_button = QPushButton('Закрыть', table)
        close_button.clicked.connect(table.close)

        close_button.setFixedHeight(40)  # Например, фиксируем высоту кнопки в 40 пикселей

        # Добавляем таблицу и кнопку на layout
        layout = QVBoxLayout(table)
        layout.addWidget(table)
        layout.addStretch(5)  # Это растягиваемое пространство
        layout.addWidget(close_button)

        # Устанавливаем layout для таблицы
        table.setLayout(layout)
        table.resize(QApplication.primaryScreen().size().width(), 600)
        table.show()

