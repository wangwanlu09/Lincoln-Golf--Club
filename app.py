from flask import Flask 
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import session
from flask_mysqldb import MySQL
from flask_mail import Mail, Message
import MySQLdb.cursors
import bcrypt
import re
import secrets

app = Flask(__name__)

app.secret_key = secrets.token_hex(16)


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'mysql native_password Rubywong&600396'
app.config['MYSQL_DB'] = 'golfclub'
app.config['MYSQL_PORT'] = 3306
mysql = MySQL(app)

# Admin Eamil config
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'wangwanlu05@gmail.com'
app.config['MAIL_PASSWORD'] = 'wwl600396'
mail = Mail(app)

@app.route("/")
def home():
    cursor = mysql.connection.cursor()
    return render_template("base.html")

@app.route("/home")
def sponsor():
    cursor = mysql.connection.cursor()
    return render_template("home.html")

@app.route('/register', methods=['GET', 'POST'])
def register():
    # Output message if something goes wrong...
    msg = ''
    # Check if "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        # Create variables for easy access
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirmpassword']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM customer WHERE email = %s', (email,))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            msg = 'Please enter a valid email address!'
        elif not re.match(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$', password):
            msg ='Password must be at least 8 characters long and contain at least one letter, one number and specified special characters!'
        elif password != confirm_password:
            msg ='Passwords must match.'
        elif not email or not password:
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            rolename = "customer"
            roleid = 1
            hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            salt = bcrypt.gensalt().decode('utf-8')
            insert_sign_query =  '''
                INSERT INTO sign(roleid,rolename,email_id,
                hash,salt,create_date,last_update_date)
                VALUES (%s, %s, %s, %s, %s, %s, NOW(), NOW())
                '''
            values_sign = (roleid,rolename,email,hashed,salt)
            cursor.execute(insert_sign_query,values_sign)
        
        
            insert_customer_query = '''
                INSERT INTO customer(role_id, role_name, customer_id, email_id)
                VALUES (%s, %s, %s)
            '''
            values_customer=(roleid, rolename,email)
            cursor.execute(insert_customer_query,values_customer)
            mysql.connection.commit()
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)


####add memebership_number!!!!!!!!!
@app.route('/login/', methods=['GET', 'POST'])
def login():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        # Create variables for easy access
        email = request.form['email']
        password = request.form['password']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM sign WHERE email = %s', (email,))
        # Fetch one record and return result
        account = cursor.fetchone()
        
        if account and 'hash' in account:
            stored_hashed_password = account['hash']
            if bcrypt.checkpw(password.encode('utf-8'),stored_hashed_password.encode('utf-8')):
                # Create session data, we can access this data in other routes
                session['loggedin'] = True
                session['email'] = account['email']
                user_role_name = account.get('rolename', 'default_role')
                session['rolename'] = user_role_name
                session['customer_eid'] = account['id']
                session['staff_eid'] = account['id']

                # Fetch and store customer information
                if account['rolename'] == 'customer':
                    cursor.execute('SELECT * FROM customer WHERE customer_id = %s', (account['id'],))
                    customer_info = cursor.fetchone()
                    print(customer_info)
                    session['account'] = customer_info
                    # Redirect to home page
                    return render_template('profile.html', account=customer_info)
                
                
                elif account['role_name'] == 'admin':
                    cursor.execute('SELECT * FROM staff WHERE staff_id = %s', (account['id'],))
                    staff_info = cursor.fetchone()
                    print(staff_info)
                    session['account'] = staff_info
                    return render_template('adminprofile.html', account=staff_info, username=session['username'])
            else:
                #password incorrect
                msg = 'Incorrect username/password!'
        else:
            # Account doesnt exist or username incorrect
            msg = 'Incorrect username'
    # Show the login form with message (if any)
    return render_template('home.html', msg=msg)


@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('email', None)
   # Redirect to login page
   return redirect(url_for('login'))


@app.route('/course')
def course():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT course_name, course_img FROM course;")
    courses = cursor.fetchall()

    return render_template('course.html', courses=courses)


@app.route("/contactdetils")
def contactdetils():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT contact_address, contact_email, contact_phone, facebook_url, contact_map FROM contact_details;")
    contactdetils = cursor.fetchall() 

    return render_template('contact_details.html', contactdetils=contactdetils)

@app.route("/contactmessage", methods=['GET', 'POST'])
def contactmessage():
    if request.method == "POST":
        sdname = request.form["Name"]
        sdemail = request.form['Email']
        sdphone = request.form['Phone']
        sdsubject = request.form['Subject']
        sdmessage = request.form['Message']
        
        if not re.match(r'^[A-Za-z\s]+$', sdname):
            msg = 'Please enter a valid name. Only letters are allowed!'
        elif not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', sdemail):
            msg = 'Please enter a valid email address!'
        elif not re.match(r'^[0-9]+$', sdphone):
            msg = 'Invalid phone number! Must be a non-negative integer.'
        elif not re.match(r'^[a-zA-Z0-9\s]+$', sdsubject):
            msg = 'Invalid subject! Must contain only letters, numbers, and spaces.'
        elif not re.match(r'^[a-zA-Z0-9\s]+$', sdmessage):
            msg = 'Invalid message! Must contain only letters, numbers, and spaces.'
        elif not sdname or not sdemail or not sdphone or not sdsubject or not sdmessage:
            msg = 'Please fill out the form!'
        else:
            msg = Message('New Contact Message from User',
                          sender='wangwanlu05@gmail.com',  
                          recipients=['admin@example.com']) 
            msg.body = f'Name: {sdname}\nEmail: {sdemail}\nPhone: {sdphone}\nSubject: {sdsubject}\nMessage: {sdmessage}'
            mail.send(msg)

            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            insert_sdmessage_query = '''
                INSERT INTO contact_message (contactsd_name, contactsd_email, contactsd_phone, contactsd_subject, 
                contactsd_message)
                VALUES (%s, %s, %s, %s, %s);
            '''
            values_sdmessage=(sdname, sdemail, sdphone, sdsubject, sdmessage)

            cursor.execute(insert_sdmessage_query, values_sdmessage)
            mysql.connection.commit()
            msg = 'You have successfully sent the message!'

    elif request.method == 'POST':
        msg = 'Please fill out the form!'
    return render_template('contact_message.html', msg=msg)



if __name__ == '__main__':
    app.run(debug="True")
