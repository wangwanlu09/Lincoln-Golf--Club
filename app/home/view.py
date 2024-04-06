from app import mysql
from flask import Blueprint, render_template
import MySQLdb.cursors

home = Blueprint('homepage', __name__)

@homepage.route("/")
def homepage():
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
    return render_template("home.html", home_details=home_details, sponsors_image=sponsors_image)


def get_news_details():
    news_cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    news_query = "SELECT * FROM homedetails WHERE homeorder = 2;"
    news_cursor.execute(news_query)
    news_details = news_cursor.fetchall()
    news_cursor.close()
    return news_details

@homepage.route("/news")
def news():
    news_tdetails = get_news_details()
    return render_template("news.html", news_tdetails= news_tdetails)

@homepage.route("/news_details")
def news_details():
    news_details = get_news_details()
    return render_template("news_details.html", news_details=news_details)

@homepage.route("/open_hours")
def open_hours():
    openhours_cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    openhours_query = "SELECT * FROM homedetails WHERE homeorder = 5;"
    openhours_cursor.execute(openhours_query)
    openhours_details = openhours_cursor.fetchall()
    openhours_cursor.close()
    return render_template("open_hours.html", openhours_details=openhours_details)




