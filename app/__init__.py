from flask import Flask 
from flask_mysqldb import MySQL
from app import connect

app = Flask(__name__)
app.secret_key = 'golfclubsecretkey'

app.config['MYSQL_HOST'] = connect.dbhost
app.config['MYSQL_USER'] = connect.dbuser
app.config['MYSQL_PASSWORD'] = connect.dbpass
app.config['MYSQL_DB'] = connect.dbname
app.config['MYSQL_PORT'] = connect.dbname

mysql = MySQL(app)

from app.home.view import home
from app.course.view import course

app.register_blueprint(home)
app.register_blueprint(course)



