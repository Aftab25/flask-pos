import json
import MySQLdb
from flask import Blueprint, render_template, request, session, flash, redirect, url_for, jsonify
from forms import LoginForm, BrandForm, ProductForm, SaleForm,  ProductSearchForm
from misc.misc import DecimalEncoder

products_bp = Blueprint('products_bp', __name__, template_folder='templates')
from flask_mysqldb import MySQL

@products_bp.route('/product', methods=['GET','POST','PUT'])
def product():
    myproductform = ProductForm(request.form)
    from app import mysql
    cursor = mysql.connection.cursor()
    cursor.execute("select brandkey, brandname from brand union all select 0, 'Select Brand' order by brandkey ")
    allbrands=cursor.fetchall()
    myproductform.brandname.choices = allbrands

    cursor.execute("select vendorkey, vendorname from vendor union all select 0, 'Select Vendor' order by vendorkey ")
    allvendors = cursor.fetchall()
    myproductform.vendorname.choices = allvendors

    cursor.execute("select categorykey, categoryname from category union all select 0, 'Select Category' order by categorykey ")
    allcategories = cursor.fetchall()
    myproductform.categoryname.choices = allcategories

    if 'usersessionid' in session:
        if myproductform.validate_on_submit():
            if request.method=='POST':
                usersessionid=session['usersessionid']
                productid = request.form['productid']
                productname=request.form['productname']
                brandkey= request.form['brandname']
                categorykey = request.form['categoryname']
                vendorkey = request.form['vendorname']
                saleprice = request.form['saleprice']
                barcode = request.form['barcode']
                cursor = mysql.connection.cursor()
                sqlst="""insert into product (usersessionid , productid , productname, brandkey, categorykey, 
                vendorkey, saleprice, barcode) 
                values (%s,%s, %s, %s, %s,%s,%s,%s)"""
                values = [(usersessionid), (productid) , (productname), (brandkey), (categorykey), (vendorkey), (saleprice), (barcode)]
                cursor.execute(sqlst, values)
                # get latest product key
                sqlst = "select productkey from product where usersessionid=%s and productkey=(select LAST_INSERT_ID())"
                myvalues = [(usersessionid)]
                cursor.execute(sqlst, myvalues)
                productkey = cursor.fetchall()
                # add product to all warehouses
                sqlst="""select warehousekey from warehouse"""
                cursor.execute(sqlst)
                recs=cursor.rowcount
                warehouselist=cursor.fetchall()
                for i in range(recs):
                    sqlst = "insert into inventory (productkey, warehousekey, onhandquantity) values (%s, %s, 0)"
                    values=[(productkey), (warehouselist[i][0])]
                    cursor.execute(sqlst, values)
                mysql.connection.commit()
                cursor.close()
                flash( 'Product Added')
                return redirect(url_for('product'))

        if request.method == 'GET' and request.args.get('productkey'):
            productkey = request.args.get('productkey')
            cursor = mysql.connection.cursor(cursorclass=MySQLdb.cursors.DictCursor)
            sqlst = """ select * from product where productkey=%s"""
            values = (productkey)
            cursor.execute(sqlst, values)
            productdetails = cursor.fetchall()
            return json.dumps(productdetails, cls=DecimalEncoder)

        if request.method == 'PUT':
            data = request.get_data()
            data2=data.decode("utf-8")
            data2 =  data2.split('&')

            productkey = data2[0]
            productid = data2[1]
            barcode = data2[2]
            productname = data2[3]
            saleprice = data2[4]
            brandkey = data2[5]
            categorykey = data2[6]
            vendorkey = data2[7]

            productid = productid.split('=')
            productid = productid[1]

            productname = productname.split('=')
            productname=productname[1]

            brandkey = brandkey.split('=')
            brandkey = brandkey[1]

            categorykey = categorykey.split('=')
            categorykey = categorykey[1]

            vendorkey = vendorkey.split('=')
            vendorkey = vendorkey[1]

            saleprice = saleprice.split('=')
            saleprice = saleprice[1]

            barcode = barcode.split('=')
            barcode = barcode[1]

            productkey = productkey.split('=')
            productkey = productkey[1]

            cursor = mysql.connection.cursor()
            sqlst = """update product set productid=%s,  productname=%s, brandkey=%s, categorykey=%s, vendorkey=%s, 
            barcode=%s , saleprice=%s where productkey=%s"""
            values = [(productid), (productname), (brandkey), (categorykey), (vendorkey), (barcode), (saleprice),
                      (productkey)]
            cursor.execute(sqlst, values)
            mysql.connection.commit()
            cursor.close()
            return ('Product Updated')
        else:
            return render_template('product.html', form=myproductform)
    else:
        return redirect (url_for('products_bp.login'))


