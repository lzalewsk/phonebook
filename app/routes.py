# -*- coding: utf-8 -*-
from flask import render_template, flash, redirect,url_for, request, jsonify
from models import Contact
from app import app, db

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Luka'}

    return render_template('index.html', title='Home', user=user)

@app.route('/api/v1/contacts', methods=['POST'])
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
    cont_fields = ['username','phone','email','comment']
    content = {}
    for field in cont_fields:
        content[field] = None
        if jo.has_key(field):
            content[field] = jo[field]

    # TODO: dodać obsługę złożonego JSONa z kilku wpisów
    try:
        contact = Contact(
            username = content['username'],
            phone = content['phone'],
            email = content['email'],
            comment = content['comment']
        )
        db.session.add(contact)
        db.session.commit()
        response['contact_id'] = contact.id
        db.session.close()
    except Exception as e:
        print 'ZONG', e
        response['status'] = 'ERROR'
        response['error'] = e.message
        return jsonify(response), 502

    response['status'] = 'OK'
    return jsonify(response)

@app.route('/api/v1/contacts', methods=['GET'])
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
        return jsonify(response), 502

    return jsonify(response)

@app.route('/api/v1/contacts/<int:id>', methods=['GET'])
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
        return jsonify(response), 502

    return jsonify(response)

@app.route('/api/v1/contacts/<int:id>', methods=['PATCH'])
def api_patch_contact(id):
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
        return jsonify(response), 502

    return jsonify(response)

@app.route('/api/v1/contacts/<int:id>', methods=['DELETE'])
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
        db.session.close()
        response['status'] = 'OK'
    except Exception as e:
        # print e
        response = {}
        response['status'] = 'ERROR'
        response['error'] = e.message
        return jsonify(response), 502

    return jsonify(response)