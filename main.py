from flask import Flask,render_template,session,request,redirect,url_for,flash
import mysql.connector,hashlib
import os
import sys
from dotenv import load_dotenv

# Optional imports for statistics (may not be available in serverless)
try:
    import matplotlib
    matplotlib.use('Agg')  # Use non-interactive backend for serverless
    import matplotlib.pyplot as plt
    import numpy as np
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    print("⚠️  matplotlib not available - statistics charts will be disabled")

# Load environment variables from .env file
load_dotenv()

# Read DB credentials from environment variables
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_USER = os.getenv('DB_USER', 'root')
DB_PASS = os.getenv('DB_PASSWORD', 'root')
DB_NAME = os.getenv('DB_NAME', 'DBMS_PROJECT')

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'sec key')
app.config['SESSION_TYPE'] = 'filesystem'

# Database connection pool (lazy initialization)
mydb = None
mycursor = None

def get_db_connection():
    """Get database connection (creates if not exists)"""
    global mydb, mycursor
    try:
        # Check if connection exists and is alive
        if mydb is not None:
            mydb.ping(reconnect=True)
            return mydb, mycursor
    except:
        pass
    
    # Create new connection
    try:
        mydb = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASS,
            database=DB_NAME,
            autocommit=True
        )
        mycursor = mydb.cursor(buffered=True)
        print(f'✅ Successfully connected to MySQL database: {DB_NAME}')
        return mydb, mycursor
    except mysql.connector.Error as e:
        print('\n❌ ERROR: Unable to connect to MySQL database.')
        print('Details:', e)
        print('\nCurrent configuration:')
        print(f'  Host: {DB_HOST}')
        print(f'  User: {DB_USER}')
        print(f'  Database: {DB_NAME}')
        raise

@app.before_request
def before_request():
    """Initialize database connection before each request"""
    global mydb, mycursor
    if mydb is None or mycursor is None:
        mydb, mycursor = get_db_connection()

@app.route("/",methods = ['POST', 'GET'])
@app.route("/home",methods = ['POST','GET'])
def home():
    if not session.get('login'):
        return render_template('login.html'),401
    else:
        if session.get('isAdmin') :
            return render_template('home.html',username=session.get('username'))
        else :
            return redirect(url_for('user_dashboard'))

@app.route("/login",methods = ['GET','POST'])
def login():
    if request.method=='POST' :
        query = """SELECT * FROM login WHERE username = '%s'""" %(request.form['username'])
        mycursor.execute(query)
        res = mycursor.fetchall()
        if mycursor.rowcount == 0:
            return home()
        if request.form['password'] != res[0][1]:
            return render_template('login.html')
        else:
            session['login'] = True
            session['username'] = request.form['username']
            session['password'] = request.form['password']
            session['isAdmin'] = (request.form['username']=='admin')
            return home()
    return render_template('login.html')

@app.route("/show_update_detail",methods=['POST','GET'])
def show_update_detail():
    if not session.get('login'):
        return redirect( url_for('home') )
    if request.method=='POST':
        if request.form['User_ID'] =='':
            return render_template("search_detail.html")
        qry = "Select * from User where User.User_ID = %s" %(request.form['User_ID'])
        qry1 = "Select * from User_phone_no where User_ID = %s" %(request.form['User_ID'])
        mycursor.execute(qry)
        not_found=False
        res=()
        if(mycursor.rowcount > 0):
            res = mycursor.fetchone()
        else:
            not_found=True
        fields = mycursor.column_names
        qry_upd = "Select * from User where User_ID = %s" %(request.form['User_ID'])
        mycursor.execute(qry_upd)
        upd_res = ()
        if(mycursor.rowcount > 0):
            upd_res = mycursor.fetchone()
        fields_upd = mycursor.column_names
        mycursor.execute(qry1)
        phone_no = mycursor.fetchall()
        qry_pat = "select Patient_ID, organ_req, reason_of_procurement, Doctor_name from Patient inner join Doctor on Doctor.Doctor_ID = Patient.Doctor_ID and User_ID = %s" %(request.form['User_ID'])
        qry_don = "select Donor_ID, organ_donated, reason_of_donation, Organization_name from Donor inner join Organization on Organization.Organization_ID = Donor.Organization_ID and User_ID = %s" %(request.form['User_ID'])
        qry_trans = "select distinct Transaction.Patient_ID, Transaction.Donor_ID, Organ_ID, Date_of_transaction, Status from Transaction, Patient, Donor where (Patient.User_ID = %s and Patient.Patient_ID = Transaction.Patient_ID) or (Donor.User_Id= %s and Donor.Donor_ID = Transaction.Donor_ID)" %((request.form['User_ID']),(request.form['User_ID']))
        #
        res_pat = ()
        res_dnr = ()
        res_trans = ()
        mycursor.execute(qry_pat)
        if(mycursor.rowcount > 0):
            res_pat = mycursor.fetchall()
        fields_pat = mycursor.column_names
        #
        mycursor.execute(qry_don)
        if(mycursor.rowcount > 0):
            res_dnr = mycursor.fetchall()
        fields_dnr = mycursor.column_names
        #
        mycursor.execute(qry_trans)
        if(mycursor.rowcount > 0):
            res_trans = mycursor.fetchall()
        fields_trans = mycursor.column_names
        print(res_trans)
        if("show" in request.form):
            return render_template('show_detail_2.html',res = res,fields = fields, not_found=not_found, phone_no = phone_no, res_dnr = res_dnr, res_pat = res_pat,res_trans = res_trans,fields_trans = fields_trans, fields_dnr = fields_dnr, fields_pat = fields_pat)
        if("update" in request.form):
            return render_template('update_detail.html',res = upd_res,fields = fields_upd, not_found=not_found)
        if "delete" in request.form:
            if not_found:
                return render_template('show_detail_2.html',res = res,fields = fields, not_found=not_found, phone_no = phone_no,  res_dnr = res_dnr, res_pat = res_pat,res_trans = res_trans,fields_trans = fields_trans, fields_dnr = fields_dnr, fields_pat = fields_pat)
            else:
                qry2 = "DELETE FROM User where User_ID = %s" %(request.form['User_ID'])
                mycursor.execute(qry2)
                mydb.commit()
                return render_template("home.html")

@app.route("/search_detail",methods = ['POST','GET'])
def search_detail():
    if not session.get('login'):
        return redirect( url_for('home') )
    return render_template('search_detail.html')

#--------------Adding Information----------------------------

@app.route("/add_<id>_page",methods = ['POST','GET'])
def add_page(id):
    if not session.get('login'):
        return redirect( url_for('home') )
    qry = "SELECT * from " + id.capitalize()
    mycursor.execute(qry)
    fields = mycursor.column_names

    return render_template('add_page.html',success=request.args.get('success'), error=request.args.get('error'), fields = fields, id= id)

@app.route("/add_User", methods=['POST','GET'])
def add_User():
    if not session.get('login'):
        return redirect( url_for('home') )
    qry = "SELECT * from User"
    mycursor.execute(qry)
    fields = mycursor.column_names

    val = ()

    for field in fields:
        temp = request.form.get(field)
        if field not in ['User_ID','Medical_insurance'] and temp != '':
            temp = "\'"+temp+"\'"
        if temp == '':
            temp = 'NULL'
        val = val + (temp,)

    qry = "INSERT INTO User Values (%s,%s,%s,%s,%s,%s,%s,%s)"%val
    print(qry)
    success = True
    error = False
    try:
        mycursor.execute(qry)
    except:
        print("Error : User not Inserted")
        error = True
        success = False
    mydb.commit()

    return redirect(url_for('add_page', id='User', error=error,success=success))

@app.route("/add_User_phone_no", methods=['POST','GET'])
def add_User_phone_no():
    if not session.get('login'):
        return redirect( url_for('home') )
    qry = "SELECT * from User_phone_no"
    mycursor.execute(qry)
    fields = mycursor.column_names

    val = ()

    for field in fields:
        temp = request.form.get(field)
        if field not in ['User_ID','Phone_no'] and temp != '':
            temp = "\'"+temp+"\'"
        if temp == '':
            temp = 'NULL'
        val = val + (temp,)

    qry = "INSERT INTO User_phone_no Values (%s,%s)"%val
    print(qry)
    success = True
    error = False
    try:
        mycursor.execute(qry)
    except:
        print("Error : User not Inserted")
        error = True
        success = False
    mydb.commit()

    return redirect(url_for('add_page', id='User_phone_no', error=error,success=success))

@app.route("/add_Patient", methods=['POST','GET'])
def add_Patient():
    if not session.get('login'):
        return redirect( url_for('home') )
    qry = "SELECT * from Patient"
    mycursor.execute(qry)
    fields = mycursor.column_names

    val = ()

    for field in fields:
        temp = request.form.get(field)
        if field not in ['Patient_ID','User_ID','Doctor_ID'] and temp != '':
            temp = "\'"+temp+"\'"
        if temp == '':
            temp = 'NULL'
        val = val + (temp,)

    qry = "INSERT INTO Patient Values (%s,%s,%s,%s,%s)"%val
    print(qry)
    success = True
    error = False
    try:
        mycursor.execute(qry)
    except:
        print("Error : User not Inserted")
        error = True
        success = False
    mydb.commit()

    return redirect(url_for('add_page', id='Patient', error=error,success=success))

