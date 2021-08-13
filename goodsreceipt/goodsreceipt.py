import json
import MySQLdb
from flask import Blueprint, render_template, request, session, redirect, url_for, jsonify
from forms import  GoodsReceiptForm, GoodsReceiptSearchForm
from misc.misc import DecimalEncoder

goodsreceipt_bp = Blueprint('goodsreceipt_bp', __name__, template_folder='templates')

@goodsreceipt_bp.route('/goodsreceipt', methods=['GET', 'POST'])
def goodsreceipt():
    mygoodsreceiptform=GoodsReceiptForm(request.form)
    from app import mysql
    cursor=mysql.connection.cursor()
    sqlst="select warehousekey, warehousename from warehouse union all select 0, 'Select Warehouse' order by warehousekey"
    cursor.execute(sqlst)
    allwarehouses = cursor.fetchall()
    mygoodsreceiptform.warehousename.choices = allwarehouses
    if 'usersessionid' in session:
        if request.method=='POST':
            goodsreceipttotal =  request.form['grandtotal']
            receiptdate = request.form['receiptdate']
            warehousekey=request.form['warehousekey']
            reason=request.form['reason']
            list = [(k, v) for k, v in dict.items(request.form)]
            productslist = list[0][1]
            chunks = [productslist[x:x+5] for x in range (0,len(productslist),5)]
            usersessionid=session['usersessionid']
            sqlst = """insert into goodsreceipt ( goodsreceipttotal ,  usersessionid, userkey,
            receiptdate, warehousekey, reason) values (%s, %s, %s, %s, %s, %s)"""
            myvalues=[(goodsreceipttotal), (usersessionid), (session['userkey']),  (receiptdate), (warehousekey), (reason)]
            cursor=mysql.connection.cursor()
            cursor.execute(sqlst, myvalues)
            sqlst="select goodsreceiptkey from goodsreceipt where usersessionid=%s and goodsreceiptkey=(select LAST_INSERT_ID())"
            myvalues=[(usersessionid)]
            cursor.execute(sqlst, myvalues)
            goodsreceiptkey=cursor.fetchall()
            for row in chunks:
                sqlst="select productkey from product where barcode=%s"
                myvalues=[(row[0])]
                cursor.execute(sqlst, myvalues)
                productkey = cursor.fetchall()
                barcode=row[0]
                productname=row[1]
                purchaseprice=row[2]
                quantity = row[3]
                linetotal=row[4]
                sqlst="""insert into goodsreceiptdetail (goodsreceiptkey, productkey, purchaseprice, quantity, linetotal,
                 productname, barcode, warehousekey) values (%s, %s,%s,%s,%s,%s,%s, %s )"""
                myvalues=[(goodsreceiptkey), (productkey), (purchaseprice), (quantity), (linetotal), (productname), (barcode), (warehousekey) ]
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
                    goodsreceiptkey=0
                    print ('Product does not exist in Inventory table')
                    mysql.connection.rollback()
            mysql.connection.commit()
            return jsonify(goodsreceiptkey)
        if request.method == 'GET' and request.args.get('goodsreceiptkey'):
            goodsreceiptkey=request.args.get('goodsreceiptkey')
            cursor = mysql.connection.cursor(cursorclass=MySQLdb.cursors.DictCursor)
            sqlst = """ select goodsreceipt.goodsreceiptkey, goodsreceiptdetail.goodsreceiptdetailkey  , goodsreceiptdetail.productkey,
                        product.barcode ,  goodsreceiptdetail.productname, quantity,
                        goodsreceiptdetail.purchaseprice, linetotal from goodsreceipt
                        left join goodsreceiptdetail on goodsreceipt.goodsreceiptkey=goodsreceiptdetail.goodsreceiptkey
                        left join product on goodsreceiptdetail.productkey=product.productkey
                        where goodsreceipt.goodsreceiptkey=%s """
            values = [(goodsreceiptkey)]
            cursor.execute(sqlst, values)
            saleorderdetails = cursor.fetchall()
            return json.dumps(saleorderdetails, cls=DecimalEncoder)
        else:
            return render_template('goodsreceipt.html', form=mygoodsreceiptform)
    else:
        return redirect (url_for('login'))


@goodsreceipt_bp.route('/searchgoodsreceipts', methods=['GET','POST'])
def searchgoodsreceipts():
    mygoodsreceiptsearchform=GoodsReceiptSearchForm(request.form)
    from app import mysql
    if 'usersessionid' in session:
        cursor = mysql.connection.cursor()
        cursor.execute("select brandkey, brandname from brand union all select 0, 'Select Brand' order by brandkey ")
        allbrands = cursor.fetchall()
        mygoodsreceiptsearchform.brandname.choices = allbrands

        cursor.execute("select vendorkey, vendorname from vendor union all select 0, 'Select Vendor' order by vendorkey ")
        allvendors = cursor.fetchall()
        mygoodsreceiptsearchform.vendorname.choices = allvendors

        cursor.execute(
            "select categorykey, categoryname from category union all select 0, 'Select Category' order by categorykey ")
        allcategories = cursor.fetchall()
        mygoodsreceiptsearchform.categoryname.choices = allcategories

        cursor.execute(
            "select warehousekey, warehousename from warehouse union all select 0, 'Select Warehouse' order by warehousekey ")
        allwarehouses = cursor.fetchall()
        mygoodsreceiptsearchform.warehousename.choices = allwarehouses

        if request.method=='POST':
            startdate=request.form['startdate']
            enddate = request.form['enddate']
            categorykey= request.form['categoryname']
            vendorkey = request.form['vendorname']
            brandkey = request.form['brandname']
            barcode = request.form['barcode']
            productname = request.form['productname']
            warehousekey = request.form['warehousename']
            conditions = ' where 1=1   '

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

            if (int(warehousekey) > 0):
                conditions = conditions + " and goodsreceipt.warehousekey = '" + warehousekey + "'"

            if (len(productname)>0) :
                conditions = conditions + " and goodsreceiptdetail.productname = '" + productname + "'"

            if (len(barcode)>0) :
                conditions = conditions + " and goodsreceiptdetail.barcode = '" + barcode + "'"


            # print (conditions)

            cursor=mysql.connection.cursor(cursorclass=MySQLdb.cursors.DictCursor)
            sqlst="""select distinct warehousename, goodsreceipt.goodsreceiptkey, receiptdate from goodsreceipt
             left join goodsreceiptdetail on goodsreceipt.goodsreceiptkey=goodsreceiptdetail.goodsreceiptkey
            left join product on goodsreceiptdetail.productkey=product.productkey
            left join warehouse on goodsreceipt.warehousekey=warehouse.warehousekey
            """ + conditions


            cursor.execute(sqlst)

            productdetails=cursor.fetchall()

            # return jsonify(productdetails)

            return render_template('goodsreceiptsearch.html', form=mygoodsreceiptsearchform ,productdetails=productdetails)

        if request.method=='GET':
            cursor=mysql.connection.cursor(cursorclass=MySQLdb.cursors.DictCursor)
            sqlst="""select * from goodsreceipt
            left join warehouse on goodsreceipt.warehousekey=warehouse.warehousekey
            order by receiptdate, goodsreceiptkey"""

            # print (values)
            cursor.execute(sqlst)
            productdetails=cursor.fetchall()
            # return jsonify(productdetails)
            return render_template('goodsreceiptsearch.html', form=mygoodsreceiptsearchform ,productdetails=productdetails)
    else:
        return redirect (url_for('login'))

