from flask import Flask, render_template, request, redirect, url_for, session,send_file
from flask_mysqldb import MySQL
import MySQLdb
import MySQLdb.cursors
import re
from datetime import date
import os

app = Flask(__name__)
app.secret_key = 'xyzsdfg'
  
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Victus123!@#'
app.config['MYSQL_DB'] = 'user_system'


mysql = MySQL(app)
  
@app.route('/')

@app.route('/index',methods =['GET','POST'])
def home():
    if request.method == 'POST':
        if request.form.get('read-more') :
            id=request.form['read-more']
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT * FROM project WHERE projectid='%s'" % (id))
            result = cursor.fetchall()
            mysql.connection.commit()
            cursor.close()
            id=result[0]
            resu=id[0]
            res=str(resu)
            session['pid']=res
            file_path="./files"+"/"+session['name']+"/"+res
            app.config['file_path'] = file_path
            files = os.listdir(app.config['file_path'])
            return render_template('proview.html',data=result,files=files)
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM project order by projectid desc limit 10')
    pro=cursor.fetchall()
    mysql.connection.commit()
    cursor.close()
    return render_template('index.html',data=pro)

@app.route('/login', methods =['GET', 'POST'])
def login():
    mesage = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        user=cursor.execute('SELECT * FROM user WHERE email = %s and password = %s',(email,password))
        user = cursor.fetchone()
        if user :
            session['loggedin'] = True
            session['userid'] = user['userid']
            session['name'] = user['name']
            session['email'] = user['email']
            mesage = 'Logged in successfully !'
            return render_template('user.html', mesage = mesage)
        else:
            mesage = 'Please enter correct email / password !'
    return render_template('login.html', mesage = mesage)

@app.route('/create_project', methods=['GET','POST'])
def create_project():
    mesage = ''
    pname=request.form['pname']
    obj=request.form['obj']
    domain=request.form['domain']
    dept=request.form['dept']
    descrp=request.form['descrp']
    outcome=request.form['outcome']
    cite=request.form['cite']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if not pname or not obj or not domain or not dept or not descrp or not outcome or not cite :
            mesage = 'Please fill out the form !'
    else:
         cursor.execute('INSERT INTO project VALUES (NULL, % s, % s,%s, % s,%s,%s,%s,%s,%s)', (pname,obj,domain,dept,descrp,outcome,cite,session['name'],date.today()))
        
    uni_name=session['name']
    cursor.execute('select max(projectid) from project')
    id = cursor.fetchall()
    mysql.connection.commit()
    pi=id[0]
    p_id=pi["max(projectid)"]
    path="./files/{}".format(uni_name)
    if not os.path.exists(path) :
        os.makedirs(path,exist_ok=True)
        file_path=path+'/'+str(p_id)
        os.mkdir(file_path)
    else :
        file_path=path+'/'+str(p_id)
        if not os.path.exists(file_path):
            os.mkdir(file_path)

    app.config['file_path'] = file_path
    file = request.files['file']
    if file:
        if file.filename != '':
            file.save(os.path.join(app.config['file_path'], file.filename))
            mesage = 'Project Created !'
            files = os.listdir(app.config['file_path'])
            print(file_path)
            print(files)
    return render_template('user.html', mesage = mesage)

@app.route('/user', methods=['GET','POST'])
def user():
    if request.method == 'POST':
        if request.form.get('create') == 'Create Project':
            return render_template('create_project.html')
    if request.method == 'POST':
        if request.form.get('project') == 'My Projects':
            return render_template('myprojects.html')
    if request.method == 'POST':
        if request.form.get('read-more') :
            id=request.form['read-more']
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT * FROM project WHERE projectid='%s'" % (id))
            result = cursor.fetchall()
            mysql.connection.commit()
            cursor.close()
            id=result[0]
            resu=id[0]
            res=str(resu)
            session['pid']=res
            file_path="./files"+"/"+session['name']+"/"+res
            app.config['file_path'] = file_path
            files = os.listdir(app.config['file_path'])
            return render_template('proview.html',data=result,files=files)
    
        """if request.form.get('search') == 'search':
            search = request.form['search']
            print(search)
            cursor.execute('SELECT * FROM project where pname like %%s%',(search))
            pro=cursor.fetchall()
            mysql.connection.commit()
            cursor.close()
        else :
        name='\'%'+"JJB"+'%\''
        print(name)"""
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM project order by projectid desc limit 10')
    pro=cursor.fetchall()
    mysql.connection.commit()
    cursor.close()
    return render_template('user.html', data=pro)
        
@app.route('/myprojects',methods=['GET','POST'])
def myprojects():
    if request.method == 'POST':
        if request.form.get('read-more') :
            id=request.form['read-more']
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT * FROM project WHERE projectid='%s'" % (id))
            result = cursor.fetchall()
            mysql.connection.commit()
            cursor.close()
            id=result[0]
            resu=id[0]
            res=str(resu)
            session['pid']=res
            file_path="./files"+"/"+session['name']+"/"+res
            app.config['file_path'] = file_path
            files = os.listdir(app.config['file_path'])
            return render_template('proview.html',data=result,files=files)
    uniname=session['name']
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM project where name = %s',(uniname,))
    data=cursor.fetchall()
    mysql.connection.commit()
    cursor.close()
    return render_template('myprojects.html', data=data)

@app.route('/download/<filename>')
def download(filename):
    id=session['pid']
    file_path="./files"+"/"+session['name']+"/"+id
    app.config['file_path'] = file_path
    return send_file(os.path.join(app.config['file_path'],filename), as_attachment=True)

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('userid', None)
    session.pop('email', None)
    return redirect(url_for('home'))
  
@app.route('/register', methods =['GET', 'POST'])
def register():
    mesage = ''
    if request.method == 'POST' and 'name' in request.form and 'code' in request.form and 'city' in request.form and 'pincode' in request.form and 'password' in request.form and 'email' in request.form :
        userName = request.form['name']
        code=request.form['code']
        city=request.form['city']
        pincode=request.form['pincode']
        password = request.form['password']
        email = request.form['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE email = % s', (email, ))
        account = cursor.fetchone()
        if account:
            mesage = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            mesage = 'Invalid email address !'
        elif not userName or not password or not email:
            mesage = 'Please fill out the form !'
        else:
            cursor.execute('INSERT INTO user VALUES (NULL, % s, % s, % s,%s,%s,%s)', (userName, email, password, code, city, pincode ))
            mysql.connection.commit()
            mesage = 'You have successfully registered !'
    elif request.method == 'POST':
        mesage = 'Please fill out the form !'
    return render_template('register.html', mesage = mesage)
    
if __name__ == "__main__":
    app.run(debug=True)