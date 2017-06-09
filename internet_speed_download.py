import pyspeedtest
import sqlite3
import datetime
import logging
from time import sleep


class DownloadInternetSpeed():
    def __init__(self, db_name='internet_speed.db',
                 table='Internet_Speed', log_name='internet_speed.log',
                 sleep_time=3):
        logging.basicConfig(filename=log_name, level=logging.INFO)
        self.db_name = db_name
        self.table = table
        self.sleep_time = sleep_time
        self.speed_test_api = pyspeedtest.SpeedTest()
        self.make_sqlite_table()
        self.run_speed_test()

    def run_speed_test(self):
        records = []
        count = 0
        while True:
            fail_count = 0
            data = self.get_data()
            logging.error("Data: {}".format(data))
            records.append(data)
            count += 1
            if count % 5 == 0:
                self.upload_data_to_db(records)
                records = []
            sleep(self.sleep_time)

    def make_sqlite_table(self):
        conn = sqlite3.connect('internet_speed.db')
        c = conn.cursor()
        column_query = ("(date text, ping real, download_speed real, "
                        "upload_speed real)")
        query = ("Create Table Internet_Speed {}".format(column_query))
        try:
            c.execute(query)
            logging.info("table: " + self.table + " for "
                         + self.db_name + " created")
        except sqlite3.OperationalError:
            logging.info("table: {} allready exists".format(self.db_name))
        conn.close()

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

    def upload_data_to_db(self, records):
        try:
            logging.info('inserting facts in to db')
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            c.executemany('INSERT INTO {} VALUES (?,?,?,?)'.format(self.table),
                          records)
            conn.commit()
            conn.close()
        except Exception as err:
            logging.error(err)
            logging.error(records)
