import json
from random import randint

import MySQLdb
from flask import Blueprint, render_template, request, session, flash, redirect, url_for, jsonify
from flask_mysqldb import MySQL

from forms import POSForm, LoginForm, RefundOrderSearchForm, RefundForm
from misc.misc import DecimalEncoder

refund_bp = Blueprint('refund_bp', __name__, template_folder='templates')



@refund_bp.route('/searchrefundorders', methods=['GET','POST'])
def searchrefundorders():
    myrefundordersearchform=RefundOrderSearchForm(request.form)
    from app import mysql
    cursor = mysql.connection.cursor()
    cursor.execute("select brandkey, brandname from brand union all select 0, 'Select Brand' order by brandkey ")
    allbrands = cursor.fetchall()
    myrefundordersearchform.brandname.choices = allbrands
    cursor.execute("select vendorkey, vendorname from vendor union all select 0, 'Select Vendor' order by vendorkey ")
    allvendors = cursor.fetchall()
    myrefundordersearchform.vendorname.choices = allvendors
    cursor.execute(
        "select categorykey, categoryname from category union all select 0, 'Select Category' order by categorykey ")
    allcategories = cursor.fetchall()
    myrefundordersearchform.categoryname.choices = allcategories
    if 'usersessionid' in session:
        if request.method=='POST':
            try:
                startdate=request.form['startdate']
                enddate = request.form['enddate']
                saleorderkey= request.form['saleorderkey']
                categorykey = request.form['categoryname']
                vendorkey = request.form['vendorname']
                brandkey = request.form['brandname']
                productname = request.form['productname']
                barcode = request.form['barcode']
                saleprice = request.form['saleprice']
                conditions = ' where storekey=%s and poskey=%s and 1=1 '
                if (len(startdate) > 0):
                    conditions = conditions + " and date(refundorderdate) >= date('" + startdate + "')"
                if (len(enddate) > 0):
                    conditions = conditions + " and date(refundorderdate) <= date('" + enddate + "')"
                if (len(saleorderkey) > 0):
                    conditions = conditions + " and saleorderkey = '" + saleorderkey + "'"
                if (int(categorykey) > 0):
                    conditions = conditions + " and product.categorykey = '" + categorykey + "'"
                if (int(vendorkey) > 0):
                    conditions = conditions + " and product.vendorkey = '" + vendorkey + "'"
                if (int(brandkey) > 0):
                    conditions = conditions + " and product.brandkey = '" + brandkey + "'"
                if (len(productname)>0) :
                    conditions = conditions + " and product.productname = '" + productname + "'"
                if (len(barcode)>0) :
                    conditions = conditions + " and product.barcode = '" + barcode + "'"
                if (len(saleprice) > 0):
                    conditions = conditions + " and refundorderdetail.saleprice = '" + saleprice + "'"
                cursor=mysql.connection.cursor(cursorclass=MySQLdb.cursors.DictCursor)
                sqlst="""select distinct refundorder.refundorderkey, refundorder.refundorderdate, refundorder.refundordertotal, refundorder.saleorderkey
                 from refundorder
                left join refundorderdetail on refundorder.refundorderkey=refundorderdetail.refundorderkey
                left join product on refundorderdetail.productkey=product.productkey
                """ + conditions
                values = [(session['storekey']), (session['poskey'])]
                cursor.execute(sqlst, values)
                productdetails=cursor.fetchall()
            except Exception as err:
                print (err)
            return render_template('refundordersearch.html', form=myrefundordersearchform ,productdetails=productdetails)
        if request.method=='GET':
            try:
                cursor=mysql.connection.cursor(cursorclass=MySQLdb.cursors.DictCursor)
                sqlst="""select refundorder.*, saleorder.saleordertotal from refundorder
                left join saleorder on refundorder.saleorderkey=saleorder.saleorderkey
                where refundorder.storekey=%s and refundorder.poskey=%s
                order by refundorderdate, refundorderkey"""
                values=[(session['storekey']), (session['poskey'])]
                cursor.execute(sqlst, values)
                productdetails=cursor.fetchall()
            except Exception as err:
                print (err)
            return render_template('refundordersearch.html', form=myrefundordersearchform ,productdetails=productdetails)
    else:
        return redirect (url_for('login'))


