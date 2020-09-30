from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'la mas segura'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///portfolios.db'
db = SQLAlchemy(app)

from portfolios import routes