from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, IntegerField, DateField, DecimalField
from wtforms.validators import  DataRequired, ValidationError
from wtforms.fields.html5 import DateField

class BrandForm (FlaskForm):
   brandid=StringField('Brand ID',  id='brandid', validators=[DataRequired()])
   brandname = StringField('Brand Name', id='brandname', validators=[DataRequired()])


class WarehouseForm (FlaskForm):
   warehouseid=StringField('Warehouse ID',  id='warehouseid', validators=[DataRequired()])
   warehousename=StringField('Warehouse Name',  id='warehousename', validators=[DataRequired()])

def validate_store (form, field):
   if field.data==0:
      raise ValidationError('Please select a Store')

def validate_pos (form, field):
   if field.data==0:
      raise ValidationError('Please select a POS')


class VendorForm (FlaskForm):
   vendorid=StringField('Vendor ID',  id='vendorid', validators=[DataRequired()])
   vendorname = StringField('Vendor Name', id='vendorname', validators=[DataRequired()])

class CategoryForm(FlaskForm):
   categoryid = StringField('Category ID', id='categoryid', validators=[DataRequired()])
   categoryname = StringField('Category Name', id='categoryname', validators=[DataRequired()])


def validate_warehouse (form, field):
   if field.data==0:
      raise ValidationError('Please select a Warehouse')


def validate_customer (form, field):
   if field.data==0:
      raise ValidationError('Please select a Customer')


class StoreForm(FlaskForm):
   storeid = StringField('Store ID', id='storeid', validators=[DataRequired()])
   storename = StringField('Store Name', id='storename', validators=[DataRequired()])
   warehousename = SelectField('Warehouse', coerce=int, id='warehousename', choices='', validators=[validate_warehouse])
   defaultcustomername = SelectField('Default Customer', coerce=int, id='defaultcustomername', choices='', validators=[validate_customer])


class POSForm(FlaskForm):
   posid = StringField('POS ID', id='posid', validators=[DataRequired()])
   posname = StringField('POS Name', id='posname', validators=[DataRequired()])
   storename = SelectField('Store', coerce=int, id='storename', choices='', validators=[validate_store])




def validate_brand (form, field):
   if field.data==0:
      raise ValidationError('Please select a Brand')

def validate_category (form, field):
   if field.data==0:
      raise ValidationError('Please select a Category')

def validate_vendor (form, field):
   if field.data==0:
      raise ValidationError('Please select a Vendor')

def validate_customer (form, field):
   if field.data==0:
      raise ValidationError('Please select a Customer')


class ProductForm (FlaskForm):
   productid = StringField('Product ID', id='productid', validators=[DataRequired()])
   productname=StringField('Product Name', id='productname' , validators=[DataRequired()])
   brandname=SelectField('Brand Name', coerce=int,  id='brandname', choices='',  validators=[validate_brand])
   categoryname = SelectField('Category Name', coerce=int, id='categoryname', choices='', validators=[validate_category])
   vendorname = SelectField('Vendor Name', coerce=int, id='vendorname', choices='', validators=[validate_vendor])
   saleprice=DecimalField('Sale Price', id='saleprice', validators=[DataRequired()])
   barcode= StringField('Barcode', id='barcode', validators=[DataRequired()])


class SaleForm (FlaskForm):
   barcode= StringField('Barcode', id='barcode', validators=[DataRequired()])
   productname=StringField('Product Name', id='productname', validators=[DataRequired()])
   quantity=IntegerField('Quantity', id='quantity', validators=[DataRequired()])
   saleprice=DecimalField('Sale Price', id='saleprice', validators=[DataRequired()])
   linetotal=DecimalField('Line Total', id='linetotal', validators=[DataRequired()])
   grandtotal = DecimalField('Grand Total', id='grandtotal', validators=[DataRequired()])
   customername = SelectField('Customer Name', coerce=int, id='customername', choices='', validators=[validate_customer])
   saledate = DateField('Sale Date', id='saledate', format='%Y-%m-%d', default=datetime.now() , validators=[DataRequired()])


class GoodsIssueForm (FlaskForm):
   barcode= StringField('Barcode', id='barcode', validators=[DataRequired()])
   productname=StringField('Product Name', id='productname', validators=[DataRequired()])
   quantity=IntegerField('Quantity', id='quantity', validators=[DataRequired()])
   saleprice=DecimalField('Sale Price', id='saleprice', validators=[DataRequired()])
   linetotal=DecimalField('Line Total', id='linetotal', validators=[DataRequired()])
   grandtotal = DecimalField('Grand Total', id='grandtotal', validators=[DataRequired()])
   warehousename = SelectField('Warehouse Name', coerce=int, id='warehousename', choices='', validators=[validate_warehouse])
   goodsissuedate = DateField('Issue Date', id='goodsissuedate', format='%Y-%m-%d', default=datetime.now() , validators=[DataRequired()])
   reason=StringField('Reason', id='reason', validators=[DataRequired()])



