import json
import MySQLdb
from flask import Blueprint, render_template, request, session, flash, redirect, url_for, jsonify, make_response
from forms import POSForm, LoginForm, SaleForm, RefundForm, SaleOrderSearchForm, DailySaleReportForm
from misc.misc import DecimalEncoder

sale_bp = Blueprint('sale_bp', __name__, template_folder='templates')

@sale_bp.route('/sale', methods=['GET','POST'])
def sale():
    mysaleform=SaleForm(request.form)
    from app import mysql
    cursor = mysql.connection.cursor()
    sqlst = "select customerkey, customername from customer union all select 0, 'Select Customer' order by customerkey"
    cursor.execute(sqlst)
    allcustomers = cursor.fetchall()
    mysaleform.customername.choices = allcustomers
    if 'usersessionid' in session:
        if request.method=='POST':
            saleordertotal =  request.form['grandtotal']
            customerkey = request.form['customername']
            saledate = request.form['saledate']
            list = [(k, v) for k, v in dict.items(request.form)]
            productslist = list[0][1]
            chunks = [productslist[x:x+5] for x in range (0,len(productslist),5)]
            usersessionid=session['usersessionid']
            sqlst = """insert into saleorder ( saleordertotal ,  usersessionid, userkey,
            storekey, poskey, warehousekey, customerkey, saleorderdate) values (%s, %s, %s, %s, %s, %s, %s, %s)"""
            myvalues=[(saleordertotal), (usersessionid), (session['userkey']), (session['storekey']), (session['poskey']), (session['warehousekey']), (customerkey), (saledate)]
            cursor=mysql.connection.cursor()
            cursor.execute(sqlst, myvalues)
            sqlst="select saleorderkey from saleorder where usersessionid=%s and saleorderkey=(select LAST_INSERT_ID())"
            myvalues=[(usersessionid)]
            cursor.execute(sqlst, myvalues)
            saleorderkey=cursor.fetchall()
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
                sqlst="""insert into saleorderdetail (saleorderkey, productkey, saleprice, quantity, linetotal,
                 productname, barcode) values (%s, %s,%s,%s,%s,%s,%s )"""
                myvalues=[(saleorderkey), (productkey), (saleprice), (quantity), (linetotal), (productname), (barcode) ]
                cursor.execute(sqlst, myvalues)
                sqlst="select onhandquantity from inventory where productkey=%s and warehousekey=%s"
                values = [(productkey), (session['warehousekey'])]
                cursor.execute(sqlst, values)
                onhandqty = cursor.fetchall()
                updatedqty = int(onhandqty[0][0]) - int(quantity)
                sqlst="""update inventory set onhandquantity=%s where productkey=%s and warehousekey=%s"""
                values=[(updatedqty), (productkey), (session['warehousekey'])]
                cursor.execute(sqlst, values)
            mysql.connection.commit()
            return jsonify(saleorderkey)
        if request.method == 'GET' and request.args.get ('saleorderkey'):
            saleorderkey = request.args.get ('saleorderkey')
            cursor = mysql.connection.cursor(cursorclass=MySQLdb.cursors.DictCursor)
            sqlst = """ select saleorder.saleorderkey, saleorderdetail.saleorderdetailkey  , saleorderdetail.productkey,
                                    product.barcode ,  saleorderdetail.productname, quantity,
                                    saleorderdetail.saleprice, linetotal from saleorder
                                    left join saleorderdetail on saleorder.saleorderkey=saleorderdetail.saleorderkey
                                    left join product on saleorderdetail.productkey=product.productkey
                                    where saleorder.saleorderkey=%s and storekey=%s and poskey=%s"""
            values = [(saleorderkey), (session['storekey']), (session['poskey'])]
            cursor.execute(sqlst, values)
            saleorderdetails = cursor.fetchall()
            return json.dumps(saleorderdetails, cls=DecimalEncoder)
        else:
            return render_template('sale2.html', form=mysaleform)
    else:
        return redirect (url_for('login'))

