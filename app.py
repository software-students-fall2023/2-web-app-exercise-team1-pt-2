from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, abort, url_for, make_response
import datetime
from bson.objectid import ObjectId
import pymongo
import re

load_dotenv()
uri=os.getenv('URI')

mongo = MongoClient(uri, server_api=ServerApi('1'))

try:
    mongo.admin.command('ping')
    print("successfully connected to mongo")
except Exception as e:
    print(e)

app=Flask(__name__, template_folder='../templates', static_folder='../static')

@app.route('/')
def display_all_contacts():
    contacts = mongo.db.contacts.find()
    return render_template('contactlist.html', contacts=contacts)

@app.route('/search')
def search():
    name_search = request.args.get('name')
    contacts = mongo.db.contacts.find({"fullName": re.compile(name_search, re.IGNORECASE)})
    return render_template('contactlist.html', contacts=contacts)

@app.route('/add_contact', methods=['GET', 'POST'])
def add_contact():
    if request.method == 'POST':
        name = request.form.get("fname")
        number = request.form.get("pnumber")
        email = request.form.get("email")

        contact_data = {
            "fullName": name,
            "phoneNumber": number,
            "emailAddress": email,
            "favorite": False,
            "createdAt": datetime.datetime.now(),
            "updatedAt": datetime.datetime.now()
        }
        mongo.db.contacts.insert_one(contact_data)
        return redirect(url_for('display_all_contacts'))
    return render_template('addcontact.html')

@app.route('/favorites')
def display_favorites():
    contacts = mongo.db.contacts.find({"favorite": "true"})
    return render_template('fav_contact_list.html', contacts=contacts)

@app.route('/contact/<contact_id>')
def contact_details(contact_id):
    contact = mongo.db.contacts.find_one_or_404({"_id": ObjectId(contact_id)})
    return render_template('contact.html', contact=contact)


@app.route('/contact/<contact_id>/edit')
def edit_contact(contact_id):
    contact = mongo.db.contacts.find_one_or_404({"_id": ObjectId(contact_id)})
    return render_template('editcontact.html', contact=contact)


@app.route('/contact/<contact_id>/update', methods=['POST'])
def update_contact(contact_id):
    mongo.db.contacts.update_one(
        {"_id": ObjectId(contact_id)},
        {
            "$set": {
                "fullName": request.form.get("fullName"),
                "phoneNumber": request.form.get("phoneNumber"),
                "emailAddress": request.form.get("emailAddress"),
                "favorite": request.form.get("favorite"),
                "updatedAt": datetime.datetime.now()
            }
        }
    )
    return redirect(url_for('contact', contact_id=contact_id))

@app.route('/contact/<contact_id>/delete', methods=['GET','DELETE'])
def delete_contact(contact_id):
    if request.method == 'GET':
        return render_template('deletecontact.html', contact_id=contact_id)
    mongo.db.contacts.delete_one({"_id": ObjectId(contact_id)})
    return redirect(url_for('contactlist'))

@app.route('/contact/<contact_id>/favorite', methods=['POST'])
def favorite_contact(contact_id):
    mongo.db.contacts.update_one(
        {"_id": ObjectId(contact_id)},
        {
            "$set": {
                "favorite": "true",
            }
        }
    )
    return redirect(url_for('contact', contact_id=contact_id))

app.run(debug=True)
