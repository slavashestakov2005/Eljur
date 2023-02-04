import os


class Config:
    UPLOAD_FOLDER = 'backend/static'
    TEMPLATES_FOLDER = 'backend/templates'
    DATA_FOLDER = 'backend/data'
    TEMPLATES_AUTO_RELOAD = True
    SECRET_KEY = os.getenv('ALL_SECRET_KEY')

    WRITER = None

    DB = 'backend/database.db'

    DEVKEY = os.getenv('ELJUR_DEVKEY')
    QUERY_PART = {'vendor': 'univers', 'out_format': 'json', 'devkey': DEVKEY}
    SERVER_API = 'https://univers.eljur.ru/api/'
    AUTH_URL = SERVER_API + 'auth'
    RULES_URL = SERVER_API + 'getrules'

    API_KEY = os.getenv('PASSWORD')
