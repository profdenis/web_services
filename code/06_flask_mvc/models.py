import json

from app import db
import datetime


class ContactEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Contact):
            return {'contact_id': o.contact_id,
                    'name': o.name,
                    'email': o.email,
                    'phone': o.phone,
                    'address': o.address
                    }
        elif isinstance(o, Call):
            return {'call_id': o.call_id,
                    'phone': o.phone,
                    'datetime': str(o.datetime),
                    'contact_id': o.contact_id
                    }
        else:
            return super().default(o)


class Contact(db.Model):
    __tablename__ = 'contact'
    contact_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    name = db.Column(db.Text(), nullable=False)
    email = db.Column(db.Text())
    phone = db.Column(db.Text())
    address = db.Column(db.Text())
    calls = db.relationship('Call', backref='contact', lazy=True)

    def __repr__(self):
        return f"<Contact {self.contact_id}: {self.name}>"

    def to_dict(self):
        return __dict__


class Call(db.Model):
    __tablename__ = 'call'
    call_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    phone = db.Column(db.Text(), nullable=False)
    datetime = db.Column(db.DateTime(), nullable=False, default=datetime.datetime.now)
    contact_id = db.Column(db.Integer(), db.ForeignKey('contact.contact_id'))

    def __repr__(self):
        return f"<Call {self.call_id}: {self.phone} {self.contact_id}>"

    def __getstate__(self):
        state = self.__dict__.copy()
        del state['_sa_instance_state']
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
