import psycopg2
from PyQt5.QtWidgets import QPushButton, QLineEdit, QLabel, QVBoxLayout, QWidget, QMessageBox, QTableWidget, \
    QTableWidgetItem

class AddTeacherWindow(QWidget):
    def __init__(self, parent):
        super().__init__()

        self.setWindowTitle('Добавить преподавателя')
        self.setGeometry(100, 100, 400, 300)

        self.parent_window = parent  # Ссылка на родительское окно

        layout = QVBoxLayout()

        self.label = QLabel("Введите данные преподавателя:", self)

        self.first_name_input = QLineEdit(self)
        self.first_name_input.setPlaceholderText('Имя')

        self.last_name_input = QLineEdit(self)
        self.last_name_input.setPlaceholderText('Фамилия')

        self.father_name_input = QLineEdit(self)
        self.father_name_input.setPlaceholderText('Отчество')

        self.old_first_name_input = QLineEdit(self)
        self.old_first_name_input.setPlaceholderText('Старое имя')

        self.old_last_name_input = QLineEdit(self)
        self.old_last_name_input.setPlaceholderText('Старая фамилия')

        self.old_father_name_input = QLineEdit(self)
        self.old_father_name_input.setPlaceholderText('Старое отчество')

        self.add_button = QPushButton('Добавить', self)
        self.add_button.clicked.connect(self.add_teacher_to_db)

        self.update_button = QPushButton('Обновить', self)
        self.update_button.clicked.connect(self.update_teacher_to_db)

        self.delete_button = QPushButton('Удалить', self)
        self.delete_button.clicked.connect(self.delete_teacher_to_db)

        self.get_teachers_button = QPushButton('Посмотреть всех преподавателей', self)
        self.get_teachers_button.clicked.connect(self.get_all_teachers)

        self.back_button = QPushButton('Назад', self)
        self.back_button.clicked.connect(self.back_to_profile)

        layout.addWidget(self.label)
        layout.addWidget(self.first_name_input)
        layout.addWidget(self.last_name_input)
        layout.addWidget(self.father_name_input)
        layout.addWidget(self.old_first_name_input)
        layout.addWidget(self.old_last_name_input)
        layout.addWidget(self.old_father_name_input)
        layout.addWidget(self.add_button)
        layout.addWidget(self.update_button)
        layout.addWidget(self.delete_button)
        layout.addWidget(self.get_teachers_button)
        layout.addWidget(self.back_button)

        self.setLayout(layout)

    def back_to_profile(self):
        """Возврат в профиль"""
        self.parent_window.show()  # Показываем окно профиля
        self.close()  # Закрываем текущее окно

    def add_teacher_to_db(self):
        """Добавляет преподавателя в базу данных."""
        teacher_name = self.first_name_input.text().strip()
        teacher_last_name = self.last_name_input.text().strip()
        teacher_father_name = self.father_name_input.text().strip()

        # Проверяем, что название группы не пустое
        if not teacher_name:
            QMessageBox.warning(self, "Ошибка", "Имя не может быть пустым.")
            return
        if not teacher_last_name:
            QMessageBox.warning(self, "Ошибка", "Фамилия не может быть пустой.")
            return

        try:
            # Подключение к базе данных
            connection = psycopg2.connect(
                dbname="university",  # Замените на название вашей базы данных
                user="postgres",  # Замените на ваше имя пользователя
                password="s46825710",  # Замените на ваш пароль
                host="localhost",  # Замените на хост, если нужно
                port="5432"  # Порт по умолчанию для PostgreSQL
            )
            cursor = connection.cursor()

            # Подготовка SQL запроса для добавления нового преподавателя
            insert_query = """INSERT INTO public.people (first_name, last_name, father_name, group_id, type)
            VALUES 
            ((%s), (%s), (%s), null, 'T') 
            """
            cursor.execute(insert_query, (teacher_name, teacher_last_name,teacher_father_name,))

            # Подтверждаем изменения в базе данных
            connection.commit()

            # Закрываем курсор и соединение
            cursor.close()
            connection.close()

            # Показываем сообщение об успехе
            QMessageBox.information(self, "Успех", f"Преподаватель '{teacher_name}' успешно добавлен.")

            # Очищаем поле ввода
            self.first_name_input.clear()
            self.last_name_input.clear()
            self.father_name_input.clear()

        except Exception as e:
            # В случае ошибки выводим сообщение
            QMessageBox.critical(self, "Ошибка", f"Не удалось добавить преподавателя: {str(e)}")
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    def update_teacher_to_db(self):
        """Изменяет преподавателя в базе данных."""
        teacher_name = self.first_name_input.text().strip()
        teacher_last_name = self.last_name_input.text().strip()
        teacher_father_name = self.father_name_input.text().strip()
        old_name = self.old_first_name_input.text().strip()
        old_last_name = self.old_last_name_input.text().strip()
        old_father_name = self.old_father_name_input.text().strip()

        # Проверяем, что название группы не пустое
        if not teacher_name:
            QMessageBox.warning(self, "Ошибка", "Имя не может быть пустым.")
            return
        if not teacher_last_name:
            QMessageBox.warning(self, "Ошибка", "Фамилия не может быть пустой.")
            return
        if not old_name:
            QMessageBox.warning(self, "Ошибка", "Имя не может быть пустым.")
            return
        if not old_last_name:
            QMessageBox.warning(self, "Ошибка", "Фамилия не может быть пустой.")
            return

        try:
            # Подключение к базе данных
            connection = psycopg2.connect(
                dbname="university",  # Замените на название вашей базы данных
                user="postgres",  # Замените на ваше имя пользователя
                password="s46825710",  # Замените на ваш пароль
                host="localhost",  # Замените на хост, если нужно
                port="5432"  # Порт по умолчанию для PostgreSQL
            )
            cursor = connection.cursor()
            # Подготовка SQL запроса для добавления нового предмета
            insert_query = """UPDATE public.people 
              SET first_name = (%s),
                  last_name = (%s),
                  father_name = (%s)
              WHERE first_name = (%s) AND last_name = (%s)
            """
            cursor.execute(insert_query, (teacher_name, teacher_last_name, teacher_father_name, old_name, old_last_name,))

            # Подтверждаем изменения в базе данных
            connection.commit()

            # Закрываем курсор и соединение
            cursor.close()
            connection.close()

            # Показываем сообщение об успехе
            QMessageBox.information(self, "Успех", f"Преподаватель '{teacher_name}' успешно изменен.")

            # Очищаем поле ввода
            self.first_name_input.clear()
            self.last_name_input.clear()
            self.father_name_input.clear()
            self.old_first_name_input.clear()
            self.old_last_name_input.clear()
            self.old_father_name_input.clear()

        except Exception as e:
            # В случае ошибки выводим сообщение
            QMessageBox.critical(self, "Ошибка", f"Не удалось изменить преподавтеля: {str(e)}")
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    def delete_teacher_to_db(self):
        """Удаляет преподавателя из базы данных."""
        teacher_name = self.old_first_name_input.text().strip()
        teacher_last_name = self.old_last_name_input.text().strip()
        teacher_father_name = self.old_father_name_input.text().strip()

        # Проверяем, что название группы не пустое
        if not teacher_name:
            QMessageBox.warning(self, "Ошибка", "Имя не может быть пустым.")
            return
        if not teacher_last_name:
            QMessageBox.warning(self, "Ошибка", "Фамилия не может быть пустой.")
            return

        try:
            # Подключение к базе данных
            connection = psycopg2.connect(
                dbname="university",  # Замените на название вашей базы данных
                user="postgres",  # Замените на ваше имя пользователя
                password="s46825710",  # Замените на ваш пароль
                host="localhost",  # Замените на хост, если нужно
                port="5432"  # Порт по умолчанию для PostgreSQL
            )
            cursor = connection.cursor()

            # Подготовка SQL запроса для добавления нового предмета
            insert_query = """DELETE FROM public.people 
                WHERE first_name = (%s) AND last_name = (%s)
             """
            cursor.execute(insert_query, (teacher_name, teacher_last_name))

            # Подтверждаем изменения в базе данных
            connection.commit()

            # Закрываем курсор и соединение
            cursor.close()
            connection.close()

            # Показываем сообщение об успехе
            QMessageBox.information(self, "Успех", f"Преподавель '{teacher_name}' успешно удален.")

            # Очищаем поле ввода
            self.old_first_name_input.clear()
            self.old_last_name_input.clear()
            self.old_father_name_input.clear()

        except Exception as e:
            # В случае ошибки выводим сообщение
            QMessageBox.critical(self, "Ошибка", f"Не удалось удалить преподавтеля: {str(e)}")
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    def get_all_teachers(self):
        """Возвращает всех студентов и их ID из базы данных."""
        try:
            # Подключение к базе данных
            connection = psycopg2.connect(
                dbname="university",  # Замените на название вашей базы данных
                user="postgres",  # Замените на ваше имя пользователя
                password="s46825710",  # Замените на ваш пароль
                host="localhost",  # Замените на хост, если нужно
                port="5432"  # Порт по умолчанию для PostgreSQL
            )
            cursor = connection.cursor()

            # SQL запрос для получения всех предметов
            select_query = """SELECT 
                s.id,
                s.first_name,
                s.last_name,
                s.father_name
            FROM public.people s
            """
            cursor.execute(select_query)

            # Извлекаем все строки результата
            teachers = cursor.fetchall()

            # Проверяем, есть ли предметы
            if not teachers:
                QMessageBox.information(self, "Информация", "Преподаватели не найдены.")
                return

            # Если необходимо отобразить группы в таблице
            self.show_teachers_in_table(teachers)

            # Закрываем курсор и соединение
            cursor.close()
            connection.close()

        except Exception as e:
            import traceback
            traceback.print_exc()  # Выводим стек ошибки
            QMessageBox.critical(self, "Ошибка", f"Не удалось получить преподавателей: {str(e)}")
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    def show_teachers_in_table(self, teachers):
        """Отображает предметы в таблице."""
        # Создаём таблицу с двумя столбцами: ID и Name
        table = QTableWidget(self)
        table.setRowCount(len(teachers))  # Строки для каждого предмета
        table.setColumnCount(4)  # Столбцы для ID и Name
        table.setHorizontalHeaderLabels(['ID', 'Имя', 'Фамилия', 'Отчество'])
        table.setEditTriggers(QTableWidget.NoEditTriggers)

        # Заполняем таблицу данными
        for row, subject in enumerate(teachers):
            table.setItem(row, 0, QTableWidgetItem(str(subject[0])))  # ID
            table.setItem(row, 1, QTableWidgetItem(subject[1]))  # Имя
            table.setItem(row, 2, QTableWidgetItem(subject[2]))  # Фамилия
            table.setItem(row, 3, QTableWidgetItem(subject[3]))  # Отчество


        # Создаём кнопку для закрытия таблицы
        close_button = QPushButton('Закрыть', table)
        close_button.clicked.connect(table.close)  # Закрытие окна при нажатии на кнопку

        # Создаём layout и добавляем таблицу и кнопку
        layout = QVBoxLayout(table)
        layout.addWidget(table)
        layout.addWidget(close_button)

        # Устанавливаем layout для окна
        table.setLayout(layout)

        # Отображаем таблицу в окне
        table.resize(400, 300)
        table.show()