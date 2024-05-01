from flask import Flask 
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import session
from flask_mysqldb import MySQL
from flask import flash
from flask_mail import Mail, Message
import random
import MySQLdb.cursors
import bcrypt
import re
import secrets

app = Flask(__name__)
mail = Mail(app)

app.secret_key = secrets.token_hex(16)


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'mysql native_password Rubywong&600396'
app.config['MYSQL_DB'] = 'golfclub'
app.config['MYSQL_PORT'] = 3306
mysql = MySQL(app)

@app.context_processor
def inject_nav_and_footer():
    nav_details = get_nav_details()
    dropdown_details = get_dropdown_details()
    footer_details = get_footer_details()
    return dict(nav_details=nav_details, footer_details=footer_details, dropdown_details=dropdown_details)

def get_nav_details():
    nav_cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    nav_query = """
    SELECT DISTINCT ni.nav_order, ni.nav_title
    FROM navbaritems ni
    ORDER BY ni.nav_order;
    """
    nav_cursor.execute(nav_query)
    nav_details = nav_cursor.fetchall()   
    nav_cursor.close()   
    return nav_details

def get_dropdown_details():
    dropdown_cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    dropdown_query = """
    SELECT *
    FROM dropdownitems
    """
    dropdown_cursor.execute(dropdown_query)
    dropdown_details = dropdown_cursor.fetchall()   
    dropdown_cursor.close()   
    return dropdown_details

def get_footer_details():
    footer_cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    footer_query = "SELECT * FROM contact_details;"
    footer_cursor.execute(footer_query)
    footer_details = footer_cursor.fetchall()
    footer_cursor.close()
    return footer_details

def get_home_details():
    home_cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    home_query = "SELECT * FROM homecontent;"
    home_cursor.execute(home_query)
    home_details = home_cursor.fetchall()
    home_cursor.close()
    return home_details

def get_sponsors_image():
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
    return sponsors_image
@app.route("/")
def home():
    home_details = get_home_details()
    sponsors_image = get_sponsors_image()
    return render_template("home.html", home_details=home_details, sponsors_image=sponsors_image)

@app.route("/mainhome", methods=['GET', 'POST'])
def mainhome():
    home_details=get_home_details()
    return render_template("mainhome.html", home_details= home_details)

@app.route("/mainhomeedit/<int:home_order>", methods=["GET", "POST"])
def mainhomeedit(home_order):
    msg = ""
    home_details = get_home_details()
    if request.method == "POST":
        newhometitle = request.form.get("hometitle")
        newhomedes = request.form.get("homedes")
        if not re.match(r'^.{1,100}$', newhometitle):
            msg = 'Please enter a valid title!'
        else:
            try:
                # Update home details information
                newhomedetails_cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                updatehomedetails_query = "UPDATE homecontent " \
                        "SET hometitle = %s, homedes = %s " \
                        "WHERE home_order = %s"
                newhomedetails_cursor.execute(updatehomedetails_query, (newhometitle, newhomedes, home_order))
                mysql.connection.commit()
                newhomedetails_cursor.close()
                msg = 'Homepage details updated successfully!'
                home_details = get_home_details()
                return render_template("mainhomeedit.html", home_details=home_details, home_order=home_order, msg=msg)
            except:
                # Handle database update failure
                return "Failed to update homepage details"
    return render_template("mainhomeedit.html", home_details=home_details, home_order=home_order, msg=msg)

@app.route("/mainhomeeditp/<int:home_order>", methods=["GET", "POST"])
def mainhomeeditp(home_order):
    msg = ""
    home_details = get_home_details()
    if request.method == "POST":
        newimg = request.form.get("img")
        try:
            # Update home details information
            newhomedetails_cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            updatehomedetails_query = "UPDATE homecontent " \
                    "SET img = %s " \
                    "WHERE home_order = %s"
            newhomedetails_cursor.execute(updatehomedetails_query, (newimg, home_order))
            mysql.connection.commit()
            newhomedetails_cursor.close()
            msg = 'Homepage image details updated successfully!'
            home_details = get_home_details()
            return render_template("mainhomeeditp.html", home_details=home_details, home_order=home_order, msg=msg)
        except Exception as e:
            # Handle database update failure
            return "Failed to update homepage image details: {}".format(str(e))
    return render_template("mainhomeeditp.html", home_details=home_details, home_order=home_order, msg=msg)

