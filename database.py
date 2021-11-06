import sqlite3


class DB:
    def __init__(self):
        self.db = sqlite3.connect('data.sqlite3')
        self.cursor = self.db.cursor()
        sql = """CREATE TABLE IF NOT EXISTS `student` (
                `id` INTEGER PRIMARY KEY,
                `name` TEXT NOT NULL,
                `class` TEXT NOT NULL,
                `sex` TEXT NOT NULL,
                `phone` TEXT,
            );"""
        self.cursor.execute(sql)
        self.db.commit()

    @classmethod
    def insert(cls):
        pass

    @classmethod
    def select(cls):
        pass