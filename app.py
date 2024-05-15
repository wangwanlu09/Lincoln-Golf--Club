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


app.config['MYSQL_HOST'] = ''
app.config['MYSQL_USER'] = ''
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = ''
app.config['MYSQL_PORT'] = 
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
    popup_details = get_popup_details()
    return render_template("home.html", home_details=home_details, sponsors_image=sponsors_image,popup_details=popup_details)

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
    if request.method == 'POST':
        hdetailsid = request.form.get('hdetailsid')
        deletenews_query = "DELETE FROM homedetails WHERE hdetailsid = %s;"
        deletenews_cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        deletenews_cursor.execute(deletenews_query, (hdetailsid,))
        mysql.connection.commit()
        deletenews_cursor.close()
        return redirect(url_for('mananews')) 
    news_details = get_news_details()
    return render_template("mananews.html", news_details=news_details)

@app.route("/mananewsedit/<int:hdetailsid>")
def mananewsedit(hdetailsid):
    msg=""
    news_details = get_news_details()
    if request.method == 'POST':
        newnewstitle = request.form.get("hdetails_title")
        newnewssubtitle = request.form.get("hdetails_subtitle")
        newnewsdes = request.form.get("hdetails_des")
        if not re.match(r'^.{1,100}$', newnewstitle):
            msg = 'Please enter a valid title!'
        elif not re.match(r'^.{0,100}$', newnewssubtitle):
            msg = 'Please enter a valid subtitle!'
        else:
            try:
                # Update home details information
                newnewsdetails_cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                updatenewsdetails_query = "UPDATE homedetails " \
                            "SET hdetails_title = %s, hdetails_subtitle = %s, hdetails_des = %s " \
                            "WHERE hdetailsid = %s"
                newnewsdetails_cursor.execute(updatenewsdetails_query, (newnewstitle, newnewssubtitle, newnewsdes, hdetailsid))
                mysql.connection.commit()
                newnewsdetails_cursor.close()
                msg = 'News details updated successfully!'
                news_details = get_news_details()
                return render_template("mananewsedit.html", news_details=news_details, hdetailsid=hdetailsid, msg=msg)
            except Exception as e:
            # Handle database update failure
                return "Failed to update function centre details: {}".format(str(e))
    return render_template("mananewsedit.html", news_details=news_details, hdetailsid=hdetailsid, msg=msg)

@app.route("/mananewseditp/<int:hdetailsid>")
def mananewseditp(hdetailsid):
    msg=""
    news_details = get_news_details()
    if request.method == 'POST':
        newimage = request.form.get("image ")
        try:
            # Update home details information
            newnewsdetails_cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            updatenewsdetails_query = "UPDATE homedetails " \
                        "SET image = %s" \
                        "WHERE hdetailsid = %s"
            newnewsdetails_cursor.execute(updatenewsdetails_query, (newimage,hdetailsid))
            mysql.connection.commit()
            newnewsdetails_cursor.close()
            msg = 'News details updated successfully!'
            news_details = get_news_details()
            return render_template("mananewseditp.html", news_details=news_details, hdetailsid=hdetailsid, msg=msg)
        except Exception as e:
        # Handle database update failure
            return "Failed to update function centre details: {}".format(str(e))
    return render_template("mananewseditp.html", news_details=news_details, hdetailsid=hdetailsid, msg=msg)

@app.route("/mananewsadd", methods=['GET', 'POST'])
def mananewsadd():
    msg=""
    news_details = get_news_details()
    if request.method == 'POST':
        homeorder= 2
        hdetails_title= ""
        hdetails_suborder = None
        hdetails_subtitle = ""
        hdetails_dropsubtitle = ""
        hdetails_des = ""
        addimage = request.form['image']
        document = ""
        try:
            newsadd_cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            insert_newsadd_query= '''INSERT INTO homedetails(homeorder, hdetails_title, hdetails_suborder,hdetails_subtitle,hdetails_dropsubtitle,hdetails_des,image,document)
                            VALUES(%s,%s,%s,%s,%s,%s,%s,%s)'''
            newsadd_cursor.execute(insert_newsadd_query, (homeorder, hdetails_title, hdetails_suborder,hdetails_subtitle, hdetails_dropsubtitle, hdetails_des, addimage,document))
            mysql.connection.commit()
            newsadd_cursor.close()
            msg = 'You have successfully add image!'
            return render_template("mananewsadd.html", news_details=news_details, msg=msg)
        except Exception as e:
            # Handle database update failure
            return "Failed to add image: {}".format(str(e))

    news_details = get_news_details()
    return render_template("mananewsadd.html", news_details=news_details,msg=msg)

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
    if request.method == 'POST':
        hdetailsid = request.form.get('hdetailsid')
        deletefuncen_query = "DELETE FROM homedetails WHERE hdetailsid = %s;"
        deletefuncen_cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        deletefuncen_cursor.execute(deletefuncen_query, (hdetailsid,))
        mysql.connection.commit()
        deletefuncen_cursor.close()
        return redirect(url_for('mananfuncen')) 
    funcentre_details = get_funcentre_details()
    return render_template("mananfuncen.html",  funcentre_details=funcentre_details)

@app.route("/mananfuncenedit/<int:hdetailsid>", methods=['GET', 'POST'])
def mananfuncenedit(hdetailsid):
    msg=""
    funcentre_details = get_funcentre_details()
    if request.method == 'POST':
        newfuncentitle = request.form.get("hdetails_title")
        newfuncensubtitle = request.form.get("hdetails_subtitle")
        newfuncendes = request.form.get("hdetails_des")
        if not re.match(r'^.{1,100}$', newfuncentitle):
            msg = 'Please enter a valid title!'
        else:
            try:
                # Update home details information
                newfuncendetails_cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                updatefuncendetails_query = "UPDATE homedetails " \
                            "SET hdetails_title = %s, hdetails_subtitle = %s, hdetails_des = %s " \
                            "WHERE hdetailsid = %s"
                newfuncendetails_cursor.execute(updatefuncendetails_query, (newfuncentitle, newfuncensubtitle, newfuncendes, hdetailsid))

                mysql.connection.commit()
                newfuncendetails_cursor.close()
                msg = 'Function Centre details updated successfully!'
                funcentre_details = get_funcentre_details()
                return render_template("mananfuncenedit.html", funcentre_details=funcentre_details,hdetailsid=hdetailsid, msg=msg)
            except Exception as e:
            # Handle database update failure
                return "Failed to update function centre details: {}".format(str(e))
    return render_template("mananfuncenedit.html",  funcentre_details=funcentre_details,hdetailsid=hdetailsid,msg=msg)

