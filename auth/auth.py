from random import randint
import MySQLdb
from flask import Blueprint, render_template, request, session, flash, redirect, url_for, jsonify
from flask_mysqldb import MySQL
from forms import POSForm, LoginForm
from warehouse.warehouse import getwarehousekey

auth_bp = Blueprint('auth_bp', __name__, template_folder='templates')



@auth_bp.route('/', methods=['GET','POST'])
def main():
    if 'usersessionid' in session:
        return render_template('index.html')
    else:
        return redirect (url_for('auth_bp.login'))


@auth_bp.route('/index')
def index():
    if 'usersessionid' in session:
        return render_template('index.html')
    else:
        return redirect (url_for('auth_bp.login'))




@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    from app import mysql
    myloginform=LoginForm(request.form)
    if request.method=='GET':
        cursor = mysql.connection.cursor()
        cursor.execute("select storekey, storename from store union all select 0, 'Select Store' order by storekey ")
        allstore = cursor.fetchall()
        myloginform.storename.choices = allstore
        cursor.execute("select poskey, posname from pos union all select 0, 'Select POS' order by poskey ")
        allpos = cursor.fetchall()
        myloginform.posname.choices = allpos
        cursor.close()

    if request.method=='POST':
        username =  request.form['username']
        userpassword = request.form['userpassword']
        storekey = request.form['storename']
        poskey= request.form['posname']
        cursor = mysql.connection.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        sqlst="""select * from user 
        left join userstore on user.userkey=userstore.userkey
        left join store on userstore.storekey=store.storekey
        left join pos on userstore.poskey=pos.poskey
        where username = (%s) and userpassword = (%s) 
        and store.storekey=%s and pos.poskey=%s
        """
        values = [(username), (userpassword) ,  (storekey), (poskey)]
        # print (values)
        cursor.execute(sqlst, values)
        userdata=cursor.fetchall()
        if (userdata):
            session['usersessionid']=randint(1000, 100000)
            session['userkey']=userdata[0]['userkey']
            session['storekey']=userdata[0]['storekey']
            session['poskey']=userdata[0]['poskey']
            session['warehousekey'] = getwarehousekey(userdata[0]['storekey'])
            session['username'] = userdata[0]['username']
            session['storename'] = userdata[0]['storename']
            session['posname'] = userdata[0]['posname']
            cursor.close()
            return render_template('index.html')
        else:
            flash('Invalid login details')
            return redirect(url_for('auth_bp.login'))
    else:
        return render_template('login.html', form=myloginform)



@auth_bp.route('/logout', methods=['GET','POST'])
def logout():
    session.pop('usersessionid')
    session.pop('userkey')
    session.pop('storekey')
    session.pop('poskey')
    session.pop('warehousekey')
    session.pop('username')
    session.pop('storename')
    session.pop('posname')

    return redirect(url_for('auth_bp.login'))


