import psycopg2
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QPushButton, QLineEdit, QLabel, QVBoxLayout, QWidget, QMessageBox, QTableWidget, \
    QTableWidgetItem, QApplication


class AddGroupWindow(QWidget):
    def __init__(self, parent):
        super().__init__()

        self.setWindowTitle('Экран группы')
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

        self.label = QLabel("Введите данные группы:", self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("font-size: 20px; font-weight: bold; color: #333; padding: 10px;")

        self.instruction_label = QLabel("Инструкция:\n"
                            "Для добавления заполните поля без слова <Старое>\n"
                            "Для удаления заполните поля со словом <Старое>\n"
                            "Для обновления заполните все поля на экране", self)
        self.instruction_label.setAlignment(Qt.AlignCenter)
        self.instruction_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #333; padding: 10px;")

        self.group_name_input = QLineEdit(self)
        self.group_name_input.setPlaceholderText('Название группы')

        self.old_group_name_input = QLineEdit(self)
        self.old_group_name_input.setPlaceholderText('Старое название группы')

        self.add_button = QPushButton('Добавить', self)
        self.add_button.setStyleSheet(button_style)
        self.add_button.clicked.connect(self.add_group_to_db)

        self.change_button = QPushButton('Изменить', self)
        self.change_button.setStyleSheet(button_style)
        self.change_button.clicked.connect(self.update_group_in_db)

        self.delete_button = QPushButton('Удалить', self)
        self.delete_button.setStyleSheet("background-color: #f44336; color: white; font-size: 14px; padding: 10px; border-radius: 5px;")
        self.delete_button.clicked.connect(self.delete_group_from_db)

        self.get_button = QPushButton('Посмотреть все группы', self)
        self.get_button.setStyleSheet(button_style)
        self.get_button.clicked.connect(self.get_all_groups)

        self.back_button = QPushButton('Назад', self)
        self.back_button.setStyleSheet("background-color: #f44336; color: white; font-size: 14px; padding: 10px; border-radius: 5px;")
        self.back_button.clicked.connect(self.back_to_profile)

        layout.addWidget(self.label)
        layout.addWidget(self.instruction_label)
        layout.addWidget(self.group_name_input)
        layout.addWidget(self.old_group_name_input)
        layout.addWidget(self.add_button)
        layout.addWidget(self.change_button)
        layout.addWidget(self.delete_button)
        layout.addWidget(self.get_button)
        layout.addWidget(self.back_button)

        self.setLayout(layout)

    def back_to_profile(self):
        """Возврат в профиль"""
        self.parent_window.show()
        self.close()

    def add_group_to_db(self):
        """Добавляет группу в базу данных."""
        group_name = self.group_name_input.text().strip()

        if not group_name:
            QMessageBox.warning(self, "Ошибка", "Название группы не может быть пустым.")
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

            insert_query = "INSERT INTO public.group (name) VALUES (%s)"
            cursor.execute(insert_query, (group_name,))

            connection.commit()

            cursor.close()
            connection.close()
            QMessageBox.information(self, "Успех", f"Группа '{group_name}' успешно добавлена.")

            self.group_name_input.clear()

        except Exception as e:
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

        if not old_group_name or not new_group_name:
            QMessageBox.warning(self, "Ошибка", "Названия групп не могут быть пустыми.")
            return

        try:
            connection = psycopg2.connect(
                dbname="university",  # Замените на название вашей базы данных
                user="postgres",  # Замените на ваше имя пользователя
                password="s46825710",  # Замените на ваш пароль
                host="localhost",  # Замените на хост, если нужно
                port="5432"  # Порт по умолчанию для PostgreSQL
            )
            cursor = connection.cursor()

            update_query = """
                    UPDATE public.group
                    SET name = (%s)
                    WHERE name = (%s);
                """

            cursor.execute(update_query, (new_group_name, old_group_name))

            connection.commit()

            if cursor.rowcount == 0:
                QMessageBox.information(self, "Информация", f"Группы с именем '{old_group_name}' не найдены.")
            else:
                QMessageBox.information(self, "Успех",
                                        f"Группа успешно изменена с '{old_group_name}' на '{new_group_name}'.")

            cursor.close()
            connection.close()

            self.group_name_input.clear()
            self.old_group_name_input.clear()

        except Exception as e:
            import traceback
            traceback.print_exc()
            QMessageBox.critical(self, "Ошибка", f"Не удалось изменить группу: {str(e)}")
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    def delete_group_from_db(self, ):
        """Удаляет группу из базы данных."""
        old_group_name = self.old_group_name_input.text().strip()

        if not old_group_name:
            QMessageBox.warning(self, "Ошибка", "Название группы не может быть пустым.")
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

            delete_query = "DELETE FROM public.group WHERE name = %s"

            cursor.execute(delete_query, (old_group_name,))

            connection.commit()

            if cursor.rowcount == 0:
                QMessageBox.information(self, "Информация", f"Группа '{old_group_name}' не найдена.")
            else:
                QMessageBox.information(self, "Успех", f"Группа '{old_group_name}' успешно удалена.")

            cursor.close()
            connection.close()

            self.old_group_name_input.clear()

        except Exception as e:
            import traceback
            traceback.print_exc()
            QMessageBox.critical(self, "Ошибка", f"Не удалось удалить группу: {str(e)}")
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()


    def get_all_groups(self):
        """Возвращает все группы и их ID из базы данных."""
        try:
            connection = psycopg2.connect(
                dbname="university",
                user="postgres",
                password="s46825710",
                host="localhost",
                port="5432"
            )
            cursor = connection.cursor()

            select_query = "SELECT id, name FROM public.group"
            cursor.execute(select_query)

            groups = cursor.fetchall()

            if not groups:
                QMessageBox.information(self, "Информация", "Группы не найдены.")
                return

            self.show_groups_in_table(groups)

            cursor.close()
            connection.close()

        except Exception as e:
            import traceback
            traceback.print_exc()
            QMessageBox.critical(self, "Ошибка", f"Не удалось получить группы: {str(e)}")
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    def show_groups_in_table(self, groups):
        """Отображает группы в таблице."""
        table = QTableWidget(self)
        table.setRowCount(len(groups))
        table.setColumnCount(2)
        table.setHorizontalHeaderLabels(['ID', 'Название'])
        table.setEditTriggers(QTableWidget.NoEditTriggers)

        for row, group in enumerate(groups):
            table.setItem(row, 0, QTableWidgetItem(str(group[0])))
            table.setItem(row, 1, QTableWidgetItem(group[1]))

        table.setColumnWidth(0, QApplication.primaryScreen().size().width() // 2)
        table.setColumnWidth(1, QApplication.primaryScreen().size().width() // 2)

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