from flask import Flask
from auth.auth import auth_bp
from brand.brand import brand_bp
from category.category import category_bp
from customer.customer import customer_bp
from goodsissue.goodsissue import goodsissue_bp
from goodsreceipt.goodsreceipt import goodsreceipt_bp
from grpo.grpo import grpo_bp
from masterdata.masterdata import masterdata_bp
from misc.misc import misc_bp
from pos.pos import pos_bp
from product.product import products_bp
from extensions import mysql
from refund.refund import refund_bp
from sale.sale import sale_bp
from store.store import store_bp
from vendor.vendor import vendor_bp
from warehouse.warehouse import warehouse_bp


def create_app():
    app = Flask(__name__)
    app.config['MYSQL_HOST'] = "localhost"
    app.config['MYSQL_USER'] = "root"
    app.config['MYSQL_PASSWORD'] = "Pass"
    app.config['MYSQL_DB'] = "pos"
    app.config['SECRET_KEY'] = '\xfd{H\xe5<\x95\xf9\xe3\x96.5\xd1\x01O<!\xd5\xa2\xa0\x9fR"\xa1\xa8'
    # app.config['EXPLAIN_TEMPLATE_LOADING'] = True
    register_extensions(app)
    app.register_blueprint(auth_bp)
    app.register_blueprint(brand_bp)
    app.register_blueprint(category_bp)
    app.register_blueprint(customer_bp)
    app.register_blueprint(grpo_bp)
    app.register_blueprint(goodsissue_bp)
    app.register_blueprint(goodsreceipt_bp)
    app.register_blueprint(misc_bp)
    app.register_blueprint(masterdata_bp)
    app.register_blueprint(products_bp)
    app.register_blueprint(pos_bp)
    app.register_blueprint(refund_bp)
    app.register_blueprint(sale_bp)
    app.register_blueprint(store_bp)
    app.register_blueprint(vendor_bp)
    app.register_blueprint(warehouse_bp)
    return app


def register_extensions(app):
    mysql.init_app(app)

