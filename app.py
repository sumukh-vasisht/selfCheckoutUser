from flask import Flask, request, render_template, redirect, url_for 
# import MySQLdb
import os
from pyzbar import pyzbar

uploadFolder = 'qrCodes'

app = Flask(__name__)

app.config['uploadFolder'] = uploadFolder

@app.route('/', methods=['GET','POST'])
def index():
    if request.method == "POST":
        c, conn = connection()
        email = request.form['email']
        password = request.form['password']
        print(email, password)
        return render_template("login.html")
    return render_template("login.html")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phoneNumber = request.form['phoneNumber']
        password = request.form['pwd1']
        print(name,email,phoneNumber,password)
        return render_template("register.html")
    return render_template("register.html")

@app.route('/guestLogin', methods=['GET', 'POST'])
def guestLogin():
    if request.method=="POST":
        qrcode = request.files['qrcode']
        if qrcode.filename=='':
            message = "No image captured"
            return redirect('guestLogin', confirm=message)
        else:
            qrcode.save(os.path.join(app.config['uploadFolder'], filename))
            message = "File uploaded successfully"
            return redirect('guestLogin', confirm=message)
    return render_template("guestLogin.html")

if __name__ == "__main__":
    app.run(debug=True)