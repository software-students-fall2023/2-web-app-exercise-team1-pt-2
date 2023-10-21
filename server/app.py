from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, abort, url_for, make_response

load_dotenv()
uri=os.getenv('URI')

mongo = MongoClient(uri, server_api=ServerApi('1'))

try:
    mongo.admin.command('ping')
    print("successfully connected to mongo")
except Exception as e:
    print(e)

app=Flask(__name__)

@app.route('/')
def display_all_contacts():
    contacts = mongo.db.contacts.find()
    return render_template('contactlist.html', contacts=contacts)

@app.route('/add_contact', methods=['GET', 'POST'])
def add_contact():
    if request.method == 'POST':
        contact_data = {
            "fullName": request.form.get("fullName"),
            "phoneNumber": request.form.get("phoneNumber"),
            "emailAddress": request.form.get("emailAddress"),
        }
        mongo.db.contacts.insert_one(contact_data)
        return redirect(url_for('contactlist'))
    return render_template('addcontact.html')


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
            }
        }
    )
    return redirect(url_for('contact', contact_id=contact_id))