@app.route("/mananfunceneditp/<int:hdetailsid>", methods=['GET', 'POST'])
def mananfunceneditp(hdetailsid):
    msg=""
    funcentre_details = get_funcentre_details()
    if request.method == 'POST':
        newimage = request.files.get("image ")
        try:
            # Update home details information
            newfuncendetails_cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            updatefuncendetails_query = "UPDATE homedetails " \
                    "SET image = %s" \
                    "WHERE hdetailsid = %s"
            newfuncendetails_cursor.execute(updatefuncendetails_query, (newimage,hdetailsid))
            mysql.connection.commit()
            newfuncendetails_cursor.close()
            msg = 'Function Centre details updated successfully!'
            funcentre_details = get_funcentre_details()
            return render_template("mananfunceneditp.html", funcentre_details=funcentre_details,hdetailsid=hdetailsid, msg=msg)
        except Exception as e:
        # Handle database update failure
            return "Failed to update function centre details: {}".format(str(e))
    return render_template("mananfunceneditp.html",  funcentre_details=funcentre_details,hdetailsid=hdetailsid,msg=msg)

@app.route("/mananfuncenadd", methods=['GET', 'POST'])
def mananfuncenadd():
    msg=""
    funcentre_details = get_funcentre_details()
    if request.method == 'POST':
        homeorder= 3
        hdetails_title= ""
        hdetails_suborder = None
        hdetails_subtitle = ""
        hdetails_dropsubtitle = ""
        hdetails_des = ""
        addimage = request.form['image']
        document = ""
        try:
            funcenadd_cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            insert_funcenadd_query= '''INSERT INTO homedetails(homeorder, hdetails_title, hdetails_suborder,hdetails_subtitle,hdetails_dropsubtitle,hdetails_des,image,document)
                            VALUES(%s,%s,%s,%s,%s,%s,%s,%s)'''
            funcenadd_cursor.execute(insert_funcenadd_query, (homeorder, hdetails_title, hdetails_suborder,hdetails_subtitle, hdetails_dropsubtitle, hdetails_des, addimage,document))
            mysql.connection.commit()
            funcenadd_cursor.close()
            msg = 'You have successfully add image!'
            return render_template("mananfuncenadd.html", funcentre_details=funcentre_details, msg=msg)
        except Exception as e:
            # Handle database update failure
            return "Failed to add image: {}".format(str(e))

    funcentre_details = get_funcentre_details()
    return render_template("mananfuncenadd.html",  funcentre_details=funcentre_details,msg=msg)

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

@app.route("/manamemberapply", methods=['GET', 'POST'])
def manamemberapply():
    if request.method == 'POST':
        hdetailsid = request.form.get('hdetailsid')
        deletemanamemberapply_query = "DELETE FROM homedetails WHERE hdetailsid = %s;"
        deletemanamemberapply_cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        deletemanamemberapply_cursor.execute(deletemanamemberapply_query, (hdetailsid,))
        mysql.connection.commit()
        deletemanamemberapply_cursor.close()
        return redirect(url_for('manamemberapply')) 
    memberapplication_details = get_memberapplication_details()
    return render_template("manamemberapply.html",  memberapplication_details=memberapplication_details)

@app.route("/manamemberapplyedit/<int:hdetailsid>", methods=['GET', 'POST'])
def manamemberapplyedit(hdetailsid): 
    msg=""
    memberapplication_details = get_memberapplication_details()
    if request.method == 'POST':
        newmemberapplicationtitle = request.form.get("hdetails_title")
        newmemberapplicationorder = request.form.get("hdetails_suborder")
        newmemberapplicationsubtitle = request.form.get("hdetails_subtitle")
        newmemberapplicationheading = request.form.get("hdetails_dropsubtitle")
        newmemberapplicationdes = request.form.get("hdetails_des")
        if not re.match(r'^.{1,100}$', newmemberapplicationtitle):
            msg = 'Please enter a valid title!'
        else:
            try:
                # Update home details information
                newmemberapplicationdetails_cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                updatememberapplicationdetails_query = "UPDATE homedetails " \
                            "SET hdetails_title = %s, hdetails_suborder=%s, hdetails_subtitle = %s, hdetails_dropsubtitle= %s,hdetails_des = %s " \
                            "WHERE hdetailsid = %s"
                newmemberapplicationdetails_cursor.execute(updatememberapplicationdetails_query, (newmemberapplicationtitle, newmemberapplicationorder,newmemberapplicationsubtitle,newmemberapplicationheading,newmemberapplicationdes,hdetailsid))

                mysql.connection.commit()
                newmemberapplicationdetails_cursor.close()
                msg = 'Member Application details updated successfully!'
                memberapplication_details = get_memberapplication_details()
                return render_template("manamemberapplyedit.html", memberapplication_details=memberapplication_details,hdetailsid=hdetailsid, msg=msg)
            except Exception as e:
            # Handle database update failure
                return "Failed to update details: {}".format(str(e))
    return render_template("manamemberapplyedit.html",  memberapplication_details=memberapplication_details,hdetailsid=hdetailsid,msg=msg)

@app.route("/manamemberapplyeditd/<int:hdetailsid>", methods=['GET', 'POST'])
def manamemberapplyeditd(hdetailsid): 
    msg=""
    memberapplication_details = get_memberapplication_details()
    if request.method == 'POST':
        newmemberapplicationdocument = request.form.get("document")
        try:
            # Update home details information
            newmemberapplicationdetails_cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            updatememberapplicationdetails_query = "UPDATE homedetails " \
                        "SET doucument = %s" \
                        "WHERE hdetailsid = %s"
            newmemberapplicationdetails_cursor.execute(updatememberapplicationdetails_query, (newmemberapplicationdocument,hdetailsid))

            mysql.connection.commit()
            newmemberapplicationdetails_cursor.close()
            msg = 'Member Application details updated successfully!'
            memberapplication_details = get_memberapplication_details()
            return render_template("manamemberapplyedit.html", memberapplication_details=memberapplication_details,hdetailsid=hdetailsid, msg=msg)
        except Exception as e:
        # Handle database update failure
            return "Failed to update function centre details: {}".format(str(e))
    return render_template("manamemberapplyeditd.html",  memberapplication_details=memberapplication_details)

