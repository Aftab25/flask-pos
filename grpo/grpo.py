import json
from random import randint
import MySQLdb
from flask import Blueprint, render_template, request, session, flash, redirect, url_for, jsonify
from flask_mysqldb import MySQL
from forms import POSForm, LoginForm, GRPOForm, GRPOSearchForm
from misc.misc import DecimalEncoder

grpo_bp = Blueprint('grpo_bp', __name__, template_folder='templates')

@grpo_bp.route('/grpo', methods=['GET', 'POST'])
def grpo():
    mygrpoform=GRPOForm(request.form)
    from app import mysql
    cursor=mysql.connection.cursor()
    sqlst="select vendorkey, vendorname from vendor union all select 0, 'Select Vendor' order by vendorkey"
    cursor.execute(sqlst)
    allvendors = cursor.fetchall()
    mygrpoform.vendorname.choices = allvendors

    sqlst="select warehousekey, warehousename from warehouse union all select 0, 'Select Warehouse' order by warehousekey"
    cursor.execute(sqlst)
    allwarehouses = cursor.fetchall()
    mygrpoform.warehousename.choices = allwarehouses

    if 'usersessionid' in session:
        if request.method=='POST':
            grpototal =  request.form['grandtotal']
            vendorkey=request.form['vendorkey']
            orderdate= request.form['orderdate']
            receiptdate = request.form['receiptdate']
            warehousekey=request.form['warehousekey']
            status=request.form['warehousekey']
            # print (request.form)
            list = [(k, v) for k, v in dict.items(request.form)]
            # print (list)
            productslist = list[0][1]
            chunks = [productslist[x:x+5] for x in range (0,len(productslist),5)]

            usersessionid=session['usersessionid']
            sqlst = """insert into grpo ( grpototal ,  usersessionid, userkey,
            vendorkey, orderdate, receiptdate, warehousekey, status) values (%s, %s, %s, %s, %s, %s, %s, %s)"""

            myvalues=[(grpototal), (usersessionid), (session['userkey']), (vendorkey), (orderdate), (receiptdate), (warehousekey), (status)]
            cursor=mysql.connection.cursor()
            cursor.execute(sqlst, myvalues)


            sqlst="select grpokey from grpo where usersessionid=%s and grpokey=(select LAST_INSERT_ID())"
            myvalues=[(usersessionid)]
            cursor.execute(sqlst, myvalues)
            grpokey=cursor.fetchall()
            # print (saleorderkey)

            for row in chunks:
                # print (row)
                # get productkey
                # print (row[0])
                sqlst="select productkey from product where barcode=%s"
                myvalues=[(row[0])]
                cursor.execute(sqlst, myvalues)
                productkey = cursor.fetchall()
                barcode=row[0]
                productname=row[1]
                purchaseprice=row[2]
                quantity = row[3]
                linetotal=row[4]


                sqlst="""insert into grpodetail (grpokey, productkey, purchaseprice, quantity, linetotal,
                 productname, barcode, warehousekey) values (%s, %s,%s,%s,%s,%s,%s, %s )"""
                myvalues=[(grpokey), (productkey), (purchaseprice), (quantity), (linetotal), (productname), (barcode), (warehousekey) ]
                cursor.execute(sqlst, myvalues)

                # get existing qty
                sqlst="""select onhandquantity from inventory where productkey=%s and warehousekey=%s"""
                values=[(productkey), (warehousekey)]
                cursor.execute(sqlst, values)
                qtydata =cursor.fetchall()
                if (qtydata):
                    updatedquantity=(int(qtydata[0][0]) + int(quantity))
                    # update qty
                    sqlst="""update inventory set onhandquantity=%s where productkey=%s and warehousekey=%s"""
                    values=[ (updatedquantity) , (productkey), (warehousekey)]
                    cursor.execute(sqlst, values)
                else:
                    grpokey=0
                    print ('Product does not exist in Inventory table')
                    mysql.connection.rollback()

            mysql.connection.commit()

            return jsonify(grpokey)
        if request.method == 'GET' and request.args.get('grpokey'):
            grpokey=request.args.get('grpokey')
            cursor = mysql.connection.cursor(cursorclass=MySQLdb.cursors.DictCursor)
            sqlst = """ select grpo.grpokey, grpodetail.grpodetailkey  , grpodetail.productkey,
                        product.barcode ,  grpodetail.productname, quantity,
                        grpodetail.purchaseprice, linetotal from grpo
                        left join grpodetail on grpo.grpokey=grpodetail.grpokey
                        left join product on grpodetail.productkey=product.productkey
                        where grpo.grpokey=%s and grpo.warehousekey=%s """
            values = [(grpokey), (session['warehousekey'])]
            cursor.execute(sqlst, values)
            saleorderdetails = cursor.fetchall()
            return json.dumps(saleorderdetails, cls=DecimalEncoder)

        else:
            return render_template('grpomanual.html', form=mygrpoform)
    else:
        return redirect (url_for('login'))






