from flask import Flask,render_template,request,flash,redirect,url_for,session
from flask_mysqldb import MySQL
import mysql.connector,sys
import MySQLdb.cursors
import re
from functools import wraps

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4ytldQ8z/n\/ec]/'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'test_1'
app.config['MYSQL_PASSWORD'] = 'password_1'
app.config['MYSQL_DB'] = 'dbms_project'

mysql = MySQL(app)


# check if user is logged in 
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'loggedin' in session:
            return f(*args, **kwargs)
        else:
            flash('UNAUTHORIZED, PLEASE LOGIN', 'error')
            return redirect(url_for('login'))
    return wrap

def is_not_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'loggedin' not in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('home'))
    return wrap

######################################

@app.route('/')
@is_logged_in   
def index():
    return render_template('base.html', data = session)

@app.route('/home')
@is_logged_in  
def home():
    return render_template('base.html', data = session)



#####################################3

@app.route('/login', methods =['GET', 'POST'])
@is_not_logged_in
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT id,username,password FROM accounts WHERE username = % s AND password = % s', (username, password, ))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            return render_template('base.html', data = session)
        else:
            flash('Incorrect username / password !','error')
    return render_template('login.html', msg = msg)
  
@app.route('/logout')
@is_logged_in
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    flash('YOU ARE NOW LOGGED OUT', 'success')
    return redirect(url_for('login'))
  
##############################################################################
#insert
@app.route('/employee',methods=['GET','POST'])
@is_logged_in
def add_employee():
    msg = ''
    if request.method == 'POST' and 'user_name' in request.form and 'password' in request.form and 'user_email' in request.form :
        details = request.form
        username = details['user_name']
        email = details['user_email']
        password = details['password']
        empl_id = details['emp_id']
        name = details['name']
        contact_no = details['contact']
        dob = details['dob']
        join_date = details['joining_date']
        aadhar = details['aadhar_id']
        salary = details['salary']

        cur = mysql.connection.cursor()

        cur.execute('SELECT * FROM accounts WHERE username = % s', (username, ))
        account = cur.fetchone()
        if account:
            flash('Account already exists !','error')
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            flash('Invalid email address !','error')
        elif not re.match(r'[A-Za-z0-9]+', username):
            flash('Username must contain only characters and numbers !','error')
        elif not username or not password or not email:
            flash('Please fill out the form !','error')
        else:
            cur.execute('INSERT INTO accounts VALUES (NULL, % s, % s, % s)', (username, password, email, ))
            mysql.connection.commit()
        try:
            cur.execute("insert into employee(EMPLOYEE_ID,EMPLOYEE_NAME,CONTACT_NO,EMAIL_ID,JOINING_DATE,SALARY,AADHAR_ID,DOB) values (%s,%s,%s,%s,%s,%s,%s,%s)",[empl_id,name,contact_no,email,join_date,salary,aadhar,dob])
            mysql.connection.commit()
            flash('Employee added successfully!','success')
        except Exception as e:
            s = e
            flash(s,'error')
        cur.close()
    return render_template('employee.html', msg = msg)

@app.route('/volunteer',methods=['GET','POST'])
@is_logged_in
def add_volunteer():
    msg = ''
    if request.method == 'POST' and 'user_name' in request.form and 'password' in request.form and 'user_email' in request.form :
        details = request.form
        username = details['user_name']
        email = details['user_email']
        password = details['password']
        vol_id = details['vol_id']
        empl_id = details['emp_id'] 
        name = details['name']
        contact_no = details['contact']
        hours = details['no_of_hours']

        cur = mysql.connection.cursor()

        cur.execute('SELECT * FROM accounts WHERE username = % s', (username, ))
        account = cur.fetchone()
        if account:
            flash('Account already exists !','error')
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            flash('Invalid email address !','error')
        elif not re.match(r'[A-Za-z0-9]+', username):
            flash('Username must contain only characters and numbers !','error')
        elif not username or not password or not email:
            flash('Please fill out the form !','error')
        else:
            cur.execute('INSERT INTO accounts VALUES (NULL, % s, % s, % s)', (username, password, email, ))
            mysql.connection.commit()
        try:
            cur.execute("insert into volunteer(VOLUNTEER_ID,EMPLOYEE_ID,VOLUNTEER_NAME,CONTACT_NO,NO_OF_HRS) values (%s,%s,%s,%s,%s)",[vol_id,empl_id,name,contact_no,hours])
            mysql.connection.commit()
            flash('Employee added successfully!','success')

        except Exception as e:
            s = e
            flash(s,'error')
        cur.close()
    return render_template('volunteer.html', msg = msg)

