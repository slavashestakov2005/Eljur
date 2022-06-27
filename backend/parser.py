from bs4 import BeautifulSoup


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
                data[year].append(func(cells, *args))
        return data
    return new_func


def get_rows(text: str):
    soup = BeautifulSoup(text, 'html.parser')
    rows = soup.find_all('tr')
    return rows


def parse_mark(elem):
    child = list(elem.children)
    if len(child) == 0:
        return ''
    child = list(child[0].children)
    return child[0].string + list(child[1].children)[0].string


def parse_mark2(elem):
    child = list(list(elem.children)[0].children)
    if len(child) == 0:
        return ''
    return child[0].string + list(child[1].children)[0].string


@parser
def parse_intellectual_events(cells: list, is_research=False):
    subject = list(cells[0].children)[0].string
    teacher = list(cells[1].children)[0].string
    if not is_research:
        etaps = [parse_mark(cells[i + 2]) for i in range(5)]
    else:
        etaps = [parse_mark2(cells[i + 2]) for i in range(5)]
    return subject, teacher, etaps


@parser
def parse_events(cells: list):
    name = list(cells[0].children)[0].string
    date = list(cells[1].children)[0].string
    teacher = list(cells[2].children)[0].string
    mark = parse_mark(cells[3])
    return name, date, teacher, mark


@parser
def parse_results(cells: list):
    time = cells[0].string
    mark = cells[1].string
    return time, mark


def writable(data: dict):
    return '\n'.join('\t' + str(_) + ':\n' + '\n'.join(str(__) for __ in data[_]) for _ in data) + '\n\n'