@app.route("/manamemberapplyadd", methods=['GET', 'POST'])
def manamemberapplyadd(): 
    memberapplication_details = get_memberapplication_details()
    return render_template("/manamemberapplyadd.html",  memberapplication_details=memberapplication_details)


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
    if request.method == 'POST':
        hdetailsid = request.form.get('hdetailsid')
        deleteopenhours_query = "DELETE FROM homedetails WHERE hdetailsid = %s;"
        deleteopenhours_cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        deleteopenhours_cursor.execute(deleteopenhours_query, (hdetailsid,))
        mysql.connection.commit()
        deleteopenhours_cursor.close()
        return redirect(url_for('manaopenhours')) 
    openhours_details = get_openhours_details()
    return render_template("manaopenhours.html", openhours_details=openhours_details)

@app.route("/manaopenhoursedit/<int:hdetailsid>", methods=['GET', 'POST'])
def manaopenhoursedit(hdetailsid):
    msg=""
    openhours_details = get_openhours_details()
    if request.method == 'POST':
        newopenhourstitle = request.form.get("hdetails_title")
        newopenhoursdes = request.form.get("hdetails_des")
        if not re.match(r'^.{1,100}$', newopenhourstitle):
            msg = 'Please enter a valid title!'
        else:
            try:
                # Update home details information
                newopenhoursdetails_cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                updateopenhoursdetails_query = "UPDATE homedetails " \
                            "SET hdetails_title = %s, hdetails_des = %s " \
                            "WHERE hdetailsid = %s"
                newopenhoursdetails_cursor.execute(updateopenhoursdetails_query, (newopenhourstitle, newopenhoursdes,hdetailsid))

                mysql.connection.commit()
                newopenhoursdetails_cursor.close()
                msg = 'Details updated successfully!'
                openhours_details = get_openhours_details()
                return render_template("manaopenhoursedit.html",  openhours_details=openhours_details,hdetailsid=hdetailsid, msg=msg)
            except Exception as e:
            # Handle database update failure
                return "Failed to update details: {}".format(str(e))
    return render_template("manaopenhoursedit.html", openhours_details=openhours_details,hdetailsid=hdetailsid,msg=msg)

@app.route("/manaopenhourseditp/<int:hdetailsid>", methods=['GET', 'POST'])
def manaopenhourseditp(hdetailsid):
    msg=""
    openhours_details = get_openhours_details()
    if request.method == 'POST':
        newimage = request.files.get("image ")
        try:
            # Update home details information
            newopenhoursdetails_cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            updateopenhoursdetails_query = "UPDATE homedetails " \
                        "SET image = %s " \
                        "WHERE hdetailsid = %s"
            newopenhoursdetails_cursor.execute(updateopenhoursdetails_query, (newimage,hdetailsid))
            mysql.connection.commit()
            newopenhoursdetails_cursor.close()
            msg = 'Details updated successfully!'
            openhours_details = get_openhours_details()
            return render_template("manaopenhourseditp.html",  openhours_details=openhours_details,hdetailsid=hdetailsid, msg=msg)
        except Exception as e:
        # Handle database update failure
            return "Failed to update details: {}".format(str(e))
    return render_template("manaopenhourseditp.html", openhours_details=openhours_details,hdetailsid=hdetailsid,msg=msg)

@app.route("/manaopenhoursadd", methods=['GET', 'POST'])
def manaopenhoursadd():
    msg=""
    openhours_details = get_openhours_details()
    if request.method == 'POST':
        homeorder= 5
        hdetails_title= ""
        hdetails_suborder = None
        hdetails_subtitle = ""
        hdetails_dropsubtitle = ""
        hdetails_des = ""
        addimage = request.form['image']
        document = ""
        try:
            openhoursadd_cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            insert_openhoursadd_query= '''INSERT INTO homedetails(homeorder, hdetails_title, hdetails_suborder,hdetails_subtitle,hdetails_dropsubtitle,hdetails_des,image,document)
                            VALUES(%s,%s,%s,%s,%s,%s,%s,%s)'''
            openhoursadd_cursor.execute(insert_openhoursadd_query, (homeorder, hdetails_title, hdetails_suborder,hdetails_subtitle, hdetails_dropsubtitle, hdetails_des, addimage,document))
            mysql.connection.commit()
            openhoursadd_cursor.close()
            msg = 'You have successfully add infromations!'
            return render_template("manaopenhoursadd.html", openhours_details=openhours_details, msg=msg)
        except Exception as e:
            # Handle database update failure
            return "Failed to add image: {}".format(str(e))

    return render_template("manaopenhoursadd.html", openhours_details=openhours_details,msg=msg)
    
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
                newcourse_cursor.execute(updatecourse_query, (newcourse_name,gid))
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

@app.route("/manacoursesadd", methods=['GET', 'POST'])
def manacoursesadd():
    msg = ""
    course_details = get_course_details()
    if request.method == 'POST':
        dropnavidg = 1
        addtitle_name= "Our Course"
        addcourse_name = request.form['course_name']
        addimage = request.form['image']

        if not re.match(r'^.{1,100}$', addcourse_name):
            msg = 'Please enter a valid course name!'
        else:
            try:
                manacoursesadd_cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                insert_manacourses_query= '''INSERT INTO golf(dropnavidg, golfcourse_title,course_name,image)
                                VALUES(%s,%s,%s,%s)'''
                manacoursesadd_cursor.execute(insert_manacourses_query, (dropnavidg, addtitle_name, addcourse_name, addimage))
                mysql.connection.commit()
                manacoursesadd_cursor.close()
                msg = 'You have successfully add course!'
                return render_template("manacoursesadd.html", course_details=course_details, msg=msg)
            except Exception as e:
                return "Failed to add course details: {}".format(str(e))
    return render_template("manacoursesadd.html", course_details=course_details,msg=msg)


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

