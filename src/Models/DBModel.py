import sqlite3
import uuid

class DBModel:
    def __init__(self):
        self.db = sqlite3.connect("src/sqlite/database.db")

    def getAge(self):
        cursor = self.db.cursor()
        rows = cursor.execute("select age from minerva_info").fetchone()
        return rows[0]

    def update_last_shutdown(self,date):
        cursor = self.db.cursor()
        cursor.execute('update minerva_info set last_shutdown=? where id=1',[date])
        self.db.commit()

    def create_reminder(self,text,created_at,remember_in):
        cursor = self.db.cursor()

        id = str(uuid.uuid4())

        cursor.execute('insert into reminder (id,content,created_at,remember_in) values(?,?,?,?)',(id,text,created_at,remember_in))
        self.db.commit()

    def find_in_reminders(self,date):
        cursor = self.db.cursor()

        rows = cursor.execute('select * from reminder where remember_in=?',[date]).fetchall()

        return rows
    