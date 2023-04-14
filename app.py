#TODO MAKE SURE NO TWO USERNAMES ARE THE SAME

#imports
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date
import requests

#Connect to database
app = Flask(__name__)
app.config['MYSQL_HOST'] = 'mysql.2122.lakeside-cs.org'
app.config['MYSQL_USER'] = 'student2122'
app.config['MYSQL_PASSWORD'] = 'm545CS42122'
app.config['MYSQL_DB'] = '2122project'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.config['SECRET_KEY'] = 'meatlessmondaysaresorrowful'
mysql = MySQL(app)

@app.route('/')
@app.route('/index')
def index():
    """
    Function that sets up index page
    parameters: none
    return: rendered template for index.html
    """
    cursor = mysql.connection.cursor()
    query = 'SELECT username FROM catelewison_login'
    cursor.execute(query,)
    mysql.connection.commit()
    results = cursor.fetchall()
    return render_template('index.html', username=session.get('catelewison_username'), rows=results)

@app.route('/signup', methods=['GET','POST'])
def signup():
    """
    Function that puts a new user into the database
    parameters: none
    return: redirect to home page
    """
    if request.method == 'GET':
        return render_template('signup.html')
    else: #Signup form
        firstName = request.form.get('firstName')
        lastName = request.form.get('lastName')
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        #Hash password
        securedPassword = generate_password_hash(password)
        #Insert into database
        cursor = mysql.connection.cursor()
        query = 'INSERT INTO catelewison_login(first_name, last_name, email, username, password) VALUES (%s, %s, %s, %s, %s)'
        queryVars = (firstName, lastName, email, username,securedPassword,)
        cursor.execute(query, queryVars)
        mysql.connection.commit()
        #Back to home page
        return redirect(url_for('index'))

@app.route('/login', methods=['GET','POST'])
def login():
    """
    Function that logs the user in
    parameters: none
    return: redirect to login page if password incorrect, to home page if correct
    """
    if request.method == 'GET':
        return render_template('login.html', error=request.args.get('error'))
    else:
        #Login form
        username = request.form.get('username')
        password = request.form.get('password')

        #Check database for valid username/password

        #Get the password for this username.
        cursor = mysql.connection.cursor()
        query = 'SELECT password FROM catelewison_login WHERE username=%s'
        queryVars = (username,)
        cursor.execute(query, queryVars)
        mysql.connection.commit()
        results = cursor.fetchall()

        if (len(results) == 1):
            hashedPassword = results[0]['password']
            #Verify that their password matches
            if check_password_hash(hashedPassword, password):
                #Log in
                session['catelewison_username'] = username
                return redirect(url_for('index'))
            else:
                #Incorrect password
                return redirect(url_for('login', error=True)) #Passing GET param error=True
        else:
            #Bad username
            return redirect(url_for('login', error=True))

@app.route('/logout')
def logout():
    """
    Function that sets up the logout page
    parameters: none
    return: redirect back to homepage
    """
    #Remove username from session
    session.pop('catelewison_username', None)
    #Redirect back to the homepage.
    return redirect(url_for('index'))

@app.route('/tripreport',methods=['GET','POST'])
def tripreport():
    """
    Function that sets up the tripreport page
    parameters: none
    return: file tripreport.html with information
    """
    #set up API
    response = requests.get("https://www.wsdot.wa.gov/Traffic/api/MountainPassConditions/MountainPassConditionsREST.svc/GetMountainPassConditionsAsJson?AccessCode=f41ef409-c305-4f93-a852-33987ad94f4a")
    jsonResponse = response.json()

    titles = []
    conditions = []
    advisories = []
    temperatures = []
    #Get API data
    #Iterate through to collect data we want
    for id in range(len(jsonResponse)):
        title = jsonResponse[id]["MountainPassName"]
        titles.append(title)
        condition = jsonResponse[id]["RoadCondition"]
        conditions.append(condition)
        advisory = jsonResponse[id]["TravelAdvisoryActive"]
        advisories.append(advisory)
        temperature = jsonResponse[id]["TemperatureInFahrenheit"]
        temperatures.append(temperature)

    if request.method == 'GET':
        results = getReports()
        return render_template('tripreport.html', username=session.get('catelewison_username'), rows=results, titles=titles, conditions=conditions, advisories=advisories, temperatures=temperatures)
    else:
        results = getReports()
        name = session.get('catelewison_username')
        report = stringCheck(request.form.get("report"))
        location = stringCheck(request.form.get("location"))
        rating = request.form.get("rating")
        danger =  request.form.get("danger")
        image =  stringCheck(request.form.get("image"))
        date = request.form.get("date")
        #Set up the cursor
        cur = mysql.connection.cursor()
        #Use placeholder %s for input
        query = "INSERT INTO catelewison_tripreports (location, date, rating, report, danger, name, image) VALUES (%s, %s, %s, %s, %s, %s, %s);"
        #The list of ordered variables to be inserted in placeholders
        queryVars = (location,date,rating,report,danger,name, image)
        #Execute query
        cur.execute(query, queryVars);
        #Commit query
        mysql.connection.commit()
        #Render results template
        return redirect(url_for('tripreport'))
        #redirect back to page instead of rendering template