@app.route("/add_Donor", methods=['POST','GET'])
def add_Donor():
    if not session.get('login'):
        return redirect( url_for('home') )
    qry = "SELECT * from Donor"
    mycursor.execute(qry)
    fields = mycursor.column_names
    val = ()
    for field in fields:
        temp = request.form.get(field)
        if field not in ['Donor_ID','User_ID','Organization_ID'] and temp != '':
            temp = "\'"+temp+"\'"
        if temp == '':
            temp = 'NULL'
        val = val + (temp,)
    mycursor.execute( "START TRANSACTION;" )
    qry = "INSERT INTO Donor Values (%s,%s,%s,%s,%s)"%val
    print(qry)
    success = True
    error = False
    try:
        mycursor.execute(qry)
    except:
        print("Error : User not Inserted")
        error = True
        success = False

    qry_insert = "insert into Organ_available (Organ_name, Donor_ID) Values (%s,%s) "%(val[1],val[0])

    mycursor.execute(qry_insert)

    mycursor.execute("COMMIT;")

    mydb.commit()

    return redirect(url_for('add_page', id='Donor', error=error,success=success))

@app.route("/add_Doctor", methods=['POST','GET'])
def add_Doctor():
    if not session.get('login'):
        return redirect( url_for('home') )
    qry = "SELECT * from Doctor"
    mycursor.execute(qry)
    fields = mycursor.column_names

    val = ()

    for field in fields:
        temp = request.form.get(field)
        if field not in ['Doctor_ID','Organization_ID'] and temp != '':
            temp = "\'"+temp+"\'"
        if temp == '':
            temp = 'NULL'
        val = val + (temp,)

    qry = "INSERT INTO Doctor Values (%s,%s,%s,%s)"%val
    print(qry)
    success = True
    error = False
    try:
        mycursor.execute(qry)
    except:
        print("Error : User not Inserted")
        error = True
        success = False
    mydb.commit()

    return redirect(url_for('add_page', id='Doctor', error=error,success=success))

@app.route("/add_Doctor_phone_no", methods=['POST','GET'])
def add_Doctor_phone_no():
    if not session.get('login'):
        return redirect( url_for('home') )
    qry = "SELECT * from Doctor_phone_no"
    mycursor.execute(qry)
    fields = mycursor.column_names

    val = ()

    for field in fields:
        temp = request.form.get(field)
        if field not in ['Doctor_ID','Phone_no'] and temp != '':
            temp = "\'"+temp+"\'"
        if temp == '':
            temp = 'NULL'
        val = val + (temp,)

    qry = "INSERT INTO Doctor_phone_no Values (%s,%s)"%val
    print(qry)
    success = True
    error = False
    try:
        mycursor.execute(qry)
    except:
        print("Error : User not Inserted")
        error = True
        success = False
    mydb.commit()

    return redirect(url_for('add_page', id='Doctor_phone_no', error=error,success=success))

@app.route("/add_Organ_available", methods=['POST','GET'])
def add_Organ_available():
    if not session.get('login'):
        return redirect( url_for('home') )
    qry = "SELECT * from Organ_available"
    mycursor.execute(qry)
    fields = mycursor.column_names

    val = ()

    for field in fields:
        temp = request.form.get(field)
        if field not in ['Organ_ID','Donor_ID'] and temp != '':
            temp = "\'"+temp+"\'"
        if temp == '':
            temp = 'NULL'
        val = val + (temp,)

    qry = "INSERT INTO Organ_available Values (%s,%s,%s)"%val
    print(qry)
    success = True
    error = False
    try:
        mycursor.execute(qry)
    except:
        print("Error : User not Inserted")
        error = True
        success = False
    mydb.commit()

    return redirect(url_for('add_page', id='Organ_available', error=error,success=success))


@app.route("/add_Organization", methods=['POST','GET'])
def add_Organization():
    if not session.get('login'):
        return redirect( url_for('home') )
    qry = "SELECT * from Organization"
    mycursor.execute(qry)
    fields = mycursor.column_names

    val = ()

    for field in fields:
        temp = request.form.get(field)
        if field not in ['Government_approved','Organization_ID'] and temp != '':
            temp = "\'"+temp+"\'"
        if temp == '':
            temp = 'NULL'
        val = val + (temp,)

    qry = "INSERT INTO Organization Values (%s,%s,%s,%s)"%val
    print(qry)
    success = True
    error = False
    try:
        mycursor.execute(qry)
    except:
        print("Error : User not Inserted")
        error = True
        success = False
    mydb.commit()

    return redirect(url_for('add_page', id='Organization', error=error,success=success))

@app.route("/add_Organization_phone_no", methods=['POST','GET'])
def add_Organization_phone_no():
    if not session.get('login'):
        return redirect( url_for('home') )
    qry = "SELECT * from Organization_phone_no"
    mycursor.execute(qry)
    fields = mycursor.column_names

    val = ()

    for field in fields:
        temp = request.form.get(field)
        if field not in ['Organization_ID','Phone_no'] and temp != '':
            temp = "\'"+temp+"\'"
        if temp == '':
            temp = 'NULL'
        val = val + (temp,)

    qry = "INSERT INTO Organization_phone_no Values (%s,%s)"%val
    print(qry)
    success = True
    error = False
    try:
        mycursor.execute(qry)
    except:
        print("Error : User not Inserted")
        error = True
        success = False
    mydb.commit()

    return redirect(url_for('add_page', id='Organization_phone_no', error=error,success=success))

@app.route("/add_Organization_head", methods=['POST','GET'])
def add_Organization_head():
    if not session.get('login'):
        return redirect( url_for('home') )
    qry = "SELECT * from Organization_head"
    mycursor.execute(qry)
    fields = mycursor.column_names

    val = ()

    for field in fields:
        temp = request.form.get(field)
        if field not in ['Employee_ID','Term_length','Organization_ID'] and temp != '':
            temp = "\'"+temp+"\'"
        if temp == '':
            temp = 'NULL'
        val = val + (temp,)

    qry = "INSERT INTO Organization_head Values (%s,%s,%s,%s,%s)"%val
    print(qry)
    success = True
    error = False
    try:
        mycursor.execute(qry)
    except:
        print("Error : User not Inserted")
        error = True
        success = False
    mydb.commit()

    return redirect(url_for('add_page', id='Organization_head', error=error,success=success))

@app.route("/add_Transaction", methods=['POST','GET'])
def add_Transaction_head():
    if not session.get('login'):
        return redirect( url_for('home') )
    qry = "SELECT * from Transaction"
    mycursor.execute(qry)
    fields = mycursor.column_names

    val = ()

    for field in fields:
        temp = request.form.get(field)
        if field not in ['Patient_ID','Donor_ID','Status','Organ_ID'] and temp != '':
            temp = "\'"+temp+"\'"
        if temp == '':
            temp = 'NULL'
        val = val + (temp,)

    mycursor.execute( "START TRANSACTION;" )
    qry = "INSERT INTO Transaction Values (%s,%s,%s,%s,%s)"%val
    print(qry)
    success = True
    error = False
    try:
        mycursor.execute(qry)
    except:
        print("Error : User not Inserted")
        error = True
        success = False

    qry_insert = "delete from Organ_available where Organ_ID = %s "%val[1]

    mycursor.execute(qry_insert)

    mycursor.execute("COMMIT;")

    mydb.commit()

    return redirect(url_for('add_page', id='Transaction', error=error,success=success))

#------------------------Update details-------------------------------------		#-------------------------------------------------------------

@app.route("/update_user_page",methods = ['POST','GET'])
def update_user_page():
    if not session.get('login'):
        return redirect( url_for('home') )
    qry_upd = "Select * from User"
    mycursor.execute(qry_upd)
    fields_upd = mycursor.column_names
    upd_res=[None]*len(fields_upd)
    return render_template('update_user_page.html',fields = fields_upd,res = upd_res)

@app.route("/update_user_details",methods = ['GET','POST'])
def update_details():
    if not session.get('login'):
        return redirect( url_for('home') )
    mycursor.execute("SELECT * from User")
    fields = mycursor.column_names
    qry = "UPDATE User SET "
    for field in fields:
        if request.form[field] not in ['None','']:
            if field in ['User_ID','Medical_insurance']:
                qry = qry + "%s = %s , " %(field,request.form[field])
            else:
                qry = qry + " %s = \'%s\' , " %(field,request.form[field])
        else:
            qry = qry + "%s = NULL , " %(field)
    qry = qry[:-2]
    qry = qry + "WHERE User_ID = %s;" %(request.form['User_ID'])
    print(qry)
    try:
        mycursor.execute(qry)
    except:
        print("update error")
    mydb.commit()
    qry2 = "select * from User where User_ID = %s" %(request.form['User_ID'])
    mycursor.execute(qry2)
    res = mycursor.fetchone()
    qry = "Select * from User where User.User_ID = %s" %(request.form['User_ID'])
    qry1 = "Select * from User_phone_no where User_ID = %s" %(request.form['User_ID'])
    mycursor.execute(qry)
    not_found=False
    res=()
    if(mycursor.rowcount > 0):
        res = mycursor.fetchone()
    else:
        not_found=True
    fields = mycursor.column_names
    qry_upd = "Select * from User where User_ID = %s" %(request.form['User_ID'])
    mycursor.execute(qry_upd)
    upd_res = ()
    if(mycursor.rowcount > 0):
        upd_res = mycursor.fetchone()
    fields_upd = mycursor.column_names
    mycursor.execute(qry1)
    phone_no = mycursor.fetchall()
    qry_pat = "select Patient_ID, organ_req, reason_of_procurement, Doctor_name from Patient inner join Doctor on Doctor.Doctor_ID = Patient.Doctor_ID and User_ID = %s" %(request.form['User_ID'])
    qry_don = "select Donor_ID, organ_donated, reason_of_donation, Organization_name from Donor inner join Organization on Organization.Organization_ID = Donor.Organization_ID and User_ID = %s" %(request.form['User_ID'])
    qry_trans = "select distinct Transaction.Patient_ID, Transaction.Donor_ID, Organ_ID, Date_of_transaction, Status from Transaction, Patient, Donor where (Patient.User_ID = %s and Patient.Patient_ID = Transaction.Patient_ID) or (Donor.User_Id= %s and Donor.Donor_ID = Transaction.Donor_ID)" %((request.form['User_ID']),(request.form['User_ID']))
    #
    res_pat = ()
    res_dnr = ()
    res_trans = ()
    mycursor.execute(qry_pat)
    if(mycursor.rowcount > 0):
        res_pat = mycursor.fetchall()
    fields_pat = mycursor.column_names
    #
    mycursor.execute(qry_don)
    if(mycursor.rowcount > 0):
        res_dnr = mycursor.fetchall()
    fields_dnr = mycursor.column_names
    #
    mycursor.execute(qry_trans)
    if(mycursor.rowcount > 0):
        res_trans = mycursor.fetchall()
    fields_trans = mycursor.column_names
    # if("show" in request.form):
    return render_template('show_detail_2.html',res = res,fields = fields, not_found=not_found, phone_no = phone_no, res_dnr = res_dnr, res_pat = res_pat,res_trans = res_trans,fields_trans = fields_trans, fields_dnr = fields_dnr, fields_pat = fields_pat)
    # return render_template("show_detail.html",res = res,fields=fields,not_found = False)