@app.route("/manascorecardedit/<int:gid>", methods=["GET", "POST"])
def manascorecardedit(gid):
    msg = ""
    scorecard_details = get_scorecard_details()
    if request.method == "POST":
        newimage = request.form.get("image")
        try:    
            # Update course information
            newscorecard_cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            updatescorecard_query = "UPDATE golf " \
                    "SET image = %s " \
                    "WHERE gid = %s"
            newscorecard_cursor.execute(updatescorecard_query, (newimage,gid))
            mysql.connection.commit()
            newscorecard_cursor.close()
            msg = 'Course image updated successfully!'
            return render_template("manascorecardedit.html", scorecard_details=scorecard_details, gid=gid, msg=msg)
        except Exception as e:
            # Handle database update failure
            return "Failed to update scorecard details: {}".format(str(e))
    
    return render_template("manascorecardedit.html", scorecard_details=scorecard_details,gid=gid,msg=msg)

@app.route("/manascorecardadd", methods=['GET', 'POST'])
def manascorecardadd():
    msg=""
    scorecard_details = get_scorecard_details()
    if request.method == 'POST':
        dropnavidg = 2
        addtitle_name= request.form['golfcourse_title']
        addcourse_name = None
        addimage = request.form['image']

        if not re.match(r'^.{1,100}$', addtitle_name):
            msg = 'Please enter a valid title name!'
        else:
            try:
                manascorecardadd_cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                insert_manascorecardadd_query= '''INSERT INTO golf(dropnavidg, golfcourse_title,course_name,image)
                                VALUES(%s,%s,%s,%s)'''
                manascorecardadd_cursor.execute(insert_manascorecardadd_query, (dropnavidg, addtitle_name, addcourse_name, addimage))
                mysql.connection.commit()
                manascorecardadd_cursor.close()
                msg = 'You have successfully add scorecard!'
                return render_template("manascorecardadd.html", scorecard_details=scorecard_details,msg=msg)
            except Exception as e:
                # Handle database update failure
                return "Failed to add scorecard details: {}".format(str(e))
     
    scorecard_details = get_scorecard_details()
    return render_template("manascorecardadd.html", scorecard_details=scorecard_details)


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

@app.route("/manasundaystable")
def manasundaystable():
    sundaystable_details = get_sundaystable_details()
    return render_template("manasundaystable.html", sundaystable_details=sundaystable_details)

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

@app.route("/manapitchmarks")
def manapitchmarks():
    pitchmarks_details = get_pitchmarks_details()
    return render_template("manapitchmarks.html",pitchmarks_details=pitchmarks_details)

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

@app.route("/manashootoutwin")
def manashootoutwin():
    shootoutwin_details = get_shootoutwin_details()
    return render_template("manashootoutwin.html",shootoutwin_details=shootoutwin_details)

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

@app.route("/manaladiesfinals")
def manaladiesfinals():
    ladiesfinals_details = get_ladiesfinals_details()
    return render_template("manaladiesfinals.html",ladiesfinals_details=ladiesfinals_details)


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

@app.route("/manamensopen")
def manamensopen():
    mensopen_details = get_mensopen_details()
    return render_template("manamensopen.html",mensopen_details=mensopen_details)

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

@app.route("/manaclubchamps")
def manaclubchamps():
    clubchamps_details = get_clubchamps_details()
    return render_template("manaclubchamps.html",clubchamps_details=clubchamps_details)

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

@app.route("/manapairschamps")
def manapairschamps():
    pairschamps_details = get_pairschamps_details()
    return render_template("manapairschamps.html",pairschamps_details=pairschamps_details)

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

@app.route("/manawatsontropwin")
def manawatsontropwin():
    watsontropwin_details = get_watsontropwin_details()
    return render_template("manawatsontropwin.html",watsontropwin_details=watsontropwin_details)

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

@app.route("/manaladiesopen")
def manaladiesopen():
    ladiesopen_details = get_ladiesopen_details()
    return render_template("manaladiesopen.html",ladiesopen_details=ladiesopen_details)

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

@app.route("/manaphotogallery")
def manaphotogallery():
    photogallery_details = get_photogallery_details()
    return render_template("manaphotogallery.html",photogallery_details=photogallery_details)

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

@app.route("/manaclubofficesub")
def manaclubofficesub():
    clubofficesub_details = get_clubofficesub_details()
    return render_template("manaclubofficesub.html",clubofficesub_details=clubofficesub_details)

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

@app.route("/manastartermarker")
def manastartermarker():
    startermarker_details = get_startermarker_details()
    return render_template("manastartermarker.html",startermarker_details=startermarker_details)

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

@app.route("/manamacommitteem")
def manamacommitteem():
    macommitteemyear_details = get_macommitteemyear_details()
    macommitteem_details = get_macommitteem_details()
    return render_template("manamacommitteem.html",macommitteem_details=macommitteem_details,macommitteemyear_details=macommitteemyear_details)

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

@app.route("/manaagmminutes")
def manaagmminutes():
    agmminutes_details = get_agmminutes_details()
    return render_template("manaagmminutes.html",agmminutes_details=agmminutes_details)

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

@app.route("/manaprogramme", methods=["GET", "POST"])
def manaprogramme():
    if request.method == 'POST':
        programmeid = request.form.get('programmeid')
        deleteprogramme_query = "DELETE FROM programme WHERE programmeid = %s;"
        deleteprogramme_cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        deleteprogramme_cursor.execute(deleteprogramme_query, (programmeid,))
        mysql.connection.commit()
        deleteprogramme_cursor.close()
        return redirect(url_for('manaprogramme')) 
    programme_details = get_programme_details()
    return render_template("manaprogramme.html",programme_details=programme_details)

@app.route("/programmeedit/<int:programmeid>", methods=["GET", "POST"])
def programmeedit(programmeid):
    msg = ""
    if request.method == "POST":
        newpro_title = request.form.get("pro_title")
        newpro_subtitle = request.form.get("pro_subtitle")
        newpro_des = request.form.get("pro_des")       
        try:
            # Update information
            newprogramme_cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            updateprogramme_query = "UPDATE programme " \
                    "SET pro_title = %s, pro_subtitle = %s, pro_des = %s " \
                    "WHERE programmeid= %s"
            newprogramme_cursor.execute(updateprogramme_query, (newpro_title, newpro_subtitle , newpro_des,programmeid))
            mysql.connection.commit()
            newprogramme_cursor.close()
            msg = 'Programme information updated successfully!'
            programme_details = get_programme_details()
            return render_template("programmeedit.html", programme_details=programme_details, programmeid=programmeid, msg=msg)
        except Exception as e:
            # Handle database update failure
            return "Failed to update details: {}".format(str(e))
    programme_details = get_programme_details()
    return render_template("programmeedit.html",programme_details=programme_details,programmeid=programmeid,msg=msg)

