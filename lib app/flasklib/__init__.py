from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__,template_folder='html')
app.config['SECRET_KEY']='8959cf7e6213c0ced53fdeb0b053b5d0'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'
db=SQLAlchemy(app)

from flasklib import routes