class GRPOForm (FlaskForm):
   barcode= StringField('Barcode', id='barcode', validators=[DataRequired()])
   productname=StringField('Product Name', id='productname', validators=[DataRequired()])
   quantity=IntegerField('Quantity', id='quantity', validators=[DataRequired()])
   purchaseprice=DecimalField('Purchase Price', id='purchaseprice', validators=[DataRequired()])
   linetotal=DecimalField('Line Total', id='linetotal', validators=[DataRequired()])
   grandtotal = DecimalField('Grand Total', id='grandtotal', validators=[DataRequired()])
   warehousename = SelectField('Warehouse Name', coerce=int, id='warehousename', choices='', validators=[validate_warehouse])
   vendorname = SelectField('Vendor Name', coerce=int, id='vendorname', choices='', validators=[validate_vendor])
   orderdate = DateField('Order Date', id='orderdate', format='%Y-%m-%d',default=datetime.now() , validators=[DataRequired()])
   receiptdate = DateField('Receipt Date', id='receiptdate', format='%Y-%m-%d',default=datetime.now() , validators=[DataRequired()])
   status = StringField('Status', id='status', validators=[DataRequired()])


class GoodsReceiptForm (FlaskForm):
   barcode= StringField('Barcode', id='barcode', validators=[DataRequired()])
   productname=StringField('Product Name', id='productname', validators=[DataRequired()])
   quantity=IntegerField('Quantity', id='quantity', validators=[DataRequired()])
   purchaseprice=DecimalField('Purchase Price', id='purchaseprice', validators=[DataRequired()])
   linetotal=DecimalField('Line Total', id='linetotal', validators=[DataRequired()])
   grandtotal = DecimalField('Grand Total', id='grandtotal', validators=[DataRequired()])
   warehousename = SelectField('Warehouse Name', coerce=int, id='warehousename', choices='', validators=[validate_warehouse])
   reason=StringField('Reason', id='reason', validators=[DataRequired()])
   receiptdate = DateField('Receipt Date', id='receiptdate', format='%Y-%m-%d',default=datetime.now() , validators=[DataRequired()])





class RefundForm(FlaskForm):
   saleorderkey = IntegerField('SaleOrderKey', id='saleorderkey' , validators=[DataRequired()])
   refunddate = DateField('Refund Date', id='refunddate', format='%Y-%m-%d', default=datetime.now(), validators=[DataRequired()])
   grandtotal = DecimalField('Grand Total', id='grandtotal', validators=[DataRequired()])




class ProductSearchForm (FlaskForm):
   productid = StringField('Product ID', id='productid')
   productname=StringField('Product Name', id='productname' )
   brandname=SelectField('Brand Name', coerce=int,  id='brandname', choices='')
   categoryname = SelectField('Category Name', coerce=int, id='categoryname', choices='')
   vendorname = SelectField('Vendor Name', coerce=int, id='vendorname', choices='')
   saleprice=DecimalField('Sale Price', id='saleprice')
   barcode= StringField('Barcode', id='barcode')




class InventorySearchForm (FlaskForm):
   productname=StringField('Product Name', id='productname' )
   brandname=SelectField('Brand Name', coerce=int,  id='brandname', choices='')
   categoryname = SelectField('Category Name', coerce=int, id='categoryname', choices='')
   vendorname = SelectField('Vendor Name', coerce=int, id='vendorname', choices='')
   warehousename = SelectField('Warehouse Name', coerce=int, id='warehousename', choices='')
   saleprice=DecimalField('Sale Price', id='saleprice')
   barcode= StringField('Barcode', id='barcode')





class CustomerSearchForm (FlaskForm):
   customerid=StringField('Customer ID', id='customerid' )
   customername = StringField('Customer Name', id='customername')


class POSSearchForm (FlaskForm):
   posid=StringField('POS ID', id='posid' )
   posname = StringField('POS Name', id='posname')
   storename = SelectField('Store Name', coerce=int, id='storename', choices='')

class WarehouseSearchForm (FlaskForm):
   warehouseid=StringField('Warehouse ID', id='warehouseid' )
   warehousename = StringField('Warehouse Name', id='warehousename')

class CategorySearchForm (FlaskForm):
   categoryid=StringField('Category ID', id='categoryid' )
   categoryname = StringField('Category Name', id='categoryname')

class BrandSearchForm (FlaskForm):
   brandid=StringField('Brand ID', id='brandid' )
   brandname = StringField('Brand Name', id='brandname')

class VendorSearchForm (FlaskForm):
   vendorid=StringField('Vendor ID', id='vendorid' )
   vendorname = StringField('Vendor Name', id='vendorname')


