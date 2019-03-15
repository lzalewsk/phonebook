# from datetime import datetime
from app import db
from sqlalchemy.orm import validates
import re

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), index=True, unique=True)
    phone = db.Column(db.String(20), index=True, unique=False)
    email = db.Column(db.String(120), index=True, unique=True)
    comment = db.Column(db.String(240), index=False, unique=False)

    def __repr__(self):
        return '<User {}, phone {}>'.format(self.username,self.phone)

    @validates('username')
    def validate_username(self, key, username):
      if not username:
          raise AssertionError('No username provided')

      if Contact.query.filter(Contact.username == username).first():
        raise AssertionError('Username is already in use')

      if len(username) < 5 or len(username) > 80:
        raise AssertionError('Username must be between 5 and 80 characters')

      return username

    @validates('phone')
    def validate_phone(self, key, phone):
      if not phone:
        raise AssertionError('No telephone number provided')

      # simple example of phone number validation
      if not re.match("(?<!\w)(\(?(\+|00)?\d{2}\)?)?[ -]?\d{3}[ -]?\d{3}[ -]?\d{3}(?!\w)", phone):
        raise AssertionError('Invalid phone number')

      return phone

    @validates('email')
    def validate_email(self, key, email):
      if not email:
        raise AssertionError('No email provided')

      if Contact.query.filter(Contact.email == email).first():
        raise AssertionError('Email is already in PhoneBook')

      if not re.match("[^@]+@[^@]+\.[^@]+", email):
        raise AssertionError('Provided email is not an email address')

      return email