@app.route("/programmeeditp/<int:programmeid>", methods=["GET", "POST"])
def programmeeditp(programmeid):
    msg = ""
    if request.method == "POST":
        newdocument = request.form.get("document")       
        try:
            # Update information
            newprogramme_cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            updateprogramme_query = "UPDATE programme " \
                    "SET document = %s " \
                    "WHERE programmeid= %s"
            newprogramme_cursor.execute(updateprogramme_query, (newdocument,programmeid))
            mysql.connection.commit()
            newprogramme_cursor.close()
            msg = 'Programme information updated successfully!'
            programme_details = get_programme_details()
            return render_template("programmeeditp.html", programme_details=programme_details, programmeid=programmeid, msg=msg)
        except Exception as e:
            # Handle database update failure
            return "Failed to update details: {}".format(str(e))
    programme_details = get_programme_details()
    return render_template("programmeeditp.html",programme_details=programme_details,programmeid=programmeid,msg=msg)

@app.route("/programmeadd", methods=["GET", "POST"])
def programmeadd():
    msg=""
    programme_details = get_programme_details()
    if request.method == 'POST':
        addpro_title= request.form['pro_title']
        addpro_subtitle= request.form['pro_subtitle']
        addpro_des = request.form['pro_des']
        adddocument = request.form['document']
        if not re.match(r'^.{1,100}$', addpro_title):
            msg = "Please input invalid title!"
        elif not re.match(r'^.{1,100}$', addpro_subtitle):
            msg = "Please input invalid subtitle!"
        try:
            programmeadd_cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            insert_programmeadd_query= '''INSERT INTO programme(pro_title, pro_subtitle,pro_des,document)
                            VALUES(%s,%s,%s,%s)'''
            programmeadd_cursor.execute(insert_programmeadd_query, (addpro_title, addpro_subtitle, addpro_des, adddocument))
            mysql.connection.commit()
            programmeadd_cursor.close()
            msg = 'You have successfully add programme!'
            return render_template("programmeadd.html",  programme_details=programme_details,msg=msg)
        except Exception as e:
            # Handle database update failure
            return "Failed to add scorecard details: {}".format(str(e))
    programme_details = get_programme_details()
    return render_template("programmeadd.html",programme_details=programme_details)

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

@app.route("/manasponsors", methods=["GET", "POST"])
def manasponsors():
    if request.method == 'POST':
        if 'clubsponid' in request.form:
            clubsponid = request.form.get('clubsponid')
            deleteclubsponsor_query = "DELETE FROM clubsponsors WHERE clubsponid = %s;"
            deleteclubsponsor_cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            deleteclubsponsor_cursor.execute(deleteclubsponsor_query, (clubsponid,))
            mysql.connection.commit()
            deleteclubsponsor_cursor.close()
        elif 'coursponid' in request.form:
            coursponid = request.form.get('coursponid')
            deletecoursponsor_query = "DELETE FROM coursesponsors WHERE coursponid = %s;"
            deletecoursponsor_cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            deletecoursponsor_cursor.execute(deletecoursponsor_query, (coursponid,))
            mysql.connection.commit()
            deletecoursponsor_cursor.close()
        return redirect(url_for('manasponsors'))
    
    coursesponsors_details= get_coursesponsors_details()
    clubsponsors_details=get_clubsponsors_details()
    return render_template("manasponsors.html",coursesponsors_details=coursesponsors_details,clubsponsors_details=clubsponsors_details)
#course sponsors edit
@app.route("/manasponsorseditc/<int:coursponid>", methods=["GET", "POST"])
def manasponsorseditc(coursponid):
    msg = ""
    if request.method == "POST":
        newcourspon_name = request.form.get("courspon_name")
        newcourspon_link = request.form.get("courspon_link")
        newcoweb = request.form.get("coweb")       
        try:
            # Update information
            newcosponsor_cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            updatecosponsor_query = "UPDATE coursesponsors " \
                    "SET courspon_name = %s, courspon_link = %s, web = %s " \
                    "WHERE coursponid= %s"
            newcosponsor_cursor.execute(updatecosponsor_query, (newcourspon_name, newcourspon_link, newcoweb,coursponid))
            mysql.connection.commit()
            newcosponsor_cursor.close()
            msg = 'Sponsor information updated successfully!'
            coursesponsors_details= get_coursesponsors_details()
            return render_template("manasponsorsedit.html", coursesponsors_details=coursesponsors_details, coursponid=coursponid, msg=msg)
        except Exception as e:
            # Handle database update failure
            return "Failed to update details: {}".format(str(e))
    coursesponsors_details= get_coursesponsors_details()
    return render_template("manasponsorsedit.html",coursesponsors_details=coursesponsors_details,coursponid=coursponid,msg=msg)

@app.route("/manasponsorsedit/<int:clubsponid>", methods=["GET", "POST"])
def manasponsorsedit(clubsponid):
    msg = ""
    if request.method == "POST":
        newclubspon_name = request.form.get("clubspon_name")
        newclubspon_link = request.form.get("clubspon_link")
        newclweb = request.form.get("clweb")
        try:
            # Update information
            newcosponsor_cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            updatecosponsor_query = "UPDATE clubsponsors " \
                    "SET clubspon_name = %s, clubspon_link = %s, web = %s " \
                    "WHERE clubsponid= %s"
            newcosponsor_cursor.execute(updatecosponsor_query, (newclubspon_name, newclubspon_link, newclweb,clubsponid))
            mysql.connection.commit()
            newcosponsor_cursor.close()
            msg = 'Sponsor information updated successfully!'
            clubsponsors_details=get_clubsponsors_details()
            return render_template("manasponsorsedit.html", clubsponsors_details=clubsponsors_details, clubsponid=clubsponid, msg=msg)
        except Exception as e:
            # Handle database update failure
            return "Failed to update details: {}".format(str(e))
    clubsponsors_details=get_clubsponsors_details()
    return render_template("manasponsorsedit.html",clubsponsors_details=clubsponsors_details,clubsponid=clubsponid)

