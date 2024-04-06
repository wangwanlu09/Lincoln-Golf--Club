from app import mysql
from flask import Blueprint, render_template
import MySQLdb.cursors

course = Blueprint('golf', __name__)

@golf.route("/course")
def course():
    course_cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    course_query = "SELECT * FROM golf WHERE dropnavidg = 1 ;"
    course_cursor.execute(course_query)
    course_details = course_cursor.fetchall()
    course_cursor.close()
    return render_template("course.html", course_details=course_details)

@golf.route("/score_card")
def score_card():
    scorecard_cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    scorecard_query = "SELECT * FROM golf WHERE dropnavidg = 2 ;"
    scorecard_cursor.execute(scorecard_query)
    scorecard_details = scorecard_cursor.fetchall()
    scorecard_cursor.close()
    return render_template("score_card.html", scorecard_details=scorecard_details)




