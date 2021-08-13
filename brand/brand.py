import MySQLdb
import json
from flask import Blueprint, render_template, request, session, flash, redirect, url_for, jsonify
from forms import BrandSearchForm, BrandForm

brand_bp = Blueprint('brand_bp', __name__, template_folder='templates')


@brand_bp.route('/searchbrand', methods=['GET', 'POST'])
def searchbrand():
    from app import mysql
    if 'usersessionid' in session:
        mybrandsearchform = BrandSearchForm(request.form)
        if request.method == 'POST':
            try:
                brandid = request.form['brandid']
                brandname = request.form['brandname']
                conditions = ' where 1=1 '
                if (len(brandid) > 0):
                    conditions = conditions + " and brand.brandid = '" + brandid + "'"
                if (len(brandname) > 0):
                    conditions = conditions + " and brand.brandname = '" + brandname + "'"
                cursor = mysql.connection.cursor(cursorclass=MySQLdb.cursors.DictCursor)
                sqlst = """select * from brand  """ + conditions
                # print (sqlst)
                cursor.execute(sqlst)
                productdetails = cursor.fetchall()
            except Exception as err:
                print(err)
            return render_template('brandsearch.html', form=mybrandsearchform, productdetails=productdetails)

        if request.method == 'GET':
            try:
                cursor = mysql.connection.cursor(cursorclass=MySQLdb.cursors.DictCursor)
                sqlst = """select * from brand order by brand.brandkey """
                cursor.execute(sqlst)
                productdetails = cursor.fetchall()
            except Exception as err:
                print(err)
            return render_template('brandsearch.html', form=mybrandsearchform, productdetails=productdetails)
    else:
        return redirect(url_for('login'))


@brand_bp.route('/getbrands', methods=['GET', 'POST'])
def getbrands():
    if 'usersessionid' in session:
        if request.method == 'GET':
            from app import mysql
            cursor = mysql.connection.cursor()
            sqlst = """ select brandkey, brandname from brand"""
            cursor.execute(sqlst)
            brandslist = cursor.fetchall()
            # print (saleorderdetails)
            return jsonify(brandslist)
    else:
        return redirect(url_for('login'))


@brand_bp.route('/brand', methods=['GET', 'POST', 'PUT'])
def brand():
    from app import mysql
    myform = BrandForm(request.form)
    if 'usersessionid' in session:

        if request.method == 'POST':
            brandid = request.form['brandid']
            brandname = request.form['brandname']
            cursor = mysql.connection.cursor()
            cursor.execute("insert into brand (brandid, brandname) values (%s, %s) ", ([brandid], [brandname]))
            mysql.connection.commit()
            cursor.close()
            flash('Brand Added')
            return redirect(url_for('brand_bp.brand'))

        if request.method == 'PUT':
            data = request.get_data()
            data2=data.decode("utf-8")
            data2 =  data2.split('&')

            brandid = data2[0]
            brandkey = data2[1]
            brandname = data2[2]

            brandid = brandid.split('=')
            brandid = brandid[1]

            brandkey = brandkey.split('=')
            brandkey=brandkey[1]

            brandname = brandname.split('=')
            brandname = brandname[1]

            cursor = mysql.connection.cursor()
            sqlst = """update brand set brandname=%s, brandid=%s where brandkey=%s """
            values = [(brandname), (brandid), (brandkey)]
            cursor.execute(sqlst, values)
            mysql.connection.commit()
            cursor.close()
            return ('Brand Updated')

        if request.method == 'GET' and request.args.get('brandkey'):
            brandkey = request.args.get('brandkey')
            cursor = mysql.connection.cursor(cursorclass=MySQLdb.cursors.DictCursor)
            sqlst = """ select * from brand where brandkey=%s"""
            values = [(brandkey)]
            cursor.execute(sqlst, values)
            productdetails = cursor.fetchall()
            return jsonify(productdetails)
        else:
            return render_template('brand.html', form=myform)
    else:
        return redirect(url_for('login'))
