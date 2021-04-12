from flask import Flask,render_template,request
from flask_mysqldb import MySQL
import mysql.connector
app = Flask(__name__)

#app.config['MYSQL_HOST'] = 'localhost'
#app.config['MYSQL_USER'] = 'test_1'
#app.config['MYSQL_PASSWORD'] = 'password_1'
#app.config['MYSQL_DB'] = 'mytestdb'

mysql1 = mysql.connector.connect(
    host='localhost',
    database='mytestdb',
    user='test_1',
    password='password_1',
    auth_plugin='mysql_native_password')


@app.route('/')
def hello_world():
    return 'This is our DBMS Project!!!!!'

@app.route('/register',methods=['GET','POST'])
def begin():
    if request.method == "POST":
        details = request.form
        name = details['user_name']
        email = details['user_email']
        password = details['password']
        cur = mysql1.cursor()
        try:
            cur.execute("insert into user_details (user_name,user_email,user_password) values (%s,%s,%s)",[name,email,password])
            mysql1.connection.commit()
            return 'success'
        except mysql.connector.Error as e:
            s = 'Error Code:'+str(e.errno)+' SQLSTATE: '+str(e.sqlstate)+' Message: '+str(e.msg)
            return s
        cur.close()
    return render_template('registration.html')

if __name__ == '__main__':
    app.run()

