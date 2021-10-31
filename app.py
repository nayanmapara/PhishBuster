from flask import Flask, request, render_template, redirect, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import phishbuster as pb
from flaskext.mysql import MySQL
import requests
import os

app = Flask(__name__,template_folder='static')
limiter = Limiter(app, key_func=get_remote_address) # Limiter setup for PhishBuster API
mysql = MySQL()

app.config['MYSQL_DATABASE_USER'] = os.environ['user']
app.config['MYSQL_DATABASE_PASSWORD'] = os.environ['password']
app.config['MYSQL_DATABASE_DB'] = os.environ['dbname']
app.config['MYSQL_DATABASE_HOST'] = os.environ['servername']

mysql.init_app(app) 

header = ['Sr No.', 'Orginal Site', 'Phishing Site','Action'] # Header for reports table

total,phishing,safe_site,reported = 0,0,0,0

# Stores url of site after scan if safe
redirect_url = ""

def counter_data(total,phishing,safe_site,reported,mode='r'):
    if mode == 'w':
        with open('counter_data.txt','w') as w_count:
            w_count.write(f"{total} {phishing} {safe_site} {reported}")
    else:
        with open('counter_data.txt') as r_count:
            data_read = [r_count.read().split(' ')]
        return data_read

def mysqldata_insert(seurl,inurl): # For appending values to reports_data table
    try:
        connect = mysql.connect() # for connecting to the database
        cursor = connect.cursor() # cursor to execute mysql queries
        cursor.execute("INSERT INTO reports_data(org_site,phish_site) VALUES (%(seurl)s,%(inurl)s);",{'seurl':seurl,'inurl': inurl}) # mysql query to append data to the dataabase
        connect.commit() # commit changes to database
        print('Commited Successfully')
    except Exception as e:
        print(e)
        connect.rollback() # undo changes if error occured while appending data to the database

@app.route("/") # index page
def index():
    for i in counter_data(total=total,phishing=phishing,safe_site=safe_site,reported=reported):
        total_scanned = int(i[0])
        phishing_sites = int(i[1])
        safe_sites = int(i[2])
        reported_sites = int(i[3])
    counter = [['Sites Scanned',total_scanned],['Safe Sites',safe_sites],['Phishing Sites',phishing_sites],['Sites Reported',reported_sites]]
    try:
        connect = mysql.connect() # for connecting to the database
        cursor = connect.cursor() # cursor to execute mysql queries
        cursor.execute('SELECT names,domains FROM domain_data;') # mysql query to get all the data from the database
        db_output = cursor.fetchall() # fetching all the data from the database
        lis = list(db_output) # converting tuple to list
        lis.sort() # sorting the list
        selecturl = [["SELECT THE RESEMBLING SITE","select"]]+lis # appending the list to the list
        cursor.execute('SELECT country_name,country_code FROM countries;') # mysql query to get all the data from the database
        db_output2 = cursor.fetchall() # fetching all the data from the database
        lis2 = list(db_output2) # converting tuple to list
        lis2.sort() # sorting the list
        countrydata = [["SELECT YOUR COUNTRY","select"]]+lis2 # appending the list to the list
        return render_template("index.html",selecturl=selecturl,countrydata=countrydata,counterdata=counter) # selecturl sends list containing list of real sites
    except Exception as e:
        print(e)
        selecturl = [["Error Occured","select"]] # if error occured while fetching data from the database
        countrydata = [["Error Occured","select"]] # if error occured while fetching data from the database
        return render_template("index.html",selecturl=selecturl,countrydata=countrydata,counterdata=counter) # selecturl sends error as it failed to get data from the database
    return redirect('/')

# For getting values from index and passing them to PhishBuster
@app.route('/check', methods=["GET","POST"])
def check():
    global total,phishing,safe_site,redirect_url
    if request.method == "POST":
        req = request.form 
        inurl = req['inurl'] # Storing input url in a variable
        seurl = req['seurl'] # Storing url from drop down menu in a variable
        country = req['country'] # Storing country's iso code in a variable
        inurl = inurl.lower() # Converting input url to lower case to avoid errors
        if inurl != '' and seurl != 'select' :
            total += 1
            output = pb.comparing_url(inurl,seurl,country) # Returns 'True' if it is a phishing site or 'False' if it is a safe site
            if output is True:
                mysqldata_insert(seurl,inurl) # For appending data if it is a phising site
                phishing += 1
                counter_data(total,phishing,safe_site,'w')
                return redirect('/phishing') # Redirects to It is PHISHING SITE
            safe_site += 1
            counter_data(total,phishing,safe_site,'w')
            redirect_url = inurl # Sets url to redirect
            return redirect('/safe') # Redirects to It is SAFE SITE
        return redirect('/') # Redirects to home page if values are not entered