@app.route("/manasponsorseditpc/<int:coursponid>", methods=["GET", "POST"])
def manasponsorseditpc(coursponid):
    msg = ""
    if request.method == "POST":
        newcoimage = request.form.get("coimage")       
        try:
            # Update information
            newcosponsor_cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            updatecosponsor_query = "UPDATE coursesponsors " \
                    "SET image = %s " \
                    "WHERE coursponid= %s"
            newcosponsor_cursor.execute(updatecosponsor_query, (newcoimage,coursponid))
            mysql.connection.commit()
            newcosponsor_cursor.close()
            msg = 'Sponsor image updated successfully!'
            coursesponsors_details= get_coursesponsors_details()
            return render_template("manasponsorseditp.html", coursesponsors_details=coursesponsors_details, coursponid=coursponid, msg=msg)
        except Exception as e:
            # Handle database update failure
            return "Failed to update details: {}".format(str(e))
    coursesponsors_details= get_coursesponsors_details()
    return render_template("manasponsorseditp.html",coursesponsors_details=coursesponsors_details,coursponid=coursponid)

@app.route("/manasponsorseditp/<int:clubsponid>", methods=["GET", "POST"])
def manasponsorseditp(clubsponid):
    msg = ""
    if request.method == "POST":
        newcoimage = request.form.get("coimage") 
        try:
            # Update information
            newcosponsor_cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            updatecosponsor_query = "UPDATE clubsponsors " \
                    "SET image = %s " \
                    "WHERE clubsponid= %s"
            newcosponsor_cursor.execute(updatecosponsor_query, (newcoimage,clubsponid))
            mysql.connection.commit()
            newcosponsor_cursor.close()
            msg = 'Sponsor information updated successfully!'
            clubsponsors_details=get_clubsponsors_details()
            return render_template("manasponsorseditp.html", clubsponsors_details=clubsponsors_details, clubsponid=clubsponid, msg=msg)
        except Exception as e:
            # Handle database update failure
            return "Failed to update details: {}".format(str(e))
    clubsponsors_details=get_clubsponsors_details()
    return render_template("manasponsorseditp.html",clubsponsors_details=clubsponsors_details,clubsponid=clubsponid)
    
@app.route("/manasponsorsaddc", methods=["GET", "POST"])
def manasponsorsaddc():
    msg=""
    coursesponsors_details= get_coursesponsors_details()
    if request.method == 'POST':
        spontypeid = 1
        addcourspon_name= request.form['courspon_name']
        addcourspon_link= request.form['courspon_link']
        addcoweb = request.form['coweb']
        addcoimage = request.form['coimage']

        try:
            manasponsorsadd_cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            insert_manasponsorsadd_query= '''INSERT INTO coursesponsors(spontypeid, courspon_name,courspon_link,web,image)
                            VALUES(%s,%s,%s,%s,%s)'''
            manasponsorsadd_cursor.execute(insert_manasponsorsadd_query, (spontypeid, addcourspon_name, addcourspon_link, addcoweb,addcoimage))
            mysql.connection.commit()
            manasponsorsadd_cursor.close()
            msg = 'You have successfully add sponsor!'
            return render_template("manasponsorsaddc.html",  coursesponsors_details=coursesponsors_details,msg=msg)
        except Exception as e:
            # Handle database update failure
            return "Failed to add scorecard details: {}".format(str(e))
    coursesponsors_details= get_coursesponsors_details()
    return render_template("manasponsorsaddc.html",coursesponsors_details=coursesponsors_details,msg=msg)

@app.route("/manasponsorsadd", methods=["GET", "POST"])
def manasponsorsadd():
    msg=""
    clubsponsors_details=get_clubsponsors_details()
    if request.method == 'POST':
        spontypeid_c = 2
        addclubspon_name= request.form['clubspon_name']
        addclubspon_link= request.form['clubspon_link']
        addclweb = request.form['clweb']
        addclimage = request.form['climage']

        try:
            manasponsorsadd_cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            insert_manasponsorsadd_query= '''INSERT INTO clubsponsors(spontypeid_c, clubspon_name,clubspon_link,web,image)
                            VALUES(%s,%s,%s,%s,%s)'''
            manasponsorsadd_cursor.execute(insert_manasponsorsadd_query, (spontypeid_c, addclubspon_name, addclubspon_link, addclweb,addclimage))
            mysql.connection.commit()
            manasponsorsadd_cursor.close()
            msg = 'You have successfully add sponsor!'
            return render_template("manasponsorsadd.html",  clubsponsors_details=clubsponsors_details,msg=msg)
        except Exception as e:
            # Handle database update failure
            return "Failed to add scorecard details: {}".format(str(e))

    clubsponsors_details=get_clubsponsors_details()
    return render_template("manasponsorsadd.html", clubsponsors_details=clubsponsors_details,msg=msg)

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

@app.route("/manacontact", methods=["GET", "POST"])
def manacontact():
    if request.method == 'POST':
        contact_id = request.form.get('contact_id')
        deletecontact_query = "DELETE FROM contact_details WHERE contact_id = %s;"
        deletecontact_cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        deletecontact_cursor.execute(deletecontact_query, (contact_id,))
        mysql.connection.commit()
        deletecontact_cursor.close()
        return redirect(url_for('manacontact')) 
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
                newcontact_cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                updatecontact_query = "UPDATE contact_details " \
                        "SET contact_address = %s, contact_email = %s, contact_phone = %s, facebook_url = %s, contact_map = %s " \
                        "WHERE contact_id= %s"
                newcontact_cursor.execute(updatecontact_query, (newcontact_address, newcontact_email, newcontact_phone, newfacebook_url, newcontact_map,contact_id))
                mysql.connection.commit()
                newcontact_cursor.close()
                msg = 'Contact information updated successfully!'

                contact_details = get_contact_details()
                return render_template("manacontactedit.html", contact_details=contact_details, contact_id=contact_id, msg=msg)
            except Exception as e:
                # Handle database update failure
                return render_template("error.html", error_message="Failed to update contact details: {}".format(str(e)))
    else:
        contact_details = get_contact_details()
        return render_template("manacontactedit.html", contact_details=contact_details, contact_id=contact_id)

    # If form validation fails or an error occurs, redirect user back to the form page with the error message
    return redirect(url_for('manacontactedit', contact_details=contact_details,contact_id=contact_id, msg=msg))

