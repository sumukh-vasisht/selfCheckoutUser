from flask import Flask, request, render_template, redirect, url_for
import os

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def index():
    # if request.method=="POST":
    #     global team1, team2
    #     teams[0] = request.form['team1']
    #     teams[1] = request.form['team2']
    #     # setPath()
    #     return redirect(url_for('predicc'))
    return render_template("login.html")

@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template("register.html")

@app.route('/guestLogin', methods=['GET', 'POST'])
def guestLogin():
    return render_template("guestLogin.html")

if __name__ == "__main__":
    app.run(debug=True)