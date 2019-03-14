# from datetime import datetime
from app import db

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), index=True, unique=True)
    phone = db.Column(db.String(20), index=True, unique=False)
    email = db.Column(db.String(120), index=True, unique=True)
    comment = db.Column(db.String(240), index=False, unique=False)

    def __repr__(self):
        return '<User {}, phone {}>'.format(self.username,self.phone)