def get_news_details():
    news_cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    news_query = "SELECT * FROM homedetails WHERE homeorder = 2;"
    news_cursor.execute(news_query)
    news_details = news_cursor.fetchall()
    news_cursor.close()
    return news_details
    
@app.route("/news")
def news():
    news_tdetails = get_news_details()
    return render_template("news.html", news_tdetails= news_tdetails)

@app.route("/news_details")
def news_details():
    news_details = get_news_details()
    return render_template("news_details.html", news_details=news_details)

@app.route("/mananews", methods=['GET', 'POST'])
def mananews():
    news_details = get_news_details()
    return render_template("mananews.html", news_details=news_details)

def get_funcentre_details():
    funcentre_cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    funcentre_query = "SELECT * FROM homedetails WHERE homeorder = 3;"
    funcentre_cursor.execute(funcentre_query)
    funcentre_details = funcentre_cursor.fetchall()
    funcentre_cursor.close()
    return funcentre_details

@app.route("/function_centre")
def function_centre():
    funcentre_details = get_funcentre_details()
    return render_template("function_centre.html",  funcentre_details=funcentre_details)

@app.route("/mananfuncen", methods=['GET', 'POST'])
def mananfuncen():
    funcentre_details = function_centre()
    return render_template("mananfuncen.html",  funcentre_details=funcentre_details)

def get_memberapplication_details():
    memberapplication_cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    memberapplication_query = "SELECT * FROM homedetails WHERE homeorder = 4;"
    memberapplication_cursor.execute(memberapplication_query)
    memberapplication_details = memberapplication_cursor.fetchall()
    memberapplication_cursor.close()
    return memberapplication_details

@app.route("/member_application")
def member_application():
    memberapplication_details = get_memberapplication_details()
    return render_template("member_application.html",  memberapplication_details=memberapplication_details)

@app.route("/member", methods=['GET', 'POST'])
def member():
    memberapplication_details = get_memberapplication_details()
    return render_template("member_application.html",  memberapplication_details=memberapplication_details)


def get_openhours_details():
    openhours_cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    openhours_query = "SELECT * FROM homedetails WHERE homeorder = 5;"
    openhours_cursor.execute(openhours_query)
    openhours_details = openhours_cursor.fetchall()
    openhours_cursor.close()
    return openhours_details

@app.route("/open_hours")
def open_hours():
    openhours_details = get_openhours_details()
    return render_template("open_hours.html", openhours_details=openhours_details)

@app.route("/manaopenhours", methods=['GET', 'POST'])
def manaopenhours():
    openhours_details = get_openhours_details()
    return render_template("manaopenhours.html", openhours_details=openhours_details)


def get_course_details():
    course_cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    course_query = "SELECT * FROM golf WHERE dropnavidg = 1 ;"
    course_cursor.execute(course_query)
    course_details = course_cursor.fetchall()
    course_cursor.close()
    return course_details

@app.route("/course")
def course():
    course_details = get_course_details()
    return render_template("course.html", course_details=course_details)

@app.route("/manacourses")
def manacourses():
    if request.method == 'POST':
        gid = request.form.get('gid')
        deletecourses_query = "DELETE FROM golf WHERE gid = %s;"
        cursor = mysql.connection.cursor()
        cursor.execute(deletecourses_query, (gid,))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('manacourses')) 
    course_details = get_course_details()
    return render_template("manacourses.html", course_details=course_details)

@app.route("/manacoursesedit/<int:gid>", methods=["GET", "POST"])
def manacoursesedit(gid):
    msg = ""
    course_details = get_course_details()
    if request.method == "POST":
        newcourse_name = request.form.get("course_name")
        
        if not re.match(r'^.{1,100}$', newcourse_name):
            msg = 'Please enter a valid course name!'
        else:
            try:
                # Update course information
                newcourse_cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                updatecourse_query = "UPDATE golf " \
                        "SET course_name = %s " \
                        "WHERE gid = %s"
                newcourse_cursor.execute(updatecourse_query, (newcourse_name))
                mysql.connection.commit()
                newcourse_cursor.close()
                msg = 'Course name updated successfully!'
                course_details = get_course_details()
                return render_template("manacoursesedit.html", course_details=course_details, gid=gid, msg=msg)
            except Exception as e:
                # Handle database update failure
               return "Failed to update course details: {}".format(str(e))
   
    return render_template("manacoursesedit.html", course_details=course_details, gid=gid, msg=msg)