@refund_bp.route('/refund', methods=['GET','POST'])
def refund():
    myrefundform=RefundForm(request.form)
    from app import mysql
    if 'usersessionid' in session:
        if request.method=='POST':
            usersessionid = session['usersessionid']
            refundordertotal = request.form['refundordertotal']
            saleorderkey = int(request.form['saleorderkey'])
            list = [(k, v) for k, v in dict.items(request.form)]
            productslist = list[0][1]
            chunks = [productslist[x:x+5] for x in range (0,len(productslist),5)]
            cursor = mysql.connection.cursor()
            sqlst="select customerkey from saleorder where saleorderkey=%s"
            values=[(saleorderkey)]
            cursor.execute(sqlst, values)
            customerkey = cursor.fetchall()
            sqlst = """insert into refundorder ( saleorderkey,  usersessionid, refundordertotal,
            userkey, storekey, poskey, warehousekey, customerkey
            ) values (%s, %s, %s, %s, %s, %s, %s, %s)"""
            values = [ (saleorderkey), (usersessionid), (refundordertotal), (session['userkey']), (session['storekey']),(session['poskey']),(session['warehousekey']), (customerkey)]
            cursor.execute(sqlst, values)
            sqlst = "select refundorderkey from refundorder where usersessionid=%s and refundorderkey=(select LAST_INSERT_ID())"
            values = [(usersessionid)]
            cursor.execute(sqlst, values)
            refundorderkey = cursor.fetchall()
            for row in chunks:
                sqlst="select productkey from product where barcode=%s"
                myvalues=[(row[0])]
                cursor.execute(sqlst, myvalues)
                productkey = cursor.fetchall()
                barcode=row[0]
                productname=row[1]
                saleprice=row[2]
                quantity = row[3]
                linetotal=row[4]
                sqlst = """insert into refundorderdetail (refundorderkey, productkey , quantity, saleprice, linetotal ,
                productname, barcode, warehousekey) VALUES (%s, %s,%s,%s,%s,%s, %s, %s)"""
                myval = [(refundorderkey), (productkey), (quantity), (saleprice), (linetotal), (productname), (barcode), (session['warehousekey'])]
                # print(myval)
                cursor.execute(sqlst, myval)
                # get current inventory
                sqlst="""select onhandquantity from inventory where productkey=%s and warehousekey=%s"""
                values = [(productkey),(session['warehousekey'])]
                cursor.execute(sqlst, values)
                existinginventory=cursor.fetchall()
                updatedinventory = (int(existinginventory[0][0]) + int(quantity))
                # update inventory with more stock
                sqlst="""update inventory set onhandquantity =%s where productkey=%s and warehousekey=%s"""
                values = [ (updatedinventory) , (productkey), (session['warehousekey'])]
                cursor.execute(sqlst, values)
            mysql.connection.commit()
            return jsonify(refundorderkey)
        if request.method == 'GET' and request.args.get('refundorderkey'):
            refundorderkey = request.args.get('refundorderkey')
            cursor = mysql.connection.cursor(cursorclass=MySQLdb.cursors.DictCursor)
            sqlst = """ select refundorder.refundorderkey, refundorderdetail.refundorderdetailkey  , refundorderdetail.productkey,
                                  product.barcode ,  refundorderdetail.productname, quantity,
                                  refundorderdetail.saleprice, linetotal from refundorder
                                  left join refundorderdetail on refundorder.refundorderkey=refundorderdetail.refundorderkey
                                  left join product on refundorderdetail.productkey=product.productkey
                                  where refundorder.refundorderkey=%s"""
            values = [(refundorderkey)]
            cursor.execute(sqlst, values)
            saleorderdetails = cursor.fetchall()
            return json.dumps(saleorderdetails, cls=DecimalEncoder)
        else:
            return render_template('refund2.html', form=myrefundform)
    else:
        return redirect (url_for('login'))



@refund_bp.route('/totalrefundstatus', methods=['GET','POST'])
def totalrefundstatus():
    from app import mysql
    if request.method=='POST':
        saleorderkey=request.form['saleorderkey']
        cursor = mysql.connection.cursor()
        sqlst=""" select  SUM(saleorderdetail.quantity) totalsoldquantity
        from saleorder
        left join saleorderdetail on saleorder.saleorderkey=saleorderdetail.saleorderkey
        where saleorder.saleorderkey=%s"""
        values = [(saleorderkey)]
        cursor.execute(sqlst, values)
        soldquantity = cursor.fetchall()
        # print(soldquantity)
        if soldquantity[0] is None:
            totalsoldquantity=0
        else:
            totalsoldquantity=int (soldquantity[0][0])
        sqlst = """ select SUM(refundorderdetail.quantity) as totalrefundedquantity
        from refundorder
            left join refundorderdetail on  refundorder.refundorderkey=refundorderdetail.refundorderkey
            where refundorder.saleorderkey=%s"""
        values = [(saleorderkey)]
        try:
            cursor2 = mysql.connection.cursor()
            cursor2.execute(sqlst, values)
            refundedquantity = cursor2.fetchone()
            if refundedquantity[0] is None:
                totalrefundedquantity=0
            else:
                totalrefundedquantity=int(refundedquantity[0])
        except Exception as err:
            print (err)
        if int(totalrefundedquantity)<int(totalsoldquantity):
            status = 'Y'
        else:
            status = 'N'
    return status