@products_bp.route('/searchproductname', methods=['GET','POST'])
def searchproductname():
    mysaleform=SaleForm(request.form)
    myloginform=LoginForm(request.form)
    if 'usersessionid' in session:
        if request.method=='POST':
            try:
                barcode= request.form['barcode']
                from app import mysql
                cursor=mysql.connection.cursor()
                sqlst="select productname from product where barcode=%s"
                myval=[(barcode)]
                cursor.execute(sqlst, myval)
                productdetails=cursor.fetchall()
            except Exception as err:
                print (err)
            return jsonify (productdetails)
        else:
            return render_template('sale2.html', form=mysaleform)
    else:
        return redirect (url_for('login'))


@products_bp.route('/searchproductprice', methods=['GET','POST'])
def searchproductprice():
    if 'usersessionid' in session:
        if request.method=='POST':
            try:
                barcode= request.form['barcode']
                from app import mysql
                cursor=mysql.connection.cursor()
                sqlst="select saleprice from product where barcode=%s"
                myval=[(barcode)]
                cursor.execute(sqlst, myval)
                productdetails=cursor.fetchall()
            except Exception as err:
                print (err)
            return json.dumps(productdetails, cls=DecimalEncoder)
            # return jsonify(productdetails)
    else:
        return redirect (url_for('login'))

@products_bp.route('/searchproductalldata',  methods=['GET','POST'])
def searchproductalldata():
    if 'usersessionid' in session:
        myproductsearchform=ProductSearchForm(request.form)
        from app import mysql
        cursor = mysql.connection.cursor()
        cursor.execute("select brandkey, brandname from brand union all select 0, 'Select Brand' order by brandkey ")
        allbrands = cursor.fetchall()
        myproductsearchform.brandname.choices = allbrands

        cursor.execute("select vendorkey, vendorname from vendor union all select 0, 'Select Vendor' order by vendorkey ")
        allvendors = cursor.fetchall()
        myproductsearchform.vendorname.choices = allvendors

        cursor.execute(
            "select categorykey, categoryname from category union all select 0, 'Select Category' order by categorykey ")
        allcategories = cursor.fetchall()
        myproductsearchform.categoryname.choices = allcategories


        if request.method=='POST':
            try:
                categorykey= request.form['categoryname']
                vendorkey = request.form['vendorname']
                brandkey = request.form['brandname']
                barcode = request.form['barcode']
                productname = request.form['productname']
                productid = request.form['productid']

                conditions = ' where 1=1 '

                if (int(categorykey) > 0):
                    conditions = conditions + " and product.categorykey = '" + categorykey + "'"

                if (int(vendorkey) > 0):
                    conditions = conditions + " and product.vendorkey = '" + vendorkey + "'"

                if (int(brandkey) > 0):
                    conditions = conditions + " and product.brandkey = '" + brandkey + "'"

                if (len(productname)>0) :
                    conditions = conditions + " and product.productname = '" + productname + "'"

                if (len(productid)>0) :
                    conditions = conditions + " and product.productid = '" + productid + "'"

                if (len(barcode)>0) :
                    conditions = conditions + " and product.barcode = '" + barcode + "'"


                print (conditions)

                cursor=mysql.connection.cursor(cursorclass=MySQLdb.cursors.DictCursor)
                sqlst="""select productid , productkey , barcode, productname,  categoryname, saleprice , brandname, vendorname from product
                left join category on product.categorykey=category.categorykey
                left join brand on product.brandkey=brand.brandkey
                left join vendor on product.vendorkey=vendor.vendorkey
                """ + conditions

                # print (sqlst)

                cursor.execute(sqlst)

                productdetails=cursor.fetchall()
            except Exception as err:
                print (err)
            return render_template('productsearch.html', form=myproductsearchform ,productdetails=productdetails)

        if request.method=='GET':
            try:
                cursor=mysql.connection.cursor(cursorclass=MySQLdb.cursors.DictCursor)
                sqlst="""select productid , productkey , barcode, productname,  categoryname, saleprice , brandname, vendorname from product
                left join category on product.categorykey=category.categorykey
                left join brand on product.brandkey=brand.brandkey
                left join vendor on product.vendorkey=vendor.vendorkey
                order by barcode """

                cursor.execute(sqlst)
                productdetails=cursor.fetchall()
            except Exception as err:
                print (err)
            return render_template('productsearch.html', form=myproductsearchform ,productdetails=productdetails)
    else:
        return redirect (url_for('login'))

