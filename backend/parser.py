from bs4 import BeautifulSoup
from .config import Config


def parser(func):
    def new_func(text: str, *args):
        data, year = {}, None
        rows = get_rows(text)
        for row in rows:
            cells = row.find_all('td')
            if len(cells) == 1:
                year = cells[0].string
                if year not in data:
                    data[year] = []
            else:
                value = list(func(cells, *args))
                value = ['' if _ is None else _ for _ in value]
                data[year].append(value)
        return data
    return new_func


def get_rows(text: str):
    soup = BeautifulSoup(text, 'html.parser')
    rows = soup.find_all('tr')
    return rows


def parse_mark(elem):
    child = list(list(elem.children)[0].children)
    if len(child) == 0:
        return ''
    return child[0].string + list(child[1].children)[0].string


def parse_teacher(elem):
    child = list(list(elem.children)[0].children)
    if len(child) == 0:
        return ''
    return child[0].string


def parse_editable(elem):
    return list(elem.children)[0].string


@parser
def parse_intellectual(cells: list):
    subject = parse_editable(cells[0])
    teacher = parse_teacher(cells[1])
    etaps = [parse_mark(cells[i + 2]) for i in range(5)]
    return subject, teacher, etaps


@parser
def parse_events_in(cells: list):
    name = parse_editable(cells[0])
    date = parse_editable(cells[1])
    teacher = parse_teacher(cells[2])
    mark = parse_mark(cells[3])
    return name, date, teacher, mark


@parser
def parse_events_out(cells: list):
    name = parse_editable(cells[0])
    date = parse_editable(cells[1])
    teacher = parse_teacher(cells[2])
    tp = parse_editable(cells[3])
    mark = parse_mark(cells[4])
    return name, date, teacher, tp, mark


@parser
def parse_sport_out(cells: list):
    subject = parse_editable(cells[0])
    teacher = parse_teacher(cells[1])
    name = parse_editable(cells[2])
    mark = parse_mark(cells[3])
    return subject, teacher, name, mark


@parser
def parse_creativity_out(cells: list):
    tp = parse_editable(cells[0])
    teacher = parse_teacher(cells[1])
    name = parse_editable(cells[2])
    mark = parse_mark(cells[3])
    return tp, teacher, name, mark


@parser
def parse_results(cells: list):
    time = cells[0].string
    mark = cells[1].string
    return time, mark


@parser
def parse_elective(cells: list):
    name = parse_editable(cells[0])
    teacher = parse_teacher(cells[1])
    report = parse_mark(cells[2])
    protection = parse_mark(cells[3])
    return name, teacher, report, protection


@parser
def parse_olympiad(cells: list):
    name = parse_editable(cells[0])
    teacher = parse_teacher(cells[1])
    place = parse_mark(cells[2])
    return name, teacher, place


@parser
def parse_education_out(cells: list):
    name = parse_editable(cells[0])
    place = parse_editable(cells[1])
    teacher = parse_teacher(cells[2])
    work = parse_editable(cells[3])
    exists = parse_mark(cells[4])
    protection = parse_mark(cells[5])
    return name, place, teacher, work, exists, protection


@parser
def parse_education_in(cells: list):
    name = parse_editable(cells[0])
    teacher = parse_teacher(cells[1])
    work = parse_editable(cells[2])
    exists = parse_mark(cells[3])
    protection = parse_mark(cells[4])
    return name, teacher, work, exists, protection


def writable(data: dict):
    return '\n'.join('\t' + str(_) + ':\n' + '\n'.join(str(__) for __ in data[_]) for _ in data) + '\n\n'


def write(cls: str, fio: str, data: dict, name: str):
    new_data = []
    for year in data:
        for row in data[year]:
            new_row = [cls, fio, year]
            for x in row:
                if type(x) == list:
                    new_row.extend(x)
                else:
                    new_row.append(x)
            new_data.append(new_row)
    Config.WRITER.add(name, new_data)