@app.route('/about')
def about():
    """
    Function that sets up the about page
    parameters: none
    return: file about.html with information
    """
    return render_template('about.html', username=session.get('catelewison_username'))

@app.route('/chatroom', methods=['GET','POST'])
def chatroom():
    """
    Function that sets up the chatroom and gets user information
    parameters: none
    return: file chatroom.html with information
    """
    if request.method == 'GET':
        results = getChats()
        return render_template('chatroom.html', username=session.get('catelewison_username'), rows=results)
    elif request.method == 'POST':
        results = getChats()
        chat = stringCheck(request.form.get("textchat"))
        name = session.get('catelewison_username')
        today = date.today()
        #Set up the cursor
        cur = mysql.connection.cursor()
        #Use placeholder %s for input
        query = "INSERT INTO catelewison_chat (name, chat, date) VALUES (%s, %s, %s);"
        #The list of ordered variables to be inserted in placeholders
        queryVars = (name,chat,today,)
        #Execute query
        cur.execute(query, queryVars);
        #Commit query
        mysql.connection.commit()
        #Render results template
        return redirect(url_for('chatroom'))

@app.route('/market', methods=['GET','POST'])
def market():
    """
    Function that sets up the media page
    parameters: none
    return: file media.html with information
    """
    if request.method == 'GET':
        results = getMarket()
        return render_template('market.html', username=session.get('catelewison_username'), rows=results)
    else:
        results = getMarket()
        name = session.get('catelewison_username')
        contact = stringCheck(request.form.get("contact"))
        selling = stringCheck(request.form.get("selling"))
        price = stringCheck(request.form.get("price"))
        image = stringCheck(request.form.get("image"))
        notes = stringCheck(request.form.get("notes"))
        #Set up the cursor
        cur = mysql.connection.cursor()
        #Use placeholder %s for input
        query = "INSERT INTO catelewison_market (name, contact, selling, price, image, notes) VALUES (%s, %s, %s, %s, %s, %s);"
        #The list of ordered variables to be inserted in placeholders
        queryVars = (name, contact, selling, price, image, notes,)
        #Execute query
        cur.execute(query, queryVars);
        #Commit query
        mysql.connection.commit()
        #Render results template
        return redirect(url_for('market'))
        #redirect back to page instead of rendering template

@app.route('/media', methods=['GET','POST'])
def media():
    """
    Function that sets up the media page
    parameters: none
    return: file media.html with information
    """
    if request.method == 'GET':
        results = getMedia()
        return render_template('media.html', username=session.get('catelewison_username'), rows=results)
    else:
        results = getMedia()
        name = session.get('catelewison_username')
        media = request.form.get("media")
        caption = stringCheck(request.form.get("notes"))
        mediaType = stringCheck(request.form.get("mediaType"))
        #Set up the cursor
        cur = mysql.connection.cursor()
        #Use placeholder %s for input
        query = "INSERT INTO catelewison_media (name, media, caption, type) VALUES (%s, %s, %s, %s);"
        #The list of ordered variables to be inserted in placeholders
        queryVars = (name, media, caption, mediaType)
        #Execute query
        cur.execute(query, queryVars);
        #Commit query
        mysql.connection.commit()
        #Render results template
        return redirect(url_for('media'))
        #redirect back to page instead of rendering template

def checkNum(num):
    """
    Function that checks the validity of a number input
    parameters: number to check
    return: valid integer
    """
    if num >= 0 and num <= 10:
        return num
    else:
        return 5

def stringCheck(name):
    """
    Function that checks the validity of a string input
    parameters: string to check
    return: valid string output
    """
    if type(name) == str:
        return name
    else:
        return "N/A"

def getChats():
    """
    Function that gets chats from the database
    return: chat data
    """
    cursor = mysql.connection.cursor()
    query = 'SELECT * FROM catelewison_chat ORDER BY id DESC'
    cursor.execute(query,)
    mysql.connection.commit()
    return cursor.fetchall()

def getReports():
    """
    Function that gets trip reports from the database
    return: trip report data
    """
    cursor = mysql.connection.cursor()
    query = 'SELECT * FROM catelewison_tripreports'
    cursor.execute(query,)
    mysql.connection.commit()
    return cursor.fetchall()

def getMarket():
    """
    Function that gets market data
    return: market data
    """
    cursor = mysql.connection.cursor()
    query = 'SELECT * FROM catelewison_market ORDER BY user_id DESC'
    cursor.execute(query,)
    mysql.connection.commit()
    return cursor.fetchall()

def getMedia():
    """
    Function that gets media data
    return: media data
    """
    cursor = mysql.connection.cursor()
    query = 'SELECT * FROM catelewison_media ORDER BY id DESC'
    cursor.execute(query,)
    mysql.connection.commit()
    return cursor.fetchall()
