import decimal
import json
import MySQLdb
from flask import Blueprint, render_template, request, session, flash, redirect, url_for, jsonify
from forms import InventorySearchForm

misc_bp = Blueprint('misc_bp', __name__, template_folder='templates')

@misc_bp.route('/getinventory', methods=['GET','POST'])
def getinventory():
    if 'usersessionid' in session:
        if request.method=='POST':
            barcode= request.form['barcode']
            from app import mysql
            cursor = mysql.connection.cursor()
            sqlst="""select onhandquantity from product left join inventory on product.productkey=inventory.productkey
            where barcode=%s and  warehousekey= %s """
            values = [(barcode), (session['warehousekey'])]
            cursor.execute(sqlst , values )
            onhandquantity=cursor.fetchall()
            return  jsonify(onhandquantity)
    else:
        return redirect (url_for('login'))



@misc_bp.route('/searchinventory',  methods=['GET','POST'])
def searchinventory():
    if 'usersessionid' in session:
        myinventorysearchform=InventorySearchForm(request.form)
        from app import mysql
        cursor = mysql.connection.cursor()
        cursor.execute("select brandkey, brandname from brand union all select 0, 'Select Brand' order by brandkey ")
        allbrands = cursor.fetchall()
        myinventorysearchform.brandname.choices = allbrands
        cursor.execute("select vendorkey, vendorname from vendor union all select 0, 'Select Vendor' order by vendorkey ")
        allvendors = cursor.fetchall()
        myinventorysearchform.vendorname.choices = allvendors
        cursor.execute(
            "select categorykey, categoryname from category union all select 0, 'Select Category' order by categorykey ")
        allcategories = cursor.fetchall()
        myinventorysearchform.categoryname.choices = allcategories
        cursor.execute(
            "select warehousekey, warehousename from warehouse union all select 0, 'Select Warehouse' order by warehousekey ")
        allwarehouses = cursor.fetchall()
        myinventorysearchform.warehousename.choices = allwarehouses
        if request.method=='POST':
            try:
                categorykey= request.form['categoryname']
                vendorkey = request.form['vendorname']
                brandkey = request.form['brandname']
                warehousekey = request.form['warehousename']
                barcode = request.form['barcode']
                productname = request.form['productname']
                saleprice = request.form['saleprice']
                conditions = ' where 1=1 '
                if (int(categorykey) > 0):
                    conditions = conditions + " and product.categorykey = '" + categorykey + "'"
                if (int(vendorkey) > 0):
                    conditions = conditions + " and product.vendorkey = '" + vendorkey + "'"
                if (int(brandkey) > 0):
                    conditions = conditions + " and product.brandkey = '" + brandkey + "'"
                if (int(warehousekey) > 0):
                    conditions = conditions + " and inventory.warehousekey = '" + warehousekey + "'"
                if (len(productname)>0) :
                    conditions = conditions + " and product.productname = '" + productname + "'"
                if (len(barcode)>0) :
                    conditions = conditions + " and product.barcode = '" + barcode + "'"
                if (len(saleprice)>0) :
                    conditions = conditions + " and product.saleprice = '" + saleprice + "'"
                cursor=mysql.connection.cursor(cursorclass=MySQLdb.cursors.DictCursor)
                sqlst="""select product.productkey , barcode, productname,  categoryname, saleprice , brandname,
                vendorname , warehousename, onhandquantity
                from product
                left join inventory on product.productkey =  inventory.productkey
                left join warehouse on inventory.warehousekey=warehouse.warehousekey
                left join category on product.categorykey=category.categorykey
                left join brand on product.brandkey=brand.brandkey
                left join vendor on product.vendorkey=vendor.vendorkey
                """ + conditions
                cursor.execute(sqlst)
                productdetails=cursor.fetchall()
            except Exception as err:
                print (err)
            return render_template('inventorysearch.html', form=myinventorysearchform ,productdetails=productdetails)
        if request.method=='GET':
            try:
                cursor=mysql.connection.cursor(cursorclass=MySQLdb.cursors.DictCursor)
                sqlst="""select product.productkey , barcode, productname,  categoryname, saleprice , brandname, vendorname
                 , warehousename, onhandquantity from product
                left join inventory on product.productkey=inventory.productkey
                left join warehouse on  inventory.warehousekey=warehouse.warehousekey
                left join category on product.categorykey=category.categorykey
                left join brand on product.brandkey=brand.brandkey
                left join vendor on product.vendorkey=vendor.vendorkey
                order by barcode """
                cursor.execute(sqlst)
                productdetails=cursor.fetchall()
            except Exception as err:
                print (err)
            return render_template('inventorysearch.html', form=myinventorysearchform ,productdetails=productdetails)
    else:
        return redirect (url_for('login'))

class DecimalEncoder(json.JSONEncoder):
    def default(self,o):
        if isinstance(o,decimal.Decimal):
            return str(o)
        return super(DecimalEncoder,self).default(o)
