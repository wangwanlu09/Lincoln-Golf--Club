from app import mysql
from flask import Blueprint, render_template
import MySQLdb.cursors

course = Blueprint('results', __name__)

@results.route("/saturday_am")
def saturday_am():
    saturdayam_cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    saturdayam_query = "SELECT * FROM results WHERE dropnavid = 3 ;"
    saturdayam_cursor.execute(saturdayam_query)
    saturdayam_details = saturdayam_cursor.fetchall()
    saturdayam_cursor.close()
    return render_template("saturday_am.html",saturdayam_details=saturdayam_details)

@results.route("/saturday_pm")
def saturday_pm():
    saturdaypm_cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    saturdaypm_query = "SELECT * FROM results WHERE dropnavid = 4 ;"
    saturdaypm_cursor.execute(saturdaypm_query)
    saturdaypm_details = saturdaypm_cursor.fetchall()
    saturdaypm_cursor.close()
    return render_template("saturday_pm.html",saturdaypm_details=saturdaypm_details)

@results.route("/sunday_stable")
def sunday_stable():
    sundaystable_cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    sundaystable_query = "SELECT * FROM results WHERE dropnavid = 5 ;"
    sundaystable_cursor.execute(sundaystable_query)
    sundaystable_details = sundaystable_cursor.fetchall()
    sundaystable_cursor.close()
    return render_template("sunday_stable.html", sundaystable_details=sundaystable_details)

@results.route("/wedwackers")
def wedwackers():
    wedwackers_cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    wedwackers_query = "SELECT * FROM results WHERE dropnavid = 6 ;"
    wedwackers_cursor.execute(wedwackers_query)
    wedwackers_details = wedwackers_cursor.fetchall()
    wedwackers_cursor.close()
    return render_template("wedwackers.html", wedwackers_details=wedwackers_details)

@results.route("/tueswoman")
def tueswoman():
    tueswoman_cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    tueswoman_query = "SELECT * FROM results WHERE dropnavid = 7 ;"
    tueswoman_cursor.execute(tueswoman_query)
    tueswoman_details = tueswoman_cursor.fetchall()
    tueswoman_cursor.close()
    return render_template("tueswoman.html",tueswoman_details=tueswoman_details)

@results.route("/precup")
def precup():
    precup_cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    precup_query = "SELECT * FROM results WHERE dropnavid = 8 ;"
    precup_cursor.execute(precup_query)
    precup_details = precup_cursor.fetchall()
    precup_cursor.close()
    return render_template("precup.html",precup_details=precup_details)




