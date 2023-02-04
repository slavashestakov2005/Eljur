from .config import Config
from .database import Student
from requests import Session


def decode_gender(gender: str):
    if gender.lower() == 'male':
        return Student.MALE
    if gender.lower() == 'female':
        return Student.FEMALE
    return Student.NONE


def parse_people(data, use_db=True):
    eljur_id = int(data['name'])
    if use_db:
        student = Student.select_by_eljur(eljur_id)
        if student.__is_none__:
            raise ValueError()
        return {'lastname': student.name_1, 'firstname': student.name_2, 'middlename': student.name_3,
                'gender': student.gender, 'class_n': student.class_n, 'class_l': student.class_l, 'eljur_id': eljur_id}
    return {'lastname': data['lastname'], 'firstname': data['firstname'], 'middlename': data['middlename'],
            'gender': decode_gender(data['gender']), 'eljur_id': eljur_id, }


class EljurUser:
    @staticmethod
    def auth(login: str, password: str):
        data = Config.QUERY_PART
        data['login'] = login
        data['password'] = password
        s = Session()
        response = s.post(Config.AUTH_URL, json=data).json()['response']
        if response['state'] != 200 or response['error'] is not None:
            return s, None
        return s, response['result']['token']

    @staticmethod
    def login(login: str, password: str):
        s, token = EljurUser.auth(login, password)
        if not token:
            return None
        data = Config.QUERY_PART
        data['auth_token'] = token
        response = s.get(Config.RULES_URL, json=data).json()['response']
        if response['state'] != 200 or response['error'] is not None:
            return None
        response = response['result']
        eljur_id, childs = int(response['id']), []
        childs_list = response['relations']['students']
        for child_id in childs_list:
            child = childs_list[child_id]
            if int(child_id) != eljur_id:
                childs.append(parse_people(child))
        roles = response['roles']
        return str({'status': 'OK', **parse_people(response, 'student' in roles), 'childs': childs, 'teacher':
                    'teacher' in roles, 'administrator': 'administrator' in roles, 'sysadmin': 'sysadmin' in roles})
