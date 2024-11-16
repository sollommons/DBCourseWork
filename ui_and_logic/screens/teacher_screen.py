import psycopg2
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QPushButton, QLineEdit, QLabel, QVBoxLayout, QWidget, QMessageBox, QTableWidget, \
    QTableWidgetItem, QApplication


class AddTeacherWindow(QWidget):
    def __init__(self, parent):
        super().__init__()

        self.setWindowTitle('Экран преподавателя')
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

        self.label = QLabel("Введите данные преподавателя:", self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("font-size: 20px; font-weight: bold; color: #333; padding: 10px;")

        self.instruction_label = QLabel("Инструкция:\n"
                                        "Для добавления заполните поля без слов <Старое/Старая>\n"
                                        "Для удаление заполните поля со словами <Старое/Старая>\n"
                                        "Для обновления заполните все поля на экране", self)
        self.instruction_label.setAlignment(Qt.AlignCenter)
        self.instruction_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #333; padding: 10px;")

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
        self.add_button.setStyleSheet(button_style)
        self.add_button.clicked.connect(self.add_teacher_to_db)

        self.update_button = QPushButton('Обновить', self)
        self.update_button.setStyleSheet(button_style)
        self.update_button.clicked.connect(self.update_teacher_to_db)

        self.delete_button = QPushButton('Удалить', self)
        self.delete_button.setStyleSheet("background-color: #f44336; color: white; font-size: 14px; padding: 10px; border-radius: 5px;")
        self.delete_button.clicked.connect(self.delete_teacher_to_db)

        self.get_teachers_button = QPushButton('Посмотреть всех преподавателей', self)
        self.get_teachers_button.setStyleSheet(button_style)
        self.get_teachers_button.clicked.connect(self.get_all_teachers)

        self.back_button = QPushButton('Назад', self)
        self.back_button.setStyleSheet("background-color: #f44336; color: white; font-size: 14px; padding: 10px; border-radius: 5px;")
        self.back_button.clicked.connect(self.back_to_profile)

        layout.addWidget(self.label)
        layout.addWidget(self.instruction_label)
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
        self.parent_window.show()
        self.close()

    def add_teacher_to_db(self):
        """Добавляет преподавателя в базу данных."""
        teacher_name = self.first_name_input.text().strip()
        teacher_last_name = self.last_name_input.text().strip()
        teacher_father_name = self.father_name_input.text().strip()

        if not teacher_name:
            QMessageBox.warning(self, "Ошибка", "Имя не может быть пустым.")
            return
        if not teacher_last_name:
            QMessageBox.warning(self, "Ошибка", "Фамилия не может быть пустой.")
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

            insert_query = """INSERT INTO public.people (first_name, last_name, father_name, group_id, type)
            VALUES 
            ((%s), (%s), (%s), null, 'T') 
            """
            cursor.execute(insert_query, (teacher_name, teacher_last_name,teacher_father_name,))

            connection.commit()

            cursor.close()
            connection.close()

            QMessageBox.information(self, "Успех", f"Преподаватель '{teacher_name}' успешно добавлен.")

            self.first_name_input.clear()
            self.last_name_input.clear()
            self.father_name_input.clear()

        except Exception as e:
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
            connection = psycopg2.connect(
                dbname="university",
                user="postgres",
                password="s46825710",
                host="localhost",
                port="5432"
            )
            cursor = connection.cursor()
            insert_query = """UPDATE public.people 
              SET first_name = (%s),
                  last_name = (%s),
                  father_name = (%s)
              WHERE first_name = (%s) AND last_name = (%s)
            """
            cursor.execute(insert_query, (teacher_name, teacher_last_name, teacher_father_name, old_name, old_last_name,))

            connection.commit()

            cursor.close()
            connection.close()

            QMessageBox.information(self, "Успех", f"Преподаватель '{teacher_name}' успешно изменен.")

            self.first_name_input.clear()
            self.last_name_input.clear()
            self.father_name_input.clear()
            self.old_first_name_input.clear()
            self.old_last_name_input.clear()
            self.old_father_name_input.clear()

        except Exception as e:
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

        if not teacher_name:
            QMessageBox.warning(self, "Ошибка", "Имя не может быть пустым.")
            return
        if not teacher_last_name:
            QMessageBox.warning(self, "Ошибка", "Фамилия не может быть пустой.")
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

            insert_query = """DELETE FROM public.people 
                WHERE first_name = (%s) AND last_name = (%s)
             """
            cursor.execute(insert_query, (teacher_name, teacher_last_name))

            connection.commit()

            cursor.close()
            connection.close()

            QMessageBox.information(self, "Успех", f"Преподавель '{teacher_name}' успешно удален.")

            self.old_first_name_input.clear()
            self.old_last_name_input.clear()
            self.old_father_name_input.clear()

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось удалить преподавтеля: {str(e)}")
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

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