@grpo_bp.route('/savegrpo', methods=['GET','POST'])
def savegrpo():
    mygrpoform=GRPOForm(request.form)
    from app import mysql
    if 'usersessionid' in session:
        if request.method=='POST':
            grpototal =  request.form['grandtotal']
            vendorkey=request.form['vendorkey']
            orderdate= request.form['orderdate']
            receiptdate = request.form['receiptdate']
            warehousekey=request.form['warehousekey']
            status=request.form['warehousekey']
            # print (request.form)
            list = [(k, v) for k, v in dict.items(request.form)]
            # print (list)
            productslist = list[0][1]
            chunks = [productslist[x:x+5] for x in range (0,len(productslist),5)]

            usersessionid=session['usersessionid']
            sqlst = """insert into grpo ( grpototal ,  usersessionid, userkey,
            vendorkey, orderdate, receiptdate, warehousekey, status) values (%s, %s, %s, %s, %s, %s, %s, %s)"""

            myvalues=[(grpototal), (usersessionid), (session['userkey']), (vendorkey), (orderdate), (receiptdate), (warehousekey), (status)]
            cursor=mysql.connection.cursor()
            cursor.execute(sqlst, myvalues)


            sqlst="select grpokey from grpo where usersessionid=%s and grpokey=(select LAST_INSERT_ID())"
            myvalues=[(usersessionid)]
            cursor.execute(sqlst, myvalues)
            grpokey=cursor.fetchall()
            # print (saleorderkey)

            for row in chunks:
                # print (row)
                # get productkey
                # print (row[0])
                sqlst="select productkey from product where barcode=%s"
                myvalues=[(row[0])]
                cursor.execute(sqlst, myvalues)
                productkey = cursor.fetchall()
                barcode=row[0]
                productname=row[1]
                purchaseprice=row[2]
                quantity = row[3]
                linetotal=row[4]


                sqlst="""insert into grpodetail (grpokey, productkey, purchaseprice, quantity, linetotal,
                 productname, barcode, warehousekey) values (%s, %s,%s,%s,%s,%s,%s )"""
                myvalues=[(grpokey), (productkey), (purchaseprice), (quantity), (linetotal), (productname), (barcode), (warehousekey) ]
                cursor.execute(sqlst, myvalues)

            mysql.connection.commit()

            return jsonify(grpokey)
        else:
            return render_template('grpo.html', form=mygrpoform)
    else:
        return redirect (url_for('login'))


@grpo_bp.route('/searchgrpos', methods=['GET','POST'])
def searchgrpos():
    mygrposearchform=GRPOSearchForm(request.form)
    from app import mysql
    if 'usersessionid' in session:
        cursor = mysql.connection.cursor()
        cursor.execute("select brandkey, brandname from brand union all select 0, 'Select Brand' order by brandkey ")
        allbrands = cursor.fetchall()
        mygrposearchform.brandname.choices = allbrands

        cursor.execute("select vendorkey, vendorname from vendor union all select 0, 'Select Vendor' order by vendorkey ")
        allvendors = cursor.fetchall()
        mygrposearchform.vendorname.choices = allvendors

        cursor.execute(
            "select categorykey, categoryname from category union all select 0, 'Select Category' order by categorykey ")
        allcategories = cursor.fetchall()
        mygrposearchform.categoryname.choices = allcategories

        if request.method=='POST':
            startdate=request.form['startdate']
            enddate = request.form['enddate']
            categorykey= request.form['categoryname']
            vendorkey = request.form['vendorname']
            brandkey = request.form['brandname']
            barcode = request.form['barcode']
            productname = request.form['productname']

            conditions = ' where grpo.warehousekey=%s   '

            if (len(startdate) > 0):
                conditions = conditions + " and date(receiptdate) >= date('" + startdate + "')"

            if (len(enddate) > 0):
                conditions = conditions + " and date(receiptdate) <= date('" + enddate + "')"

            if (int(categorykey) > 0):
                conditions = conditions + " and product.categorykey = '" + categorykey + "'"

            if (int(vendorkey) > 0):
                conditions = conditions + " and product.vendorkey = '" + vendorkey + "'"

            if (int(brandkey) > 0):
                conditions = conditions + " and product.brandkey = '" + brandkey + "'"

            if (len(productname)>0) :
                conditions = conditions + " and grpodetail.productname = '" + productname + "'"

            if (len(barcode)>0) :
                conditions = conditions + " and grpodetail.barcode = '" + barcode + "'"


            # print (conditions)

            cursor=mysql.connection.cursor(cursorclass=MySQLdb.cursors.DictCursor)
            sqlst="""select distinct vendorname, warehousename, grpo.grpokey, receiptdate from grpo left join grpodetail on grpo.grpokey=grpodetail.grpokey
            left join product on grpodetail.productkey=product.productkey
            left join warehouse on grpo.warehousekey=warehouse.warehousekey
            left join vendor on grpo.vendorkey=vendor.vendorkey
            """ + conditions
            values=[(session['warehousekey'])]
            # print (values)

            cursor.execute(sqlst, values)

            productdetails=cursor.fetchall()

            # return jsonify(productdetails)

            return render_template('grposearch.html', form=mygrposearchform ,productdetails=productdetails)

        if request.method=='GET':
            cursor=mysql.connection.cursor(cursorclass=MySQLdb.cursors.DictCursor)
            sqlst="""select * from grpo
            left join warehouse on grpo.warehousekey=warehouse.warehousekey
            left join vendor on grpo.vendorkey=vendor.vendorkey
            where grpo.warehousekey=%s
            order by receiptdate, grpokey"""
            values=[(session['warehousekey'])]
            # print (values)
            cursor.execute(sqlst, values)
            productdetails=cursor.fetchall()
            # return jsonify(productdetails)
            return render_template('grposearch.html', form=mygrposearchform ,productdetails=productdetails)
    else:
        return redirect (url_for('login'))


