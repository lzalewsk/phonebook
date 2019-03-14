# -*- coding: utf-8 -*-
from flask import render_template, flash, redirect,url_for, request, jsonify
from models import Contact
from app import app, db

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Luka'}

    return render_template('index.html', title='Home', user=user)

@app.route('/api/v1/contact', methods=['GET', 'POST'])
def api_contact():
    """
    API for contact
    Input JSON stucture:
    {
        username: <string>
        phone: <string>
        email: <string>
    }
    return: JSON response date from database
    """

    if request.method == 'POST':
        response = {}
        if not request.content_type == 'application/json':
            response['status'] = 'BAD_REQUEST'
            return jsonify(response), 400

        # get, parse and validate request content
        # simple example
        print request.content_type
        content = request.get_json()
        try:
            contact = Contact(
                username = content['username'],
                phone = content['phone'],
                email = content['email']
            )
            db.session.add(contact)
            db.session.commit()
            db.session.close()
        except Exception as e:
            print 'ZONG',e
            response['status'] = 'ERROR'
            response['error'] = e.message
            return jsonify(response),502

        response['status'] = 'OK'
        # reponsse['contact_id'] = contact.id
        return jsonify(response)
    else:
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
                # _cnt['comment'] = c.comment
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