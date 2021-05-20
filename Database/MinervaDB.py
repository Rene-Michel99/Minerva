import sqlite3

class DB:
    def __init__(self):
        self.db = sqlite3.connect("./minervaDB.db")

    def getAge(self):
        cursor = self.db.cursor()
        rows = cursor.execute("select age from minerva_info").fetchone()
        print(rows[0])

    def update_last_shutdown(self,date):
        cursor = self.db.cursor()
        cursor.execute('update minerva_info set last_execution=? where id=1',[date])
        self.db.commit()

db = DB()
db.update_last_shutdown("20/05/2020 10:40")