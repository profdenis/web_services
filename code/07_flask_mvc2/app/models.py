import json

from app import db
# import datetime
from datetime import datetime


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
                    'datetime': str(o.datetime)
                    }
        else:
            return super().default(o)


contact_call = db.Table('contact_call',
                        db.Column('contact_id', db.Integer(), db.ForeignKey('contact.contact_id'), primary_key=True),
                        db.Column('call_id', db.Integer(), db.ForeignKey('call.call_id'), primary_key=True)
                        )


class Contact(db.Model):
    __tablename__ = 'contact'
    contact_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    name = db.Column(db.Text(), nullable=False)
    email = db.Column(db.Text())
    phone = db.Column(db.Text())
    address = db.Column(db.Text())
    calls = db.relationship('Call', secondary=contact_call, backref=db.backref('calls', lazy=True), lazy=True,
                            viewonly=True)

    def __repr__(self):
        return f"<Contact {self.contact_id}: {self.name}>"


class Call(db.Model):
    __tablename__ = 'call'
    call_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    phone = db.Column(db.Text(), nullable=False)
    datetime = db.Column(db.DateTime(), nullable=False, default=datetime.now)
    contacts = db.relationship('Contact', secondary=contact_call, backref=db.backref('contacts', lazy=True), lazy=True)

    def __repr__(self):
        return f"<Call {self.call_id}: {self.phone} >"
