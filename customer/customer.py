import MySQLdb
from flask import Blueprint, render_template, request, session, flash, redirect, url_for, jsonify
from flask_mysqldb import MySQL
from forms import POSForm, CustomerSearchForm, CustomerForm

customer_bp = Blueprint('customer_bp', __name__, template_folder='templates')


@customer_bp.route('/searchcustomer',  methods=['GET','POST'])
def searchcustomer():
    from app import mysql
    if 'usersessionid' in session:
        mycustomersearchform=CustomerSearchForm(request.form)
        if request.method=='POST':
            try:
                customerid= request.form['customerid']
                customername = request.form['customername']
                conditions = ' where 1=1 '
                if (len(customerid) > 0):
                    conditions = conditions + " and customer.customerid = '" + customerid + "'"
                if (len(customername) > 0):
                    conditions = conditions + " and customer.customername = '" + customername + "'"
                cursor=mysql.connection.cursor(cursorclass=MySQLdb.cursors.DictCursor)
                sqlst="""select * from customer  """ + conditions

                # print (sqlst)

                cursor.execute(sqlst)

                productdetails=cursor.fetchall()
            except Exception as err:
                print (err)
            return render_template('customersearch.html', form=mycustomersearchform ,productdetails=productdetails)

        if request.method=='GET':
            try:
                cursor=mysql.connection.cursor(cursorclass=MySQLdb.cursors.DictCursor)
                sqlst="""select * from customer order by customer.customerkey """
                cursor.execute(sqlst)
                productdetails=cursor.fetchall()
            except Exception as err:
                print (err)
            return render_template('customersearch.html', form=mycustomersearchform ,productdetails=productdetails)
    else:
        return redirect (url_for('login'))


@customer_bp.route('/getdefaultcustomer', methods=['GET', 'POST'])
def getdefaultcustomer():
    if 'usersessionid' in session:
        if request.method=='GET':
            from app import mysql
            cursor = mysql.connection.cursor()
            sqlst = """ select defaultcustomerkey, customername from store
            left join customer on store.defaultcustomerkey=customer.customerkey where storekey=%s"""
            values=[(session['storekey'])]
            cursor.execute(sqlst, values)
            defaultcustomername = cursor.fetchall()
            # print (saleorderdetails)
            return jsonify(defaultcustomername)
    else:
        return redirect (url_for('login'))




@customer_bp.route('/getcustomers', methods=['GET', 'POST'])
def getcustomers():
    if 'usersessionid' in session:
        if request.method=='GET':
            from app import mysql
            cursor = mysql.connection.cursor()
            sqlst = """ select customerkey, customername from customer"""
            cursor.execute(sqlst)
            customerslist = cursor.fetchall()
            # print (saleorderdetails)
            return jsonify(customerslist)
    else:
        return redirect (url_for('login'))




@customer_bp.route('/customer', methods=['GET','POST','PUT'])
def customer():
    from app import mysql
    mycustomerform = CustomerForm(request.form)

    if 'usersessionid' in session:
        if mycustomerform.validate_on_submit():
            if request.method=='POST':
                # Process Form
                usersessionid=session['usersessionid']
                customerid = request.form['customerid']
                customername=request.form['customername']
                cursor = mysql.connection.cursor()
                sqlst="""insert into customer (usersessionid , customerid , customername) values (%s, %s , %s )"""
                values = [usersessionid, (customerid) , (customername)]
                cursor.execute(sqlst, values)
                mysql.connection.commit()
                cursor.close()
                flash( 'Customer Added')
                return redirect(url_for('customer'))

        if request.method == 'GET' and request.args.get('customerkey'):
            customerkey = request.args.get('customerkey')

            print (customerkey)
            cursor = mysql.connection.cursor(cursorclass=MySQLdb.cursors.DictCursor)
            sqlst = """ select * from customer where customerkey=%s"""
            values = [(customerkey)]
            cursor.execute(sqlst, values)
            productdetails = cursor.fetchall()
            # print (saleorderdetails)
            return jsonify(productdetails)
        if request.method=='PUT':
            data = request.get_data()
            data2 = data.decode("utf-8")
            data2 = data2.split('&')

            customerid = data2[0]
            customerkey = data2[1]
            customername = data2[2]

            customerid = customerid.split('=')
            customerid = customerid[1]

            customerkey = customerkey.split('=')
            customerkey = customerkey[1]

            customername = customername.split('=')
            customername = customername[1]


            cursor = mysql.connection.cursor()
            sqlst="""update customer set customername=%s, customerid=%s where customerkey=%s """
            values=[(customername), (customerid), (customerkey)]
            # print (values)

            cursor.execute(sqlst, values)
            mysql.connection.commit()
            cursor.close()
            return ( 'Customer Updated')

        else:
            return render_template('customer.html', form=mycustomerform)
    else:
        return redirect (url_for('login'))

