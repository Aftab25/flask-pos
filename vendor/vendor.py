import MySQLdb
from flask import Blueprint, render_template, request, session, flash, redirect, url_for, jsonify
from forms import VendorSearchForm, VendorForm

vendor_bp = Blueprint('vendor_bp', __name__, template_folder='templates')

@vendor_bp.route('/searchvendor',  methods=['GET','POST'])
def searchvendor():
    from app import mysql
    if 'usersessionid' in session:
        myvendorsearchform=VendorSearchForm(request.form)
        if request.method=='POST':
            try:
                vendorid= request.form['vendorid']
                vendorname = request.form['vendorname']
                conditions = ' where 1=1 '
                if (len(vendorid) > 0):
                    conditions = conditions + " and vendor.vendorid = '" + vendorid + "'"
                if (len(vendorname) > 0):
                    conditions = conditions + " and vendor.vendorname = '" + vendorname + "'"
                cursor=mysql.connection.cursor(cursorclass=MySQLdb.cursors.DictCursor)
                sqlst="""select * from vendor  """ + conditions
                # print (sqlst)
                cursor.execute(sqlst)
                productdetails=cursor.fetchall()
            except Exception as err:
                print (err)
            return render_template('vendorsearch.html', form=myvendorsearchform ,productdetails=productdetails)

        if request.method=='GET':
            try:
                cursor=mysql.connection.cursor(cursorclass=MySQLdb.cursors.DictCursor)
                sqlst="""select * from vendor order by vendor.vendorkey """
                cursor.execute(sqlst)
                productdetails=cursor.fetchall()
            except Exception as err:
                print (err)
            return render_template('vendorsearch.html', form=myvendorsearchform ,productdetails=productdetails)
    else:
        return redirect (url_for('login'))


@vendor_bp.route('/getvendors', methods=['GET', 'POST'])
def getvendors():
    if 'usersessionid' in session:
        if request.method=='GET':
            from app import mysql
            cursor = mysql.connection.cursor()
            sqlst = """ select vendorkey, vendorname from vendor"""
            cursor.execute(sqlst)
            vendorslist = cursor.fetchall()
            # print (saleorderdetails)
            return jsonify(vendorslist)
    else:
        return redirect (url_for('login'))

@vendor_bp.route('/vendor', methods=['GET','POST', 'PUT'])
def vendor():
    myvendorform = VendorForm(request.form)
    from app import mysql
    if 'usersessionid' in session:
        if request.method=='POST':
            vendorid = request.form['vendorid']
            vendorname= request.form['vendorname']
            cursor = mysql.connection.cursor()
            cursor.execute("insert into vendor (vendorid, vendorname) values (%s, %s) " ,  ([vendorid],[vendorname]))
            mysql.connection.commit()
            cursor.close()
            flash( 'Vendor Added')
            return redirect(url_for('vendor'))

        if request.method == 'GET' and request.args.get('vendorkey'):
            vendorkey=request.args.get('vendorkey')
            cursor = mysql.connection.cursor(cursorclass=MySQLdb.cursors.DictCursor)
            sqlst = """ select * from vendor where vendorkey=%s"""
            values = [(vendorkey) ]
            cursor.execute(sqlst, values)
            productdetails = cursor.fetchall()
            # print (saleorderdetails)
            return jsonify(productdetails)

        if request.method == 'PUT':
            data = request.get_data()
            data2=data.decode("utf-8")
            data2 =  data2.split('&')

            vendorid = data2[0]
            vendorkey = data2[1]
            vendorname = data2[2]

            vendorid = vendorid.split('=')
            vendorid = vendorid[1]

            vendorkey = vendorkey.split('=')
            vendorkey=vendorkey[1]

            vendorname = vendorname.split('=')
            vendorname = vendorname[1]

            cursor = mysql.connection.cursor()
            sqlst = """update vendor set vendorname=%s, vendorid=%s where vendorkey=%s"""
            values = [(vendorname), (vendorid), (vendorkey)]
            cursor.execute(sqlst, values)
            mysql.connection.commit()
            cursor.close()
            return ('Vendor Updated')
        else:
            return render_template('vendor.html', form=myvendorform)
    else:
        return redirect (url_for('login'))
