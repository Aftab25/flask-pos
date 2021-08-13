import MySQLdb
from flask import Blueprint, render_template, request, session, flash, redirect, url_for, jsonify
from forms import WarehouseSearchForm, WarehouseForm

warehouse_bp = Blueprint('warehouse_bp', __name__, template_folder='templates')


@warehouse_bp.route('/searchwarehouse',  methods=['GET','POST'])
def searchwarehouse():
    from app import mysql
    if 'usersessionid' in session:
        mywarehousesearchform=WarehouseSearchForm(request.form)
        if request.method=='POST':
            try:
                warehouseid= request.form['warehouseid']
                warehousename = request.form['warehousename']
                conditions = ' where 1=1 '
                if (len(warehouseid) > 0):
                    conditions = conditions + " and warehouse.warehouseid = '" + warehouseid + "'"
                if (len(warehousename) > 0):
                    conditions = conditions + " and warehouse.warehousename = '" + warehousename + "'"
                cursor=mysql.connection.cursor(cursorclass=MySQLdb.cursors.DictCursor)
                sqlst="""select * from warehouse  """ + conditions
                cursor.execute(sqlst)
                productdetails=cursor.fetchall()
            except Exception as err:
                print (err)
            return render_template('warehousesearch.html', form=mywarehousesearchform ,productdetails=productdetails)

        if request.method=='GET':
            try:
                cursor=mysql.connection.cursor(cursorclass=MySQLdb.cursors.DictCursor)
                sqlst="""select * from warehouse order by warehouse.warehousekey """
                cursor.execute(sqlst)
                productdetails=cursor.fetchall()
            except Exception as err:
                print (err)
            return render_template('warehousesearch.html', form=mywarehousesearchform ,productdetails=productdetails)
    else:
        return redirect (url_for('login'))


@warehouse_bp.route('/warehouse', methods=['GET','POST', 'PUT'])
def warehouse():
    mywarehouseform = WarehouseForm(request.form)
    from app import mysql
    cursor = mysql.connection.cursor()
    cursor.execute("select warehousekey, warehouseid from warehouse union all select 0, 'Select Warehouse' order by warehouseid ")
    allwarehouses = cursor.fetchall()
    mywarehouseform.warehousename.choices = allwarehouses
    if 'usersessionid' in session:
        if request.method=='POST':
            warehousename= request.form['warehousename']
            warehouseid = request.form['warehouseid']
            cursor = mysql.connection.cursor()
            sqlst="insert into warehouse (warehouseid ,warehousename) values (%s, %s) "
            values=[(warehouseid), (warehousename)]
            cursor.execute(sqlst ,values)
            mysql.connection.commit()
            cursor.close()
            flash( 'Warehouse Added')
            return redirect(url_for('store'))

        if request.method == 'GET' and request.args.get('warehousekey'):
            warehousekey = request.args.get('warehousekey')
            cursor = mysql.connection.cursor(cursorclass=MySQLdb.cursors.DictCursor)
            sqlst = """ select * from warehouse where warehousekey=%s"""
            values = [(warehousekey)]
            cursor.execute(sqlst, values)
            productdetails = cursor.fetchall()
            return jsonify(productdetails)

        if request.method == 'PUT':
            data = request.get_data()
            data2=data.decode("utf-8")
            data2 =  data2.split('&')

            warehouseid = data2[0]
            warehousekey = data2[1]
            warehousename = data2[2]

            warehouseid = warehouseid.split('=')
            warehouseid = warehouseid[1]

            warehousekey = warehousekey.split('=')
            warehousekey=warehousekey[1]

            warehousename = warehousename.split('=')
            warehousename = warehousename[1]

            cursor = mysql.connection.cursor()
            sqlst = """update warehouse set warehousename=%s, warehouseid=%s where warehousekey=%s """
            values = [(warehousename), (warehouseid), (warehousekey)]
            cursor.execute(sqlst, values)
            mysql.connection.commit()
            cursor.close()
            return ('Warehouse Updated')
        else:
            return render_template('warehouse.html', form=mywarehouseform)
    else:
        return redirect (url_for('login'))

@warehouse_bp.route('/getwarehouses', methods=['GET', 'POST'])
def getwarehouses():
    if 'usersessionid' in session:
        if request.method=='GET':
            from app import mysql
            cursor = mysql.connection.cursor()
            sqlst = """ select warehousekey, warehousename from warehouse"""
            cursor.execute(sqlst)
            warehouseslist = cursor.fetchall()
            # print (saleorderdetails)
            return jsonify(warehouseslist)
    else:
        return redirect (url_for('login'))



def getwarehousekey(storekey):
    sqlst="select warehousekey from store where storekey=%s"
    values = [(storekey)]
    from app import mysql
    cursor=mysql.connection.cursor()
    cursor.execute(sqlst, values)
    warehousekey = cursor.fetchall()
    return warehousekey

