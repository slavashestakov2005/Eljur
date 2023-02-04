import os
from dotenv import load_dotenv
os.chdir(os.path.dirname(os.path.abspath(__file__)))
load_dotenv('.env')


from backend import app


os.chdir(os.path.dirname(os.path.abspath(__file__)))
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