@app.route("/manacontactadd", methods=["GET", "POST"])
def manacontactadd():
    msg=""
    contact_details = None 

    if request.method == 'POST':
        addcontact_address= request.form['contact_address']
        addcontact_email= request.form['contact_email']
        addcontact_phone = request.form['contact_phone']
        addfacebook_url = request.form['facebook_url']
        addcontact_map = request.form['contact_map']

        if not re.match(r'.*\d+.*', addcontact_address) and not re.match(r'.*[a-zA-Z]+.*', addcontact_address):
            msg = 'Please enter a valid address!'
        elif not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', addcontact_email ):
            msg = 'Please enter a valid email address!'
        elif not re.match(r'^.*$', addcontact_phone):  
            msg = 'Please enter a valid phone number!'
        else:
            try:
                manascontactadd_cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                insert_manacontactadd_query= '''INSERT INTO contact_details(contact_address, contact_email,contact_phone,facebook_url,contact_map)
                                VALUES(%s,%s,%s,%s,%s)'''
                manascontactadd_cursor.execute(insert_manacontactadd_query, (addcontact_address, addcontact_email, addcontact_phone, addfacebook_url,addcontact_map))
                mysql.connection.commit()
                manascontactadd_cursor.close()
                msg = 'You have successfully add contact information!'
            except Exception as e:
                # Handle database update failure
                return "Failed to add contact details: {}".format(str(e))

    contact_details = get_contact_details()  
    return render_template("manacontactadd.html", contact_details=contact_details, msg=msg)


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
            active = 1
            insert_secure_query =  '''
                INSERT INTO membersign(roleid, rolename, membernum, firstname, surname, email, hash, salt, create_date, last_update_date,active)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, NOW(), NOW(),%s)
                '''
            values_membersign= (roleid, rolename, membernum, firstname, surname, email, hashed, salt,active)
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
                    
                    if account['active'] ==1:
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
                        msg = 'Your account is not activated. Please contact the administrator.'
                    
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

def get_membersign_details():
    members_cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    members_query = "SELECT * FROM membersign;"
    members_cursor.execute(members_query)
    members_details = members_cursor.fetchall()
    members_cursor.close()
    return members_details

def searchmember():
    if request.method == "POST":
        search_term = request.form.get("search_term")
        if search_term:
            search_condition = "%" + search_term + "%"
            members_cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            members_query = "SELECT * FROM membersign WHERE firstname LIKE %s OR surname LIKE %s OR membernum LIKE %s ORDER BY membernum ASC ;"
            members_cursor.execute(members_query, (search_condition, search_condition, search_condition))
            search_list = members_cursor.fetchall()
            return search_list
    # Return all members if search term is empty or no search term is provided
    return get_membersign_details()

@app.route("/manamembers", methods=['GET', 'POST'])
def manamembers():
    search_list = searchmember()
    if 'loggedin' in session:
        if request.method == "POST":
            membernum = request.form.get('membernum')
            isChecked = request.form.get('isChecked')

            try:
                deactivemembers_cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                update_member_status_query = "UPDATE membersign SET active = %s WHERE membernum = %s"
                deactivemembers_cursor.execute(update_member_status_query, (not isChecked, membernum))
                mysql.connection.commit()
                deactivemembers_cursor.close()

                return redirect(url_for('manamembers'))
            except Exception as e:
                return "Failed to update member status: {}".format(str(e))
        else:
            members_details = get_membersign_details()
            return render_template("manamembers.html", members_details=members_details,search_list=search_list)
    else:
        return redirect(url_for('login'))

@app.route("/manamembersedit/<int:membernum>", methods=['GET', 'POST'])
def manamembersedit(membernum):
    msg = ""
    if 'loggedin' in session:
        if request.method == "POST":
            newfirstname = request.form.get("firstname") 
            newsurname = request.form.get("surname") 

            if not re.match(r'^[A-Za-z]{2,20}$', newfirstname):
                msg = 'First name must contain only letters and be between 2 and 20 characters long.'
            elif not re.match(r'^[A-Za-z]{2,20}$', newsurname):
                msg = 'Surname must contain only letters and be between 2 and 20 characters long.'  
            else:  
                try:
                    # Update information
                    newmembers_cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                    updatemembers_query = "UPDATE membersign " \
                            "SET firstname = %s, surname = %s " \
                            "WHERE membernum= %s"
                    newmembers_cursor.execute(updatemembers_query, (newfirstname, newsurname, membernum))
                    mysql.connection.commit()
                    newmembers_cursor.close()
                    msg = 'Member name updated successfully!'
                    session['firstname'] = newfirstname
                    session['surname'] = newsurname
                except Exception as e:
                    # Handle database update failure
                    return "Failed to update details: {}".format(str(e))
        members_details = get_membersign_details()
        return render_template("manamembersedit.html", members_details=members_details, membernum=membernum, msg=msg)
    else:
        return redirect(url_for('login'))

@app.route("/manamemberadmin", methods=['GET', 'POST'])
def manamemberadmin():
    if 'loggedin' in session:
        if request.method == "POST":
            adminmembernum = request.form.get('membernum')
            isChecked = request.form.get('isChecked')

            try:
                deactiveadminmembers_cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                update_adminmember_status_query = "UPDATE membersign SET active = %s WHERE membernum = %s"
                deactiveadminmembers_cursor.execute(update_adminmember_status_query, (not isChecked, adminmembernum))
                mysql.connection.commit()
                deactiveadminmembers_cursor.close()

                return redirect(url_for('manamemberadmin'))
            except Exception as e:
                return "Failed to update admin status: {}".format(str(e))
        else:
            members_details = get_membersign_details()
            return render_template("manamemberadmin.html", members_details=members_details)
    else:
        return redirect(url_for('login'))
    
