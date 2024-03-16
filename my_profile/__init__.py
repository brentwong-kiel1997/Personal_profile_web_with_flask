from flask import Flask, url_for
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SECRET_KEY'] = '7b67c2145e61ce351ca20887'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

from my_profile import routes