@sale_bp.route('/getsaleordertotal', methods=['GET', 'POST'])
def getsaleordertotal():
    if 'usersessionid' in session:
        if request.method=='POST':
            saleorderkey=request.form['saleorderkey']
            from app import mysql
            cursor = mysql.connection.cursor(cursorclass=MySQLdb.cursors.DictCursor)
            sqlst = """ select saleordertotal from saleorder
                        where storekey=%s and poskey=%s and saleorder.saleorderkey=%s"""
            values = [(session['storekey']), (session['poskey']), (saleorderkey) ]
            cursor.execute(sqlst, values)
            saleorderdetails = cursor.fetchall()
            # print (saleorderdetails)
            return json.dumps(saleorderdetails, cls=DecimalEncoder)
    else:
        return redirect (url_for('login'))



@sale_bp.route('/getsoldproductquantity', methods=['GET', 'POST'])
def getsoldproductquantity():
    loginform=LoginForm(request.form)
    myrefundform=RefundForm(request.form)
    if 'usersessionid' in session:
        if request.method=='POST':
            saleorderkey=request.form['saleorderkey']
            barcode=request.form['barcode']
            from app import mysql
            cursor = mysql.connection.cursor()
            sqlst = """ select  SUM(quantity) as soldquantity
             from `pos`.saleorder
                        left join saleorderdetail on saleorder.saleorderkey=saleorderdetail.saleorderkey
                        left join product on saleorderdetail.productkey=product.productkey
                        where saleorder.saleorderkey=%s and saleorderdetail.barcode=%s"""
            values = [(saleorderkey), (barcode)]
            cursor.execute(sqlst, values)
            productsoldquantity = cursor.fetchall()
            return jsonify(productsoldquantity)
        else:
            return render_template('refund2.html', form=myrefundform)
    else:
        return redirect (url_for('login'))




@sale_bp.route('/searchsaleorders', methods=['GET','POST'])
def searchsaleorders():
    from app import mysql
    mysaleordersearchform=SaleOrderSearchForm(request.form)
    if 'usersessionid' in session:
        cursor = mysql.connection.cursor()
        cursor.execute("select brandkey, brandname from brand union all select 0, 'Select Brand' order by brandkey ")
        allbrands = cursor.fetchall()
        mysaleordersearchform.brandname.choices = allbrands

        cursor.execute("select vendorkey, vendorname from vendor union all select 0, 'Select Vendor' order by vendorkey ")
        allvendors = cursor.fetchall()
        mysaleordersearchform.vendorname.choices = allvendors

        cursor.execute(
            "select categorykey, categoryname from category union all select 0, 'Select Category' order by categorykey ")
        allcategories = cursor.fetchall()
        mysaleordersearchform.categoryname.choices = allcategories

        cursor.execute(
            "select customerkey, customername from customer union all select 0, 'Select Customer' order by customerkey ")
        allcustomers = cursor.fetchall()
        mysaleordersearchform.customername.choices = allcustomers

        if request.method=='POST':
            startdate=request.form['startdate']
            enddate = request.form['enddate']
            categorykey= request.form['categoryname']
            vendorkey = request.form['vendorname']
            brandkey = request.form['brandname']
            customerkey = request.form['customername']
            barcode = request.form['barcode']
            productname = request.form['productname']

            conditions = ' where saleorder.storekey=%s and poskey=%s  '

            if (len(startdate) > 0):
                conditions = conditions + " and date(saleorderdate) >= date('" + startdate + "')"

            if (len(enddate) > 0):
                conditions = conditions + " and date(saleorderdate) <= date('" + enddate + "')"

            if (int(categorykey) > 0):
                conditions = conditions + " and categorykey = '" + categorykey + "'"

            if (int(customerkey) > 0):
                conditions = conditions + " and saleorder.customerkey = '" + customerkey + "'"

            if (int(vendorkey) > 0):
                conditions = conditions + " and vendorkey = '" + vendorkey + "'"

            if (int(brandkey) > 0):
                conditions = conditions + " and product.brandkey = '" + brandkey + "'"

            if (len(productname)>0) :
                conditions = conditions + " and saleorderdetail.productname = '" + productname + "'"

            if (len(barcode)>0) :
                conditions = conditions + " and saleorderdetail.barcode = '" + barcode + "'"
            cursor=mysql.connection.cursor(cursorclass=MySQLdb.cursors.DictCursor)
            sqlst="""select distinct customername, saleorder.saleorderkey, saleorder.saleorderdate, saleorder.saleordertotal
            from saleorder left join saleorderdetail on saleorder.saleorderkey=saleorderdetail.saleorderkey
            left join product on saleorderdetail.productkey=product.productkey
            left join customer on saleorder.customerkey=customer.customerkey
            """ + conditions
            values=[(session['storekey']), (session['poskey'])]
            cursor.execute(sqlst, values)
            productdetails=cursor.fetchall()
            return render_template('saleordersearch.html', form=mysaleordersearchform ,productdetails=productdetails)

        if request.method=='GET':
            cursor=mysql.connection.cursor(cursorclass=MySQLdb.cursors.DictCursor)
            sqlst="""select * from saleorder left join customer on saleorder.customerkey=customer.customerkey
            where saleorder.storekey=%s and poskey=%s
            order by saleorderdate, saleorderkey"""
            values=[(session['storekey']), (session['poskey'])]
            cursor.execute(sqlst, values)
            productdetails=cursor.fetchall()
            return render_template('saleordersearch.html', form=mysaleordersearchform ,productdetails=productdetails)
    else:
        return redirect (url_for('login'))