@app.route("/update_patient_page",methods = ['POST','GET'])
def update_patient_page():
    if not session.get('login'):
        return redirect( url_for('home') )
    qry_upd = "Select * from Patient"
    mycursor.execute(qry_upd)
    fields_upd = mycursor.column_names
    upd_res=[None]*len(fields_upd)
    return render_template('update_patient_page.html',fields = fields_upd,res = upd_res)

@app.route("/update_patient_details",methods = ['GET','POST'])
def update_patient_details():
    if not session.get('login'):
        return redirect( url_for('home') )
    mycursor.execute("SELECT * from Patient")
    fields = mycursor.column_names
    qry = "UPDATE Patient SET "
    for field in fields:
        if request.form[field] not in ['None','']:
            if field in ['User_ID','Doctor_ID','Patient_ID']:
                qry = qry + "%s = %s , " %(field,request.form[field])
            else:
                qry = qry + " %s = \'%s\' , " %(field,request.form[field])
        else:
            qry = qry + "%s = NULL , " %(field)
    qry = qry[:-2]
    qry = qry + "WHERE Patient_ID = %s and organ_req = \'%s\';" %(request.form['Patient_ID'],request.form['organ_req'])
    print(qry)
    try:
        mycursor.execute(qry)
    except:
        print("update error")
    mydb.commit()
    qry2 = "select * from Patient WHERE Patient_ID = %s and organ_req = \'%s\';" %(request.form['Patient_ID'],request.form['organ_req'])
    mycursor.execute(qry2)
    res = mycursor.fetchone()
    print(res)
    print(qry2)
    return render_template("show_detail.html",res = res,fields=fields,not_found = False)

@app.route("/update_donor_page",methods = ['POST','GET'])
def update_donor_page():
    if not session.get('login'):
        return redirect( url_for('home') )
    qry_upd = "Select * from Donor"
    mycursor.execute(qry_upd)
    fields_upd = mycursor.column_names
    upd_res=[None]*len(fields_upd)
    return render_template('update_donor_page.html',fields = fields_upd,res = upd_res)

@app.route("/update_donor_details",methods = ['GET','POST'])
def update_donor_details():
    if not session.get('login'):
        return redirect( url_for('home') )
    mycursor.execute("SELECT * from Donor")
    fields = mycursor.column_names
    qry = "UPDATE Donor SET "
    for field in fields:
        if request.form[field] not in ['None','']:
            if field in ['User_ID','Organization_ID','Donor_ID']:
                qry = qry + "%s = %s , " %(field,request.form[field])
            else:
                qry = qry + " %s = \'%s\' , " %(field,request.form[field])
        else:
            qry = qry + "%s = NULL , " %(field)
    qry = qry[:-2]
    qry = qry + "WHERE Donor_ID = %s and organ_donated = \"%s\";" %(request.form['Donor_ID'],request.form['organ_donated'])
    print(qry)
    try:
        mycursor.execute(qry)
    except:
        print("update error")
    mydb.commit()
    qry2 = "select * from Patient WHERE Donor_ID = %s and organ_donated = \"%s\";" %(request.form['Donor_ID'],request.form['organ_donated'])
    mycursor.execute(qry2)
    res = mycursor.fetchone()
    print(res)
    print(qry2)
    return render_template("show_detail.html",res = res,fields=fields,not_found = False)

@app.route("/update_doctor_page",methods = ['POST','GET'])
def update_doctor_page():
    if not session.get('login'):
        return redirect( url_for('home') )
    qry_upd = "Select * from Doctor"
    mycursor.execute(qry_upd)
    fields_upd = mycursor.column_names
    upd_res=[None]*len(fields_upd)
    return render_template('update_doctor_page.html',fields = fields_upd,res = upd_res)

@app.route("/update_doctor_details",methods = ['GET','POST'])
def update_doctor_details():
    if not session.get('login'):
        return redirect( url_for('home') )
    mycursor.execute("SELECT * from Doctor")
    fields = mycursor.column_names
    qry = "UPDATE Doctor SET "
    for field in fields:
        if request.form[field] not in ['None','']:
            if field in ['Doctor_ID','Organization_ID']:
                qry = qry + "%s = %s , " %(field,request.form[field])
            else:
                qry = qry + " %s = \'%s\' , " %(field,request.form[field])
        else:
            qry = qry + "%s = NULL , " %(field)
    qry = qry[:-2]
    qry = qry + "WHERE Doctor_ID = %s;" %(request.form['Doctor_ID'])
    print(qry)
    try:
        mycursor.execute(qry)
    except:
        print("update error")
        return render_template('error_page.html')
    mydb.commit()
    qry2 = "select * from Doctor WHERE Doctor_ID = %s;" %(request.form['Doctor_ID'])
    mycursor.execute(qry2)
    res = mycursor.fetchone()
    return render_template("show_detail.html",res = res,fields=fields,not_found = False)

@app.route("/update_organization_page",methods = ['POST','GET'])
def update_organization_page():
    if not session.get('login'):
        return redirect( url_for('home') )
    qry_upd = "Select * from Organization"
    mycursor.execute(qry_upd)
    fields_upd = mycursor.column_names
    upd_res=[None]*len(fields_upd)
    return render_template('update_organization_page.html',fields = fields_upd,res = upd_res)

@app.route("/update_organization_details",methods = ['GET','POST'])
def update_organization_details():
    if not session.get('login'):
        return redirect( url_for('home') )
    mycursor.execute("SELECT * from Organization")
    fields = mycursor.column_names
    qry = "UPDATE Organization SET "
    for field in fields:
        if request.form[field] not in ['None','']:
            if field in ['Organization_ID','Government_approved']:
                qry = qry + "%s = %s , " %(field,request.form[field])
            else:
                qry = qry + " %s = \'%s\' , " %(field,request.form[field])
        else:
            qry = qry + "%s = NULL , " %(field)
    qry = qry[:-2]
    qry = qry + "WHERE Organization_ID = %s;" %(request.form['Organization_ID'])
    print(qry)
    try:
        mycursor.execute(qry)
    except:
        print("update error")
        return render_template('error_page.html')
    mydb.commit()
    qry2 = "select * from Organization WHERE Organization_ID = %s;" %(request.form['Organization_ID'])
    mycursor.execute(qry2)
    res = mycursor.fetchone()
    return render_template("show_detail.html",res = res,fields=fields,not_found = False)
# @app.route("/update_organization_head_page",methods = ['POST','GET'])
# def update_organization_head_page():
#     if not session.get('login'):
#         return redirect( url_for('home') )
#     qry_upd = "Select * from Organization_head"
#     mycursor.execute(qry_upd)
#     fields_upd = mycursor.column_names
#     upd_res=[None]*len(fields_upd)
#     return render_template('update_organization_head_page.html',fields = fields_upd,res = upd_res)
# @app.route("/update_organization_head_details",methods = ['GET','POST'])
# def update_organization_head_details():
#     if not session.get('login'):
#         return redirect( url_for('home') )
#     mycursor.execute("SELECT * from Organization_head")
#     fields = mycursor.column_names
#     qry = "UPDATE Organization_head SET "
#     for field in fields:
#         if request.form[field] not in ['None','']:
#             if field in ['Organization_ID','Employee_ID','Term_length']:
#                 qry = qry + "%s = %s , " %(field,request.form[field])
#             else:
#                 qry = qry + " %s = \'%s\' , " %(field,request.form[field])
#         else:
#             qry = qry + "%s = NULL , " %(field)
#     qry = qry[:-2]
#     qry = qry + "WHERE Organization_ID = %s and Employee_ID = %s;" %(request.form['Organization_ID'],request.form['Employee_ID'])
#     print(qry)
#     try:
#         mycursor.execute(qry)
#     except:
#         return render_template('error_page.html',qry=qry)
#     mydb.commit()
#     qry2 = "select * from Organization WHERE Organization_ID = %s and Employee_ID = %s;" %(request.form['Organization_ID'],request.form['Employee_ID'])
#     mycursor.execute(qry2)
#     res = mycursor.fetchone()
#     return render_template("show_detail.html",res = res,fields=fields,not_found = False)

#----------------------------Logout-----------------------------------------
@app.route("/logout", methods=['POST','GET'])
def logout():
    session['login'] = False
    session['isAdmin'] = False
    return redirect("/login")

#-----------------------Searching Information------------------------------

@app.route("/search_User_details",methods=['GET','POST'])
def search_User_details():
    if not session.get('login'):
        return redirect( url_for('home') )
    qry = "SELECT * from User"
    mycursor.execute(qry)
    fields = mycursor.column_names
    res = mycursor.fetchall()

    return render_template('/search_and_show_list.html',res=res,fields=fields)

