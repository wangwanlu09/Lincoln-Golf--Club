from app import mysql
from flask import Blueprint, render_template
import MySQLdb.cursors

course = Blueprint('course', __name__)

@course.route("/course")
def coursepage():
    return render_template("course.html")




