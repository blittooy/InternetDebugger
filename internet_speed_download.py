import pyspeedtest
from mysql_db import MySQLDB
import datetime
import logging
from time import sleep


class DownloadInternetSpeed():
    def __init__(self, log_name='internet_speed.log',
                 sleep_time=3):
        logging.basicConfig(filename=log_name, level=logging.INFO)
        self.db = MySQLDB.pi_mysql_db()
        self.sleep_time = sleep_time
        self.speed_test_api = pyspeedtest.SpeedTest()
        self.make_mysql_table()
        self.run_speed_test()

    def run_speed_test(self):
        count = 0
        while True:
            fail_count = 0
            data = self.get_data()
            logging.info("Data: {}".format(data))
            count += 1
            self.upload_data_to_db(data)
            sleep(self.sleep_time)

    def make_mysql_table(self):
        query = ("CREATE TABLE internet_speed ("
                 " time datetime Not Null, "
                 " ping real Not Null, "
                 " download_speed real Not Null,"
                 " upload_speed real Not Null,"
                 " Primary Key(time));"
                 )
        try:
            self.db.execute_query(query)
            logging.info("table: internet_speed created")
        except Exception:
            logging.info("table: internet_speed allready exists")

    def get_data(self):
        timestamp = str(datetime.datetime.now())
        try:
            download_speed = self.speed_test_api.download()/1000000
            upload_speed = self.speed_test_api.upload()/1000000
            ping = self.speed_test_api.ping()
            return (timestamp, ping, download_speed, upload_speed)
        except Exception as err:
            logging.error("No data dl error: {}".format(err))
            return (timestamp, 0, 0, 0)

    def upload_data_to_db(self, data):
        try:
            logging.info('inserting facts in to db')
            insert_query = ("INSERT INTO internet_speed "
                            "(time, ping, download_speed, upload_speed) "
                            "VALUES (%s, %s, %s, %s)")
            self.db.execute_values_query(insert_query, data)
        except Exception as err:
            logging.error(err)