@app.route("/search_Patient_details",methods=['GET','POST'])
def search_Patient_details():
    if not session.get('login'):
        return redirect( url_for('home') )
    qry = "SELECT * from Patient"
    mycursor.execute(qry)
    fields = mycursor.column_names
    res = mycursor.fetchall()

    return render_template('/search_and_show_list.html',res=res,fields=fields)

@app.route("/search_Donor_details",methods=['GET','POST'])
def search_Donor_details():
    if not session.get('login'):
        return redirect( url_for('home') )
    qry = "SELECT * from Donor"
    mycursor.execute(qry)
    fields = mycursor.column_names
    res = mycursor.fetchall()

    return render_template('/search_and_show_list.html',res=res,fields=fields)

@app.route("/search_Organ_details",methods=['GET','POST'])
def search_Organ_details():
    if not session.get('login'):
        return redirect( url_for('home') )
    qry = "SELECT * from Organ_available"
    mycursor.execute(qry)
    fields = mycursor.column_names
    res = mycursor.fetchall()

    return render_template('/search_and_show_list.html',res=res,fields=fields)

@app.route("/search_Organization_details",methods=['GET','POST'])
def search_Organization_details():
    if not session.get('login'):
        return redirect( url_for('home') )
    qry = "SELECT * from Organization"
    mycursor.execute(qry)
    fields = mycursor.column_names
    res = mycursor.fetchall()

    return render_template('/search_and_show_list.html',res=res,fields=fields)

@app.route("/search_Organization_head_details",methods=['GET','POST'])
def search_Organization_head_details():
    if not session.get('login'):
        return redirect( url_for('home') )
    qry = "SELECT * from Organization_head"
    mycursor.execute(qry)
    fields = mycursor.column_names
    res = mycursor.fetchall()

    return render_template('/search_and_show_list.html',res=res,fields=fields)

@app.route("/search_Doctor_details",methods=['GET','POST'])
def search_Doctor_details():
    if not session.get('login'):
        return redirect( url_for('home') )
    qry = "SELECT * from Doctor"
    mycursor.execute(qry)
    fields = mycursor.column_names
    res = mycursor.fetchall()

    return render_template('/search_and_show_list.html',res=res,fields=fields)

@app.route("/search_Transaction",methods=['GET','POST'])
def search_Transaction_details():
    if not session.get('login'):
        return redirect( url_for('home') )
    qry = "SELECT * from Transaction"
    mycursor.execute(qry)
    fields = mycursor.column_names
    res = mycursor.fetchall()
    return render_template('/search_and_show_list.html',res=res,fields=fields)

@app.route("/search_log",methods=['GET','POST'])
def search_log_details():
    if not session.get('login'):
        return redirect( url_for('home') )
    qry = "SELECT * from log"
    mycursor.execute(qry)
    fields = mycursor.column_names
    res = mycursor.fetchall()
    return render_template('/search_and_show_list.html',res=res,fields=fields)

#---------------------Remove Pages--------------------------------------

@app.route('/remove_user',methods=['GET','POST'])
def remove_user():
    if not session.get('login'):
        return redirect( url_for('home') )
    return render_template('/remove_user.html')

@app.route('/remove_patient',methods=['GET','POST'])
def remove_hostel():
    if not session.get('login'):
        return redirect( url_for('home') )
    return render_template('/remove_patient.html')

@app.route('/remove_donor',methods=['GET','POST'])
def remove_room():
    if not session.get('login'):
        return redirect( url_for('home') )
    return render_template('/remove_donor.html')

@app.route('/remove_doctor',methods=['GET','POST'])
def remove_doctor():
    if not session.get('login'):
        return redirect( url_for('home') )
    return render_template('/remove_doctor.html')

@app.route('/remove_organization',methods=['GET','POST'])
def remove_organization():
    if not session.get('login'):
        return redirect( url_for('home') )
    return render_template('/remove_organization.html')

@app.route('/remove_organization_head',methods=['GET','POST'])
def remove_organization_head():
    if not session.get('login'):
        return redirect( url_for('home') )
    return render_template('/remove_organization_head.html')


#----------------Actual Deletion from database------------------------

@app.route('/del_user',methods=['GET','POST'])
def del_hostel():
    if not session.get('login'):
        return redirect( url_for('home') )
    qry = "delete from User where User_ID="+str(request.form['User_ID'])
    print(qry)
    try:
        mycursor.execute(qry)
    except:
        print("Error in deletion")
    mydb.commit()
    return redirect( url_for('home') )

@app.route('/del_patient',methods=['GET','POST'])
def del_patient():
    if not session.get('login'):
        return redirect( url_for('home') )
    qry = "delete from Patient where Patient_ID="+str(request.form['Patient_ID'])+" and organ_req=\'%s\'"%(request.form['organ_req'])
    print(qry)
    try:
        mycursor.execute(qry)
    except:
        print("Error in deletion")
    mydb.commit()
    return redirect( url_for('home') )

@app.route('/del_donor',methods=['GET','POST'])
def del_donor():
    if not session.get('login'):
        return redirect( url_for('home') )
    qry = "delete from Donor where Donor_ID="+str(request.form['Donor_ID'])+" and organ_donated=\'%s\'" %request.form['organ_donated']
    try:
        mycursor.execute(qry)
    except:
        print("Error in deletion")
    mydb.commit()
    return redirect( url_for('home') )


@app.route('/del_doctor',methods=['GET','POST'])
def del_doctor():
    if not session.get('login'):
        return redirect( url_for('home') )
    qry = "delete from Doctor where Doctor_ID="+str(request.form['Doctor_ID'])
    try:
        mycursor.execute(qry)
    except:
        print("Error in deletion")
    mydb.commit()
    return redirect( url_for('home') )


@app.route('/del_organization',methods=['GET','POST'])
def del_organization():
    if not session.get('login'):
        return redirect( url_for('home') )
    qry = "delete from Organization where Organization_ID="+str(request.form['Organization_ID'])
    try:
        mycursor.execute(qry)
    except:
        print("Error in deletion")
    mydb.commit()
    return redirect( url_for('home') )


@app.route('/del_organization_head',methods=['GET','POST'])
def del_organization_head():
    if not session.get('login'):
        return redirect( url_for('home') )
    qry = "delete from Organization_head where Organization_ID="+str(request.form['Organization_ID'])+" and Employee_ID="+str(request.form['Employee_ID'])
    try:
        mycursor.execute(qry)
    except:
        print("Error in deletion")
    mydb.commit()
    return redirect( url_for('home') )
#------------------------------------------------------------------------

@app.route('/contact_admin_page',methods=['GET','POST'])
def contact_admin_page():
    print(session.get('isAdmin'))
    if not session.get('login') or session.get('isAdmin'):
        return redirect( url_for('home') )
    return render_template('contact_admin_page.html')

@app.route('/contact_admin',methods=['GET','POST'])
def contact_admin():
    if not session.get('login') or session.get('isAdmin'):
        return redirect( url_for('home') )
    username = session.get('username')
    message = request.form['message']

    qry = "insert into Messages (username,message) values (\'"+username+"\',\'"+message+"\')"

    success = True
    error = False
    try:
        mycursor.execute(qry)
    except:
        print("Error")
        error = True
        success = False
    mydb.commit()

    return render_template('contact_admin_page.html',error=error,success=success)


@app.route('/see_messages',methods=['GET','POST'])
def see_messages():
    if not session.get('login') or not session.get('isAdmin'):
        return redirect( url_for('home') )

    qry = "Select * from Messages"
    mycursor.execute(qry)
    msg = mycursor.fetchall()

    return render_template('see_messages.html',msg=msg)

@app.route('/seen_message',methods=['GET','POST'])
def seen_message():
    if not session.get('login') or not session.get('isAdmin'):
        return redirect( url_for('home') )

    print(request.form['id'])

    msg_id = request.form['id']

    qry = "delete from Messages where message_id=\'"+msg_id+"\'"
    mycursor.execute(qry)
    mydb.commit()

    return redirect(url_for('see_messages'))

@app.route('/statistics', methods=['GET','POST'])
def stats():
    if not session.get('login') or not session.get('isAdmin'):
        return redirect( url_for('home') )
    qry = "select organ_donated, count(Donor_ID) from Donor group by organ_donated"
    mycursor.execute(qry)
    stats_donor = mycursor.fetchall()
    A = []
    B = []
    for organ in stats_donor:
        A.append(organ[0])
        B.append(organ[1])
    plt.pie(B, labels = A)
    plt.savefig('./static/donor_stat.png')
    # plt.show()
    plt.close()
    A.clear()
    B.clear()
    qry = "select organ_req, count(Patient_Id) from Patient group by organ_req"
    mycursor.execute(qry)
    stats_patient = mycursor.fetchall()
    A = []
    B = []
    for Patient in stats_patient:
        A.append(Patient[0])
        B.append(Patient[1])
    plt.pie(B, labels = A)
    plt.savefig('./static/Patient_stat.jpeg')
    # plt.show()
    plt.close()
    qry = "select distinct Organ_donated from Transaction inner join Donor on Transaction.Donor_ID = Donor.Donor_ID"
    mycursor.execute(qry)
    list = mycursor.fetchall()
    organ_list = []
    for organ in list:
        print(organ)
        organ_list.append(organ[0])
    print(organ)
    A.clear()
    B.clear()
    for organ in organ_list:
        qry = "select count(*) from Transaction inner join Donor on Donor.Donor_ID = Transaction.Donor_ID where Organ_donated = '%s' and Status = 1" %organ
        print(qry)
        mycursor.execute(qry)
        a = mycursor.fetchone()
        A.append(a[0])
        qry = "select count(*) from Transaction inner join Donor on Donor.Donor_ID = Transaction.Donor_ID where Organ_donated = '%s' and Status = 0" %organ
        print(qry)
        mycursor.execute(qry)
        b = mycursor.fetchone()
        B.append(b[0])
    print(A)
    print(B)
    print(organ_list)
    N = len(organ_list)
    fig, ax = plt.subplots()
    ind = np.arange(N)
    width = 0.05
    plt.bar(ind, A, width, label='SUCCESS')
    plt.bar(ind + width, B, width,label='FAILURE')
    plt.ylabel('Number of transplantation')
    plt.xlabel('Organ')
    plt.title('SUCCESS V/S FAILURE IN ORGAN TRANSPLANTATION')
    plt.xticks(ind + width / 2, organ_list)
    plt.legend(loc='best')
    plt.savefig('./static/success.jpeg')
    return render_template('statistics.html')

