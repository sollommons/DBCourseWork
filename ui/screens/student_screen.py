import psycopg2
from PyQt5.QtWidgets import QPushButton, QLineEdit, QLabel, QVBoxLayout, QWidget, QMessageBox, QTableWidget, \
    QTableWidgetItem

class AddStudentWindow(QWidget):
    def __init__(self, parent):
        super().__init__()

        self.setWindowTitle('Экран студента')
        self.setGeometry(100, 100, 400, 300)

        self.parent_window = parent

        layout = QVBoxLayout()

        self.label = QLabel("Введите данные студента:", self)

        self.first_name_input = QLineEdit(self)
        self.first_name_input.setPlaceholderText('Имя')

        self.last_name_input = QLineEdit(self)
        self.last_name_input.setPlaceholderText('Фамилия')

        self.father_name_input = QLineEdit(self)
        self.father_name_input.setPlaceholderText('Отчество')

        self.group_input = QLineEdit(self)
        self.group_input.setPlaceholderText('Группа')

        self.old_first_name_input = QLineEdit(self)
        self.old_first_name_input.setPlaceholderText('Старое имя')

        self.old_last_name_input = QLineEdit(self)
        self.old_last_name_input.setPlaceholderText('Старая фамилия')

        self.old_father_name_input = QLineEdit(self)
        self.old_father_name_input.setPlaceholderText('Старое отчество')

        self.old_group_input = QLineEdit(self)
        self.old_group_input.setPlaceholderText('Старая группа')

        self.add_button = QPushButton('Добавить', self)
        self.add_button.clicked.connect(self.add_student_to_db)

        self.update_button = QPushButton('Обновить', self)
        self.update_button.clicked.connect(self.update_student_to_db)

        self.delete_button = QPushButton('Удалить', self)
        self.delete_button.clicked.connect(self.delete_student_to_db)

        self.get_students_button = QPushButton('Посмотреть всех студентов', self)
        self.get_students_button.clicked.connect(self.get_all_students)

        self.back_button = QPushButton('Назад', self)
        self.back_button.clicked.connect(self.back_to_profile)

        layout.addWidget(self.label)
        layout.addWidget(self.first_name_input)
        layout.addWidget(self.last_name_input)
        layout.addWidget(self.father_name_input)
        layout.addWidget(self.group_input)
        layout.addWidget(self.old_first_name_input)
        layout.addWidget(self.old_last_name_input)
        layout.addWidget(self.old_father_name_input)
        layout.addWidget(self.old_group_input)
        layout.addWidget(self.add_button)
        layout.addWidget(self.update_button)
        layout.addWidget(self.delete_button)
        layout.addWidget(self.get_students_button)
        layout.addWidget(self.back_button)

        self.setLayout(layout)

    def back_to_profile(self):
        """Возврат в профиль"""
        self.parent_window.show()
        self.close()

    def add_student_to_db(self):
        """Добавляет студента в базу данных."""
        student_name = self.first_name_input.text().strip()
        student_last_name = self.last_name_input.text().strip()
        student_father_name = self.father_name_input.text().strip()
        group = self.group_input.text().strip()

        if not student_name:
            QMessageBox.warning(self, "Ошибка", "Имя не может быть пустым.")
            return
        if not student_last_name:
            QMessageBox.warning(self, "Ошибка", "Фамилия не может быть пустой.")
            return
        if not group:
            QMessageBox.warning(self, "Ошибка", "Группа не может быть пустой.")
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
            ((%s), (%s), (%s), (SELECT id FROM public.group WHERE name = (%s)), 'S') 
            """
            cursor.execute(insert_query, (student_name, student_last_name,student_father_name,group,))

            connection.commit()

            cursor.close()
            connection.close()

            QMessageBox.information(self, "Успех", f"Студент '{student_name}' успешно добавлен.")

            self.first_name_input.clear()
            self.last_name_input.clear()
            self.father_name_input.clear()
            self.group_input.clear()


        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось добавить студента: {str(e)}")
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    def update_student_to_db(self):
        """Изменяет студента в базе данных."""
        student_name = self.first_name_input.text().strip()
        student_last_name = self.last_name_input.text().strip()
        student_father_name = self.father_name_input.text().strip()
        group = self.group_input.text().strip()
        old_name = self.old_first_name_input.text().strip()
        old_last_name = self.old_last_name_input.text().strip()
        old_father_name = self.old_father_name_input.text().strip()
        old_group = self.old_group_input.text().strip()

        if not student_name:
            QMessageBox.warning(self, "Ошибка", "Имя не может быть пустым.")
            return
        if not student_last_name:
            QMessageBox.warning(self, "Ошибка", "Фамилия не может быть пустой.")
            return
        if not group:
            QMessageBox.warning(self, "Ошибка", "Группа не может быть пустой.")
            return
        if not old_name:
            QMessageBox.warning(self, "Ошибка", "Имя не может быть пустым.")
            return
        if not old_last_name:
            QMessageBox.warning(self, "Ошибка", "Фамилия не может быть пустой.")
            return
        if not old_group:
            QMessageBox.warning(self, "Ошибка", "Группа не может быть пустой.")
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
                  father_name = (%s),
                  group_id = (SELECT id FROM public.group WHERE name = (%s))
              WHERE first_name = (%s) AND last_name = (%s)
            """
            cursor.execute(insert_query, (student_name, student_last_name, student_father_name, group, old_name, old_last_name,))

            connection.commit()

            cursor.close()
            connection.close()

            QMessageBox.information(self, "Успех", f"Студент '{student_name}' успешно изменен.")

            self.first_name_input.clear()
            self.last_name_input.clear()
            self.father_name_input.clear()
            self.group_input.clear()
            self.old_first_name_input.clear()
            self.old_last_name_input.clear()
            self.old_father_name_input.clear()
            self.old_group_input.clear()

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось изменить студента: {str(e)}")
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    def delete_student_to_db(self):
        """Удаляет студента из базы данных."""
        student_name = self.old_first_name_input.text().strip()
        student_last_name = self.old_last_name_input.text().strip()
        student_father_name = self.old_father_name_input.text().strip()
        group = self.old_group_input.text().strip()

        if not student_name:
            QMessageBox.warning(self, "Ошибка", "Имя не может быть пустым.")
            return
        if not student_last_name:
            QMessageBox.warning(self, "Ошибка", "Фамилия не может быть пустой.")
            return
        if not group:
            QMessageBox.warning(self, "Ошибка", "Группа не может быть пустой.")
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
            cursor.execute(insert_query, (student_name, student_last_name))

            connection.commit()

            cursor.close()
            connection.close()

            QMessageBox.information(self, "Успех", f"Студент '{student_name}' успешно удален.")

            self.old_first_name_input.clear()
            self.old_last_name_input.clear()
            self.old_father_name_input.clear()
            self.old_group_input.clear()

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось удалить студента: {str(e)}")
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

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


        close_button = QPushButton('Закрыть', table)
        close_button.clicked.connect(table.close)

        layout = QVBoxLayout(table)
        layout.addWidget(table)
        layout.addWidget(close_button)

        table.setLayout(layout)

        table.resize(400, 300)
        table.show()