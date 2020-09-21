from flask import Flask, Response
from flask_sqlalchemy import SQLAlchemy, event
import json
import os
import time
from dotenv import load_dotenv


# load .env
load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI')
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)


class Guest(db.Model):

    __tablename__ = 'guest'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String, unique=True)

    def __iter__(self):
        yield 'id', self.id
        yield 'name', self.name
        yield 'email', self.email


# init data after table created
@event.listens_for(Guest.__table__, 'after_create')
def init_guest(*args, **kwargs):
    db.session.add(Guest(name='Happy Indra Wijaya', email='me@hiwijaya.com'))
    db.session.commit()


# it required when waiting postgres container ready to accept connection
retries = 5
while retries:
    try:
        db.create_all()     # generate tables if not exist
        break
    except:
        retries = retries-1
        print('RETRIES LEFT: ' + str(retries))
        time.sleep(1)


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


# start
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
