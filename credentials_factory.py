import os


class CredentialsFactory:

    def get_env_var(self, variable):
        return os.environ.get(variable, None)

    def get_pi_mysql_db_dsn(self):
        dsn = {"host": self.get_env_var('PI_MYSQL_HOST'),
               "database": self.get_env_var('PI_MYSQL_DB_NAME'),
               "user": self.get_env_var('PI_MYSQL_USER'),
               "password": self.get_env_var('PI_MYSQL_PASSWORD')}
        return dsn