class StoreSearchForm(FlaskForm):
   storeid = StringField('Store ID', id='storeid')
   storename = StringField('Store Name', id='storename')
   warehousename = SelectField('Warehouse', coerce=int, id='warehousename', choices='')
   defaultcustomername = SelectField('Default Customer', coerce=int, id='defaultcustomername', choices='')





class SaleOrderSearchForm (FlaskForm):
   startdate = DateField('Start Date', id='startdate', format='%Y-%m-%d')
   enddate = DateField('End Date', id='enddate', format='%Y-%m-%d')
   productname=StringField('Product Name', id='productname' )
   brandname=SelectField('Brand Name', coerce=int,  id='brandname', choices='')
   categoryname = SelectField('Category Name', coerce=int, id='categoryname', choices='')
   vendorname = SelectField('Vendor Name', coerce=int, id='vendorname', choices='')
   customername = SelectField('Customer Name', coerce=int, id='customername', choices='')
   saleprice=DecimalField('Sale Price', id='saleprice')
   barcode= StringField('Barcode', id='barcode')



class DailySaleReportForm (FlaskForm):
   startdate = DateField('Start Date', id='startdate', format='%Y-%m-%d')
   enddate = DateField('End Date', id='enddate', format='%Y-%m-%d')
   storename=SelectField('Store Name', coerce=int,  id='storename', choices='')
   posname = SelectField('POS Name', coerce=int, id='posname', choices='')







class GoodsIssueSearchForm (FlaskForm):
   startdate = DateField('Start Date', id='startdate', format='%Y-%m-%d')
   enddate = DateField('End Date', id='enddate', format='%Y-%m-%d')
   productname=StringField('Product Name', id='productname' )
   brandname=SelectField('Brand Name', coerce=int,  id='brandname', choices='')
   categoryname = SelectField('Category Name', coerce=int, id='categoryname', choices='')
   vendorname = SelectField('Vendor Name', coerce=int, id='vendorname', choices='')
   warehousename = SelectField('Warehouse Name', coerce=int, id='warehousename', choices='')
   saleprice=DecimalField('Sale Price', id='saleprice')
   barcode= StringField('Barcode', id='barcode')



class GRPOSearchForm (FlaskForm):
   startdate = DateField('Start Date', id='startdate', format='%Y-%m-%d')
   enddate = DateField('End Date', id='enddate', format='%Y-%m-%d')
   productname=StringField('Product Name', id='productname' )
   brandname=SelectField('Brand Name', coerce=int,  id='brandname', choices='')
   categoryname = SelectField('Category Name', coerce=int, id='categoryname', choices='')
   vendorname = SelectField('Vendor Name', coerce=int, id='vendorname', choices='')
   warehousename = SelectField('Warehouse Name', coerce=int, id='warehousename', choices='')
   purchaseprice=DecimalField('Purchase Price', id='purchaseprice')
   barcode= StringField('Barcode', id='barcode')



class GoodsReceiptSearchForm (FlaskForm):
   startdate = DateField('Start Date', id='startdate', format='%Y-%m-%d')
   enddate = DateField('End Date', id='enddate', format='%Y-%m-%d')
   productname=StringField('Product Name', id='productname' )
   brandname=SelectField('Brand Name', coerce=int,  id='brandname', choices='')
   categoryname = SelectField('Category Name', coerce=int, id='categoryname', choices='')
   vendorname = SelectField('Vendor Name', coerce=int, id='vendorname', choices='')
   warehousename = SelectField('Warehouse Name', coerce=int, id='warehousename', choices='')
   purchaseprice=DecimalField('Purchase Price', id='purchaseprice')
   barcode= StringField('Barcode', id='barcode')




class RefundOrderSearchForm (FlaskForm):
   startdate = DateField('Start Date', id='startdate', format='%Y-%m-%d')
   enddate = DateField('End Date', id='enddate', format='%Y-%m-%d')
   saleorderkey=StringField('Sale Order Number', id='saleorderkey' )
   productname=StringField('Product Name', id='productname' )
   brandname=SelectField('Brand Name', coerce=int,  id='brandname', choices='')
   categoryname = SelectField('Category Name', coerce=int, id='categoryname', choices='')
   vendorname = SelectField('Vendor Name', coerce=int, id='vendorname', choices='')
   saleprice=DecimalField('Sale Price', id='saleprice')
   barcode= StringField('Barcode', id='barcode')



class CustomerForm (FlaskForm):
   customerid = StringField('Customer ID', id='customerid', validators=[DataRequired()])
   customername=StringField('Customer Name', id='customername' , validators=[DataRequired()])




class LoginForm (FlaskForm):
   username=StringField ('User Name', id='username', validators=[DataRequired()])
   userpassword = StringField('User Password', id='userpassword', validators=[DataRequired()])
   storename=SelectField('Store Name', coerce=int,  id='storename', choices='',  validators=[validate_store])
   posname = SelectField('POS Name', coerce=int, id='posname', choices='', validators=[validate_pos])
