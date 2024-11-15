import psycopg2
from PyQt5.QtWidgets import QPushButton, QLineEdit, QLabel, QVBoxLayout, QWidget, QMessageBox, QTableWidget, \
    QTableWidgetItem


class AddSubWindow(QWidget):
    def __init__(self, parent):
        super().__init__()

        self.setWindowTitle('Добавить предмет')
        self.setGeometry(100, 100, 400, 300)

        self.parent_window = parent  # Ссылка на родительское окно

        layout = QVBoxLayout()

        self.label = QLabel("Введите данные предмета:\n Инструкция:\n- Чтобы добавить предмет или вписать новый  используйте\n"
                            "поле со значением <Новое название предмета>\n- Чтобы удалить или изменить старое - поле со значением <Старое название предмета>", self)

        self.subject_name_input = QLineEdit(self)
        self.subject_name_input.setPlaceholderText('Новое название предмета')

        self.old_subject_name_input = QLineEdit(self)
        self.old_subject_name_input.setPlaceholderText('Старое название предмета')

        self.add_button = QPushButton('Добавить', self)
        self.add_button.clicked.connect(self.add_subject_to_db)

        self.change_button = QPushButton('Изменить', self)
        self.change_button.clicked.connect(self.update_subject_in_db)

        self.delete_button = QPushButton('Удалить', self)
        self.delete_button.clicked.connect(self.delete_subject_from_db)

        self.get_button = QPushButton('Посмотреть все группы', self)
        self.get_button.clicked.connect(self.get_all_subjects)

        self.back_button = QPushButton('Назад', self)
        self.back_button.clicked.connect(self.back_to_profile)

        layout.addWidget(self.label)
        layout.addWidget(self.subject_name_input)
        layout.addWidget(self.old_subject_name_input)
        layout.addWidget(self.add_button)
        layout.addWidget(self.change_button)
        layout.addWidget(self.delete_button)
        layout.addWidget(self.get_button)
        layout.addWidget(self.back_button)

        self.setLayout(layout)

    def back_to_profile(self):
        """Возврат в профиль администратора"""
        self.parent_window.show()  # Показываем окно профиля
        self.close()  # Закрываем текущее окно

    def add_subject_to_db(self):
        """Добавляет предмет в базу данных."""
        subject_name = self.subject_name_input.text().strip()

        # Проверяем, что название группы не пустое
        if not subject_name:
            QMessageBox.warning(self, "Ошибка", "Название предмета не может быть пустым.")
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
            insert_query = "INSERT INTO public.subject (name) VALUES (%s)"
            cursor.execute(insert_query, (subject_name,))

            # Подтверждаем изменения в базе данных
            connection.commit()

            # Закрываем курсор и соединение
            cursor.close()
            connection.close()

            # Показываем сообщение об успехе
            QMessageBox.information(self, "Успех", f"Предмет '{subject_name}' успешно добавлен.")

            # Очищаем поле ввода
            self.subject_name_input.clear()

        except Exception as e:
            # В случае ошибки выводим сообщение
            QMessageBox.critical(self, "Ошибка", f"Не удалось добавить предмет: {str(e)}")
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()


    def update_subject_in_db(self):
        """Изменяет предмет для пользователей."""

        old_subject_name = self.old_subject_name_input.text().strip()
        new_subject_name = self.subject_name_input.text().strip()

        # Проверяем, что название предметов не пустые
        if not old_subject_name or not new_subject_name:
            QMessageBox.warning(self, "Ошибка", "Названия предметов не могут быть пустыми.")
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

            # SQL запрос для обновления группы
            update_query = """
                    UPDATE public.subject
                    SET name = (%s)
                    WHERE name = (%s);
                """

            # Выполнение запроса с параметрами
            cursor.execute(update_query, (new_subject_name, old_subject_name))

            # Подтверждаем изменения в базе данных
            connection.commit()

            # Проверка количества изменённых строк
            if cursor.rowcount == 0:
                QMessageBox.information(self, "Информация", f"Предмет с именем '{old_subject_name}' не найдены.")
            else:
                QMessageBox.information(self, "Успех",
                                        f"Предмет успешно изменен с '{old_subject_name}' на '{new_subject_name}'.")

            # Закрываем курсор и соединение
            cursor.close()
            connection.close()

        except Exception as e:
            import traceback
            traceback.print_exc()  # Выводим стек ошибки
            QMessageBox.critical(self, "Ошибка", f"Не удалось изменить предмет: {str(e)}")
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    def delete_subject_from_db(self, ):
        """Удаляет предмет из базы данных."""
        old_subject_name = self.old_subject_name_input.text().strip()

        # Проверяем, что название предмета не пустое
        if not old_subject_name:
            QMessageBox.warning(self, "Ошибка", "Название предмета не может быть пустым.")
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

            # SQL запрос для удаления предмета
            delete_query = "DELETE FROM public.subject WHERE name = %s"

            # Выполнение запроса
            cursor.execute(delete_query, (old_subject_name,))

            # Подтверждаем изменения в базе данных
            connection.commit()

            # Проверяем, был ли удален предмет
            if cursor.rowcount == 0:
                QMessageBox.information(self, "Информация", f"Предмет '{old_subject_name}' не найден.")
            else:
                QMessageBox.information(self, "Успех", f"Предмет '{old_subject_name}' успешно удален.")

            # Закрываем курсор и соединение
            cursor.close()
            connection.close()

        except Exception as e:
            import traceback
            traceback.print_exc()  # Выводим стек ошибки
            QMessageBox.critical(self, "Ошибка", f"Не удалось удалить предмет: {str(e)}")
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()


    def get_all_subjects(self):
        """Возвращает все предметы и их ID из базы данных."""
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
            select_query = "SELECT id, name FROM public.subject"
            cursor.execute(select_query)

            # Извлекаем все строки результата
            subjects = cursor.fetchall()

            # Проверяем, есть ли предметы
            if not subjects:
                QMessageBox.information(self, "Информация", "Группы не найдены.")
                return

            # Если необходимо отобразить группы в таблице
            self.show_subjects_in_table(subjects)

            # Закрываем курсор и соединение
            cursor.close()
            connection.close()

        except Exception as e:
            import traceback
            traceback.print_exc()  # Выводим стек ошибки
            QMessageBox.critical(self, "Ошибка", f"Не удалось получить предметы: {str(e)}")
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    def show_subjects_in_table(self, subjects):
        """Отображает предметы в таблице."""
        # Создаём таблицу с двумя столбцами: ID и Name
        table = QTableWidget(self)
        table.setRowCount(len(subjects))  # Строки для каждого предмета
        table.setColumnCount(2)  # Столбцы для ID и Name
        table.setHorizontalHeaderLabels(['ID', 'Название'])
        table.setEditTriggers(QTableWidget.NoEditTriggers)

        # Заполняем таблицу данными
        for row, subject in enumerate(subjects):
            table.setItem(row, 0, QTableWidgetItem(str(subject[0])))  # ID
            table.setItem(row, 1, QTableWidgetItem(subject[1]))  # Название

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