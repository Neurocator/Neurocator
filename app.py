from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
app = Flask(__name__) 

import mysql.connector
mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "Teamb1#123",
    database = "neurocator",
    auth_plugin='mysql_native_password'
)
cursor = mydb.cursor()

# @app.route('/', methods=['GET','POST'])
# def home():
#     return render_template('index.html.j2')

@app.route('/', methods=['GET'])
def index():
    if request.method == 'GET':
        return render_template('login.html.j2')
    
@app.route('/checklogin', methods=['GET', 'POST'])
def checkLogin():
    inputEmail = request.values.get("email")
    usertypedPassword = request.values.get("password")
    #checking server-side validation using specific methods
    inputs = ['email', 'password']
    #validated = serverSideValidation(inputs)
    return redirect(url_for(''))
    if validated==True:
        cursor = mysql.connection.cursor()
        query = "SELECT password, id FROM aanikatangirala_students WHERE email=%s"
        queryVars = (inputEmail, )
        cursor.execute(query, queryVars)
        mysql.connection.commit()
        results = cursor.fetchall()
        if (len(results) == 1):
            hashedPassword = results[0]['password']
            if check_password_hash(hashedPassword, usertypedPassword):
                session['aanikatangirala_username'] = inputEmail
                return redirect(url_for('home'))
            else:
                return redirect(url_for('index', incorrectLoginError=True))
        else:
            return redirect(url_for('index', incorrectLoginError=True))
    else:
        return redirect(url_for('index', blankLoginError=True))
    
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html.j2')
    else:
        inputFirstName = request.values.get("first-name")
        inputLastName = request.values.get("last-name")
        inputEmail = request.values.get("email")
        inputGradYear = request.values.get("year")
        inputPhoneNumber = request.values.get("phone-number")
        userTypedPassword = request.values.get("password")
        cursor = mysql.connection.cursor()
        query = "SELECT email FROM aanikatangirala_students WHERE email=%s"
        queryVars = (inputEmail, )
        cursor.execute(query, queryVars)
        mysql.connection.commit()
        results = cursor.fetchall()
        if (len(results) == 1):
            return redirect(url_for('signup', usernameTaken=True))
        else:
            #checking server-side validation using specific methods
            inputs = ['first-name', 'last-name', 'email', 'year', 'phone-number', 'password']
            validated = serverSideValidation(inputs)
            if validated==True:
                yearValidated = gradYearValidated(inputGradYear)    
                if yearValidated==True:
                    query = "INSERT INTO aanikatangirala_students (firstName, lastName, email, password, gradYear, phoneNumber) VALUES (%s, %s, %s, %s, %s, %s)"
                    queryVars = (inputFirstName, inputLastName, inputEmail, securedPassword, inputGradYear, inputPhoneNumber)
                    cursor.execute(query, queryVars)
                    mysql.connection.commit()
                    return redirect(url_for('index'))
                else:
                    return redirect(url_for('signup', blankSignupError=True))
            else:
                return redirect(url_for('signup', blankSignupError=True))

@app.route('/forum', methods=['GET','POST'])
def forum():
    return render_template('forum.html.j2')

@app.route('/live')
def live():
    return render_template("live.html.j2")

@app.route('/longtermplanning')
def planning():
    return render_template("longtermplanning.html.j2")

@app.route('/resources')
def resources():
    return render_template("resources.html.j2")

@app.route('/about')
def about():
    return render_template("about_us.html")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

#if __name__ == '__main__':
#    app.run(debug=True)
    
