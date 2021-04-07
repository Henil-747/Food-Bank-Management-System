from flask import Flask,render_template,request
from flask_mysqldb import MySQL
app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'test_1'
app.config['MYSQL_PASSWORD'] = 'password_1'
app.config['MYSQL_DB'] = 'mytestdb'

mysql = MySQL(app)


@app.route('/')
def hello_world():
    return 'This is our DBMS Project'

@app.route('/begin',methods=['GET','POST'])
def begin():
    if request.method == "POST":
        details = request.form
        name = details['user_name']
        email = details['user_email']
        password = details['password']
        cur = mysql.connection.cursor()
        cur.execute("insert into user_details (user_name,user_email,password) values (%s,%s,%s)",[name,email,password])
        mysql.connection.commit()
        cur.close()
        return 'success'
    return render_template('registration.html')

if __name__ == '__main__':
    app.run()

