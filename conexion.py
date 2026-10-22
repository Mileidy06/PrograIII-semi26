import mysql.connector
from mysql.connector import Error

class DatabaseConnection:
    def __init__(self):
        self.config = {
            'host': 'localhost',
            'user': 'root',
            'password': '',
            'database': 'db_sistema_impuestos',
            'raise_on_warnings': True
        }
        self._conn = None

    def get_connection(self):
        try:
            if self._conn is None or not self._conn.is_connected():
                self._conn = mysql.connector.connect(**self.config)
            return self._conn
        except Error as err:
            print(f"Error crítico de conexión MySQL: {err}")
            return None

    def execute_query(self, query, params=None):
        connection = self.get_connection()
        if not connection:
            return []
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query, params or ())
            result = cursor.fetchall()
            cursor.close()
            return result
        except Error as err:
            print(f"Error al ejecutar consulta SELECT: {err}")
            return []

    def execute_statement(self, query, params=None):
        connection = self.get_connection()
        if not connection:
            return "Error de conexión"
        try:
            cursor = connection.cursor()
            cursor.execute(query, params or ())
            connection.commit()
            cursor.close()
            return "ok"
        except Error as err:
            if connection.is_connected():
                connection.rollback()
            return f"Error: {err}"