from flask import Flask
import os
# from dotenv import load_dotenv


app = Flask(__name__)
# load_dotenv()


@app.route('/')
def index():
    return 'Hello ' + os.environ.get('NAME')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
