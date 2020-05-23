from flask import Flask, request, render_template, redirect, url_for 
import os
import firebase_admin as firebase
from firebase_admin import firestore
import pyrebase
import json

#FOR FIRESTORE
cred = firebase.credentials.Certificate("firebaseKey.json")
firebase.initialize_app(cred)
db = firestore.client()

#FOR AUTH
keyFile = open('pyrebaseKey.json','r')
keyJson = keyFile.read()
key = json.loads(keyJson)
auth = pyrebase.initialize_app(key).auth()

#FIRESTORE COMMANDS
# db.collection('collectionName').document('documentID').set(data(as a dictionary)) -- To create/edit document
# db.collection('collectionName').document('documentID').get() -- To get document
# db.collection('collectionName').where('LHS','relational operator','RHS').stream() -- To get documents based on condition, eg .where('name','==','Varun'). to get all documents just remove the .where
# db.collection('collectionName').order_by('name of field').limit('number of docs').stream() -- To limit the number of docs fetched or to order them. can also use along with .where
# db.collection('collectionName').document('documentID').get().to_dict() -- To get document as dictionary (used most often)
# db.collection('collectionName').document('documentID').delete() -- To delete document

#AUTH COMMANDS
# auth.create_user_with_email_and_password(email, password) -- Make a user
# auth.sign_in_with_email_and_password(email, password) -- Sign in a user, returns a session key that expires in 60 mins I think.

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def login():
    if request.method == "POST":
        email = request.form['username']
        password = request.form['password']
        print(email, password)
        return render_template("home.html")
    return render_template("login.html")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phoneNumber = request.form['phoneNumber']
        password = request.form['pwd1']
        print(name,email,phoneNumber,password)
        return render_template("home.html")
    return render_template("register.html")

@app.route('/guestLogin', methods=['GET', 'POST'])
def guestLogin():
    return render_template("guestLogin.html")

@app.route('/home', methods=['GET','POST'])
def home():
    return render_template("home.html")

@app.route('/contact', methods=['GET','POST'])
def contact():
    return render_template("contact.html")

@app.route('/viewCurrentBill', methods=['GET','POST'])
def viewCurrentBill():
    return render_template("viewCurrentBill.html")

@app.route('/viewAllBills', methods=['GET','POST'])
def viewAllBills():
    return render_template("viewAllBills.html")

if __name__ == "__main__":
    app.run(debug=True)