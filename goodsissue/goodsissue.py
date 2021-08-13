import json
from random import randint

import MySQLdb
from flask import Blueprint, render_template, request, session, flash, redirect, url_for, jsonify
from flask_mysqldb import MySQL

from forms import POSForm, LoginForm, GoodsIssueForm, GoodsIssueSearchForm
from misc.misc import DecimalEncoder

goodsissue_bp = Blueprint('goodsissue_bp', __name__, template_folder='templates')


@goodsissue_bp.route('/goodsissue', methods=['GET','POST'])
def goodsissue():
    mygoodsissueform=GoodsIssueForm(request.form)
    from app import mysql
    cursor = mysql.connection.cursor()
    sqlst = "select warehousekey, warehousename from warehouse union all select 0, 'Select Warehouse' order by warehousekey"
    cursor.execute(sqlst)
    allwarehouses = cursor.fetchall()
    mygoodsissueform.warehousename.choices = allwarehouses

    if 'usersessionid' in session:
        if request.method=='POST':
            goodsissuetotal =  request.form['grandtotal']
            warehousename = request.form['warehousename']
            goodsissuedate = request.form['goodsissuedate']
            reason = request.form['reason']

            # print (request.form)
            list = [(k, v) for k, v in dict.items(request.form)]
            # print (list)
            productslist = list[0][1]
            chunks = [productslist[x:x+5] for x in range (0,len(productslist),5)]

            usersessionid=session['usersessionid']
            sqlst = """insert into goodsissue ( goodsissuetotal ,  usersessionid, userkey,
             warehousekey, reason, goodsissuedate) values (%s, %s, %s, %s, %s, %s)"""

            myvalues=[(goodsissuetotal), (usersessionid), (session['userkey']), (warehousename),  (reason), (goodsissuedate)]
            cursor=mysql.connection.cursor()
            cursor.execute(sqlst, myvalues)


            sqlst="select goodsissuekey from goodsissue where usersessionid=%s and goodsissuekey=(select LAST_INSERT_ID())"
            myvalues=[(usersessionid)]
            cursor.execute(sqlst, myvalues)
            goodsissuekey=cursor.fetchall()
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
                saleprice=row[2]
                quantity = row[3]
                linetotal=row[4]


                sqlst="""insert into goodsissuedetail (goodsissuekey, productkey, saleprice, quantity, linetotal,
                 productname, barcode) values (%s, %s,%s,%s,%s,%s,%s )"""
                myvalues=[(goodsissuekey), (productkey), (saleprice), (quantity), (linetotal), (productname), (barcode) ]
                cursor.execute(sqlst, myvalues)

                # get existing inventory
                sqlst="select onhandquantity from inventory where productkey=%s and warehousekey=%s"
                values = [(productkey), (warehousename)]
                cursor.execute(sqlst, values)
                onhandqty = cursor.fetchall()
                updatedqty = int(onhandqty[0][0]) - int(quantity)

                # update inventory
                sqlst="""update inventory set onhandquantity=%s where productkey=%s and warehousekey=%s"""
                values=[(updatedqty), (productkey), (warehousename)]
                cursor.execute(sqlst, values)

            mysql.connection.commit()

            return jsonify(goodsissuekey)
        if request.method == 'GET' and request.args.get('goodsissuekey'):
            goodsissuekey=request.args.get('goodsissuekey')
            cursor = mysql.connection.cursor(cursorclass=MySQLdb.cursors.DictCursor)
            sqlst = """ select goodsissue.goodsissuekey, goodsissuedetail.goodsissuedetailkey  , goodsissuedetail.productkey,
                        product.barcode ,  goodsissuedetail.productname, quantity,
                        goodsissuedetail.saleprice, linetotal from goodsissue
                        left join goodsissuedetail on goodsissue.goodsissuekey=goodsissuedetail.goodsissuekey
                        left join product on goodsissuedetail.productkey=product.productkey
                        where goodsissue.goodsissuekey=%s """
            values = [(goodsissuekey)]
            cursor.execute(sqlst, values)
            saleorderdetails = cursor.fetchall()
            return json.dumps(saleorderdetails, cls=DecimalEncoder)

        else:
            return render_template('goodsissue.html', form=mygoodsissueform)
    else:
        return redirect (url_for('login'))