@app.route('/donar',methods=['GET','POST'])
@is_logged_in
def add_donar():
    if request.method == "POST":
        details = request.form
        don_id = details['donar_id']
        empl_id = details['emp_id'] 
        name = details['name']
        address = details['street'] +', '+ details['city']
        aadhar = details['aadhar_id']
        contact_no = details['contact']
        
        cur = mysql.cursor()
        try:
            cur.execute("insert into donar(DONAR_ID,EMPLOYEE_ID,DONAR_NAME,AADHAR_ID,ADDRESS,CONTACT_NO) values (%s,%s,%s,%s,%s,%s)",[don_id,empl_id,name,aadhar,address,contact_no])
            mysql.commit()
            return 'success'
        except Exception as e:
            s = e
            flash(s,'error')
        cur.close()
    return render_template('donar.html')

@app.route('/donee',methods=['GET','POST'])
@is_logged_in   
def add_donee():
    if request.method == "POST":
        details = request.form
        vol_id = details['vol_id']
        donee_id = details['donee_id'] 
        name = details['name']
        contact_no = details['contact']
        aadhar = details['aadhar_id']

        cur = mysql.cursor()
        try:
            cur.execute("insert into donee(VOLUNTEER_ID,DONEE_ID,DONEE_NAME,CONTACT_NO,AADHAR_ID) values (%s,%s,%s,%s,%s)",[vol_id,donee_id,name,contact_no,aadhar])
            mysql.commit()
            return 'success'
        except Exception as e:
            s = e
            flash(s,'error')
        cur.close()
    return render_template('donee.html')

@app.route('/donation',methods=['GET','POST'])
@is_logged_in   
def add_donation():
    if request.method == "POST":
        details = request.form
        don_id = details['donar_id'] 
        i_type = details['item_type']
        name = details['name']
        qty = details['quantity']
        date = details['entry_date']

        cur = mysql.cursor()
        try:
            cur.execute("insert into donation(DONAR_ID,ITEM_TYPE,ITEM_NAME,QUANTITY,ENTRY_DATE) values (%s,%s,%s,%s,%s)",[don_id,i_type,name,qty,date])
            mysql.commit()
            return 'success'
        except Exception as e:
            s = e
            flash(s,'error')
        cur.close()
    return render_template('donation.html')

@app.route('/donated',methods=['GET','POST'])
@is_logged_in   
def add_donated():
    if request.method == "POST":
        details = request.form
        donee_id = details['donee_id'] 
        i_type = details['item_type']
        name = details['name']
        qty = details['quantity']
        date = details['don_date']

        cur = mysql.cursor()
        try:
            cur.execute("insert into donated(DONEE_ID,ITEM_TYPE,ITEM_NAME,QUANTITY,DONATION_DATE) values (%s,%s,%s,%s,%s)",[donee_id,i_type,name,qty,date])
            mysql.commit()
            return 'success'
        except Exception as e:
            s = e
            flash(s,'error')
        cur.close()
    return render_template('donated.html')

####################################################################
#PROCEDURES
@app.route('/city-search-donar',methods=['GET','POST'])
@is_logged_in   
def city_search_donar():
    if request.method == "POST":
        details = request.form
        city_name = details['name']
        cur = mysql.connection.cursor()
        cur.execute('call city_search_donar(%s);',[city_name])
        data = cur.fetchall()
        n = len(data[0])
        cur.close()
    else:
        data = ''
        n = 0
    return render_template('city-search-donar.html',data=data,l=len(data),n=n)

@app.route('/name-search-donar',methods=['GET','POST'])
@is_logged_in   
def name_search_donar():
    if request.method == "POST":
        details = request.form
        don_name = details['name']
        cur = mysql.connection.cursor()
        cur.execute('call name_search_donar(%s);',[don_name])
        data = cur.fetchall()
        n = len(data[0])
        cur.close()
    else:
        data = ''
        n = 0
    return render_template('name-search.html',data=data,l=len(data),n=n)