#-----------------------User Dashboard and Pages------------------------------

@app.route('/user/dashboard', methods=['GET'])
def user_dashboard():
    if not session.get('login'):
        return redirect(url_for('home'))
    
    username = session.get('username')
    
    # Get User_ID from login table based on username
    qry_login = "SELECT User_ID FROM login WHERE username = '%s'" % username
    mycursor.execute(qry_login)
    login_result = mycursor.fetchone()
    
    patient_count = 0
    donor_count = 0
    transaction_count = 0
    organs_available = 0
    
    if login_result and login_result[0]:
        user_id = login_result[0]
        
        # Count patient records for THIS specific user
        qry_patient = "SELECT COUNT(*) FROM Patient WHERE User_ID = %s" % user_id
        mycursor.execute(qry_patient)
        patient_count = mycursor.fetchone()[0] if mycursor.rowcount > 0 else 0
        
        # Count donor records for THIS specific user
        qry_donor = "SELECT COUNT(*) FROM Donor WHERE User_ID = %s" % user_id
        mycursor.execute(qry_donor)
        donor_count = mycursor.fetchone()[0] if mycursor.rowcount > 0 else 0
        
        # Count transactions involving THIS user (as patient or donor)
        qry_trans = """
            SELECT COUNT(DISTINCT t.Patient_ID, t.Donor_ID, t.Organ_ID) 
            FROM `Transaction` t
            LEFT JOIN Patient p ON t.Patient_ID = p.Patient_ID
            LEFT JOIN Donor d ON t.Donor_ID = d.Donor_ID
            WHERE p.User_ID = %s OR d.User_ID = %s
        """ % (user_id, user_id)
        mycursor.execute(qry_trans)
        transaction_count = mycursor.fetchone()[0] if mycursor.rowcount > 0 else 0
    
    # Count ALL available organs (not user-specific)
    qry_organs = "SELECT COUNT(*) FROM Organ_available"
    mycursor.execute(qry_organs)
    organs_available = mycursor.fetchone()[0] if mycursor.rowcount > 0 else 0
    
    return render_template('user_dashboard.html', 
                         username=username,
                         patient_count=patient_count,
                         donor_count=donor_count,
                         transaction_count=transaction_count,
                         organs_available=organs_available)

@app.route('/user/profile', methods=['GET'])
def user_profile():
    if not session.get('login'):
        return redirect(url_for('home'))
    
    username = session.get('username')
    
    # Get User_ID from login table based on username
    qry_login = "SELECT User_ID FROM login WHERE username = '%s'" % username
    mycursor.execute(qry_login)
    login_result = mycursor.fetchone()
    
    user_data = None
    phone_numbers = []
    
    if login_result and login_result[0]:
        user_id = login_result[0]
        
        # Get user data for this specific user
        qry = "SELECT * FROM User WHERE User_ID = %s" % user_id
        mycursor.execute(qry)
        user_data = mycursor.fetchone()
        
        # Get phone numbers for this user
        qry_phone = "SELECT Phone_no FROM User_phone_no WHERE User_ID = %s" % user_id
        mycursor.execute(qry_phone)
        phone_numbers = mycursor.fetchall()
    
    return render_template('user_profile.html', 
                         username=username,
                         user_data=user_data,
                         phone_numbers=phone_numbers)

@app.route('/user/request_organ', methods=['GET'])
def user_request_organ():
    if not session.get('login'):
        return redirect(url_for('home'))
    
    username = session.get('username')
    
    # Get User_ID from login table
    qry_login = "SELECT User_ID FROM login WHERE username = '%s'" % username
    mycursor.execute(qry_login)
    login_result = mycursor.fetchone()
    
    my_requests = []
    available_organs = []
    
    if login_result and login_result[0]:
        user_id = login_result[0]
        
        # Get THIS user's organ requests
        qry_requests = """
            SELECT p.Patient_ID, p.organ_req, p.reason_of_procurement, 
                   d.Doctor_Name, d.Department_Name, o.Organization_name
            FROM Patient p
            INNER JOIN Doctor d ON p.Doctor_ID = d.Doctor_ID
            INNER JOIN Organization o ON d.Organization_ID = o.Organization_ID
            WHERE p.User_ID = %s
        """ % user_id
        mycursor.execute(qry_requests)
        my_requests = mycursor.fetchall()
    
    # Get all available organs (global)
    qry_organs = """
        SELECT oa.Organ_ID, oa.Organ_name, oa.Donor_ID, 
               u.Name as donor_name, org.Organization_name
        FROM Organ_available oa
        INNER JOIN Donor d ON oa.Donor_ID = d.Donor_ID
        INNER JOIN User u ON d.User_ID = u.User_ID
        INNER JOIN Organization org ON d.Organization_ID = org.Organization_ID
    """
    mycursor.execute(qry_organs)
    available_organs = mycursor.fetchall()
    
    return render_template('user_request_organ.html',
                         username=username,
                         my_requests=my_requests,
                         available_organs=available_organs,
                         success=request.args.get('success'),
                         error=request.args.get('error'))

@app.route('/user/submit_organ_request', methods=['POST'])
def submit_organ_request():
    if not session.get('login'):
        return redirect(url_for('home'))
    
    try:
        username = session.get('username')
        
        # Get User_ID from login table
        qry_login = "SELECT User_ID FROM login WHERE username = '%s'" % username
        mycursor.execute(qry_login)
        login_result = mycursor.fetchone()
        
        if not login_result or not login_result[0]:
            return redirect(url_for('user_request_organ', error=True))
        
        user_id = login_result[0]
        patient_id = request.form['patient_id']
        organ_req = request.form['organ_req']
        reason = request.form['reason']
        doctor_id = request.form['doctor_id']
        
        qry = "INSERT INTO Patient (Patient_ID, organ_req, reason_of_procurement, Doctor_ID, User_ID) VALUES (%s, '%s', '%s', %s, %s)" % (patient_id, organ_req, reason, doctor_id, user_id)
        mycursor.execute(qry)
        mydb.commit()
        
        return redirect(url_for('user_request_organ', success=True))
    except Exception as e:
        print("Error submitting organ request:", e)
        return redirect(url_for('user_request_organ', error=True))

@app.route('/user/donate_organ', methods=['GET'])
def user_donate_organ():
    if not session.get('login'):
        return redirect(url_for('home'))
    
    username = session.get('username')
    
    # Get User_ID from login table
    qry_login = "SELECT User_ID FROM login WHERE username = '%s'" % username
    mycursor.execute(qry_login)
    login_result = mycursor.fetchone()
    
    my_donations = []
    organizations = []
    
    if login_result and login_result[0]:
        user_id = login_result[0]
        
        # Get THIS user's donation history
        qry_donations = """
            SELECT d.Donor_ID, d.organ_donated, d.reason_of_donation, 
                   o.Organization_name, o.Location, o.Government_approved
            FROM Donor d
            INNER JOIN Organization o ON d.Organization_ID = o.Organization_ID
            WHERE d.User_ID = %s
        """ % user_id
        mycursor.execute(qry_donations)
        my_donations = mycursor.fetchall()
    
    # Fetch all organizations for dropdown
    qry_orgs = "SELECT Organization_ID, Organization_name FROM Organization ORDER BY Organization_name"
    mycursor.execute(qry_orgs)
    organizations = mycursor.fetchall()
    
    return render_template('user_donate_organ.html',
                         username=username,
                         my_donations=my_donations,
                         organizations=organizations,
                         success=request.args.get('success'),
                         error=request.args.get('error'))

@app.route('/user/submit_organ_donation', methods=['POST'])
def submit_organ_donation():
    if not session.get('login'):
        return redirect(url_for('home'))
    
    try:
        username = session.get('username')
        
        # Get User_ID from login table
        qry_login = "SELECT User_ID FROM login WHERE username = '%s'" % username
        mycursor.execute(qry_login)
        login_result = mycursor.fetchone()
        
        if not login_result or not login_result[0]:
            return redirect(url_for('user_donate_organ', error=True))
        
        user_id = login_result[0]
        
        # Auto-generate Donor ID (get max ID and increment)
        qry_max_id = "SELECT IFNULL(MAX(Donor_ID), 200) + 1 FROM Donor"
        mycursor.execute(qry_max_id)
        donor_id = mycursor.fetchone()[0]
        
        organ_donated = request.form['organ_donated']
        reason = request.form['reason']
        organization_id = request.form['organization_id']
        
        # Insert into Donor table
        qry_donor = "INSERT INTO Donor (Donor_ID, organ_donated, reason_of_donation, Organization_ID, User_ID) VALUES (%s, '%s', '%s', %s, %s)" % (donor_id, organ_donated, reason, organization_id, user_id)
        mycursor.execute(qry_donor)
        
        # Auto-generate Organ ID for Organ_available table
        qry_max_organ_id = "SELECT IFNULL(MAX(Organ_ID), 300) + 1 FROM Organ_available"
        mycursor.execute(qry_max_organ_id)
        organ_id = mycursor.fetchone()[0]
        
        # Insert into Organ_available table (this makes the organ visible in matching system)
        qry_organ = "INSERT INTO Organ_available (Organ_ID, Organ_name, Donor_ID) VALUES (%s, '%s', %s)" % (organ_id, organ_donated, donor_id)
        mycursor.execute(qry_organ)
        
        mydb.commit()
        
        return redirect(url_for('user_donate_organ', success=True))
    except Exception as e:
        print("Error submitting organ donation:", e)
        return redirect(url_for('user_donate_organ', error=True))

