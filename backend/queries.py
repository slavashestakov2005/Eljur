from backend import app
from flask import request, jsonify
from flask_cors import cross_origin
from .parser import *
from .excel_writer import ExcelFullWriter
from .config import Config


@app.route("/parse", methods=['POST'])
@cross_origin()
def download_data():
    cls, fio = request.form['cls'], request.form['fio']
    write(cls, fio, parse_results(request.form['educational']), Config.WRITER.add_educational)
    write(cls, fio, parse_intellectual(request.form['olympiads']), Config.WRITER.add_olympiads)
    write(cls, fio, parse_intellectual(request.form['contest']), Config.WRITER.add_contest)
    write(cls, fio, parse_intellectual(request.form['research']), Config.WRITER.add_research)
    write(cls, fio, parse_elective(request.form['elective']), Config.WRITER.add_elective)
    write(cls, fio, parse_education_out(request.form['additional_education_out']), Config.WRITER.add_additional_education_out)
    write(cls, fio, parse_education_in(request.form['additional_education_in']), Config.WRITER.add_additional_education_in)
    write(cls, fio, parse_intellectual(request.form['sport']), Config.WRITER.add_sport)
    write(cls, fio, parse_olympiad(request.form['other_olympiads']), Config.WRITER.add_other_olympiads)
    write(cls, fio, parse_events_in(request.form['events_in']), Config.WRITER.add_events_in)
    write(cls, fio, parse_events_out(request.form['events_out']) , Config.WRITER.add_events_out)
    write(cls, fio, parse_sport_out(request.form['sport_out']), Config.WRITER.add_sport_out)
    write(cls, fio, parse_creativity_out(request.form['creativity_out']), Config.WRITER.add_creativity_out)
    return jsonify({'status': 'OK'})


@app.route("/start", methods=['GET'])
@cross_origin()
def start():
    Config.WRITER = ExcelFullWriter('log.xlsx')
    return jsonify({'status': 'OK'})


@app.route("/end", methods=['GET'])
@cross_origin()
def end():
    if Config.WRITER is not None:
        Config.WRITER.save()
    return jsonify({'status': 'OK'})