@app.route("/manacourseseditp/<int:gid>", methods=["GET", "POST"])
def manacourseseditp(gid):
    msg = ""
    course_details = get_course_details()
    if request.method == "POST":
        newimage = request.form.get("image")
        try:    
            # Update course information
            newcourse_cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            updatecourse_query = "UPDATE golf " \
                    "SET image = %s " \
                    "WHERE gid = %s"
            newcourse_cursor.execute(updatecourse_query, (newimage,gid))
            mysql.connection.commit()
            newcourse_cursor.close()
            msg = 'Course image updated successfully!'
            course_details = get_course_details()
            return render_template("manacourseseditp.html", course_details=course_details, gid=gid, msg=msg)
        except Exception as e:
            # Handle database update failure
            return "Failed to update course details: {}".format(str(e))
    
    return render_template("manacourseseditp.html", course_details=course_details, gid=gid, msg=msg)



def get_scorecard_details():
    scorecard_cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    scorecard_query = "SELECT * FROM golf WHERE dropnavidg = 2 ;"
    scorecard_cursor.execute(scorecard_query)
    scorecard_details = scorecard_cursor.fetchall()
    scorecard_cursor.close()
    return scorecard_details

@app.route("/score_card")
def score_card():
    scorecard_details = get_scorecard_details()
    return render_template("score_card.html", scorecard_details=scorecard_details)

@app.route("/manascorecard", methods=['GET', 'POST'])
def manascorecard():
    if request.method == 'POST':
        gid = request.form.get('gid')
        deletescorecard_query = "DELETE FROM golf WHERE gid = %s;"
        cursor = mysql.connection.cursor()
        cursor.execute(deletescorecard_query, (gid,))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('manascorecard')) 
     
    scorecard_details = get_scorecard_details()
    return render_template("manascorecard.html", scorecard_details=scorecard_details)


def get_saturdayam_details():
    saturdayam_cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    saturdayam_query = "SELECT * FROM results WHERE dropnavid = 3 ;"
    saturdayam_cursor.execute(saturdayam_query)
    saturdayam_details = saturdayam_cursor.fetchall()
    saturdayam_cursor.close()
    return saturdayam_details

@app.route("/saturday_am")
def saturday_am():
    saturdayam_details = get_saturdayam_details()
    return render_template("saturday_am.html",saturdayam_details=saturdayam_details)

@app.route("/manasaturdayam", methods=['GET', 'POST'])
def manasaturdayam():
    saturdayam_details = get_saturdaypm_details()
    return render_template("manasaturdayam.html",saturdayam_details=saturdayam_details)

def get_saturdaypm_details():
    saturdaypm_cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    saturdaypm_query = "SELECT * FROM results WHERE dropnavid = 4 ;"
    saturdaypm_cursor.execute(saturdaypm_query)
    saturdaypm_details = saturdaypm_cursor.fetchall()
    saturdaypm_cursor.close()
    return saturdaypm_details

@app.route("/saturday_pm")
def saturday_pm():
    saturdaypm_details = get_saturdaypm_details()
    return render_template("saturday_pm.html",saturdaypm_details=saturdaypm_details)

@app.route("/manasaturdaypm", methods=['GET', 'POST'])
def manasaturdaypm():
    saturdaypm_details = get_saturdaypm_details()
    return render_template("manasaturdaypm.html",saturdaypm_details=saturdaypm_details)

def get_sundaystable_details():
    sundaystable_cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    sundaystable_query = "SELECT * FROM results WHERE dropnavid = 5 ;"
    sundaystable_cursor.execute(sundaystable_query)
    sundaystable_details = sundaystable_cursor.fetchall()
    sundaystable_cursor.close()
    return sundaystable_details

@app.route("/sunday_stable")
def sunday_stable():
    sundaystable_details = get_sundaystable_details()
    return render_template("sunday_stable.html", sundaystable_details=sundaystable_details)

def get_wedwackers_details():
    wedwackers_cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    wedwackers_query = "SELECT * FROM results WHERE dropnavid = 6 ;"
    wedwackers_cursor.execute(wedwackers_query)
    wedwackers_details = wedwackers_cursor.fetchall()
    wedwackers_cursor.close()
    return wedwackers_details

@app.route("/wedwackers")
def wedwackers():
    wedwackers_details = get_wedwackers_details()
    return render_template("wedwackers.html", wedwackers_details=wedwackers_details)

def get_tueswoman_details():
    tueswoman_cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    tueswoman_query = "SELECT * FROM results WHERE dropnavid = 7 ;"
    tueswoman_cursor.execute(tueswoman_query)
    tueswoman_details = tueswoman_cursor.fetchall()
    tueswoman_cursor.close()
    return tueswoman_details