@app.route('/user/transaction_history', methods=['GET'])
def user_transaction_history():
    if not session.get('login'):
        return redirect(url_for('home'))
    
    username = session.get('username')
    
    # Get User_ID from login table
    qry_login = "SELECT User_ID FROM login WHERE username = '%s'" % username
    mycursor.execute(qry_login)
    login_result = mycursor.fetchone()
    
    transactions = []
    total_transactions = 0
    successful_transactions = 0
    failed_transactions = 0
    
    if login_result and login_result[0]:
        user_id = login_result[0]
        
        # Get transactions involving THIS user (as patient or donor)
        qry_trans = """
            SELECT DISTINCT 
                t.Patient_ID, 
                t.Organ_ID, 
                t.Donor_ID, 
                t.Date_of_transaction, 
                t.Status,
                oa.Organ_name,
                pu.Name as patient_name,
                du.Name as donor_name,
                pu.Date_of_Birth as patient_dob,
                du.Date_of_Birth as donor_dob,
                pu.Medical_insurance as patient_insurance,
                du.Medical_insurance as donor_insurance,
                pu.City as patient_city,
                du.City as donor_city,
                p.reason_of_procurement,
                d.reason_of_donation,
                doc.Doctor_Name,
                org.Organization_name,
                du.Street as donor_street,
                du.State as donor_state,
                (SELECT GROUP_CONCAT(Phone_no SEPARATOR ', ') 
                 FROM User_phone_no 
                 WHERE User_ID = du.User_ID) as donor_phones,
                pu.Street as patient_street,
                pu.State as patient_state,
                (SELECT GROUP_CONCAT(Phone_no SEPARATOR ', ') 
                 FROM User_phone_no 
                 WHERE User_ID = pu.User_ID) as patient_phones,
                p.User_ID as patient_user_id,
                d.User_ID as donor_user_id
            FROM `Transaction` t
            LEFT JOIN Patient p ON t.Patient_ID = p.Patient_ID
            LEFT JOIN Donor d ON t.Donor_ID = d.Donor_ID
            LEFT JOIN User pu ON p.User_ID = pu.User_ID
            LEFT JOIN User du ON d.User_ID = du.User_ID
            LEFT JOIN Organ_available oa ON t.Organ_ID = oa.Organ_ID
            LEFT JOIN Doctor doc ON p.Doctor_ID = doc.Doctor_ID
            LEFT JOIN Organization org ON d.Organization_ID = org.Organization_ID
            WHERE p.User_ID = %s OR d.User_ID = %s
            ORDER BY t.Date_of_transaction DESC
        """ % (user_id, user_id)
        mycursor.execute(qry_trans)
        transactions = mycursor.fetchall()
        
        # Calculate stats
        total_transactions = len(transactions) if transactions else 0
        successful_transactions = sum(1 for t in transactions if t[4] == 1) if transactions else 0
        pending_transactions = sum(1 for t in transactions if t[4] == 0) if transactions else 0
        failed_transactions = sum(1 for t in transactions if t[4] == 2) if transactions else 0
    
    return render_template('user_transaction_history.html',
                         username=username,
                         current_user_id=user_id if login_result and login_result[0] else None,
                         transactions=transactions,
                         total_transactions=total_transactions,
                         successful_transactions=successful_transactions,
                         pending_transactions=pending_transactions,
                         failed_transactions=failed_transactions)

@app.route('/user/find_matches', methods=['GET'])
def find_matches():
    """
    Smart Organ Matching Algorithm
    
    This algorithm matches patients who need organs with available donors based on:
    1. Organ type compatibility (exact match required)
    2. Organ availability (not already allocated)
    3. Organization network (same or affiliated organizations get priority)
    4. Medical compatibility factors
    
    Matching Score Calculation:
    - Base score: 60 points for organ type match
    - +20 points if same organization
    - +10 points for living donation (fresher organs)
    - +10 points if patient has medical insurance
    
    Returns: List of compatible matches sorted by compatibility score
    """
    if not session.get('login'):
        return redirect(url_for('home'))
    
    # Step 1: Get all active patient requests
    qry_patients = """
        SELECT 
            p.Patient_ID,
            p.organ_req,
            p.reason_of_procurement,
            u.Name as patient_name,
            u.Medical_insurance,
            d.Doctor_Name,
            d.Organization_ID as patient_org_id
        FROM Patient p
        INNER JOIN User u ON p.User_ID = u.User_ID
        INNER JOIN Doctor d ON p.Doctor_ID = d.Doctor_ID
    """
    mycursor.execute(qry_patients)
    patients = mycursor.fetchall()
    print(f"DEBUG: Found {len(patients)} patients")
    
    # Step 2: Get all available organs with donor info
    qry_available = """
        SELECT 
            oa.Organ_ID,
            oa.Organ_name,
            oa.Donor_ID,
            don.organ_donated,
            don.reason_of_donation,
            don.Organization_ID as donor_org_id,
            u.Name as donor_name,
            org.Organization_name
        FROM Organ_available oa
        INNER JOIN Donor don ON oa.Donor_ID = don.Donor_ID
        INNER JOIN User u ON don.User_ID = u.User_ID
        INNER JOIN Organization org ON don.Organization_ID = org.Organization_ID
        WHERE oa.Organ_ID NOT IN (
            SELECT Organ_ID FROM `Transaction` WHERE Status IN (0, 1)
        )
    """
    mycursor.execute(qry_available)
    available_organs = mycursor.fetchall()
    print(f"DEBUG: Found {len(available_organs)} available organs")
    
    # Step 3: Match patients with compatible donors
    matches = []
    
    for patient in patients:
        patient_id = patient[0]
        organ_needed = patient[1]
        patient_name = patient[3]
        has_insurance = patient[4]
        doctor_name = patient[5]
        patient_org_id = patient[6]
        
        for organ in available_organs:
            organ_id = organ[0]
            organ_type = organ[1]
            donor_id = organ[2]
            organ_donated = organ[3]
            donation_reason = organ[4]
            donor_org_id = organ[5]
            donor_name = organ[6]
            organization_name = organ[7]
            
            # MATCHING CRITERIA
            # Check if organ types match
            if organ_needed.lower() == organ_type.lower():
                # Initialize compatibility score
                compatibility_score = 60  # Base score for organ match
                
                # Bonus: Same organization (better logistics, faster transport)
                if patient_org_id == donor_org_id:
                    compatibility_score += 20
                
                # Bonus: Living donation (better organ quality)
                if donation_reason and 'living' in donation_reason.lower():
                    compatibility_score += 10
                
                # Bonus: Patient has medical insurance (better post-op care)
                if has_insurance == 1:
                    compatibility_score += 10
                
                # Create match record
                match = {
                    'patient_id': patient_id,
                    'patient_name': patient_name,
                    'organ_type': organ_type,
                    'donor_id': donor_id,
                    'donor_name': donor_name,
                    'organ_id': organ_id,
                    'organization': organization_name,
                    'compatibility_score': min(compatibility_score, 100),  # Cap at 100%
                    'doctor': doctor_name,
                    'donation_type': donation_reason
                }
                
                matches.append(match)
    
    # Step 4: Sort matches by compatibility score (highest first)
    matches.sort(key=lambda x: x['compatibility_score'], reverse=True)
    
    # Step 5: Get statistics
    total_requests = len(patients)
    total_donors = len(set(organ[2] for organ in available_organs))  # Unique donors
    available_organs_count = len(available_organs)
    total_matches = len(matches)
    
    return render_template('user_find_matches.html',
                         username=session.get('username'),
                         matches=matches,
                         total_matches=total_matches,
                         total_requests=total_requests,
                         total_donors=total_donors,
                         available_organs_count=available_organs_count)

@app.route('/user/register_patient', methods=['GET'])
def register_patient():
    """Display patient registration form"""
    if not session.get('login'):
        return redirect(url_for('home'))
    
    username = session.get('username')
    
    # Check if user is already registered as a patient
    qry_login = "SELECT User_ID FROM login WHERE username = '%s'" % username
    mycursor.execute(qry_login)
    login_result = mycursor.fetchone()
    
    already_registered = False
    doctors = []
    
    if login_result and login_result[0]:
        user_id = login_result[0]
        qry_check = "SELECT COUNT(*) FROM Patient WHERE User_ID = %s" % user_id
        mycursor.execute(qry_check)
        count = mycursor.fetchone()[0]
        already_registered = count > 0
    
    # Fetch all doctors with their hospital names
    qry_doctors = """
        SELECT d.Doctor_ID, d.Doctor_Name, o.Organization_name
        FROM Doctor d
        LEFT JOIN Organization o ON d.Organization_ID = o.Organization_ID
        ORDER BY d.Doctor_Name
    """
    mycursor.execute(qry_doctors)
    doctors = mycursor.fetchall()
    
    return render_template('user_register_patient.html',
                         username=username,
                         already_registered=already_registered,
                         doctors=doctors,
                         success=request.args.get('success'),
                         error=request.args.get('error'),
                         error_message=request.args.get('error_message'))

