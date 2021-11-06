import sqlite3
from builtins import set


class DB:
    def __init__(self):
        self.db = sqlite3.connect('data.sqlite3')
        self.cursor = self.db.cursor()
        sql = """CREATE TABLE IF NOT EXISTS `student` (
                `id` INTEGER PRIMARY KEY,
                `name` TEXT NOT NULL,
                `class` TEXT NOT NULL,
                `sex` TEXT NOT NULL,
                `phone` TEXT
            );"""
        self.cursor.execute(sql)
        self.db.commit()

    def insert(self, dict):
        self.cursor = self.db.cursor()
        sql = f"""INSERT INTO `student` (`name`, `class`, `sex`, `phone`) 
                VALUES ('{dict['name']}', '{dict['class']}', 
                '{dict['sex']}', '{dict['phone']}')"""
        print(sql)
        self.cursor.execute(sql)
        self.db.commit()

    def select_by_id(self, id):
        self.cursor = self.db.cursor()
        sql = f"""select * from `student` where id = {id}"""
        self.cursor.execute(sql)
        data = self.cursor.fetchall()[0]
        self.db.commit()
        return data


data = [
    {'name': 'Tran Xuan Bang', 'class': 'KT24', 'sex': 'Nam', 'phone': '0362721313'},
    {'name': 'Vu Xuan Manh', 'class': 'ĐTVT', 'sex': 'Nam', 'phone': 'xxxxxxxxx'}
]
db = DB()
for i in data:
    db.insert(i)

