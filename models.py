from flask_sqlalchemy import SQLAlchemy, event


db = SQLAlchemy()


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