# reports page
@app.route("/reports")
def reports():
    global reported
    try:
        for i in counter_data(total=total,phishing=phishing,safe_site=safe_site,reported=reported):
            total_scanned = int(i[0])
            phishing_sites = int(i[1])
            safe_sites = int(i[2])
            reported_sites = int(i[3])
        counter = [['Sites Scanned',total_scanned],['Safe Sites',safe_sites],['Phishing Sites',phishing_sites],['Sites Reported',reported_sites]]
        connect = mysql.connect() # for connecting to the database
        cursor = connect.cursor() # cursor to execute mysql queries
        cursor.execute('SELECT * FROM reports_data') # '*' here is for id, orginal site and phising site
        db_output = cursor.fetchall()
        # converting to list to pass the data to html
        report = list(db_output) if list(db_output) else []  
        reported = report[-1][0] if report else 0  
        counter_data(total=total,phishing=phishing,safe_site=safe_site,reported=reported,mode='w')
        return render_template("reports.html",head=header,reports=report,counterdata=counter) # header for column names and reports for rows/site data
    except Exception as e:
        print(e)
        report = ["Error Occured to connect with DB"] # if error occured while fetching data from the database
        return render_template("reports.html",head=header,reports=report,counterdata=counter)
    return redirect('/')

# phising label page
@app.route("/phishing")
def phish():
    return render_template("phish.html")

# Accepts post request and redirects to safe site when visit button is clicked
@app.route("/turn", methods=["GET","POST"])
def turn():
    if request.method == "POST":
        return redirect(pb.url_syntax(redirect_url))
    return redirect("/safe")

# safe label page
@app.route("/safe")
def safe():
    return render_template("safe.html")

# For deleteing a desired row
@app.route('/delete/<id>/')
def delete(id):
    connect = mysql.connect() # for connecting to the database
    cursor = connect.cursor() # cursor to execute mysql queries
    cursor.execute("DELETE FROM reports_data WHERE id=%(id)s;",{'id': id}) # mysql query to delete data of a row
    connect.commit() # commit changes to the database
    print('Commited Successfully')
    return redirect('/reports') # Redirecting to reports page to show that changes were made successfully

# For manually adding values to the database of reports
@app.route('/manualadd', methods = ['POST'])
def manualadd():
    if request.method == 'POST':
        req = request.form
        seurl = req['org'] # getting values through post request and storing to a variable
        inurl = req['phish'] # getting values through post request and storing to a variable   
        mysqldata_insert(seurl,inurl) # To adding data to the database
        return redirect('/reports') # Redirecting to reports page to show that changes were made successfully

@app.route("/api/", methods=['GET','POST']) # Geeting values from the url
@limiter.limit("50/minute") # Setting a limit of 50 PhishBuster API requests in a minute
def api():
    global total,phishing,safe_site
    if request.method == 'POST':
        req = request.form
        inurl = req['check-url']
        seurl = req['org-url']
        country = req['country']
        store = req['save-scan-data']
        inurl = inurl.lower() # Converting input url to lower case to avoid errors
        seurl = seurl.lower() # Converting url from original domain to lower case to avoid errors
        total += 1
        output = pb.comparing_url(inurl,seurl,country) # Returns 'True' if it is a phishing site or 'False' if it is a safe site

        if store == 'True': # String as the input can be made to anything and to overcoming error if the input is coverted to boolean before filtering
            if output is True:
                phishing += 1
                counter_data(total,phishing,safe_site,'w')
                mysqldata_insert(seurl,inurl) # To adding data to the database
                return jsonify({'Input Url':inurl,'Orginal Url':seurl,'Phishing Site':output,'Data Saved':bool(store),'Region':country}) # API response with data saved information
            safe_site += 1
            counter_data(total,phishing,safe_site,'w')
            return jsonify({'Input Url':inurl,'Orginal Url':seurl,'Phishing Site':output,'Data Saved':bool(store),'Region':country}) # API response with data saved information
        return jsonify({'Input Url':inurl,'Orginal Url':seurl,'Phishing Site':output,'Region':country}) # API response if values are not saved
    return render_template('api.html') # Redirecting to reports page to show that changes were made successfully


if __name__ == '__main__':
    app.run(debug=True)
