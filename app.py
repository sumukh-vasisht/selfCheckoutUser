from flask import Flask, render_template, request, redirect, session, url_for, flash
import json
from datetime import timedelta
import time
import pyrebase
import firebase_admin as firebase
from firebase_admin import firestore, storage
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

#FOR FIRESTORE
cred = firebase.credentials.Certificate("firebaseKey.json")
keyFile = open('pyrebaseKey.json','r')
keyJson = keyFile.read()
key = json.loads(keyJson)

firebase.initialize_app(cred,{'storageBucket':'selfcheckout-8b125.appspot.com'})
db = firestore.client() #For database
bucket = storage.bucket()
auth = pyrebase.initialize_app(key).auth() #For authentication

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

app.secret_key = "(SHITTU_CANNOT_CODE)-1"

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

@app.route('/')
def home():
    if 'token' in session:
        # print(session['token'])
        # email = session['email']
        # billDetails = db.collection('bills').document(email).get().to_dict()
        # print(billDetails)
        return render_template('home.html')
    else:
        return redirect(url_for('login'))

@app.route('/login', methods=['GET','POST'])
def login():
    if 'token' not in session:
        message = ""
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            try:
                userData = auth.sign_in_with_email_and_password(username,password)
                userDetails = db.collection('users').document(username).get().to_dict()
                print(userDetails)
                session['name'] = userDetails['name']
                session['email'] = userDetails['email']
                session['phoneNumber'] = userDetails['phoneNumber']
                session['age'] = userDetails['age']
                session['address'] = userDetails['address']
                session['token'] = userData['idToken']
                print(dict(session))
                return redirect('/')
            except Exception as e:
                error = ""
                error = json.loads(e.args[1])['error']['message']
                message = error.replace('_',' ')
        return render_template('login.html',message=message)
    else:
        return redirect('/')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phoneNumber = request.form['phoneNumber']
        age = request.form['age']
        address = request.form['address']
        password = request.form['pwd1']
        print(name,email,phoneNumber,age,address,password)
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
        auth.create_user_with_email_and_password(email,password)
        db.collection(u'users').document(email).set({
            'name':name,
            'email':email,
            'phoneNumber':phoneNumber,
            'age':age,
            'address':address,
            'billQuantity':0
        })
        userData = auth.sign_in_with_email_and_password(email,password) 
        session['name'] = name
        session['email'] = email
        session['phoneNumber'] = phoneNumber
        session['age'] = age
        session['address'] = address
        session['token'] = userData['idToken']
        return redirect(url_for('home'))
    return render_template("register.html")

@app.route('/guestLogin', methods=['GET', 'POST'])
def guestLogin():
    return render_template("guestLogin.html")

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
    if 'token' in session:
        email = session['email']
        userDetails = db.collection('users').document(email).get().to_dict()
        currentBillNumber = userDetails['billQuantity']
        if currentBillNumber==0:
            message = "There are no bills yet"
            return render_template('viewCurrentBill.html', date=message,items=[], quantity=[], prices=[], totalPrice=0, leng=0)
        documentID = email+str(currentBillNumber)
        billDetails = db.collection('bills').document(documentID).get().to_dict()
        date=billDetails['date']
        totalPrice=billDetails['totalPrice']
        number = len(billDetails)
        numberOfItems = number-2        
        items=['0' for i in range(numberOfItems//3)]
        quantity=['0' for i in range(numberOfItems)]
        prices=['0' for i in range(numberOfItems)]
        for key,value in billDetails.items():
            if 'item' in key:
                for z in key:
                    if z.isdigit():
                        items[int(z)-1]=value
            elif 'quantity' in key:
                for z in key:
                    if z.isdigit():
                        quantity[int(z)-1]=value
            elif 'price' in key:
                for z in key:
                    if z.isdigit():
                        prices[int(z)-1]=value                        
        return render_template('viewCurrentBill.html',date=date, items=items, quantity=quantity, prices=prices, totalPrice=totalPrice, leng=len(items))
    return render_template("viewCurrentBill.html")

@app.route('/viewCurrentBillFromAllBills/<string:id>', methods=['GET','POST'])
def viewCurrentBillFromAllBills(id):
    if 'token' in session:
        email = session['email']
        userDetails = db.collection('users').document(email).get().to_dict()
        documentID = email+id
        billDetails = db.collection('bills').document(documentID).get().to_dict()
        date=billDetails['date']
        totalPrice=billDetails['totalPrice']
        number = len(billDetails)
        numberOfItems = number-2        
        items=['0' for i in range(numberOfItems//3)]
        quantity=['0' for i in range(numberOfItems)]
        prices=['0' for i in range(numberOfItems)]
        for key,value in billDetails.items():
            if 'item' in key:
                for z in key:
                    if z.isdigit():
                        items[int(z)-1]=value
            elif 'quantity' in key:
                for z in key:
                    if z.isdigit():
                        quantity[int(z)-1]=value
            elif 'price' in key:
                for z in key:
                    if z.isdigit():
                        prices[int(z)-1]=value                        
        return render_template('viewCurrentBill.html',date=date, items=items, quantity=quantity, prices=prices, totalPrice=totalPrice, leng=len(items))
    return render_template("viewCurrentBill.html")

@app.route('/viewAllBills', methods=['GET','POST'])
def viewAllBills():
    if 'token' in session:
        email = session['email']
        userDetails = db.collection('users').document(email).get().to_dict()
        currentBillNumber=userDetails['billQuantity']
        documentIDs=[]
        for i in range(currentBillNumber):
            documentIDs.append(email+str(i+1))
        dates=[]
        for i in range(len(documentIDs)):
            billDetails = db.collection('bills').document(documentIDs[i]).get().to_dict()
            date=billDetails['date']
            dates.append(date)
        return render_template("viewAllBills.html", dates=dates, leng=len(dates))
    return render_template("viewAllBills.html")

@app.route('/logout')
def logout():
    if 'token' in session:
        session.pop('token')
        session.pop('name')
        session.pop('email')
        session.pop('phoneNumber')
        session.pop('age')
        session.pop('address')
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)