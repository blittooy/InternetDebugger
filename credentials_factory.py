import os


class CredentialsFactory:

    def get_env_var(self, variable):
        return os.environ.get(variable, None)

    def get_pi_mysql_db(self):
        dsn = 'host={} dbname={} user={} password={}'.format(
            self.get_env_var('PI_MYSQL_HOST'),
            self.get_env_var('PI_MYSQL_DB_NAME'),
            self.get_env_var('PI_MYSQL_USER'),
            self.get_env_var('PI_MYSQL_PASSWORD'))
        return dsn
