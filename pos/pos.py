import MySQLdb
from flask import Blueprint, render_template, request, session, flash, redirect, url_for, jsonify
from flask_mysqldb import MySQL
from forms import POSForm, POSSearchForm

pos_bp = Blueprint('pos_bp', __name__, template_folder='templates')


@pos_bp.route('/pos', methods=['GET','POST', 'PUT'])
def pos():
    myposform = POSForm(request.form)
    from app import mysql
    cursor = mysql.connection.cursor()
    cursor.execute("select storekey, storeid from store union all select 0, 'Select Store' order by storekey ")
    allstores = cursor.fetchall()
    myposform.storename.choices = allstores
    if 'usersessionid' in session:
        if myposform.validate_on_submit():
            if request.method=='POST':
                storename= request.form['storename']
                posid = request.form['posid']
                posname=request.form['posname']
                cursor = mysql.connection.cursor()
                sqlst="insert into pos (posid ,posname, storekey) values (%s, %s, %s) "
                values=[ (posid), (posname) , (storename)]
                cursor.execute(sqlst ,values)
                mysql.connection.commit()
                cursor.close()
                flash( 'POS Added')
                return redirect(url_for('pos_bp.pos'))
            else:
                return render_template('pos.html', form=myposform)
        if request.method == 'GET' and request.args.get('poskey'):
            poskey = request.args.get('poskey')
            cursor = mysql.connection.cursor(cursorclass=MySQLdb.cursors.DictCursor)
            sqlst = """ select * from pos where poskey=%s"""
            values = [(poskey)]
            cursor.execute(sqlst, values)
            productdetails = cursor.fetchall()
            # print (saleorderdetails)
            return jsonify(productdetails)
        if request.method == 'PUT':
            data = request.get_data()
            print (data)
            data2=data.decode("utf-8")
            data2 =  data2.split('&')

            posid = data2[1]
            poskey = data2[0]
            posname = data2[2]
            store = data2[3]

            posid = posid.split('=')
            posid = posid[1]

            poskey = poskey.split('=')
            poskey=poskey[1]

            posname = posname.split('=')
            posname = posname[1]

            store = store.split('=')
            storekey = store[1]

            cursor = mysql.connection.cursor()
            sqlst = """update pos set posname=%s, posid=%s, storekey=%s where poskey=%s """
            values = [(posname), (posid), (storekey), (poskey)]
            # print (values)
            cursor.execute(sqlst, values)
            mysql.connection.commit()
            cursor.close()
            return ('POS Updated')
        else:
            return render_template('pos.html', form=myposform)
    else:
        return redirect (url_for('login'))





@pos_bp.route('/searchpos',  methods=['GET','POST'])
def searchpos():
    if 'usersessionid' in session:
        mypossearchform=POSSearchForm(request.form)
        from app import mysql
        cursor = mysql.connection.cursor()
        cursor.execute("select storekey, storename from store union all select 0, 'Select Store' order by storekey ")
        allwarehouses = cursor.fetchall()
        mypossearchform.storename.choices = allwarehouses
        if request.method=='POST':
            try:
                posname= request.form['posname']
                storekey = request.form['storename']
                posid = request.form['posid']

                conditions = ' where 1=1 '

                if (int(storekey) > 0):
                    conditions = conditions + " and pos.storekey = '" + storekey + "'"

                if (len(posname) > 0):
                    conditions = conditions + " and pos.posname = '" + posname + "'"

                if (len(posid)>0) :
                    conditions = conditions + " and pos.posid = '" + posid + "'"


                print (conditions)

                cursor=mysql.connection.cursor(cursorclass=MySQLdb.cursors.DictCursor)
                sqlst="""select poskey , posid, storename,  posname  from pos
                left join store on pos.storekey=store.storekey
                """ + conditions

                # print (sqlst)

                cursor.execute(sqlst)

                productdetails=cursor.fetchall()
            except Exception as err:
                print (err)
            return render_template('accounts/possearch.html', form=mypossearchform ,productdetails=productdetails)

        if request.method=='GET':
            try:
                cursor=mysql.connection.cursor(cursorclass=MySQLdb.cursors.DictCursor)
                sqlst="""select poskey , posid, storename,  posname  from pos
                left join store on pos.storekey=store.storekey
                order by poskey """

                cursor.execute(sqlst)
                productdetails=cursor.fetchall()
            except Exception as err:
                print (err)
            return render_template('possearch.html', form=mypossearchform ,productdetails=productdetails)
    else:
        return redirect (url_for('login'))

