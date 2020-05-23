from flask import Flask, render_template, request, redirect, session, url_for, flash
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

app = Flask(__name__)

def sendEmail(email, html, text):
    senderAddress = "selfcheckoutsample@gmail.com"
    senderPassword = "@Sample123"
    server = 'smtp.gmail.com:587'
    recieverAddress = email
    message = MIMEMultipart("alternative", None, [MIMEText(text), MIMEText(html,'html')])
    message['Subject'] = "Self-Checkout | Admin"
    message['From'] = senderAddress
    message['To'] = recieverAddress
    server = smtplib.SMTP(server)
    server.ehlo()
    server.starttls()
    server.login(senderAddress, senderPassword)
    server.sendmail(senderAddress, recieverAddress, message.as_string())
    print('Email Sent')
    server.quit()

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
        age = request.form['age']
        address = request.form['address']
        password = request.form['pwd1']
        print(name,email,phoneNumber,password)
        text = """
        Dear %s,
        Thank you for signing-up on self-checkout!
        Your account has been activated!
        Happy shopping!
        Thanks & Regards,
        Admin,
        Self-Checkout
        """ %name
        html = """
        <html>
        <head>
        </head>
        <body>
            <p>Dear %s,</p>
            <p>Thank you for signing up on Self-Checkout!<br/>
            Your account has been activated!<br/>
            Happy Shopping!</p><br/>
            <p>Thanks & Regards,<br/>
            <p>Admin,<br/>
            <p>Self-Checkout</p>
        </body>
        </html>
        """ %name
        sendEmail(email, html, text)
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
    if request.method=="POST":
        subject = request.form['subject']
        text = """
        Dear Customer,
        Thank you for contacting us!
        We whave recieved your message/query!
        One of our teammates will get in tough with you shortly.
        Thanks & Regards,
        Admin,
        Self-Checkout
        """ 
        html = """
        <html>
        <head>
        </head>
        <body>
            <p>Dear %s,</p>
            <p>Thank you for contacting us!<br/>
            We whave recieved your message/query!<br/>
            One of our teammates will get in tough with you shortly.</p><br/>
            <p>Thanks & Regards,<br/>
            <p>Admin,<br/>
            <p>Self-Checkout</p>
        </body>
        </html>
        """ %name
        sendEmail('svsumukh18@gmail.com', html, text)
        email = 'svsumukh18@gmail.com'
        text = """
        You have got a query!
        Sender : """ + email + """
        Subject : %s
        """  %subject
        html = """
        <html>
        <head>
        </head>
        <body>
            <p>You have recieved a query!<br/>
            Sender : """ + str(email) + """ <br/>
            Subject : %s</p><br/>
        </body>
        </html>
        """  %subject
        sendEmail('selfcheckoutsample@gmail.com', html, text)
        return render_template("contact.html")
    return render_template("contact.html")

@app.route('/viewCurrentBill', methods=['GET','POST'])
def viewCurrentBill():
    return render_template("viewCurrentBill.html")

@app.route('/viewAllBills', methods=['GET','POST'])
def viewAllBills():
    return render_template("viewAllBills.html")

if __name__ == "__main__":
    app.run(debug=True)