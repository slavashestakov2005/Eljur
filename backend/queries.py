from backend import app
from flask import request, jsonify
from flask_cors import cross_origin
from .parser import *


@app.route("/parse", methods=['POST'])
@cross_origin()
def download_data():
    educational = parse_results(request.form['educational'])
    olympiads = parse_intellectual_events(request.form['olympiads'])
    research = parse_intellectual_events(request.form['research'], True)
    events = parse_events(request.form['events'])
    with open('log.txt', 'w', encoding='UTF-8') as f:
        f.write(writable(educational))
        f.write(writable(olympiads))
        f.write(writable(research))
        f.write(writable(events))
    return jsonify({'status': 'OK'})
