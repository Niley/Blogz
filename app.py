from flask import Flask, request, redirect, render_template, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://Blogz:123@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
app.static_folder = 'static'
db = SQLAlchemy(app)
app.secret_key = '13375417'