@app.route("/tueswoman")
def tueswoman():
    tueswoman_details = get_tueswoman_details()
    return render_template("tueswoman.html",tueswoman_details=tueswoman_details)

def get_precup_details():
    precup_cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    precup_query = "SELECT * FROM results WHERE dropnavid = 8 ;"
    precup_cursor.execute(precup_query)
    precup_details = precup_cursor.fetchall()
    precup_cursor.close()
    return precup_details

@app.route("/precup")
def precup():
    precup_details = get_precup_details()
    return render_template("precup.html",precup_details=precup_details)

def get_pitchmarks_details():
    pitchmarks_cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    pitchmarks_query = "SELECT * FROM events WHERE dropnavide = 9 ;"
    pitchmarks_cursor.execute(pitchmarks_query)
    pitchmarks_details = pitchmarks_cursor.fetchall()
    pitchmarks_cursor.close()
    return pitchmarks_details

@app.route("/pitchmarks")
def pitchmarks():
    pitchmarks_details = get_pitchmarks_details()
    return render_template("pitchmarks.html",pitchmarks_details=pitchmarks_details)

def get_shootoutwin_details():
    shootoutwin_cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    shootoutwin_query = "SELECT * FROM events WHERE dropnavide = 10 ;"
    shootoutwin_cursor.execute(shootoutwin_query)
    shootoutwin_details = shootoutwin_cursor.fetchall()
    shootoutwin_cursor.close()
    return shootoutwin_details

@app.route("/shootoutwin")
def shootoutwin():
    shootoutwin_details = get_shootoutwin_details()
    return render_template("shootoutwin.html",shootoutwin_details=shootoutwin_details)

def get_ladiesfinals_details():
    ladiesfinals_cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    ladiesfinals_query = "SELECT * FROM events WHERE dropnavide = 11 ;"
    ladiesfinals_cursor.execute(ladiesfinals_query)
    ladiesfinals_details = ladiesfinals_cursor.fetchall()
    ladiesfinals_cursor.close()
    return ladiesfinals_details

@app.route("/ladiesfinals")
def ladiesfinals():
    ladiesfinals_details = get_ladiesfinals_details()
    return render_template("ladiesfinals.html",ladiesfinals_details=ladiesfinals_details)

def get_ladiestournament_details():
    ladiestournament_cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    ladiestournament_query = "SELECT * FROM events WHERE dropnavide = 12 ;"
    ladiestournament_cursor.execute(ladiestournament_query)
    ladiestournament_details = ladiestournament_cursor.fetchall()
    ladiestournament_cursor.close()
    return ladiestournament_details

@app.route("/ladiestournament")
def ladiestournament():
    ladiestournament_details = get_ladiestournament_details()
    return render_template("ladiestournament.html",ladiestournament_details=ladiestournament_details)

def get_mensopen_details():
    mensopen_cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    mensopen_query = "SELECT * FROM events WHERE dropnavide = 13 ;"
    mensopen_cursor.execute(mensopen_query)
    mensopen_details = mensopen_cursor.fetchall()
    mensopen_cursor.close()
    return mensopen_details

@app.route("/mensopen")
def mensopen():
    mensopen_details = get_mensopen_details()
    return render_template("mensopen.html",mensopen_details=mensopen_details)

def get_clubchamps_details():
    clubchamps_cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    clubchamps_query = "SELECT * FROM events WHERE dropnavide = 14 ;"
    clubchamps_cursor.execute(clubchamps_query)
    clubchamps_details = clubchamps_cursor.fetchall()
    clubchamps_cursor.close()
    return clubchamps_details

@app.route("/clubchamps")
def clubchamps():
    clubchamps_details = get_clubchamps_details()
    return render_template("clubchamps.html",clubchamps_details=clubchamps_details)

def get_pairschamps_details():
    pairschamps_cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    pairschamps_query = "SELECT * FROM events WHERE dropnavide = 15 ;"
    pairschamps_cursor.execute(pairschamps_query)
    pairschamps_details = pairschamps_cursor.fetchall()
    pairschamps_cursor.close()
    return pairschamps_details

@app.route("/pairs_champs")
def pairs_champs():
    pairschamps_details = get_pairschamps_details()
    return render_template("pairs_champs.html",pairschamps_details=pairschamps_details)

