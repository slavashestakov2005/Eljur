from typing import Tuple
import sqlite3 as db
from .config import Config


class DataBase:
    @staticmethod
    def connect():
        return db.connect(Config.DB)

    @staticmethod
    def prepare_sql(sql: str) -> str:
        return sql

    @staticmethod
    def just_execute(sql: str, params=()) -> None:
        sql = DataBase.prepare_sql(sql)
        connection = DataBase.connect()
        cursor = connection.cursor()
        cursor.execute(sql, params)
        connection.commit()
        connection.close()

    @staticmethod
    def execute(sql: str, params=()) -> list:
        sql = DataBase.prepare_sql(sql)
        connection = DataBase.connect()
        cursor = connection.cursor()
        cursor.execute(sql, params)
        result = cursor.fetchall()
        connection.commit()
        connection.close()
        return result

    @staticmethod
    def execute_one(sql: str, params=()) -> Tuple:
        result = DataBase.execute(sql, params)
        if not result or len(result) == 0:
            return ()
        return result[0]


class Student:
    NONE, MALE, FEMALE = 0, 1, 2
    fields = ['eljur_id', 'name_1', 'name_2', 'name_3', 'gender', 'class_n', 'class_l']

    def __init__(self, *args):
        if not args:
            self.__is_none__ = True
        else:
            self.__is_none__ = False
            self.eljur_id, self.name_1, self.name_2, self.name_3, self.gender, self.class_n, self.class_l = args

    def simple_json(self):
        return {'lastname': self.name_1, 'firstname': self.name_2, 'middlename': self.name_3,
                'class_n': self.class_n, 'class_l': self.class_l}

    @staticmethod
    def select_by_eljur(eljur_id: int):
        text = 'SELECT * FROM "students" WHERE eljur_id=?'
        return Student(*DataBase.execute_one(text, [eljur_id]))

    @staticmethod
    def select_by_student(student):
        text = 'SELECT * FROM "students" WHERE name_1 = ? AND name_2 = ? AND name_3 = ? AND class_n = ? AND class_l = ?'
        args = student.name_1, student.name_2, student.name_3, student.class_n, student.class_l
        return [Student(*_) for _ in DataBase.execute(text, args)]

    @staticmethod
    def select_none_gender():
        text = 'SELECT * FROM "students" WHERE gender = ?'
        return [Student(*_) for _ in DataBase.execute(text, [Student.NONE])]

    @staticmethod
    def __update__(student, eljur_id):
        use_fields = Student.fields[1:]
        text = 'UPDATE "students" SET {} WHERE eljur_id=?'.format(', '.join(_ + '= ?' for _ in use_fields))
        DataBase.just_execute(text, [student.__getattribute__(_) for _ in use_fields] + [eljur_id])

    @staticmethod
    def insert_info(student):
        old = Student.select_by_eljur(student.eljur_id)
        if old.__is_none__:
            use_fields = Student.fields
            text = 'INSERT INTO "students" ({}) VALUES ({})'.format(', '.join(use_fields), ', '.join('?' for _ in use_fields))
            DataBase.just_execute(text, [student.__getattribute__(_) for _ in use_fields])
        else:
            Student.__update__(student, old.eljur_id)

    @staticmethod
    def update_gender(student):
        Student.__update__(student, student.eljur_id)

    @staticmethod
    def clear_table():
        DataBase.execute('DELETE FROM "students"', [])
