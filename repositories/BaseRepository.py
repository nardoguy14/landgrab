import mysql.connector

class BaseRepository(object):
    def __init__(self):
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="CAMera14",
            database="tinnitus_talks"
        )
        self.cursor = self.mydb.cursor()


    def __enter__(self):
        return self.cursor

    def __exit__(self, a, b, c):
        self.mydb.commit()
        self.cursor.close()
        self.mydb.close()