@app.route('/user/submit_patient_registration', methods=['POST'])
def submit_patient_registration():
    """Handle patient registration form submission"""
    if not session.get('login'):
        return redirect(url_for('home'))
    
    try:
        username = session.get('username')
        
        # Get User_ID from login table
        qry_login = "SELECT User_ID FROM login WHERE username = '%s'" % username
        mycursor.execute(qry_login)
        login_result = mycursor.fetchone()
        
        if not login_result or not login_result[0]:
            return redirect(url_for('register_patient', error=True, error_message='User not found'))
        
        user_id = login_result[0]
        
        # Auto-generate Patient ID (get max ID and increment)
        qry_max_id = "SELECT IFNULL(MAX(Patient_ID), 100) + 1 FROM Patient"
        mycursor.execute(qry_max_id)
        patient_id = mycursor.fetchone()[0]
        
        # Get form data
        organ_req = request.form['organ_req']
        reason = request.form['reason']
        doctor_id = request.form['doctor_id']
        
        # Insert patient record
        qry = """INSERT INTO Patient (Patient_ID, organ_req, reason_of_procurement, Doctor_ID, User_ID) 
                 VALUES (%s, '%s', '%s', %s, %s)""" % (patient_id, organ_req, reason, doctor_id, user_id)
        mycursor.execute(qry)
        mydb.commit()
        
        # Redirect to smart organ request page
        return redirect(url_for('request_organ_smart'))
        
    except Exception as e:
        print("Error registering patient:", e)
        return redirect(url_for('register_patient', error=True, error_message=str(e)))

@app.route('/user/edit_patient', methods=['GET'])
def edit_patient():
    """Display edit patient form"""
    if not session.get('login'):
        return redirect(url_for('home'))
    
    username = session.get('username')
    
    # Get User_ID from login table
    qry_login = "SELECT User_ID FROM login WHERE username = '%s'" % username
    mycursor.execute(qry_login)
    login_result = mycursor.fetchone()
    
    patient_data = None
    doctors = []
    
    if login_result and login_result[0]:
        user_id = login_result[0]
        
        # Get patient data
        qry_patient = """
            SELECT p.Patient_ID, p.organ_req, p.reason_of_procurement, p.Doctor_ID,
                   d.Doctor_Name, o.Organization_name
            FROM Patient p
            LEFT JOIN Doctor d ON p.Doctor_ID = d.Doctor_ID
            LEFT JOIN Organization o ON d.Organization_ID = o.Organization_ID
            WHERE p.User_ID = %s
        """ % user_id
        mycursor.execute(qry_patient)
        patient_data = mycursor.fetchone()
        
        # Get all doctors for dropdown
        qry_doctors = "SELECT Doctor_ID, Doctor_Name FROM Doctor"
        mycursor.execute(qry_doctors)
        doctors = mycursor.fetchall()
    
    return render_template('user_edit_patient.html', 
                         username=username, 
                         patient_data=patient_data,
                         doctors=doctors,
                         error=request.args.get('error'),
                         error_message=request.args.get('error_message'))

@app.route('/user/update_patient', methods=['POST'])
def update_patient():
    """Handle patient details update"""
    if not session.get('login'):
        return redirect(url_for('home'))
    
    try:
        username = session.get('username')
        
        # Get User_ID from login table
        qry_login = "SELECT User_ID FROM login WHERE username = '%s'" % username
        mycursor.execute(qry_login)
        login_result = mycursor.fetchone()
        
        if not login_result or not login_result[0]:
            return redirect(url_for('edit_patient', error=True, error_message='User not found'))
        
        user_id = login_result[0]
        
        # Get form data
        patient_id = request.form['patient_id']
        organ_req = request.form['organ_req']
        reason = request.form['reason']
        doctor_id = request.form['doctor_id']
        
        # Update patient record
        qry = """UPDATE Patient 
                 SET organ_req = '%s', reason_of_procurement = '%s', Doctor_ID = %s
                 WHERE Patient_ID = %s AND User_ID = %s""" % (organ_req, reason, doctor_id, patient_id, user_id)
        mycursor.execute(qry)
        mydb.commit()
        
        # Redirect to dashboard with success message
        return redirect(url_for('user_dashboard'))
        
    except Exception as e:
        print("Error updating patient:", e)
        return redirect(url_for('edit_patient', error=True, error_message=str(e)))

@app.route('/user/unregister_patient', methods=['POST'])
def unregister_patient():
    """Unregister user as patient"""
    if not session.get('login'):
        return redirect(url_for('home'))
    
    try:
        username = session.get('username')
        
        # Get User_ID from login table
        qry_login = "SELECT User_ID FROM login WHERE username = '%s'" % username
        mycursor.execute(qry_login)
        login_result = mycursor.fetchone()
        
        if not login_result or not login_result[0]:
            return redirect(url_for('user_dashboard'))
        
        user_id = login_result[0]
        
        # Get patient ID
        qry_patient = "SELECT Patient_ID FROM Patient WHERE User_ID = %s" % user_id
        mycursor.execute(qry_patient)
        patient_result = mycursor.fetchone()
        
        if patient_result:
            patient_id = patient_result[0]
            
            # Check if patient has pending transactions
            qry_check = "SELECT COUNT(*) FROM `Transaction` WHERE Patient_ID = %s AND Status = 0" % patient_id
            mycursor.execute(qry_check)
            pending_count = mycursor.fetchone()[0]
            
            if pending_count > 0:
                return redirect(url_for('edit_patient', error=True, 
                              error_message='Cannot unregister: You have pending transactions'))
            
            # Delete patient record
            qry_delete = "DELETE FROM Patient WHERE Patient_ID = %s AND User_ID = %s" % (patient_id, user_id)
            mycursor.execute(qry_delete)
            mydb.commit()
        
        # Redirect to dashboard
        return redirect(url_for('user_dashboard'))
        
    except Exception as e:
        print("Error unregistering patient:", e)
        return redirect(url_for('edit_patient', error=True, error_message=str(e)))

@app.route('/user/request_organ_smart', methods=['GET'])
def request_organ_smart():
    """Smart organ request page with auto-fetched patient data and matching"""
    if not session.get('login'):
        return redirect(url_for('home'))
    
    username = session.get('username')
    
    # Get User_ID from login table
    qry_login = "SELECT User_ID FROM login WHERE username = '%s'" % username
    mycursor.execute(qry_login)
    login_result = mycursor.fetchone()
    
    patient_data = None
    matches = []
    available_donors = 0
    total_matches = 0
    all_patient_requests = []
    all_available_donors = []
    organ_catalog = []
    
    if login_result and login_result[0]:
        user_id = login_result[0]
        
        # Get patient data for this user
        qry_patient = """
            SELECT p.Patient_ID, p.organ_req, p.reason_of_procurement,
                   d.Doctor_Name, o.Organization_name
            FROM Patient p
            LEFT JOIN Doctor d ON p.Doctor_ID = d.Doctor_ID
            LEFT JOIN Organization o ON d.Organization_ID = o.Organization_ID
            WHERE p.User_ID = %s
            LIMIT 1
        """ % user_id
        mycursor.execute(qry_patient)
        patient_data = mycursor.fetchone()
        
        # Get ALL patient requests in the network
        qry_all_patients = """
            SELECT 
                p.Patient_ID,
                p.organ_req,
                p.reason_of_procurement,
                u.Name as patient_name,
                u.Medical_insurance,
                d.Doctor_Name,
                o.Organization_name
            FROM Patient p
            INNER JOIN User u ON p.User_ID = u.User_ID
            INNER JOIN Doctor d ON p.Doctor_ID = d.Doctor_ID
            INNER JOIN Organization o ON d.Organization_ID = o.Organization_ID
            ORDER BY p.Patient_ID
        """
        mycursor.execute(qry_all_patients)
        all_patient_requests = mycursor.fetchall()
        
        # Get ALL available donors in the network
        qry_all_donors = """
            SELECT 
                oa.Organ_ID,
                oa.Organ_name,
                oa.Donor_ID,
                don.organ_donated,
                don.reason_of_donation,
                don.Organization_ID,
                u.Name as donor_name,
                org.Organization_name
            FROM Organ_available oa
            INNER JOIN Donor don ON oa.Donor_ID = don.Donor_ID
            INNER JOIN User u ON don.User_ID = u.User_ID
            INNER JOIN Organization org ON don.Organization_ID = org.Organization_ID
            WHERE oa.Organ_ID NOT IN (SELECT Organ_ID FROM `Transaction`)
            ORDER BY oa.Organ_name, oa.Organ_ID
        """
        mycursor.execute(qry_all_donors)
        all_available_donors = mycursor.fetchall()
        
        # Get organ catalog - all organ types that can be donated
        qry_organ_catalog = """
            SELECT 
                oa.Organ_name,
                COUNT(DISTINCT oa.Organ_ID) as total_available,
                COUNT(DISTINCT oa.Donor_ID) as total_donors,
                GROUP_CONCAT(DISTINCT org.Organization_name SEPARATOR ', ') as hospitals
            FROM Organ_available oa
            INNER JOIN Donor don ON oa.Donor_ID = don.Donor_ID
            INNER JOIN Organization org ON don.Organization_ID = org.Organization_ID
            WHERE oa.Organ_ID NOT IN (SELECT Organ_ID FROM `Transaction`)
            GROUP BY oa.Organ_name
            ORDER BY oa.Organ_name
        """
        mycursor.execute(qry_organ_catalog)
        organ_catalog = mycursor.fetchall()
        
        if patient_data:
            # Run matching algorithm for this patient's organ need
            organ_needed = patient_data[1]
            patient_id = patient_data[0]
            
            # Get patient's organization for scoring
            qry_pat_org = """
                SELECT d.Organization_ID
                FROM Patient p
                INNER JOIN Doctor d ON p.Doctor_ID = d.Doctor_ID
                WHERE p.Patient_ID = %s
            """ % patient_id
            mycursor.execute(qry_pat_org)
            pat_org_result = mycursor.fetchone()
            patient_org_id = pat_org_result[0] if pat_org_result else None
            
            # Get available organs matching the needed type
            qry_available = """
                SELECT 
                    oa.Organ_ID,
                    oa.Organ_name,
                    oa.Donor_ID,
                    don.organ_donated,
                    don.reason_of_donation,
                    don.Organization_ID as donor_org_id,
                    u.Name as donor_name,
                    org.Organization_name
                FROM Organ_available oa
                INNER JOIN Donor don ON oa.Donor_ID = don.Donor_ID
                INNER JOIN User u ON don.User_ID = u.User_ID
                INNER JOIN Organization org ON don.Organization_ID = org.Organization_ID
                WHERE oa.Organ_name = '%s'
                AND oa.Organ_ID NOT IN (SELECT Organ_ID FROM `Transaction`)
            """ % organ_needed
            mycursor.execute(qry_available)
            available_organs = mycursor.fetchall()
            
            available_donors = len(set(organ[2] for organ in available_organs))
            
            # Match and score each available organ
            for organ in available_organs:
                organ_id = organ[0]
                organ_type = organ[1]
                donor_id = organ[2]
                donation_reason = organ[4]
                donor_org_id = organ[5]
                donor_name = organ[6]
                organization_name = organ[7]
                
                # Calculate compatibility score
                compatibility_score = 60  # Base score for organ match
                
                # Bonus: Same organization
                if patient_org_id and donor_org_id == patient_org_id:
                    compatibility_score += 20
                
                # Bonus: Living donation
                if donation_reason and 'living' in donation_reason.lower():
                    compatibility_score += 10
                
                # Bonus: Patient has medical insurance
                qry_insurance = "SELECT Medical_insurance FROM User WHERE User_ID = %s" % user_id
                mycursor.execute(qry_insurance)
                insurance_result = mycursor.fetchone()
                if insurance_result and insurance_result[0] == 1:
                    compatibility_score += 10
                
                match = {
                    'organ_type': organ_type,
                    'donor_id': donor_id,
                    'donor_name': donor_name,
                    'organ_id': organ_id,
                    'organization': organization_name,
                    'compatibility_score': min(compatibility_score, 100),
                    'donation_type': donation_reason
                }
                
                matches.append(match)
            
            # Sort by compatibility score
            matches.sort(key=lambda x: x['compatibility_score'], reverse=True)
            total_matches = len(matches)
    
    return render_template('user_request_organ_smart.html',
                         username=username,
                         patient_data=patient_data,
                         matches=matches,
                         available_donors=available_donors,
                         total_matches=total_matches,
                         all_patient_requests=all_patient_requests,
                         all_available_donors=all_available_donors,
                         organ_catalog=organ_catalog)