def get_watsontropwin_details():
    watsontropwin_cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    watsontropwin_query = "SELECT * FROM events WHERE dropnavide = 16 ;"
    watsontropwin_cursor.execute(watsontropwin_query)
    watsontropwin_details = watsontropwin_cursor.fetchall()
    watsontropwin_cursor.close()
    return watsontropwin_details

@app.route("/watsontropwin")
def watsontropwin():
    watsontropwin_details = get_watsontropwin_details()
    return render_template("watsontropwin.html",watsontropwin_details=watsontropwin_details)

def get_ladiesopen_details():
    ladiesopen_cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    ladiesopen_query = "SELECT * FROM events WHERE dropnavide = 17 ;"
    ladiesopen_cursor.execute(ladiesopen_query)
    ladiesopen_details = ladiesopen_cursor.fetchall()
    ladiesopen_cursor.close()
    return ladiesopen_details

@app.route("/ladiesopen")
def ladiesopen():
    ladiesopen_details = get_ladiesopen_details()
    return render_template("ladiesopen.html",ladiesopen_details=ladiesopen_details)

def get_photogallery_details():
    photogallery_cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    photogallery_query = "SELECT * FROM members WHERE dropnavidm = 19 ;"
    photogallery_cursor.execute(photogallery_query)
    photogallery_details = photogallery_cursor.fetchall()
    photogallery_cursor.close()
    return photogallery_details

@app.route("/photogallery")
def photogallery():
    photogallery_details = get_photogallery_details()
    return render_template("photogallery.html",photogallery_details=photogallery_details)

def get_clubofficesub_details():
    clubofficesub_cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    clubofficesub_query = "SELECT * FROM members WHERE dropnavidm = 20 ;"
    clubofficesub_cursor.execute(clubofficesub_query)
    clubofficesub_details = clubofficesub_cursor.fetchall()
    clubofficesub_cursor.close()
    return clubofficesub_details

@app.route("/clubofficesub")
def clubofficesub():
    clubofficesub_details = get_clubofficesub_details()
    return render_template("clubofficesub.html",clubofficesub_details=clubofficesub_details)

def get_startermarker_details():
    startermarker_cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    startermarker_query = "SELECT * FROM members WHERE dropnavidm = 21 ;"
    startermarker_cursor.execute(startermarker_query)
    startermarker_details = startermarker_cursor.fetchall()
    startermarker_cursor.close()
    return startermarker_details

@app.route("/startermarker")
def startermarker():
    startermarker_details = get_startermarker_details()
    return render_template("startermarker.html",startermarker_details=startermarker_details)

def get_macommitteemyear_details():
    macommitteemyear_cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    macommitteemyear_query = """SELECT DISTINCT members_title,members_subtitle
                        FROM members WHERE dropnavidm = 22 
                        ORDER BY members_title DESC
                        ;"""
    macommitteemyear_cursor.execute(macommitteemyear_query)
    macommitteemyear_details = macommitteemyear_cursor.fetchall()
    macommitteemyear_cursor.close()
    return macommitteemyear_details

def get_macommitteem_details():
    macommitteem_cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    macommitteem_query = "SELECT * FROM members WHERE dropnavidm = 22 ;"
    macommitteem_cursor.execute(macommitteem_query)
    macommitteem_details = macommitteem_cursor.fetchall()
    macommitteem_cursor.close()
    return macommitteem_details

@app.route("/macommitteem")
def macommitteem():
    macommitteemyear_details = get_macommitteemyear_details()
    macommitteem_details = get_macommitteem_details()
    return render_template("macommitteem.html",macommitteem_details=macommitteem_details,macommitteemyear_details=macommitteemyear_details)

def get_agmminutes_details():
    agmminutes_cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    agmminutes_query = "SELECT * FROM members WHERE dropnavidm = 23 ;"
    agmminutes_cursor.execute(agmminutes_query)
    agmminutes_details = agmminutes_cursor.fetchall()
    agmminutes_cursor.close()
    return agmminutes_details

@app.route("/agmminutes")
def agmminutes():
    agmminutes_details = get_agmminutes_details()
    return render_template("agmminutes.html",agmminutes_details=agmminutes_details)

def get_programme_details():
    programme_cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    programme_query = "SELECT * FROM programme ;"
    programme_cursor.execute(programme_query)
    programme_details = programme_cursor.fetchall()
    programme_cursor.close()
    return programme_details

@app.route("/programme")
def programme():
    programme_details = get_programme_details()
    return render_template("programme.html",programme_details=programme_details)

