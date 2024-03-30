from app import mysql
from flask import Blueprint, render_template
import MySQLdb.cursors

home = Blueprint('home', __name__)

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

@home.route("/")
def homepage():
    nav_details = get_nav_details()
    dropdown_details = get_dropdown_details()

    home_cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    home_query = "SELECT * FROM homecontent;"
    home_cursor.execute(home_query)
    home_details = home_cursor.fetchall()
    home_cursor.close()

    sponsors_cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    sponsors_query = """SELECT image 
                        FROM coursesponsors
                        WHERE image IS NOT NULL
                        UNION
                        SELECT image 
                        FROM clubsponsors
                        WHERE image IS NOT NULL;
                        """
    sponsors_cursor.execute(sponsors_query)
    sponsors_image = sponsors_cursor.fetchall()
    sponsors_cursor.close()
    return render_template("home.html", home_details=home_details, sponsors_image=sponsors_image, nav_details=nav_details, dropdown_details=dropdown_details)