@sale_bp.route('/dailysalereport', methods=['GET','POST'])
def dailysalereport():
    mydailysalereportform=DailySaleReportForm(request.form)
    if 'usersessionid' in session:
        from app import mysql
        cursor = mysql.connection.cursor()
        cursor.execute("select storekey, storename from store union all select 0, 'Select Store' order by storekey ")
        allstores = cursor.fetchall()
        mydailysalereportform.storename.choices = allstores
        cursor.execute("select poskey, posname from pos union all select 0, 'Select POS' order by poskey ")
        allposs = cursor.fetchall()
        mydailysalereportform.posname.choices = allposs
        if request.method=='POST':
            startdate=request.form['startdate']
            enddate = request.form['enddate']
            storekey= request.form['storename']
            poskey = request.form['posname']
            conditions = ' where 1=1   '
            if (len(startdate) > 0):
                conditions = conditions + " and date(saleorderdate) >= date('" + startdate + "')"

            if (len(enddate) > 0):
                conditions = conditions + " and date(saleorderdate) <= date('" + enddate + "')"

            if (int(storekey) > 0):
                conditions = conditions + " and saleorder.storekey = '" + storekey + "'"

            if (int(poskey) > 0):
                conditions = conditions + " and saleorder.poskey = '" + poskey + "'"

            cursor = mysql.connection.cursor(cursorclass=MySQLdb.cursors.DictCursor)

            # print (conditions)

            sqlst = """
                  select saleorderdate ,store.storename, pos.posname , product.productname, product.barcode,
                  categoryname, brandname, vendorname , SUM(quantity)soldquantity, sum(linetotal)linetotal
                  from saleorder
                  left join saleorderdetail on saleorder.saleorderkey=saleorderdetail.saleorderkey
                  left join product on saleorderdetail.productkey=product.productkey
                  left join brand on product.brandkey=brand.brandkey
                  left join category on product.categorykey=category.categorykey
                  left join vendor on product.vendorkey=vendor.vendorkey
                  left join store on saleorder.storekey=store.storekey
                  left join pos on saleorder.poskey=pos.poskey""" + conditions

            sqlst = sqlst +  """ group by saleorderdate , store.storename, pos.posname , product.productname,
                   product.barcode, categoryname, brandname, vendorname
                  """

            cursor.execute(sqlst)
            productdetails=cursor.fetchall()



            if request.form['btnview']=='btnprint':
                options = {
                    "enable-local-file-access": None
                }
                rendered =  render_template('reportprint.html', form=mydailysalereportform ,productdetails=productdetails)
                from pdfkit import pdfkit
                pdf = pdfkit.from_string(rendered, False,  options=options)
                response=make_response(pdf)
                response.headers['Content-Type']='application/pdf'
                response.headers['Content-Disposition'] = 'attachment; filename=output.pdf'
                return response

            if request.form['btnview'] == 'btnview':
                return render_template('dailysalereport.html', form=mydailysalereportform, productdetails=productdetails)



        if request.method=='GET':
            return render_template('dailysalereport.html', form=mydailysalereportform )
    else:
        return redirect (url_for('login'))