def get_coursesponsors_details():
    coursesponsors_cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    coursesponsors_query = "SELECT * FROM coursesponsors;"
    coursesponsors_cursor.execute(coursesponsors_query)
    coursesponsors_details = coursesponsors_cursor.fetchall()
    coursesponsors_cursor.close()
    return coursesponsors_details

def get_clubsponsors_details():
    clubsponsors_cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    clubsponsors_query = "SELECT * FROM clubsponsors;"
    clubsponsors_cursor.execute(clubsponsors_query)
    clubsponsors_details = clubsponsors_cursor.fetchall() 
    clubsponsors_cursor.close()
    return clubsponsors_details
@app.route("/sponsors")
def sponsors():
    coursesponsors_details= get_coursesponsors_details()
    clubsponsors_details=get_clubsponsors_details()
    sponsors_image = get_sponsors_image()
    return render_template("sponsors.html", coursesponsors_details=coursesponsors_details,clubsponsors_details=clubsponsors_details,sponsors_image=sponsors_image)


def get_contact_details():
    contact_cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    contact_query = "SELECT * FROM contact_details;"
    contact_cursor.execute(contact_query)
    contact_details = contact_cursor.fetchall()
    contact_cursor.close()
    return contact_details

@app.route("/contact_details")
def contact_details():
    contact_details = get_contact_details()
    return render_template("contact_details.html", contact_details=contact_details)

@app.route("/manacontact")
def manacontact():
    contact_details = get_contact_details()
    return render_template("manacontact.html", contact_details=contact_details)

@app.route("/manacontactedit/<int:contact_id>", methods=["GET", "POST"])
def manacontactedit(contact_id):
    msg = ""
    if request.method == "POST":
        newcontact_address = request.form.get("contact_address")
        newcontact_email = request.form.get("contact_email")
        newcontact_phone = request.form.get("contact_phone")
        newfacebook_url = request.form.get("facebook_url")
        newcontact_map = request.form.get("contact_map")
        
        if not re.match(r'.*\d+.*', newcontact_address) and not re.match(r'.*[a-zA-Z]+.*', newcontact_address):
            msg = 'Please enter a valid address!'
        elif not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', newcontact_email ):
            msg = 'Please enter a valid email address!'
        elif not re.match(r'^.*$', newcontact_phone):  
            msg = 'Please enter a valid phone number!'
        else:
            try:
                # Update contact information
                newcontactd_cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                updatecontact_query = "UPDATE contact_details " \
                        "SET contact_address = %s, contact_email = %s, contact_phone = %s, facebook_url = %s, contact_map = %s " \
                        "WHERE contact_id= %s"
                newcontactd_cursor.execute(updatecontact_query, (newcontact_address, newcontact_email, newcontact_phone, newfacebook_url, newcontact_map,contact_id))
                mysql.connection.commit()
                newcontactd_cursor.close()
                msg = 'Contact information updated successfully!'

                contact_details = get_contact_details()
                return render_template("manacontactedit.html", contact_details=contact_details, contact_id=contact_id, msg=msg)
            except Exception as e:
                # Handle database update failure
                return render_template("error.html", error_message="Failed to update contact details: {}".format(str(e)))
    else:
        contactd_details = get_contact_details()
        return render_template("manacontactedit.html", contactd_details=contactd_details, contact_id=contact_id)

    # If form validation fails or an error occurs, redirect user back to the form page with the error message
    return redirect(url_for('manacontactedit', contact_id=contact_id, msg=msg))

@app.route("/contact_message", methods=["GET", "POST"])
def contact_message():
    msg = None
    
    if request.method == "POST":
        name = request.form.get('inputName')
        email = request.form.get('inputEmail4')
        phone = request.form.get('inputPhone')
        subject = request.form.get('inputSubject')
        message = request.form.get('inputMessage')

        if not re.match(r'^[A-Za-z\s]+$', name):
            msg = 'Please enter a valid name. Only letters are allowed!'
        elif not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            msg = 'Please enter a valid email address!'
        elif not re.match(r'^\d{1,12}$', phone):
            msg = 'Invalid phone number! Must be a non-negative integer.'
        elif not re.match(r'^[a-zA-Z0-9\s]+$', subject):
            msg = 'Invalid subject! Must contain only letters, numbers, and spaces.'
        elif not re.match(r'^[a-zA-Z0-9\s]{1,255}$', message):
            msg = 'Invalid message! Must contain only letters, numbers, and spaces with maximum length of 255 characters.'
        elif not name or not email or not phone or not subject or not message:
            msg = 'Please fill out the form!'
        else:
            msg = Message('New Contact Message from User',
                          sender='423582595@qq.com',  
                          recipients=['admin@example.com']) 
            msg.body = f'Name: {name}\nEmail: {email}\nPhone: {phone}\nSubject: {subject}\nMessage: {message}'
            mail.send(msg)

            contactsd_cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            insert_sdmessage_query = '''
                INSERT INTO contact_message (contactsd_name, contactsd_email, contactsd_phone, contactsd_subject, 
                contactsd_message)
                VALUES (%s, %s, %s, %s, %s);
            '''
            values_messagesd =(name, email, phone, subject, message)

            contactsd_cursor.execute(insert_sdmessage_query, values_messagesd)
            mysql.connection.commit()
            msg = 'You have successfully sent the message!'

    return render_template("contact_message.html", msg=msg)


