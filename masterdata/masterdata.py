from random import randint

import MySQLdb
from flask import Blueprint, render_template, request, session, flash, redirect, url_for, jsonify
from flask_mysqldb import MySQL

from forms import POSForm, LoginForm

masterdata_bp = Blueprint('masterdata_bp', __name__)





























