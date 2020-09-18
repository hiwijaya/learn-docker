from flask import Flask, Response
from flask_sqlalchemy import SQLAlchemy
import json
import os
from dotenv import load_dotenv


load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI')
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


def objects_to_dict(_list):
    i = 0
    for obj in _list:
        _list[i] = dict(obj)
        i += 1

    return _list


@app.route('/')
def index():
    return 'Hello ' + os.environ.get('NAME')


@app.route('/guest')
def get_guest():
    guest = Guest.query.all()
    guest = objects_to_dict(guest)

    return Response(json.dumps(guest), mimetype='application/json')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
