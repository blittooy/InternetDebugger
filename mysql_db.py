from mysql.connector import MySQLConnection
from mysql.connector import errors

from credentials_factory import CredentialsFactory


class MySQLDB:

    def __init__(self, dsn):
        self.set_connection(dsn)

    def set_connection(self, dsn):
        try:
            self.connection = MySQLConnection(**dsn)
        except (errors.InterfaceError):
            print("Couldn't connect to the database,"
                  " check your DSN credentials.")

    @staticmethod
    def pi_mysql_db():
        return MySQLDB(CredentialsFactory().get_pi_mysql_db_dsn())

    def get_data(self, query, raise_when_no_data=True):
        cursor = self.connection.cursor()
        data = self.fetch_query(cursor, query, raise_when_no_data)
        return data

    def fetch_query(self, cursor, query):
        cursor.execute(query)
        data = cursor.fetchall()
        return data

    def execute_query(self, query):
        self.connection.cursor().execute(query)
        self.connection.commit()

    def execute_values_query(self, query, values):
        self.connection.cursor().execute(query, values)
        self.connection.commit()