def generate_unique_member_number():
    while True:
        random_suffix = str(random.randint(1000, 9999))
        membernum = int('227' + random_suffix)
        
        # Check if the generated membernum already exists in the database
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM membersign WHERE membernum = %s', (membernum,))
        existing_member = cursor.fetchone()
        if not existing_member:
            return membernum

@app.route("/register" , methods=['GET', 'POST'])
def register():
    msg = ''   
    # Check if "email" and "password" exist in form data
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form :
        # Create variables for easy access
        firstname = request.form['firstname']
        surname = request.form['surname']
        email = request.form['email']
        password = request.form['password']
        confirmpassword = request.form['confirmpassword']
        
        # Generate unique member number
        membernum = generate_unique_member_number()
       
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM membersign WHERE email = %s', (email,))
        account = cursor.fetchone()
        
        # If account exists, show error message
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'^[A-Za-z]{2,20}$', firstname):
            msg = 'First name must contain only letters and be between 2 and 20 characters long.'
        elif not re.match(r'^[A-Za-z]{2,20}$', surname):
            msg = 'Surname must contain only letters and be between 2 and 20 characters long.'
        elif not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            msg = 'Invalid email address!'
        elif not re.match(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$', password):
            msg = 'Password must be at least 8 characters long and contain at least one letter, one number, and one special character.'
        elif password != confirmpassword:
            msg = 'Passwords must match.'
        elif not firstname or not surname or not password or not email:
            msg = 'Please fill out the form!'
        else:
            # Account doesn't exist and the form data is valid, now insert new account into membersign table
            rolename = "Member"
            roleid = 1
            hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            salt = bcrypt.gensalt().decode('utf-8')
            insert_secure_query =  '''
                INSERT INTO membersign(roleid, rolename, membernum, firstname, surname, email, hash, salt, create_date, last_update_date)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, NOW(), NOW())
                '''
            values_membersign= (roleid, rolename, membernum, firstname, surname, email, hashed, salt)
            cursor.execute(insert_secure_query, values_membersign)
    
            mysql.connection.commit()  # Commit the transaction
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)


@app.route('/login/', methods=['GET', 'POST'])
def login():
    # Output message if something goes wrong...
    msg = ''
    # Check if "email" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and (('email' in request.form) or ('membernum' in request.form)) and 'password' in request.form:
        # Create variables for easy access
        email = request.form.get('email')
        membernum = request.form.get('membernum')
        password = request.form['password']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        try:
            if email:
                cursor.execute('SELECT * FROM membersign WHERE email = %s', (email,))
            else:
                cursor.execute('SELECT * FROM membersign WHERE membernum = %s', (membernum,))
            # Fetch one record and return result
            account = cursor.fetchone()
            
            if account and 'hash' in account:
                stored_hashed_password = account['hash']
                if bcrypt.checkpw(password.encode('utf-8'), stored_hashed_password.encode('utf-8')):
                    
                    session['loggedin'] = True
                    session['email'] = account['email']
                    session['membernum'] = account['membernum']
                    user_rolename = account.get('rolename', 'default_role')
                    session['rolename'] = user_rolename
                    session['firstname'] = account['firstname']
                    session['surname'] = account['surname']
                    session['account'] = account

                    # Fetch and store customer information
                    if user_rolename == 'Member':
                        cursor.execute('SELECT * FROM membersign WHERE roleid = %s', (account['roleid'],))
                        Member_info = cursor.fetchone()
                        session['Member_info'] = Member_info
                        # Redirect to home page
                        return redirect(url_for('home'))
                    
                    elif user_rolename == 'Admin':
                        cursor.execute('SELECT * FROM membersign WHERE roleid = %s', (account['roleid'],))
                        admin_info = cursor.fetchone()
                        session['admin_info'] = admin_info
                        return redirect(url_for('home'))
                    
                else:
                    # Password incorrect
                    msg = 'Incorrect email/password!'
            else:
                # Account doesn't exist or email incorrect
                msg = 'Incorrect email'
        except Exception as e:
            mysql.connection.rollback()
            msg = 'Failed to login: {}'.format(str(e))
        finally:
            cursor.close()
    # Show the login form with message (if any)
    return render_template('login.html', msg=msg)

