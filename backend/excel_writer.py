from .excel_parent import ExcelParentWriter


class ExcelFullWriter(ExcelParentWriter):
    def __init__(self, filename: str):
        self.begin = ['Класс', 'ФИО', 'Год']
        self.stages = ['Школьный тур', 'Окружной / Муниципальный тур', 'Городской / Региональный тур', 'Всероссийский тур', 'Международный тур']
        self.__styles__(filename)
        self.educational = self.workbook.add_worksheet('Результаты учебной деятельности')
        self.educational_ = 0
        self.olympiads = self.workbook.add_worksheet('Олимпиады')
        self.olympiads_ = 0
        self.contest = self.workbook.add_worksheet('Конкурсы')
        self.contest_ = 0
        self.research = self.workbook.add_worksheet('Исследовательская работа')
        self.research_ = 0
        self.elective = self.workbook.add_worksheet('Элективные курсы')
        self.elective_ = 0
        self.additional_education_out = self.workbook.add_worksheet('Доп. образование (вне ОУ)')
        self.additional_education_out_ = 0
        self.additional_education_in = self.workbook.add_worksheet('Доп. образование (в ОУ)')
        self.additional_education_in_ = 0
        self.sport = self.workbook.add_worksheet('Спортивные достижения')
        self.sport_ = 0
        self.other_olympiads = self.workbook.add_worksheet('Прочие олимпиады')
        self.other_olympiads_ = 0
        self.events_in = self.workbook.add_worksheet('Мероприятия (в ОУ)')
        self.events_in_ = 0
        self.events_out = self.workbook.add_worksheet('Мероприятия (вне ОУ)')
        self.events_out_ = 0
        self.sport_out = self.workbook.add_worksheet('Спорт (вне ОУ)')
        self.sport_out_ = 0
        self.creativity_out = self.workbook.add_worksheet('Творчество (вне ОУ)')
        self.creativity_out_ = 0
        self.__gen_educational__()
        self.__gen_olympiads__()
        self.__gen_contest__()
        self.__gen_research__()
        self.__gen_elective__()
        self.__gen_additional_education_out__()
        self.__gen_additional_education_in__()
        self.__gen_sport__()
        self.__gen_other_olympiads__()
        self.__gen_events_in__()
        self.__gen_events_out__()
        self.__gen_sport_out__()
        self.__gen_creativity_out__()

    def __gen_educational__(self):
        self.__head__(self.educational, *self.begin, 'Название рубежа', 'Средний балл')

    def add_educational(self, data):
        self.__write__(self.educational, data, row_idx=self.educational_, cols_cnt=4)
        self.educational_ += len(data)

    def __gen_olympiads__(self):
        self.__head__(self.olympiads, *self.begin, 'Предмет', 'Учитель', *self.stages)

    def add_olympiads(self, data):
        self.__write__(self.olympiads, data, row_idx=self.olympiads_, cols_cnt=9)
        self.olympiads_ += len(data)

    def __gen_contest__(self):
        self.__head__(self.contest, *self.begin, 'Конкурс', 'Руководитель', *self.stages)

    def add_contest(self, data):
        self.__write__(self.contest, data, row_idx=self.contest_, cols_cnt=9)
        self.contest_ += len(data)

    def __gen_research__(self):
        self.__head__(self.research, *self.begin, 'Работа', 'Научный руководитель', *self.stages)

    def add_research(self, data):
        self.__write__(self.research, data, row_idx=self.research_, cols_cnt=9)
        self.research_ += len(data)

    def __gen_elective__(self):
        self.__head__(self.elective, *self.begin, 'Курс', 'Учитель', 'Реферат', 'Защита')

    def add_elective(self, data):
        self.__write__(self.elective, data, row_idx=self.elective_, cols_cnt=6)
        self.elective_ += len(data)

    def __gen_additional_education_out__(self):
            self.__head__(self.additional_education_out, *self.begin, 'Название', 'Место прохождения', 'Руководитель', 'Работа', 'Наличие работы', 'Защита работы')

    def add_additional_education_out(self, data):
        self.__write__(self.additional_education_out, data, row_idx=self.additional_education_out_, cols_cnt=8)
        self.additional_education_out_ += len(data)

    def __gen_additional_education_in__(self):
        self.__head__(self.additional_education_in, *self.begin, 'Программа доп. образования', 'Педагог', '	Работа', 'Наличие работы', 'Защита работы')

    def add_additional_education_in(self, data):
        self.__write__(self.additional_education_in, data, row_idx=self.additional_education_in_, cols_cnt=7)
        self.additional_education_in_ += len(data)

    def __gen_sport__(self):
        self.__head__(self.sport, *self.begin, 'Вид спорта', 'Тренер', *self.stages)

    def add_sport(self, data):
        self.__write__(self.sport, data, row_idx=self.sport_, cols_cnt=9)
        self.sport_ += len(data)

    def __gen_other_olympiads__(self):
        self.__head__(self.other_olympiads, *self.begin, 'Название олимпиады', 'Педагог', 'Занятое место')

    def add_other_olympiads(self, data):
        self.__write__(self.other_olympiads, data, row_idx=self.other_olympiads_, cols_cnt=5)
        self.other_olympiads_ += len(data)

    def __gen_events_in__(self):
        self.__head__(self.events_in, *self.begin, 'Название мероприятия', 'Дата', 'Организатор', 'Степень вклада')

    def add_events_in(self, data):
        self.__write__(self.events_in, data, row_idx=self.events_in_, cols_cnt=6)
        self.events_in_ += len(data)

    def __gen_events_out__(self):
        self.__head__(self.events_out, *self.begin, 'Название мероприятия', 'Дата', 'Организатор', 'Тип мероприятия', 'Степень вклада')

    def add_events_out(self, data):
        self.__write__(self.events_out, data, row_idx=self.events_out_, cols_cnt=7)
        self.events_out_ += len(data)

    def __gen_sport_out__(self):
        self.__head__(self.sport_out, *self.begin, 'Вид спорта', 'Тренер', 'Мероприятие', 'Степень вклада')

    def add_sport_out(self, data):
        self.__write__(self.sport_out, data, row_idx=self.sport_out_, cols_cnt=6)
        self.sport_out_ += len(data)

    def __gen_creativity_out__(self):
        self.__head__(self.creativity_out, *self.begin, 'Вид творчества', 'Руководитель', 'Мероприятие', 'Степень вклада')

    def add_creativity_out(self, data):
        self.__write__(self.creativity_out, data, row_idx=self.creativity_out_, cols_cnt=6)
        self.creativity_out_ += len(data)

    def save(self):
        self.workbook.close()
