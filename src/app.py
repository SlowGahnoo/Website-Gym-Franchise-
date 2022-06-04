from flask import Flask, redirect, url_for, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from db_models import db

app = Flask(__name__)

# Set SQLAlchemy engine
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
db.init_app(app)
app.app_context().push()
from db_models import *

@app.route("/")
@app.route("/main")
def home():
    return render_template("main.html")

@app.route("/news")
def news():
    return render_template("news.html")

@app.route("/gyms")
def gyms():
    return render_template("gyms.html")

@app.route("/schedule")
def schedule():
    return render_template("schedule.html")

@app.route("/personnel")
def personnel():
    return render_template("personnel.html")

@app.route("/subscription")
def subscription():
    return render_template("subscription.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/shop")
def shop():
    return render_template("shop.html")

@app.route("/account")
def account():
    return render_template("account.html")

@app.route("/admin")
def admin():
    return render_template("admin.html")

if __name__ == "__main__":
    app.run(debug = True)
