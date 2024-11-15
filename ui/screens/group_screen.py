import psycopg2
from PyQt5.QtWidgets import QPushButton, QLineEdit, QLabel, QVBoxLayout, QWidget, QMessageBox, QTableWidget, \
    QTableWidgetItem


class AddGroupWindow(QWidget):
    def __init__(self, parent):
        super().__init__()

        self.setWindowTitle('Добавить группу')
        self.setGeometry(100, 100, 400, 300)

        self.parent_window = parent  # Ссылка на родительское окно

        layout = QVBoxLayout()

        self.label = QLabel("Введите данные группы:\n Инструкция:\n- Чтобы добавить группу или вписать новое название используйте\n"
                            "поле со значением <Новое название группы>\n- Чтобы удалить или изменить старое - поле со значением <Старое название группы>", self)

        self.group_name_input = QLineEdit(self)
        self.group_name_input.setPlaceholderText('Новое название группы')

        self.old_group_name_input = QLineEdit(self)
        self.old_group_name_input.setPlaceholderText('Старое название группы')

        self.add_button = QPushButton('Добавить', self)
        self.add_button.clicked.connect(self.add_group_to_db)

        self.change_button = QPushButton('Изменить', self)
        self.change_button.clicked.connect(self.update_group_in_db)

        self.delete_button = QPushButton('Удалить', self)
        self.delete_button.clicked.connect(self.delete_group_from_db)

        self.get_button = QPushButton('Посмотреть все группы', self)
        self.get_button.clicked.connect(self.get_all_groups)

        self.back_button = QPushButton('Назад', self)
        self.back_button.clicked.connect(self.back_to_profile)

        layout.addWidget(self.label)
        layout.addWidget(self.group_name_input)
        layout.addWidget(self.old_group_name_input)
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

    def add_group_to_db(self):
        """Добавляет группу в базу данных."""
        group_name = self.group_name_input.text().strip()

        # Проверяем, что название группы не пустое
        if not group_name:
            QMessageBox.warning(self, "Ошибка", "Название группы не может быть пустым.")
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

            # Подготовка SQL запроса для добавления новой группы
            insert_query = "INSERT INTO public.group (name) VALUES (%s)"
            cursor.execute(insert_query, (group_name,))

            # Подтверждаем изменения в базе данных
            connection.commit()

            # Закрываем курсор и соединение
            cursor.close()
            connection.close()

            # Показываем сообщение об успехе
            QMessageBox.information(self, "Успех", f"Группа '{group_name}' успешно добавлена.")

            # Очищаем поле ввода
            self.group_name_input.clear()

        except Exception as e:
            # В случае ошибки выводим сообщение
            QMessageBox.critical(self, "Ошибка", f"Не удалось добавить группу: {str(e)}")
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()


    def update_group_in_db(self):
        """Изменяет группу для пользователей."""

        old_group_name = self.old_group_name_input.text().strip()
        new_group_name = self.group_name_input.text().strip()

        # Проверяем, что имена групп не пустые
        if not old_group_name or not new_group_name:
            QMessageBox.warning(self, "Ошибка", "Названия групп не могут быть пустыми.")
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
                    UPDATE public.group
                    SET name = (%s)
                    WHERE name = (%s);
                """

            # Выполнение запроса с параметрами
            cursor.execute(update_query, (new_group_name, old_group_name))

            # Подтверждаем изменения в базе данных
            connection.commit()

            # Проверка количества изменённых строк
            if cursor.rowcount == 0:
                QMessageBox.information(self, "Информация", f"Группы с именем '{old_group_name}' не найдены.")
            else:
                QMessageBox.information(self, "Успех",
                                        f"Группа успешно изменена с '{old_group_name}' на '{new_group_name}'.")

            # Закрываем курсор и соединение
            cursor.close()
            connection.close()

        except Exception as e:
            import traceback
            traceback.print_exc()  # Выводим стек ошибки
            QMessageBox.critical(self, "Ошибка", f"Не удалось изменить группу: {str(e)}")
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    def delete_group_from_db(self, ):
        """Удаляет группу из базы данных."""
        old_group_name = self.old_group_name_input.text().strip()

        # Проверяем, что название группы не пустое
        if not old_group_name:
            QMessageBox.warning(self, "Ошибка", "Название группы не может быть пустым.")
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

            # SQL запрос для удаления группы
            delete_query = "DELETE FROM public.group WHERE name = %s"

            # Выполнение запроса
            cursor.execute(delete_query, (old_group_name,))

            # Подтверждаем изменения в базе данных
            connection.commit()

            # Проверяем, была ли удалена группа
            if cursor.rowcount == 0:
                QMessageBox.information(self, "Информация", f"Группа '{old_group_name}' не найдена.")
            else:
                QMessageBox.information(self, "Успех", f"Группа '{old_group_name}' успешно удалена.")

            # Закрываем курсор и соединение
            cursor.close()
            connection.close()

        except Exception as e:
            import traceback
            traceback.print_exc()  # Выводим стек ошибки
            QMessageBox.critical(self, "Ошибка", f"Не удалось удалить группу: {str(e)}")
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()


    def get_all_groups(self):
        """Возвращает все группы и их ID из базы данных."""
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

            # SQL запрос для получения всех групп
            select_query = "SELECT id, name FROM public.group"
            cursor.execute(select_query)

            # Извлекаем все строки результата
            groups = cursor.fetchall()

            # Проверяем, есть ли группы
            if not groups:
                QMessageBox.information(self, "Информация", "Группы не найдены.")
                return

            # Если необходимо отобразить группы в таблице
            self.show_groups_in_table(groups)

            # Закрываем курсор и соединение
            cursor.close()
            connection.close()

        except Exception as e:
            import traceback
            traceback.print_exc()  # Выводим стек ошибки
            QMessageBox.critical(self, "Ошибка", f"Не удалось получить группы: {str(e)}")
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    def show_groups_in_table(self, groups):
        """Отображает группы в таблице."""
        # Создаём таблицу с двумя столбцами: ID и Name
        table = QTableWidget(self)
        table.setRowCount(len(groups))  # Строки для каждой группы
        table.setColumnCount(2)  # Столбцы для ID и Name
        table.setHorizontalHeaderLabels(['ID', 'Название'])
        table.setEditTriggers(QTableWidget.NoEditTriggers)

        # Заполняем таблицу данными
        for row, group in enumerate(groups):
            table.setItem(row, 0, QTableWidgetItem(str(group[0])))  # ID
            table.setItem(row, 1, QTableWidgetItem(group[1]))  # Название

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