import psycopg2
from PyQt5.QtWidgets import QPushButton, QLineEdit, QLabel, QVBoxLayout, QWidget, QMessageBox, QTableWidget, \
    QTableWidgetItem

class AddGradeWindow(QWidget):
    def __init__(self, parent):
        super().__init__()

        self.setWindowTitle('Добавить Оценку')
        self.setGeometry(100, 100, 400, 300)

        self.parent_window = parent  # Ссылка на родительское окно

        layout = QVBoxLayout()

        self.label = QLabel("Введите данные оценки:", self)

        self.student_name_input = QLineEdit(self)
        self.student_name_input.setPlaceholderText('Имя студента')

        self.student_surname_input = QLineEdit(self)
        self.student_surname_input.setPlaceholderText('Фамилия студента')

        self.subject_input = QLineEdit(self)
        self.subject_input.setPlaceholderText('Предмет')

        self.teacher_name_input = QLineEdit(self)
        self.teacher_name_input.setPlaceholderText('Имя преподавателя')

        self.teacher_surname_input = QLineEdit(self)
        self.teacher_surname_input.setPlaceholderText('Фамилия преподавателя')

        self.grade_input = QLineEdit(self)
        self.grade_input.setPlaceholderText('Оценка')

        self.add_button = QPushButton('Добавить', self)
        self.add_button.clicked.connect(self.add_grade_to_db)

        self.update_button = QPushButton('Обновить', self)
        self.update_button.clicked.connect(self.update_grade_to_db)

        self.delete_button = QPushButton('Удалить', self)
        self.delete_button.clicked.connect(self.delete_grade_to_db)

        self.get_grades_button = QPushButton('Посмотреть оценки и студентов', self)
        self.get_grades_button.clicked.connect(self.get_all_grades)

        self.back_button = QPushButton('Назад', self)
        self.back_button.clicked.connect(self.back_to_profile)

        layout.addWidget(self.label)
        layout.addWidget(self.student_name_input)
        layout.addWidget(self.student_surname_input)
        layout.addWidget(self.subject_input)
        layout.addWidget(self.teacher_name_input)
        layout.addWidget(self.teacher_surname_input)
        layout.addWidget(self.grade_input)
        layout.addWidget(self.add_button)
        layout.addWidget(self.update_button)
        layout.addWidget(self.delete_button)
        layout.addWidget(self.get_grades_button)
        layout.addWidget(self.back_button)

        self.setLayout(layout)

    def back_to_profile(self):
        """Возврат в профиль преподавателя"""
        self.parent_window.show()  # Показываем окно профиля
        self.close()  # Закрываем текущее окно

    def add_grade_to_db(self):
        """Добавляет предмет в базу данных."""
        student_name = self.student_name_input.text().strip()
        student_last_name = self.student_surname_input.text().strip()
        subject = self.subject_input.text().strip()
        teacher_name = self.teacher_name_input.text().strip()
        teacher_surname = self.teacher_surname_input.text().strip()
        grade = self.grade_input.text().strip()


        # Проверяем, что название группы не пустое
        if not student_name:
            QMessageBox.warning(self, "Ошибка", "Имя не может быть пустым.")
            return
        if not student_last_name:
            QMessageBox.warning(self, "Ошибка", "Фамилия не может быть пустой.")
            return
        if not subject:
            QMessageBox.warning(self, "Ошибка", "Предмет не может быть пустой.")
            return
        if not teacher_name:
            QMessageBox.warning(self, "Ошибка", "Имя не может быть пустым.")
            return
        if not teacher_surname:
            QMessageBox.warning(self, "Ошибка", "Фамилия не может быть пустой.")
            return
        if not grade:
            QMessageBox.warning(self, "Ошибка", "Оценка не может быть пустой.")
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

            # Подготовка SQL запроса для добавления нового студента
            insert_query = """INSERT INTO public.mark (student_id, subject_id, teacher_id, value)
            VALUES 
            (
	            (SELECT id FROM public.people WHERE first_name = (%s) AND last_name = (%s)),
	            (SELECT id FROM public.subject WHERE name = (%s)),
	            (SELECT id FROM public.people WHERE first_name = (%s) AND last_name = (%s)),
	            (%s)
            );
            """
            cursor.execute(insert_query, (student_name, student_last_name,subject,teacher_name,teacher_surname,grade,))

            # Подтверждаем изменения в базе данных
            connection.commit()

            # Закрываем курсор и соединение
            cursor.close()
            connection.close()

            # Показываем сообщение об успехе
            QMessageBox.information(self, "Успех", f"Оценка '{student_name}' успешно добавлена.")

            # Очищаем поле ввода
            self.student_name_input.clear()
            self.student_surname_input.clear()
            self.subject_input.clear()
            self.teacher_name_input.clear()
            self.teacher_surname_input.clear()
            self.grade_input.clear()

        except Exception as e:
            # В случае ошибки выводим сообщение
            QMessageBox.critical(self, "Ошибка", f"Не удалось добавить оценку: {str(e)}")
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    def update_grade_to_db(self):
        """Изменяет студента в базу данных."""
        student_name = self.student_name_input.text().strip()
        student_last_name = self.student_surname_input.text().strip()
        subject = self.subject_input.text().strip()
        teacher_name = self.teacher_name_input.text().strip()
        teacher_surname = self.teacher_surname_input.text().strip()
        grade = self.grade_input.text().strip()

        # Проверяем, что название группы не пустое
        if not student_name:
            QMessageBox.warning(self, "Ошибка", "Имя не может быть пустым.")
            return
        if not student_last_name:
            QMessageBox.warning(self, "Ошибка", "Фамилия не может быть пустой.")
            return
        if not subject:
            QMessageBox.warning(self, "Ошибка", "Предмет не может быть пустой.")
            return
        if not teacher_name:
            QMessageBox.warning(self, "Ошибка", "Имя не может быть пустым.")
            return
        if not teacher_surname:
            QMessageBox.warning(self, "Ошибка", "Фамилия не может быть пустой.")
            return
        if not grade:
            QMessageBox.warning(self, "Ошибка", "Оценка не может быть пустой.")
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

            # Подготовка SQL запроса для добавления нового студента
            insert_query = """UPDATE public.mark
                    SET value = (%s)
                    WHERE subject_id = (SELECT id FROM public.subject WHERE name = (%s)) AND
                          student_id = (SELECT id FROM public.people WHERE first_name = (%s) AND last_name = (%s)) AND
                          teacher_id = (SELECT id FROM public.people WHERE first_name = (%s) AND last_name = (%s))
                    """
            cursor.execute(insert_query,
                           (grade, subject, student_name, student_last_name, teacher_name, teacher_surname,))

            # Подтверждаем изменения в базе данных
            connection.commit()

            # Закрываем курсор и соединение
            cursor.close()
            connection.close()

            # Показываем сообщение об успехе
            QMessageBox.information(self, "Успех", f"Оценка '{student_name}' успешно изменена.")

            # Очищаем поле ввода
            self.student_name_input.clear()
            self.student_surname_input.clear()
            self.subject_input.clear()
            self.teacher_name_input.clear()
            self.teacher_surname_input.clear()
            self.grade_input.clear()

        except Exception as e:
            # В случае ошибки выводим сообщение
            QMessageBox.critical(self, "Ошибка", f"Не удалось изменить оценку: {str(e)}")
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
                connection.close()

    def delete_grade_to_db(self):
        """Удаляет студента из базы данных."""
        student_name = self.student_name_input.text().strip()
        student_last_name = self.student_surname_input.text().strip()
        subject = self.subject_input.text().strip()
        teacher_name = self.teacher_name_input.text().strip()
        teacher_surname = self.teacher_surname_input.text().strip()
        grade = self.grade_input.text().strip()

        # Проверяем, что название группы не пустое
        if not student_name:
            QMessageBox.warning(self, "Ошибка", "Имя не может быть пустым.")
            return
        if not student_last_name:
            QMessageBox.warning(self, "Ошибка", "Фамилия не может быть пустой.")
            return
        if not subject:
            QMessageBox.warning(self, "Ошибка", "Предмет не может быть пустой.")
            return
        if not teacher_name:
            QMessageBox.warning(self, "Ошибка", "Имя не может быть пустым.")
            return
        if not teacher_surname:
            QMessageBox.warning(self, "Ошибка", "Фамилия не может быть пустой.")
            return
        if not grade:
            QMessageBox.warning(self, "Ошибка", "Оценка не может быть пустой.")
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

            # Подготовка SQL запроса для добавления нового студента
            insert_query = """DELETE FROM public.mark
                    WHERE subject_id = (SELECT id FROM public.subject WHERE name = (%s)) AND
                          student_id = (SELECT id FROM public.people WHERE first_name = (%s) AND last_name = (%s)) AND
                          teacher_id = (SELECT id FROM public.people WHERE first_name = (%s) AND last_name = (%s)) AND
                          value = (%s)
                    """
            cursor.execute(insert_query,
                           (subject, student_name, student_last_name, teacher_name, teacher_surname,grade,))

            # Подтверждаем изменения в базе данных
            connection.commit()

            # Закрываем курсор и соединение
            cursor.close()
            connection.close()

            # Показываем сообщение об успехе
            QMessageBox.information(self, "Успех", f"Оценка '{student_name}' успешно удалена.")

            # Очищаем поле ввода
            self.student_name_input.clear()
            self.student_surname_input.clear()
            self.subject_input.clear()
            self.teacher_name_input.clear()
            self.teacher_surname_input.clear()
            self.grade_input.clear()

        except Exception as e:
            # В случае ошибки выводим сообщение
            QMessageBox.critical(self, "Ошибка", f"Не удалось удалить оценку: {str(e)}")
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    def get_all_grades(self):
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
            select_query = """SELECT CONCAT(public.people.first_name, ' ', public.people.last_name),
	            public.subject.name, public.mark.value
                FROM public.subject
                CROSS JOIN public.people
                LEFT JOIN   
	            public.mark ON public.people.id = public.mark.student_id AND public.subject.id = public.mark.subject_id
                WHERE public.people.type = 'S'
                ORDER BY public.people.first_name, public.subject.name
            """
            cursor.execute(select_query)

            # Извлекаем все строки результата
            grades = cursor.fetchall()

            # Проверяем, есть ли предметы
            if not grades:
                QMessageBox.information(self, "Информация", "Оценки не найдены.")
                return

            # Если необходимо отобразить группы в таблице
            self.show_grades_in_table(grades)

            # Закрываем курсор и соединение
            cursor.close()
            connection.close()

        except Exception as e:
            import traceback
            traceback.print_exc()  # Выводим стек ошибки
            QMessageBox.critical(self, "Ошибка", f"Не удалось получить оценки: {str(e)}")
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    def show_grades_in_table(self, grades):
        """Отображает предметы в таблице."""
        # Создаём таблицу с двумя столбцами: ID и Name
        table = QTableWidget(self)
        table.setRowCount(len(grades))  # Строки для каждого предмета
        table.setColumnCount(3)  # Столбцы для ID и Name
        table.setHorizontalHeaderLabels(['Имя и фамилия', 'Предмет', 'Оценка'])
        table.setEditTriggers(QTableWidget.NoEditTriggers)

        # Заполняем таблицу данными
        for row, subject in enumerate(grades):
            table.setItem(row, 0, QTableWidgetItem(str(subject[0])))
            table.setItem(row, 1, QTableWidgetItem(subject[1]))
            table.setItem(row, 2, QTableWidgetItem(str(subject[2])))


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