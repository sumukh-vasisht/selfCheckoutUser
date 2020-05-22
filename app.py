from flask import Flask, request, render_template, redirect, url_for 
import os

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