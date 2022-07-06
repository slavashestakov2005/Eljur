from .excel_parent import ExcelParentWriter


class ExcelFullWriter(ExcelParentWriter):
    def __init__(self, filename: str):
        self.begin = ['Класс', 'ФИО', 'Год']
        self.stages = ['Школьный тур', 'Окружной / Муниципальный тур', 'Городской / Региональный тур',
                       'Всероссийский тур', 'Международный тур']
        self.__styles__(filename)
        self.data = dict()
        self.data['educational'] = [self.workbook.add_worksheet('Результаты учебной деятельности'), 0,
                                    [*self.begin, 'Название рубежа', 'Средний балл']]
        self.data['olympiads'] = [self.workbook.add_worksheet('Олимпиады'), 0,
                                  [*self.begin, 'Предмет', 'Учитель', *self.stages]]
        self.data['contest'] = [self.workbook.add_worksheet('Конкурсы'), 0,
                                [*self.begin, 'Конкурс', 'Руководитель', *self.stages]]
        self.data['research'] = [self.workbook.add_worksheet('Исследовательская работа'), 0,
                                 [*self.begin, 'Работа', 'Научный руководитель', *self.stages]]
        self.data['elective'] = [self.workbook.add_worksheet('Элективные курсы'), 0,
                                 [*self.begin, 'Курс', 'Учитель', 'Реферат', 'Защита']]
        self.data['additional_education_out'] = [self.workbook.add_worksheet('Доп. образование (вне ОУ)'), 0,
                                                 [*self.begin, 'Название', 'Место прохождения', 'Руководитель',
                                                  'Работа', 'Наличие работы', 'Защита работы']]
        self.data['additional_education_in'] = [self.workbook.add_worksheet('Доп. образование (в ОУ)'), 0,
                                                [*self.begin, 'Программа доп. образования', 'Педагог', 'Работа',
                                                 'Наличие работы', 'Защита работы']]
        self.data['sport'] = [self.workbook.add_worksheet('Спортивные достижения'), 0,
                              [*self.begin, 'Вид спорта', 'Тренер', *self.stages]]
        self.data['other_olympiads'] = [self.workbook.add_worksheet('Прочие олимпиады'), 0,
                                        [*self.begin, 'Название олимпиады', 'Педагог', 'Занятое место']]
        self.data['events_in'] = [self.workbook.add_worksheet('Мероприятия (в ОУ)'), 0,
                                  [*self.begin, 'Название мероприятия', 'Дата', 'Организатор', 'Степень вклада']]
        self.data['events_out'] = [self.workbook.add_worksheet('Мероприятия (вне ОУ)'), 0,
                                   [*self.begin, 'Название мероприятия', 'Дата', 'Организатор', 'Тип мероприятия',
                                    'Степень вклада']]
        self.data['sport_out'] = [self.workbook.add_worksheet('Спорт (вне ОУ)'), 0,
                                  [*self.begin, 'Вид спорта', 'Тренер', 'Мероприятие', 'Степень вклада']]
        self.data['creativity_out'] = [self.workbook.add_worksheet('Творчество (вне ОУ)'), 0,
                                       [*self.begin, 'Вид творчества', 'Руководитель', 'Мероприятие', 'Степень вклада']]
        self.__gen_heads__()

    def __gen_heads__(self):
        for name in self.data:
            value = self.data[name]
            self.__head__(value[0], *value[2])

    def add(self, name, data):
        value = self.data[name]
        self.__write__(value[0], data, row_idx=value[1], cols_cnt=len(value[2]) - 1)
        value[1] += len(data)

    def save(self):
        self.workbook.close()
