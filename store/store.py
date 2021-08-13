import MySQLdb
from flask import Blueprint, render_template, request, session, flash, redirect, url_for, jsonify
from flask_mysqldb import MySQL
from forms import POSForm, StoreSearchForm, StoreForm

store_bp = Blueprint('store_bp', __name__, template_folder='templates')



@store_bp.route('/store', methods=['GET','POST','PUT'])
def store():
    mystoreform = StoreForm(request.form)
    from app import mysql
    cursor = mysql.connection.cursor()
    cursor.execute("select warehousekey, warehouseid from warehouse union all select 0, 'Select Warehouse' order by warehousekey ")
    allwarehouses = cursor.fetchall()
    mystoreform.warehousename.choices = allwarehouses

    cursor.execute(
        "select customerkey, customername from customer union all select 0, 'Select Customer' order by customerkey ")
    allcustomers = cursor.fetchall()
    mystoreform.defaultcustomername.choices = allcustomers

    if 'usersessionid' in session:
        if mystoreform.validate_on_submit():
            if request.method == 'POST':
                storename= request.form['storename']
                storeid = request.form['storeid']
                warehousekey=request.form['warehousename']
                defaultcustomerkey = request.form['defaultcustomername']
                cursor = mysql.connection.cursor()
                sqlst="insert into store (storeid ,storename, warehousekey, defaultcustomerkey) values (%s, %s, %s,  %s) "
                values=[ (storeid), (storename),(warehousekey), (defaultcustomerkey)]
                cursor.execute(sqlst ,values)
                mysql.connection.commit()
                cursor.close()
                flash( 'Store Added')
                return redirect(url_for('store'))

        if request.method == 'GET' and request.args.get('storekey'):
            storekey = request.args.get('storekey')
            cursor = mysql.connection.cursor(cursorclass=MySQLdb.cursors.DictCursor)
            sqlst = """ select * from store where storekey=%s"""
            values = [(storekey)]
            cursor.execute(sqlst, values)
            productdetails = cursor.fetchall()
            # print (saleorderdetails)
            return jsonify(productdetails)

        if request.method == 'PUT':
            data = request.get_data()
            data2=data.decode("utf-8")
            data2 =  data2.split('&')

            storekey = data2[0]
            storeid = data2[1]
            storename = data2[2]
            warehouse = data2[3]
            defaultcustomername = data2[4]

            storekey = storekey.split('=')
            storekey = storekey[1]

            storeid = storeid.split('=')
            storeid=storeid[1]

            storename = storename.split('=')
            storename = storename[1]

            warehouse = warehouse.split('=')
            warehouse = warehouse[1]

            defaultcustomername = defaultcustomername.split('=')
            defaultcustomername = defaultcustomername[1]

            cursor = mysql.connection.cursor()
            sqlst = """update store set storename=%s, storeid=%s, warehousekey=%s, defaultcustomerkey=%s where storekey=%s
            """
            values = [(storename), (storeid), (warehouse), (defaultcustomername), (storekey)]
            cursor.execute(sqlst, values)
            mysql.connection.commit()
            cursor.close()
            return ('Store Updated')
        else:
            return render_template('store.html', form=mystoreform)
    else:
        return redirect (url_for('login'))




@store_bp.route('/searchstore',  methods=['GET','POST'])
def searchstore():
    if 'usersessionid' in session:
        mystoresearchform=StoreSearchForm(request.form)
        from app import mysql
        cursor = mysql.connection.cursor()
        cursor.execute("select warehousekey, warehousename from warehouse union all select 0, 'Select Warehouse' order by warehousekey ")
        allwarehouses = cursor.fetchall()
        mystoresearchform.warehousename.choices = allwarehouses

        cursor.execute("select customerkey, customername from customer union all select 0, 'Select Customer' order by customerkey ")
        allcustomers = cursor.fetchall()
        mystoresearchform.defaultcustomername.choices = allcustomers

        if request.method=='POST':
            try:
                warehousekey= request.form['warehousename']
                customerkey = request.form['defaultcustomername']
                storename = request.form['storename']
                storeid = request.form['storeid']

                conditions = ' where 1=1 '

                if (int(warehousekey) > 0):
                    conditions = conditions + " and store.warehousekey = '" + warehousekey + "'"

                if (int(customerkey) > 0):
                    conditions = conditions + " and store.defaultcustomerkey = '" + customerkey + "'"

                if (len(storename) > 0):
                    conditions = conditions + " and store.storename = '" + storename + "'"

                if (len(storeid)>0) :
                    conditions = conditions + " and store.storeid = '" + storeid + "'"

                cursor=mysql.connection.cursor(cursorclass=MySQLdb.cursors.DictCursor)
                sqlst="""select storekey , storeid, storename,  warehousename, customername from store
                left join warehouse on store.warehousekey=warehouse.warehousekey
                left join customer on store.defaultcustomerkey=customer.customerkey
                """ + conditions

                cursor.execute(sqlst)

                productdetails=cursor.fetchall()
            except Exception as err:
                print (err)
            return render_template('storesearch.html', form=mystoresearchform ,productdetails=productdetails)

        if request.method=='GET':
            try:
                cursor=mysql.connection.cursor(cursorclass=MySQLdb.cursors.DictCursor)
                sqlst="""select storekey , storeid, storename,  warehousename, customername from store
                left join warehouse on store.warehousekey=warehouse.warehousekey
                left join customer on store.defaultcustomerkey=customer.customerkey
                order by storename """

                cursor.execute(sqlst)
                productdetails=cursor.fetchall()
            except Exception as err:
                print (err)
            return render_template('storesearch.html', form=mystoresearchform ,productdetails=productdetails)
    else:
        return redirect (url_for('login'))


@store_bp.route('/getstores', methods=['GET', 'POST'])
def getstores():
    if 'usersessionid' in session:
        if request.method=='GET':
            from app import mysql
            cursor = mysql.connection.cursor()
            sqlst = """ select storekey, storename from store"""
            cursor.execute(sqlst)
            storeslist = cursor.fetchall()
            # print (saleorderdetails)
            return jsonify(storeslist)
    else:
        return redirect (url_for('login'))
