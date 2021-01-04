from flask import Flask
from flask_sqlalchemy import SQLAlchemy
#import flask.ext.whooshalchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///site.db'
app.secret_key = "hello"
db = SQLAlchemy(app)

from ChessOpens import views, models, initialize_db