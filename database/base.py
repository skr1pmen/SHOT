import psycopg2


class Database:
    def __init__(self, host, user, password, database):
        try:
            self.connection = psycopg2.connect(
                host=host,
                user=user,
                password=password,
                database=database
            )
            self.connection.autocommit = True
            self.cursor = self.connection.cursor()
            print("Подключение прошло успешно!")
        except psycopg2.Error as e:
            print(f"Ошибка: {e}")

    def execute(self, query):
        try:
            self.cursor.execute(query)
        except psycopg2.Error as e:
            print(f"Ошибка: {e}")

    def fetch(self, query):
        try:
            self.cursor.execute(query)
            result = self.cursor.fetchall()
            return result
        except psycopg2.Error as e:
            print(f"Ошибка: {e}")
            return []


    def __del__(self):
        try:
            self.cursor.close()
            self.connection.close()
            print("Подключение закрыто")
        except psycopg2.Error as e:
            print(f"Ошибка при закрытии: {e}")
