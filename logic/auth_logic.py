# logic/auth_logic.py
import psycopg2

class AuthLogic:
    def __init__(self, db_config):
        self.db_config = db_config

    def authenticate(self, username, password):
        try:
            connection = psycopg2.connect(**self.db_config)
            cursor = connection.cursor()
            cursor.execute("SELECT role FROM users WHERE username = %s AND password = %s", (username, password))
            result = cursor.fetchone()
            if result:
                return True, result[0]  # Возвращаем роль пользователя
            else:
                return False, None
        except Exception as e:
            print(f"Ошибка при подключении к БД: {e}")
            return False, None
        finally:
            if connection:
                connection.close()
