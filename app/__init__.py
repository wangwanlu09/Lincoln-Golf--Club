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

def get_nav_details():
    nav_cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    nav_query = '''SELECT nav_order, nav_title
                FROM navbaritems
                ORDER BY nav_order;'''
    nav_cursor.execute(nav_query)
    nav_details = nav_cursor.fetchall()
    nav_cursor.close()
    return nav_details

def get_dropdown_details():
    dropdown_cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    dropdown_query = '''SELECT category, droptitle,drop_order
                        FROM dropdownitems;
                     '''
    dropdown_cursor.execute(dropdown_query)
    dropdown_details = dropdown_cursor.fetchall()
    dropdown_cursor.close()
    return dropdown_details

def get_footer_details():
    footer_cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    footer_query = '''SELECT contact_address, contact_email, contact_phone, facebook_url
                      FROM contact_details;
                    '''
    footer_cursor.execute(footer_query)
    footer_details = footer_cursor.fetchall()
    footer_cursor.close()
    return footer_details

@app.context_processor
def inject_common_data():
    nav_details = get_nav_details()
    dropdown_details = get_dropdown_details()
    footer_details = get_footer_details()
    
    return dict(nav_details=nav_details, dropdown_details=dropdown_details, footer_details=footer_details)

from app.homepag.view import home
from app.golf.view import golf
from app.results.view import golf

app.register_blueprint(home)
app.register_blueprint(golf)
app.register_blueprint(results)