@app.route('/user/initiate_transaction', methods=['POST'])
def initiate_transaction():
    """Create a transaction when user requests an organ"""
    if not session.get('login'):
        return redirect(url_for('home'))
    
    try:
        patient_id = request.form['patient_id']
        organ_id = request.form['organ_id']
        donor_id = request.form['donor_id']
        
        # Check if this transaction already exists
        qry_check = """SELECT COUNT(*) FROM `Transaction` 
                      WHERE Patient_ID = %s AND Organ_ID = %s AND Status = 0""" % (patient_id, organ_id)
        mycursor.execute(qry_check)
        existing = mycursor.fetchone()[0]
        
        if existing > 0:
            flash('You already have a pending request for this organ!', 'warning')
            return redirect(url_for('find_matches'))
        
        # Insert transaction with current date and pending status
        from datetime import datetime
        current_date = datetime.now().strftime('%Y-%m-%d')
        
        qry = """INSERT INTO `Transaction` (Patient_ID, Organ_ID, Donor_ID, Date_of_transaction, Status)
                 VALUES (%s, %s, %s, '%s', 0)""" % (patient_id, organ_id, donor_id, current_date)
        mycursor.execute(qry)
        mydb.commit()
        
        flash('Organ transplant request submitted successfully! Awaiting admin approval.', 'success')
        return redirect(url_for('user_transaction_history'))
        
    except Exception as e:
        print("Error creating transaction:", e)
        flash('Error submitting request. Please try again.', 'error')
        return redirect(url_for('find_matches'))
        return redirect(url_for('request_organ_smart'))

@app.route('/admin/pending_approvals', methods=['GET'])
def pending_approvals():
    """Admin page to view and approve/reject pending organ transplant requests"""
    if not session.get('login') or not session.get('isAdmin'):
        return redirect(url_for('home'))
    
    # Get all pending transactions (Status = 0)
    qry_pending = """
        SELECT 
            t.Patient_ID,
            t.Organ_ID,
            t.Donor_ID,
            t.Date_of_transaction,
            t.Status,
            pu.Name as patient_name,
            p.organ_req,
            p.reason_of_procurement,
            du.Name as donor_name,
            d.organ_donated,
            d.reason_of_donation,
            org.Organization_name,
            doc.Doctor_Name
        FROM `Transaction` t
        INNER JOIN Patient p ON t.Patient_ID = p.Patient_ID
        INNER JOIN User pu ON p.User_ID = pu.User_ID
        INNER JOIN Donor d ON t.Donor_ID = d.Donor_ID
        INNER JOIN User du ON d.User_ID = du.User_ID
        INNER JOIN Organization org ON d.Organization_ID = org.Organization_ID
        INNER JOIN Doctor doc ON p.Doctor_ID = doc.Doctor_ID
        WHERE t.Status = 0
        ORDER BY t.Date_of_transaction DESC
    """
    mycursor.execute(qry_pending)
    pending_requests = mycursor.fetchall()
    
    return render_template('admin_pending_approvals.html',
                         username=session.get('username'),
                         pending_requests=pending_requests)

@app.route('/admin/approve_transaction', methods=['POST'])
def approve_transaction():
    """Approve a pending organ transplant transaction"""
    if not session.get('login') or not session.get('isAdmin'):
        return redirect(url_for('home'))
    
    patient_id = request.form.get('patient_id')
    organ_id = request.form.get('organ_id')
    action = request.form.get('action')  # 'approve' or 'reject'
    
    if action == 'approve':
        # Update status to 1 (Approved)
        qry_update = """UPDATE `Transaction` SET Status = 1 
                       WHERE Patient_ID = %s AND Organ_ID = %s""" % (patient_id, organ_id)
    else:
        # Update status to 2 (Rejected)
        qry_update = """UPDATE `Transaction` SET Status = 2 
                       WHERE Patient_ID = %s AND Organ_ID = %s""" % (patient_id, organ_id)
    
    mycursor.execute(qry_update)
    mydb.commit()
    
    return redirect(url_for('pending_approvals'))

@app.route('/admin/all_transactions')
def admin_all_transactions():
    """View all transactions in the system (admin only)"""
    if not session.get('login') or not session.get('isAdmin'):
        return redirect(url_for('home'))
    
    # Get all transactions with full details
    qry_all_trans = """
        SELECT DISTINCT 
            t.Patient_ID, 
            t.Organ_ID, 
            t.Donor_ID, 
            t.Date_of_transaction, 
            t.Status,
            oa.Organ_name,
            pu.Name as patient_name,
            du.Name as donor_name,
            pu.Date_of_Birth as patient_dob,
            du.Date_of_Birth as donor_dob,
            pu.Medical_insurance as patient_insurance,
            du.Medical_insurance as donor_insurance,
            pu.City as patient_city,
            du.City as donor_city,
            p.reason_of_procurement,
            d.reason_of_donation,
            doc.Doctor_Name,
            org.Organization_name,
            du.Street as donor_street,
            du.State as donor_state,
            (SELECT GROUP_CONCAT(Phone_no SEPARATOR ', ') 
             FROM User_phone_no 
             WHERE User_ID = du.User_ID) as donor_phones,
            pu.Street as patient_street,
            pu.State as patient_state,
            (SELECT GROUP_CONCAT(Phone_no SEPARATOR ', ') 
             FROM User_phone_no 
             WHERE User_ID = pu.User_ID) as patient_phones
        FROM `Transaction` t
        LEFT JOIN Patient p ON t.Patient_ID = p.Patient_ID
        LEFT JOIN Donor d ON t.Donor_ID = d.Donor_ID
        LEFT JOIN User pu ON p.User_ID = pu.User_ID
        LEFT JOIN User du ON d.User_ID = du.User_ID
        LEFT JOIN Organ_available oa ON t.Organ_ID = oa.Organ_ID
        LEFT JOIN Doctor doc ON p.Doctor_ID = doc.Doctor_ID
        LEFT JOIN Organization org ON d.Organization_ID = org.Organization_ID
        ORDER BY t.Date_of_transaction DESC
    """
    mycursor.execute(qry_all_trans)
    transactions = mycursor.fetchall()
    
    # Calculate stats
    total_transactions = len(transactions) if transactions else 0
    approved_transactions = sum(1 for t in transactions if t[4] == 1) if transactions else 0
    pending_transactions = sum(1 for t in transactions if t[4] == 0) if transactions else 0
    rejected_transactions = sum(1 for t in transactions if t[4] == 2) if transactions else 0
    
    return render_template('admin_all_transactions.html',
                         username=session.get('username'),
                         transactions=transactions,
                         total_transactions=total_transactions,
                         approved_transactions=approved_transactions,
                         pending_transactions=pending_transactions,
                         rejected_transactions=rejected_transactions)

if __name__ == "__main__":
    # Get debug mode from environment (default: True for development)
    debug_mode = os.getenv('FLASK_DEBUG', 'True').lower() in ('true', '1', 'yes')
    
    app.run(debug=debug_mode)

