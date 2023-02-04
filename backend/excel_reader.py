import pandas as pd
from .database import Student


def find(titles, exists, not_exists=None):
    i = 0
    for x in titles:
        t = x.lower()
        if exists in t and (not not_exists or not_exists not in t):
            return i
        i += 1
    return -1


class ExcelFullReader:
    STUDENTS = ['name', 'cls', 'gender']

    def __init__(self, file: str):
        self.file = file

    def __frames__(self):
        sheet_name = list(self.sheet.keys())
        self.sheet = list(self.sheet.values())
        data = find(sheet_name, 'список')
        self.data = self.sheet[data]

    def __get_students_cols__(self):
        columns = self.data.columns
        name, cls = columns[find(columns, 'имя')], columns[find(columns, 'класс')]
        gender = columns[find(columns, 'пол')]
        frame = pd.DataFrame(self.data, columns=[name, cls, gender])
        frame.columns = self.STUDENTS
        self.student = frame[frame[self.STUDENTS[0]].notna() & frame[self.STUDENTS[1]].notna() & frame[self.STUDENTS[2]].notna()]

    def __gen_only_students__(self):
        errors = []
        for i, row in self.student.iterrows():
            student = Student(None, *row[0].split(), Student.MALE if row[2].lower() == 'м' else Student.FEMALE,
                              row[1][:-1], row[1][-1])
            st = Student.select_by_student(student)
            ex = student.simple_json()
            if len(st) > 1:
                errors.append({**ex, 'message': 'Найдено несколько человек'})
            elif len(st) == 0:
                errors.append({**ex, 'message': 'Человек не найден'})
            else:
                st[0].gender = student.gender
                Student.update_gender(st[0])
        return errors

    def read(self):
        self.sheet = pd.read_excel(self.file, sheet_name=None, engine="openpyxl")
        self.__frames__()
        self.__get_students_cols__()
        return self.__gen_only_students__()
