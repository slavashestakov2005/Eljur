from backend import app
from flask import request, jsonify, send_file
from flask_cors import cross_origin
from .parser import *
from .excel_writer import ExcelFullWriter
from .config import Config
from time import sleep


@app.route("/parse", methods=['POST'])
@cross_origin()
def download_data():
    cls, fio = request.form['cls'], request.form['fio']
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


@app.route("/start", methods=['POST'])
@cross_origin()
def start():
    Config.WRITER = ExcelFullWriter(Config.DATA_FOLDER + '/log.xlsx')
    return jsonify({'status': 'OK'})


@app.route("/end", methods=['POST'])
@cross_origin()
def end():
    if Config.WRITER is not None:
        Config.WRITER.save()
        sleep(3)
        filename = './data/log.xlsx'
        return send_file(filename, as_attachment=True, attachment_filename='log.xlsx')
    return jsonify({'status': 'Error'})
