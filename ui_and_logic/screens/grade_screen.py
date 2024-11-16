import psycopg2
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QPushButton, QLineEdit, QLabel, QVBoxLayout, QWidget, QMessageBox, QTableWidget, \
    QTableWidgetItem, QApplication


class AddGradeWindow(QWidget):
    def __init__(self, parent):
        super().__init__()

        self.setWindowTitle('Экран оценки')
        self.setFixedSize(QApplication.primaryScreen().size().width(),QApplication.primaryScreen().size().height()-100)

        self.parent_window = parent  # Ссылка на родительское окно

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

        self.label = QLabel("Введите данные оценки:", self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("font-size: 20px; font-weight: bold; color: #333; padding: 10px;")

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
        self.add_button.setStyleSheet(button_style)
        self.add_button.clicked.connect(self.add_grade_to_db)

        self.update_button = QPushButton('Обновить', self)
        self.update_button.setStyleSheet(button_style)
        self.update_button.clicked.connect(self.update_grade_to_db)

        self.delete_button = QPushButton('Удалить', self)
        self.delete_button.setStyleSheet("background-color: #f44336; color: white; font-size: 14px; padding: 10px; border-radius: 5px;")
        self.delete_button.clicked.connect(self.delete_grade_to_db)

        self.get_grades_button = QPushButton('Посмотреть оценки и студентов', self)
        self.get_grades_button.setStyleSheet(button_style)
        self.get_grades_button.clicked.connect(self.get_all_grades)

        self.back_button = QPushButton('Назад', self)
        self.back_button.setStyleSheet("background-color: #f44336; color: white; font-size: 14px; padding: 10px; border-radius: 5px;")
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
        """Возврат в профиль"""
        self.parent_window.show()
        self.close()

    def add_grade_to_db(self):
        """Добавляет оценку в базу данных."""
        student_name = self.student_name_input.text().strip()
        student_last_name = self.student_surname_input.text().strip()
        subject = self.subject_input.text().strip()
        teacher_name = self.teacher_name_input.text().strip()
        teacher_surname = self.teacher_surname_input.text().strip()
        grade = self.grade_input.text().strip()

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
            connection = psycopg2.connect(
                dbname="university",
                user="postgres",
                password="s46825710",
                host="localhost",
                port="5432"
            )
            cursor = connection.cursor()

            insert_query = """INSERT INTO public.mark (student_id, subject_id, teacher_id, value)
            VALUES 
            (
	            (SELECT id FROM public.people WHERE first_name = (%s) AND last_name = (%s) AND type = 'S'),
	            (SELECT id FROM public.subject WHERE name = (%s)),
	            (SELECT id FROM public.people WHERE first_name = (%s) AND last_name = (%s) AND type = 'T'),
	            (%s)
            );
            """
            cursor.execute(insert_query, (student_name, student_last_name,subject,teacher_name,teacher_surname,grade,))
            connection.commit()
            cursor.close()
            connection.close()
            QMessageBox.information(self, "Успех", f"Оценка '{student_name}' успешно добавлена.")

            # Очищаем поле ввода
            self.student_name_input.clear()
            self.student_surname_input.clear()
            self.subject_input.clear()
            self.teacher_name_input.clear()
            self.teacher_surname_input.clear()
            self.grade_input.clear()

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось добавить оценку: {str(e)}")
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    def update_grade_to_db(self):
        """Изменяет оценку в базе данных."""
        student_name = self.student_name_input.text().strip()
        student_last_name = self.student_surname_input.text().strip()
        subject = self.subject_input.text().strip()
        teacher_name = self.teacher_name_input.text().strip()
        teacher_surname = self.teacher_surname_input.text().strip()
        grade = self.grade_input.text().strip()

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
            connection = psycopg2.connect(
                dbname="university",
                user="postgres",
                password="s46825710",
                host="localhost",
                port="5432"
            )
            cursor = connection.cursor()
            insert_query = """UPDATE public.mark
                    SET value = (%s)
                    WHERE subject_id = (SELECT id FROM public.subject WHERE name = (%s)) AND
                          student_id = (SELECT id FROM public.people WHERE first_name = (%s) AND last_name = (%s)) AND
                          teacher_id = (SELECT id FROM public.people WHERE first_name = (%s) AND last_name = (%s))
                    """
            cursor.execute(insert_query,
                           (grade, subject, student_name, student_last_name, teacher_name, teacher_surname,))
            connection.commit()
            cursor.close()
            connection.close()
            QMessageBox.information(self, "Успех", f"Оценка '{student_name}' успешно изменена.")

            # Очищаем поле ввода
            self.student_name_input.clear()
            self.student_surname_input.clear()
            self.subject_input.clear()
            self.teacher_name_input.clear()
            self.teacher_surname_input.clear()
            self.grade_input.clear()

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось изменить оценку: {str(e)}")
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
                connection.close()

    def delete_grade_to_db(self):
        """Удаляет оценку из базы данных."""
        student_name = self.student_name_input.text().strip()
        student_last_name = self.student_surname_input.text().strip()
        subject = self.subject_input.text().strip()
        teacher_name = self.teacher_name_input.text().strip()
        teacher_surname = self.teacher_surname_input.text().strip()
        grade = self.grade_input.text().strip()

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
            connection = psycopg2.connect(
                dbname="university",
                user="postgres",
                password="s46825710",
                host="localhost",
                port="5432"
            )
            cursor = connection.cursor()

            insert_query = """DELETE FROM public.mark
                    WHERE subject_id = (SELECT id FROM public.subject WHERE name = (%s)) AND
                          student_id = (SELECT id FROM public.people WHERE first_name = (%s) AND last_name = (%s)) AND
                          teacher_id = (SELECT id FROM public.people WHERE first_name = (%s) AND last_name = (%s)) AND
                          value = (%s)
                    """
            cursor.execute(insert_query,
                           (subject, student_name, student_last_name, teacher_name, teacher_surname,grade,))

            connection.commit()
            cursor.close()
            connection.close()
            QMessageBox.information(self, "Успех", f"Оценка '{student_name}' успешно удалена.")

            # Очищаем поле ввода
            self.student_name_input.clear()
            self.student_surname_input.clear()
            self.subject_input.clear()
            self.teacher_name_input.clear()
            self.teacher_surname_input.clear()
            self.grade_input.clear()

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось удалить оценку: {str(e)}")
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    def get_all_grades(self):
        """Возвращает всех студентов и их оценки из базы данных."""
        try:
            connection = psycopg2.connect(
                dbname="university",
                user="postgres",
                password="s46825710",
                host="localhost",
                port="5432"
            )
            cursor = connection.cursor()
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
            grades = cursor.fetchall()
            if not grades:
                QMessageBox.information(self, "Информация", "Оценки не найдены.")
                return
            self.show_grades_in_table(grades)
            cursor.close()
            connection.close()

        except Exception as e:
            import traceback
            traceback.print_exc()
            QMessageBox.critical(self, "Ошибка", f"Не удалось получить оценки: {str(e)}")
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    def show_grades_in_table(self, grades):
        """Отображает в таблице."""
        table = QTableWidget(self)
        table.setRowCount(len(grades))
        table.setColumnCount(3)
        table.setHorizontalHeaderLabels(['Имя и фамилия', 'Предмет', 'Оценка'])
        table.setEditTriggers(QTableWidget.NoEditTriggers)

        for row, subject in enumerate(grades):
            table.setItem(row, 0, QTableWidgetItem(str(subject[0])))
            table.setItem(row, 1, QTableWidgetItem(subject[1]))
            table.setItem(row, 2, QTableWidgetItem(str(subject[2])))

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