@app.route("/loginmember")
def loginmember():
    return render_template("loginmember.html")

@app.route("/logout")
def logout():
   session.pop('loggedin', None)
   session.pop('email', None)
   session.pop('membernum', None)
   # Redirect to login page
   return redirect(url_for('login'))

@app.route("/profile", methods=["GET", "POST"])
def profile():
    if 'loggedin' in session:
        rolename = session['rolename']
        email = session['email']
        membernum = session['membernum']
        account = session.get('account')
    return render_template("profile.html", rolename = rolename, email=email,membernum=membernum,account=account)

@app.route("/profileedit", methods=["GET", "POST"])
def profileedit():
    if 'loggedin' in session:
        firstname = session['firstname']
        surname = session['surname']
        email = session['email']
        membernum = session['membernum']
        account = session.get('account')
        msg = ''  

        if request.method == "POST":
            newfirstname = request.form.get("firstname")
            newsurname = request.form.get("surname")
            
            if not re.match(r'^[a-zA-Z]{2,20}$', newfirstname):
                msg = 'Please enter a valid first name (2-20 characters, letters only)!'
            elif not re.match(r'^[a-zA-Z]{2,20}$', newsurname):
                msg = 'Please enter a valid surname (2-20 characters, letters only)!'
            else:
                try:    
                    # Update name information
                    newname_cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                    updatename_query = "UPDATE membersign " \
                            "SET firstname = %s, surname = %s " \
                            "WHERE email = %s and membernum = %s"
                    newname_cursor.execute(updatename_query, (newfirstname, newsurname, email, membernum))
                    mysql.connection.commit()
                    newname_cursor.close()
                    msg = 'Name updated successfully!'

                    session['firstname'] = newfirstname
                    session['surname'] = newsurname

                    session.pop('loggedin', None)
                    session.pop('firstname', None)
                    session.pop('surname', None)
                    session.pop('email', None)
                    session.pop('membernum', None)
                    session.pop('account', None)
                    flash('Profile updated successfully!', 'success')
                    return redirect(url_for('login', msg='Profile updated successfully!'))
                
                except:
                    return "Failed to update name"
        
        return render_template("profileedit.html", firstname=firstname, surname=surname, account=account, msg=msg)
    else:
        return redirect(url_for('login'))
    
@app.route("/passwordedit", methods=["GET", "POST"])
def passwordedit():
    if 'loggedin' in session:
        msg = ''  
        if request.method == 'POST' and 'password' in request.form and 'confirm_password' in request.form:
            password = request.form['password']
            confirm_password = request.form['confirm_password']

            if not re.match(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$', password):
                msg = 'Password must be at least 8 characters long and contain at least one letter, one number, and specified special characters!'
            elif password != confirm_password:
                msg = 'Passwords must match.'
            else:
                try:
                    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                    cursor.execute('UPDATE membersign SET hash = %s WHERE membernum = %s and email = %s', (hashed_password, session['membernum'],session['email']))
                    mysql.connection.commit()
                    cursor.close()
                    session.pop('loggedin', None)
                    session.pop('firstname', None)
                    session.pop('surname', None)
                    session.pop('email', None)
                    session.pop('membernum', None)
                    session.pop('account', None)
                    return redirect(url_for('login', msg='Password changed successfully'))
                except Exception as e:
                    return "Failed to update password: {}".format(str(e))
        return render_template('passwordedit.html', msg=msg)
    return redirect(url_for('login'))

@app.route("/managenavbar")
def managenavbar():
    return render_template("managenavbar.html")
@app.route("/manaresults")
def manaresults():
    return render_template("manaresults.html")
@app.route("/manaevents")
def manaevents():
    return render_template("manaevents.html")
@app.route("/manamembers")
def manamembers():
    return render_template("manamembers.html")
if __name__ == '__main__':
    app.run(debug="True")