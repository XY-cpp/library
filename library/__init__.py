import os
import pymysql

from flask import Flask

app = Flask(__name__)
app.secret_key = "asjdlfjasldjf"

from . import controller
