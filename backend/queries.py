from backend import app
from flask import request, jsonify, send_file, render_template
from flask_cors import cross_origin
from functools import wraps
import os
from .parser import *
from .excel_reader import ExcelFullReader
from .excel_writer import ExcelFullWriter
from .config import Config
from time import sleep
from .database import Student
from .eljur import EljurUser


# Вспомогательные функции


def non_throwing():
    def my_decorator(func):

        @wraps(func)
        def wrapped(*args, **kwargs):
            try:
                if request.form['api_key'] != Config.API_KEY:
                    raise ValueError()
                return func(*args, **kwargs)
            except Exception:
                return jsonify({'status': 'ERROR'})

        return wrapped

    return my_decorator


def data_folder():
    try:
        os.makedirs(Config.DATA_FOLDER)
    except:
        pass


# Запросы на парсинг Eljur


@app.route("/start", methods=['POST'])
@cross_origin()
@non_throwing()
def start():
    data_folder()
    Config.WRITER = ExcelFullWriter(Config.DATA_FOLDER + '/log.xlsx')
    return jsonify({'status': 'OK'})


@app.route("/parse", methods=['POST'])
@cross_origin()
@non_throwing()
def parse():
    eljur_id, cls, fio = int(request.form['student_id']), request.form['cls'], request.form['fio']
    student = Student(eljur_id, *fio.split(), Student.NONE, cls[:-1], cls[-1])
    Student.insert_info(student)
    write(cls, fio, parse_results(request.form['educational']), 'educational')
    write(cls, fio, parse_intellectual(request.form['olympiads']), 'olympiads')
    write(cls, fio, parse_intellectual(request.form['contest']), 'contest')
    write(cls, fio, parse_intellectual(request.form['research']), 'research')
    write(cls, fio, parse_elective(request.form['elective']), 'elective')
    write(cls, fio, parse_education_out(request.form['additional_education_out']), 'additional_education_out')
    write(cls, fio, parse_education_in(request.form['additional_education_in']), 'additional_education_in')
    write(cls, fio, parse_intellectual(request.form['sport']), 'sport')
    write(cls, fio, parse_olympiad(request.form['other_olympiads']), 'other_olympiads')
    write(cls, fio, parse_events_in(request.form['events_in']), 'events_in')
    write(cls, fio, parse_events_out(request.form['events_out']) , 'events_out')
    write(cls, fio, parse_sport_out(request.form['sport_out']), 'sport_out')
    write(cls, fio, parse_creativity_out(request.form['creativity_out']), 'creativity_out')
    return jsonify({'status': 'OK'})


@app.route("/end", methods=['POST'])
@cross_origin()
@non_throwing()
def end():
    if Config.WRITER is not None:
        Config.WRITER.save()
        sleep(3)
        filename = './data/log.xlsx'
        return send_file(filename, as_attachment=True, download_name='log.xlsx')
    raise ValueError()


# Данные из Excel


@app.route("/clear", methods=['POST'])
@cross_origin()
@non_throwing()
def clear():
    Student.clear_table()
    return jsonify({'status': 'OK'})


@app.route("/parse_excel", methods=['POST'])
@cross_origin()
@non_throwing()
def parse_excel():
    data_folder()
    file = request.files['excel']
    parts = [x.lower() for x in file.filename.rsplit('.', 1)]
    filename = Config.DATA_FOLDER + '/tmp' + '.' + parts[1]
    file.save(filename)
    reader = ExcelFullReader(filename)
    errors = reader.read()
    students = Student.select_none_gender()
    eljur_errors = [{**student.simple_json(), 'message': 'Не найден в таблице'} for student in students]
    return jsonify({'status': ('ERROR' if len(errors) else 'OK'), 'excel_errors': errors, 'eljur_errors': eljur_errors})


# Вход на сайт через журнал


@app.route("/login", methods=['POST'])
@cross_origin()
@non_throwing()
def login():
    user_login = request.form['login']
    user_password = request.form['password']
    user = EljurUser.login(user_login, user_password)
    if not user:
        raise ValueError()
    return user


@app.route("/")
@app.route("/forms")
@app.route("/forms.html")
@cross_origin()
def forms():
    return render_template('forms.html')