@app.route("/manamemberadminedit/<int:membernum>", methods=['GET', 'POST'])
def manamemberadminedit(membernum):
    msg = ""
    if 'loggedin' in session:
        if request.method == "POST":
            newfirstname = request.form.get("firstname") 
            newsurname = request.form.get("surname") 

            if not re.match(r'^[A-Za-z]{2,20}$', newfirstname):
                msg = 'First name must contain only letters and be between 2 and 20 characters long.'
            elif not re.match(r'^[A-Za-z]{2,20}$', newsurname):
                msg = 'Surname must contain only letters and be between 2 and 20 characters long.'  
            else:  
                try:
                    # Update information
                    newmembers_cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                    updatemembers_query = "UPDATE membersign " \
                            "SET firstname = %s, surname = %s " \
                            "WHERE membernum= %s"
                    newmembers_cursor.execute(updatemembers_query, (newfirstname, newsurname, membernum))
                    mysql.connection.commit()
                    newmembers_cursor.close()
                    msg = 'Member name updated successfully!'
                    session['firstname'] = newfirstname
                    session['surname'] = newsurname
                except Exception as e:
                    # Handle database update failure
                    return "Failed to update details: {}".format(str(e))
        members_details = get_membersign_details()
        return render_template("manamemberadminedit.html", members_details=members_details, membernum=membernum, msg=msg)
    else:
        return redirect(url_for('login'))

@app.route("/manamemberadminadd", methods=['GET', 'POST'])
def manamemberadminadd():
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
            rolename = "Admin"
            roleid = 2
            hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            salt = bcrypt.gensalt().decode('utf-8')
            active = 1
            insert_secure_query =  '''
                INSERT INTO membersign(roleid, rolename, membernum, firstname, surname, email, hash, salt, create_date, last_update_date,active)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, NOW(), NOW(),%s)
                '''
            values_membersign= (roleid, rolename, membernum, firstname, surname, email, hashed, salt,active)
            cursor.execute(insert_secure_query, values_membersign)
    
            mysql.connection.commit()  # Commit the transaction
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    
    # Show registration form with message (if any)
    return render_template('manamemberadminadd.html', msg=msg)

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

def get_allnav_details():
    allnav_cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    allnav_query = """
   SELECT nav.navtypeid, nav.nav_type, nav.nav_order, nav.nav_title,
       dropdown.dropnavid, dropdown.droptitle, dropdown.drop_order
       FROM navbaritems AS nav
       INNER JOIN dropdownitems AS dropdown ON nav.nav_order = dropdown.category;
    """
    allnav_cursor.execute(allnav_query)
    allnav_details = allnav_cursor.fetchall()   
    allnav_cursor.close()   
    return allnav_details

@app.route("/managenavbar", methods=["GET", "POST"])
def managenavbar():
    if request.method == "POST":
        selected_nav_title = request.form.get("selectnavtitle")

        filtered_data_query = """
            SELECT nav.navtypeid, nav.nav_type, nav.nav_order, nav.nav_title,
                dropdown.dropnavid, dropdown.droptitle, dropdown.drop_order
                FROM navbaritems AS nav
                INNER JOIN dropdownitems AS dropdown ON nav.nav_order = dropdown.category
                WHERE nav.nav_title = %s;
            """

        allnav_cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        allnav_cursor.execute(filtered_data_query, (selected_nav_title,))
        filtered_data = allnav_cursor.fetchall()
        allnav_cursor.close()

        return render_template("managenavbar.html", allnav_details=filtered_data)

    else:
        allnav_details = get_allnav_details()
        return render_template("managenavbar.html", allnav_details=allnav_details)

@app.route("/managenavbaredit/<int:dropnavid>", methods=["GET", "POST"])
def managenavbaredit(dropnavid):
    msg = ""
    allnav_details = get_allnav_details()
    if request.method == "POST":
        newdropnavtitle = request.form.get("droptitle")
        if not re.match(r'^.{1,100}$', newdropnavtitle):
            msg = 'Please enter a valid dropdwon title!'
        else:
            try:
                # Update home details information
                newallnavdetails_cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                updatenewallnavdetails_query = "UPDATE dropdownitems " \
                        "SET droptitle = %s " \
                        "WHERE dropnavid = %s"
                newallnavdetails_cursor.execute( updatenewallnavdetails_query, (newdropnavtitle, dropnavid))
                mysql.connection.commit()
                newallnavdetails_cursor.close()
                msg = 'Navgition dropdown title updated successfully!'
                allnav_details = get_allnav_details()
                return render_template("managenavbaredit.html", allnav_details=allnav_details, dropnavid=dropnavid, msg=msg)
            except:
                # Handle database update failure
                return "Failed to update homepage details"
    return render_template("managenavbaredit.html",allnav_details=allnav_details,dropnavid=dropnavid,msg=msg)



def get_popup_details():
    popup_cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    popup_query = "SELECT * FROM popup;"
    popup_cursor.execute(popup_query)
    popup_details = popup_cursor.fetchall()
    popup_cursor.close()
    return popup_details

@app.route("/manapopup", methods=["GET", "POST"])
def manapopup():
    popup_details = get_popup_details()
    return render_template("manapopup.html",popup_details=popup_details)

@app.route("/manapopupedit/<int:popupid>", methods=["GET", "POST"])
def manapopupedit(popupid):
    msg=""
    popup_details = get_popup_details()
    if request.method == "POST":
        newinformation = request.form.get("information")
        newdate = request.form.get("date")
        newtime = request.form.get("time")
        newendtime = request.form.get("endtime")
        try:
            # Update home details information
            newpopupdetails_cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            updatepopupdetails_query = "UPDATE popup " \
                    "SET information = %s, date = %s, time = %s, endtime = %s" \
                    "WHERE popupid = %s"
            newpopupdetails_cursor.execute( updatepopupdetails_query, (newinformation, newdate,newtime,newendtime,popupid))
            mysql.connection.commit()
            newpopupdetails_cursor.close()
            msg = 'Pop up updated successfully!'
            popup_details = get_popup_details()
            return render_template("manapopupedit.html", popup_details=popup_details,popupid=popupid,msg=msg)
        except Exception as e:
        # Handle database update failure
            error_message = str(e) 
            return "Failed to update details. Error: " + error_message

    return render_template("manapopupedit.html",popup_details=popup_details,popupid=popupid,msg=msg)

if __name__ == '__main__':
    app.run(debug="True")