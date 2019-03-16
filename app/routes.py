# -*- coding: utf-8 -*-
from functools import wraps
from flask import render_template, flash, redirect,url_for, request, Response, jsonify
from models import Contact
from app import app, db
from os import environ

# Flask simple Auth Basic
def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    # TODO: rozbudowa np. o bardziej zaawansowany rodzaj autentykacji

    _user = 'user'
    _pass = 'secret'

    # if os env, set provided _user and _pass
    if environ.get('PHONEBOOK_USER') is not None:
        _user = environ.get('PHONEBOOK_USER')

    if environ.get('PHONEBOOK_PASS') is not None:
        _pass = environ.get('PHONEBOOK_USER')

    return username == _user and password == _pass

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        # very simple one token auth (for example)
        _token = '!@#$5678QwErTyU='
        # if os env, set _token
        if environ.get('PHONEBOOK_TOKEN') is not None:
            _token = environ.get('PHONEBOOK_TOKEN')

        try:
            token = request.headers['X-PhoneBook-Token']
        except:
            token = None
            pass

        if token != _token:
            # if not check BasicAuth
            if not auth or not check_auth(auth.username, auth.password):
                return authenticate()
        return f(*args, **kwargs)
    return decorated

@app.route('/')
@app.route('/index')
@requires_auth
def index():
    contacts = Contact.query.order_by(Contact.id).all()
    return render_template('table.html', title='Home', contacts=contacts)

@app.route('/api/v1/contacts', methods=['GET'])
@requires_auth
def api_get_all_contact():
    """
    API for contact
    method: GET
    return: JSON response data for all
    """
    response = {}

    try:
        # User.query.filter(User.email.endswith('@example.com')).all()
        contacts = Contact.query.order_by(Contact.username).all()
        res_contacts = []
        for c in contacts:
            # print c.username
            _cnt = {}
            _cnt['id'] = c.id
            _cnt['username'] = c.username
            _cnt['phone'] = c.phone
            _cnt['emial'] = c.email
            _cnt['comment'] = c.comment
            res_contacts.append(_cnt)

        response['status'] = 'OK'
        response['contacts'] = res_contacts
    except Exception as e:
        # print e
        response = {}
        response['status'] = 'ERROR'
        response['error'] = e.message
        return jsonify(response), 500

    return jsonify(response)

@app.route('/api/v1/contacts/<int:id>', methods=['GET'])
@requires_auth
def api_get_contact(id):
    """
    API for contact
    method: GET
    return: JSON with all data of contact with <id>
    """
    response = {}

    try:
        # User.query.filter(User.email.endswith('@example.com')).all()
        contact = Contact.query.get(id)

        _cnt = {}
        _cnt['id'] = contact.id
        _cnt['username'] = contact.username
        _cnt['phone'] = contact.phone
        _cnt['emial'] = contact.email
        _cnt['comment'] = contact.comment

        response['status'] = 'OK'
        response['contact'] = _cnt
    except Exception as e:
        # print e
        response = {}
        response['status'] = 'ERROR'
        response['error'] = e.message
        return jsonify(response), 500

    return jsonify(response)

@app.route('/api/v1/contacts', methods=['POST'])
@requires_auth
def api_post_contact():
    """
    API for contact
    Input JSON stucture:
    {
        username: <string>
        phone: <string>
        email: <string>
        comment: <string>
    }
    return: JSON response date from database
    """
    response = {}
    if not request.content_type == 'application/json':
        response['status'] = 'BAD_REQUEST'
        return jsonify(response), 400

    # get, parse and validate request content
    # simple example
    # print request.content_type
    jo = request.get_json()

    # check and transforme json object to set of objects
    if type(jo) is dict:
        jdata = []
        jdata.append(jo)
    else:
        jdata = jo

    print jdata

    response['contact_id'] = []

    for jelement in jdata:
        cont_fields = ['username','phone','email','comment']
        content = {}
        for field in cont_fields:
            content[field] = None
            if jelement.has_key(field):
                content[field] = jelement[field]

        try:
            contact = Contact(
                username = content['username'],
                phone = content['phone'],
                email = content['email'],
                comment = content['comment']
            )
            db.session.add(contact)
            db.session.commit()
            if len(jdata) < 2:
                response['contact_id'] = contact.id
            else:
                response['contact_id'].append(contact.id)
            # db.session.close()
        except Exception as e:
            response = {}
            response['status'] = 'ERROR'
            response['error'] = e.message
            return jsonify(response), 500

    response['status'] = 'OK'
    return jsonify(response)

@app.route('/api/v1/contacts/<int:id>', methods=['PATCH'])
@requires_auth
def api_patch_contact(id):
    """
    API for contact
    method: PATCH
    return: status of operation
    """
    response = {}
    if not request.content_type == 'application/json':
        response['status'] = 'BAD_REQUEST'
        return jsonify(response), 400

    jdata = request.get_json()

    try:
        contact = Contact.query.get(id)

        cont_fields = ['username', 'phone', 'email', 'comment']
        for field in cont_fields:
            if jdata.has_key(field):
                setattr(contact, field, jdata[field])

        response['status'] = 'OK'
        db.session.commit()
    except Exception as e:
        # print e
        response = {}
        response['status'] = 'ERROR'
        response['error'] = e.message
        return jsonify(response), 400

    return jsonify(response)

@app.route('/api/v1/contacts/<int:id>', methods=['PUT'])
@requires_auth
def api_put_contact(id):
    """
    API for contact
    method: PUT (update or insert with selected <id>)
    return: status of operation
    """
    response = {}
    if not request.content_type == 'application/json':
        response['status'] = 'BAD_REQUEST'
        return jsonify(response), 400

    jdata = request.get_json()
    cont_fields = ['username', 'phone', 'email', 'comment']

    try:
        contact = Contact.query.get(id)
        if contact is None:
            content = {}
            for field in cont_fields:
                content[field] = None
                if jdata.has_key(field):
                    content[field] = jdata[field]

            contact = Contact(
                username=content['username'],
                phone=content['phone'],
                email=content['email'],
                comment=content['comment']
            )
            contact.id = id
            db.session.add(contact)
            db.session.commit()
            response['status'] = 'OK (NEW)'
            # response['contact_id'] = contact.id
        else:
            for field in cont_fields:
                if jdata.has_key(field):
                    setattr(contact, field, jdata[field])
            db.session.commit()
            response['status'] = 'OK (UPDATED)'
    except Exception as e:
        # print e
        response = {}
        response['status'] = 'ERROR'
        response['error'] = e.message
        return jsonify(response), 400

    return jsonify(response)

@app.route('/api/v1/contacts/<int:id>', methods=['DELETE'])
@requires_auth
def api_delete_contact(id):
    """
    API for contact
    method: DELETE
    return: JSON with operation status
    """
    response = {}

    try:
        # User.query.filter(User.email.endswith('@example.com')).all()
        contact = Contact.query.get(id)
        db.session.delete(contact)
        db.session.commit()
        # db.session.close()
        response['status'] = 'OK'
    except Exception as e:
        # print e
        response = {}
        response['status'] = 'ERROR'
        response['error'] = e.message
        return jsonify(response), 500

    return jsonify(response)