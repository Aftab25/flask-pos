import MySQLdb
from flask import Blueprint, render_template, request, session, flash, redirect, url_for, jsonify
from flask_mysqldb import MySQL
from forms import POSForm, CategoryForm, CategorySearchForm

category_bp = Blueprint('category_bp', __name__, template_folder='templates')


@category_bp.route('/searchcategory',  methods=['GET','POST'])
def searchcategory():
    from app import mysql
    if 'usersessionid' in session:
        mycategorysearchform=CategorySearchForm(request.form)

        if request.method=='POST':
            try:
                categoryid= request.form['categoryid']
                categoryname = request.form['categoryname']
                conditions = ' where 1=1 '
                if (len(categoryid) > 0):
                    conditions = conditions + " and category.categoryid = '" + categoryid + "'"
                if (len(categoryname) > 0):
                    conditions = conditions + " and category.categoryname = '" + categoryname + "'"
                cursor=mysql.connection.cursor(cursorclass=MySQLdb.cursors.DictCursor)
                sqlst="""select * from category  """ + conditions
                # print (sqlst)
                cursor.execute(sqlst)
                productdetails=cursor.fetchall()
            except Exception as err:
                print (err)
            return render_template('categorysearch.html', form=mycategorysearchform ,productdetails=productdetails)

        if request.method=='GET':
            try:
                cursor=mysql.connection.cursor(cursorclass=MySQLdb.cursors.DictCursor)
                sqlst="""select * from category
                 order by category.categorykey
                 """
                cursor.execute(sqlst)
                productdetails=cursor.fetchall()
            except Exception as err:
                print (err)
            return render_template('categorysearch.html', form=mycategorysearchform ,productdetails=productdetails)
    else:
        return redirect (url_for('login'))




@category_bp.route('/getcategories', methods=['GET', 'POST'])
def getcategories():
    if 'usersessionid' in session:
        if request.method=='GET':
            from app import mysql
            cursor = mysql.connection.cursor()
            sqlst = """ select categorykey, categoryname from category"""
            cursor.execute(sqlst)
            categorieslist = cursor.fetchall()
            # print (saleorderdetails)
            return jsonify(categorieslist)
    else:
        return redirect (url_for('login'))


@category_bp.route('/category', methods=['GET','POST', 'PUT'])
def category():
    from app import mysql
    mycategoryform = CategoryForm(request.form)
    if 'usersessionid' in session:

        if request.method=='POST':
            # Process Form
            categoryid = request.form['categoryid']
            categoryname= request.form['categoryname']
            cursor = mysql.connection.cursor()
            cursor.execute("insert into category (categoryid ,categoryname) values (%s,%s) " ,  ([categoryid], [categoryname]))
            mysql.connection.commit()
            cursor.close()
            flash( 'Category Added')
            return redirect(url_for('category'))

        if request.method == 'GET' and request.args.get('categorykey'):
            # Called in searchcategory
            categorykey = request.args.get('categorykey')
            cursor = mysql.connection.cursor(cursorclass=MySQLdb.cursors.DictCursor)
            sqlst = """ select * from category where categorykey=%s"""
            values = [(categorykey)]
            cursor.execute(sqlst, values)
            productdetails = cursor.fetchall()
            # print (saleorderdetails)
            return jsonify(productdetails)
        if request.method == 'PUT':
            data = request.get_data()
            data2=data.decode("utf-8")
            data2 =  data2.split('&')

            categoryid = data2[0]
            categorykey = data2[1]
            categoryname = data2[2]

            categoryid = categoryid.split('=')
            categoryid = categoryid[1]

            categorykey = categorykey.split('=')
            categorykey = categorykey[1]

            categoryname = categoryname.split('=')
            categoryname = categoryname[1]

            cursor = mysql.connection.cursor()
            sqlst = """update category set categoryname=%s, categoryid=%s
            where categorykey=%s
            """
            values = [(categoryname), (categoryid), (categorykey)]
            # print (values)
            cursor.execute(sqlst, values)
            mysql.connection.commit()
            cursor.close()
            return ('Category Updated')
        else:
            return render_template('category.html', form=mycategoryform)
    else:
        return redirect (url_for('login'))