@app.route('/name-search-donee',methods=['GET','POST'])
@is_logged_in   
def name_search_donee():
    if request.method == "POST":
        details = request.form
        donee_name = details['name']
        cur = mysql.connection.cursor()
        cur.execute('call name_search_donee(%s);',[donee_name])
        data = cur.fetchall()
        n = len(data[0])
        cur.close()
    else:
        data = ''
        n = 0
    return render_template('name-search.html',data=data,l=len(data),n=n)

@app.route('/volunteers-under-employee',methods=['GET','POST'])
@is_logged_in   
def disp_vol():
    if request.method == "POST":
        details = request.form
        emp_name = details['name']
        cur = mysql.connection.cursor()
        cur.execute('call disp_volunteers_under_employee(%s);',[emp_name])
        data = cur.fetchall()
        n = len(data[0])
        cur.close()
    else:
        data = ''
        n = 0
    return render_template('name-search.html',data=data,l=len(data),n=n)

@app.route('/donation-date-details',methods=['GET','POST'])
@is_logged_in   
def donation_details():
    if request.method == "POST":
        details = request.form
        date = details['date']
        cur = mysql.connection.cursor()
        cur.execute('call donation_date_details(%s);',[date])
        data = cur.fetchall()
        n = len(data[0])
        cur.close()
    else:
        data = ''
        n = 0
    return render_template('date-details.html',data=data,l=len(data),n=n)

@app.route('/donated-date-details',methods=['GET','POST'])
@is_logged_in   
def donated_details():
    if request.method == "POST":
        details = request.form
        date = details['date']
        cur = mysql.connection.cursor()
        cur.execute('call donated_date_details(%s);',[date])
        data = cur.fetchall()
        n = len(data[0])
        cur.close()
    else:
        data = ''
        n = 0
    return render_template('date-details.html',data=data,l=len(data),n=n)


@app.route('/calc-new-salary',methods=['GET','POST'])
@is_logged_in   
def city_search():
    cur = mysql.connection.cursor()
    cur.execute('call calc_new_salary();')
    data = cur.fetchall()
    n = len(data[0])
    cur.close()
    return render_template('new-salary.html',data=data,l=len(data),n=n)

        

####################################################################
#FUNCTIONS

@app.route('/donated-count',methods=['GET','POST'])
@is_logged_in   
def donated_count():
    if request.method == "POST":
        details = request.form
        date = details['date']
        cur = mysql.connection.cursor()
        cur.execute('select donated_count(%s);',[date])
        data = cur.fetchall()
        n = len(data[0])
        cur.close()
    else:
        data = ''
        n = 0
    return render_template('date-details.html',data=data,l=len(data),n=n)

@app.route('/donation-count',methods=['GET','POST'])
@is_logged_in   
def donation_count():
    if request.method == "POST":
        details = request.form
        date = details['date']
        cur = mysql.connection.cursor()
        cur.execute('select donation_count(%s);',[date])
        data = cur.fetchall()
        n = len(data[0])
        cur.close()
    return render_template('date-details.html',data=data,l=len(data),n=n)

@app.route('/donar-count',methods=['GET','POST'])
@is_logged_in   
def donar_count():
    if request.method == "POST":
        details = request.form
        date = details['date']
        cur = mysql.connection.cursor()
        cur.execute('select donar_count(%s);',[date])
        data = cur.fetchall()
        n = len(data[0])
        cur.close()
    return render_template('date-details.html',data=data,l=len(data),n=n)

@app.route('/max-time-donar')
@is_logged_in   
def max_time_donar():
    cur = mysql.connection.cursor()
    cur.execute('select max_time_donar()')
    data = cur.fetchall()
    cur.close()
    return render_template('homepage.html',data=data,l=len(data))

@app.route('/max-donation')
@is_logged_in   
def max_donation():
        cur = mysql.connection.cursor()
        cur.execute('select max_donation();')
        data = cur.fetchall()
        cur.close()
        return render_template('homepage.html',data=data,l=len(data))

@app.route('/sum-quantity')
@is_logged_in   
def sum_quantity(): 
        cur = mysql.connection.cursor()
        cur.execute('select sum_quantity();')
        data = cur.fetchall()
        cur.close()
        return render_template('homepage.html',data=data,l=len(data))


if __name__ == '__main__':
    app.run()

