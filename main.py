from flask import Flask, Response
import json
import os
from dotenv import load_dotenv
from models import *


# load .env
load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI')
db.init_app(app)

# generate tables if not exist
db.create_all(app=app)


@app.route('/')
def index():
    return 'Hello ' + os.environ.get('NAME')


@app.route('/guest')
def get_guest():
    
    guest = Guest.query.all()

    return Response(json.dumps(guest, cls=JsonEncoder), mimetype='application/json')


# to prevent unserializable object
class JsonEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, object):
            return dict(obj)

        return json.JSONEncoder.default(self, obj)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
