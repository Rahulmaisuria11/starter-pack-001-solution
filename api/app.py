from dotenv import load_dotenv

# Need to load dot env here.
load_dotenv('.env')

from app import create_app
from config import Config

app = create_app(config=Config)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5001, threaded=True)
