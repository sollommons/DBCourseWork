import psycopg2
from PyQt5.QtWidgets import QPushButton, QLineEdit, QLabel, QVBoxLayout, QWidget, QMessageBox, QTableWidget, \
    QTableWidgetItem


class AddSubWindow(QWidget):
    def __init__(self, parent):
        super().__init__()

        self.setWindowTitle('Экран предмета')
        self.setGeometry(100, 100, 400, 300)

        self.parent_window = parent

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
        """Возврат в профиль """
        self.parent_window.show()
        self.close()

    def add_subject_to_db(self):
        """Добавляет предмет в базу данных."""
        subject_name = self.subject_name_input.text().strip()

        if not subject_name:
            QMessageBox.warning(self, "Ошибка", "Название предмета не может быть пустым.")
            return

        try:
            connection = psycopg2.connect(
                dbname="university",
                user="postgres",
                password="s46825710",
                host="localhost",
                port="5432"
            )
            cursor = connection.cursor()

            insert_query = "INSERT INTO public.subject (name) VALUES (%s)"
            cursor.execute(insert_query, (subject_name,))

            connection.commit()

            cursor.close()
            connection.close()

            QMessageBox.information(self, "Успех", f"Предмет '{subject_name}' успешно добавлен.")

            self.subject_name_input.clear()

        except Exception as e:
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

        if not old_subject_name or not new_subject_name:
            QMessageBox.warning(self, "Ошибка", "Названия предметов не могут быть пустыми.")
            return

        try:
            connection = psycopg2.connect(
                dbname="university",
                user="postgres",
                password="s46825710",
                host="localhost",
                port="5432"
            )
            cursor = connection.cursor()

            update_query = """
                    UPDATE public.subject
                    SET name = (%s)
                    WHERE name = (%s);
                """

            cursor.execute(update_query, (new_subject_name, old_subject_name))

            connection.commit()

            if cursor.rowcount == 0:
                QMessageBox.information(self, "Информация", f"Предмет с именем '{old_subject_name}' не найдены.")
            else:
                QMessageBox.information(self, "Успех",
                                        f"Предмет успешно изменен с '{old_subject_name}' на '{new_subject_name}'.")

            cursor.close()
            connection.close()

        except Exception as e:
            import traceback
            traceback.print_exc()
            QMessageBox.critical(self, "Ошибка", f"Не удалось изменить предмет: {str(e)}")
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    def delete_subject_from_db(self, ):
        """Удаляет предмет из базы данных."""
        old_subject_name = self.old_subject_name_input.text().strip()

        if not old_subject_name:
            QMessageBox.warning(self, "Ошибка", "Название предмета не может быть пустым.")
            return

        try:
            connection = psycopg2.connect(
                dbname="university",
                user="postgres",
                password="s46825710",
                host="localhost",
                port="5432"
            )
            cursor = connection.cursor()

            delete_query = "DELETE FROM public.subject WHERE name = %s"

            cursor.execute(delete_query, (old_subject_name,))

            connection.commit()

            if cursor.rowcount == 0:
                QMessageBox.information(self, "Информация", f"Предмет '{old_subject_name}' не найден.")
            else:
                QMessageBox.information(self, "Успех", f"Предмет '{old_subject_name}' успешно удален.")

            cursor.close()
            connection.close()

        except Exception as e:
            import traceback
            traceback.print_exc()
            QMessageBox.critical(self, "Ошибка", f"Не удалось удалить предмет: {str(e)}")
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()


    def get_all_subjects(self):
        """Возвращает все предметы и их ID из базы данных."""
        try:
            connection = psycopg2.connect(
                dbname="university",
                user="postgres",
                password="s46825710",
                host="localhost",
                port="5432"
            )
            cursor = connection.cursor()

            select_query = "SELECT id, name FROM public.subject"
            cursor.execute(select_query)

            subjects = cursor.fetchall()

            if not subjects:
                QMessageBox.information(self, "Информация", "Группы не найдены.")
                return

            self.show_subjects_in_table(subjects)

            cursor.close()
            connection.close()

        except Exception as e:
            import traceback
            traceback.print_exc()
            QMessageBox.critical(self, "Ошибка", f"Не удалось получить предметы: {str(e)}")
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    def show_subjects_in_table(self, subjects):
        """Отображает предметы в таблице."""
        table = QTableWidget(self)
        table.setRowCount(len(subjects))
        table.setColumnCount(2)
        table.setHorizontalHeaderLabels(['ID', 'Название'])
        table.setEditTriggers(QTableWidget.NoEditTriggers)

        for row, subject in enumerate(subjects):
            table.setItem(row, 0, QTableWidgetItem(str(subject[0])))
            table.setItem(row, 1, QTableWidgetItem(subject[1]))

        close_button = QPushButton('Закрыть', table)
        close_button.clicked.connect(table.close)

        layout = QVBoxLayout(table)
        layout.addWidget(table)
        layout.addWidget(close_button)

        table.setLayout(layout)

        table.resize(400, 300)
        table.show()