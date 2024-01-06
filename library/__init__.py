import os
import pymysql

from flask import Flask

app = Flask(__name__)


def init_db(host, port, username, password, database):
    from library.db import Sql
    Sql.host = host
    Sql.port = port
    Sql.username = username
    Sql.password = password
    Sql.database = database

import library.auth