@goodsissue_bp.route('/searchgoodsissues', methods=['GET','POST'])
def searchgoodsissues():
    mygoodsissuesearchform=GoodsIssueSearchForm(request.form)
    from app import mysql
    if 'usersessionid' in session:
        cursor = mysql.connection.cursor()
        cursor.execute("select brandkey, brandname from brand union all select 0, 'Select Brand' order by brandkey ")
        allbrands = cursor.fetchall()
        mygoodsissuesearchform.brandname.choices = allbrands
        cursor.execute("select vendorkey, vendorname from vendor union all select 0, 'Select Vendor' order by vendorkey ")
        allvendors = cursor.fetchall()
        mygoodsissuesearchform.vendorname.choices = allvendors
        cursor.execute(
            "select categorykey, categoryname from category union all select 0, 'Select Category' order by categorykey ")
        allcategories = cursor.fetchall()
        mygoodsissuesearchform.categoryname.choices = allcategories
        cursor.execute(
            "select warehousekey, warehousename from warehouse union all select 0, 'Select Warehouse' order by warehousekey ")
        allwarehouses = cursor.fetchall()
        mygoodsissuesearchform.warehousename.choices = allwarehouses
        if request.method=='POST':
            startdate=request.form['startdate']
            enddate = request.form['enddate']
            categorykey= request.form['categoryname']
            warehousekey = request.form['warehousename']
            vendorkey = request.form['vendorname']
            brandkey = request.form['brandname']
            barcode = request.form['barcode']
            productname = request.form['productname']
            conditions = ' where 1=1  '
            if (len(startdate) > 0):
                conditions = conditions + " and date(goodsissuedate) >= date('" + startdate + "')"
            if (len(enddate) > 0):
                conditions = conditions + " and date(goodsissuedate) <= date('" + enddate + "')"
            if (int(categorykey) > 0):
                conditions = conditions + " and categorykey = '" + categorykey + "'"
            if (int(vendorkey) > 0):
                conditions = conditions + " and vendorkey = '" + vendorkey + "'"
            if (int(warehousekey) > 0):
                conditions = conditions + " and goodsissue.warehousekey = '" + warehousekey + "'"
            if (int(brandkey) > 0):
                conditions = conditions + " and product.brandkey = '" + brandkey + "'"
            if (len(productname)>0) :
                conditions = conditions + " and goodsissuedetail.productname = '" + productname + "'"
            if (len(barcode)>0) :
                conditions = conditions + " and goodsissuedetail.barcode = '" + barcode + "'"
            cursor=mysql.connection.cursor(cursorclass=MySQLdb.cursors.DictCursor)
            sqlst="""select distinct  warehousename,goodsissue.goodsissuekey, goodsissue.goodsissuedate, goodsissue.goodsissuetotal
            from goodsissue left join goodsissuedetail on goodsissue.goodsissuekey=goodsissuedetail.goodsissuekey
            left join warehouse on goodsissue.warehousekey=warehouse.warehousekey
            left join product on goodsissuedetail.productkey=product.productkey
            """ + conditions
            cursor.execute(sqlst)
            productdetails=cursor.fetchall()
            return render_template('goodsissuesearch.html', form=mygoodsissuesearchform ,productdetails=productdetails)
        if request.method=='GET':
            cursor=mysql.connection.cursor(cursorclass=MySQLdb.cursors.DictCursor)
            sqlst="""select * from goodsissue
            left join warehouse on goodsissue.warehousekey=warehouse.warehousekey
            order by goodsissuedate, goodsissuekey"""
            cursor.execute(sqlst)
            productdetails=cursor.fetchall()
            return render_template('goodsissuesearch.html', form=mygoodsissuesearchform ,productdetails=productdetails)
    else:
        return redirect (url_for('login'))

