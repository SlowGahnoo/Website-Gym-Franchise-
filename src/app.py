from flask import Flask, redirect, url_for, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from db_models import db

app = Flask(__name__)

# Set SQLAlchemy engine
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
app.secret_key = 'test'
db.init_app(app)
app.app_context().push()
from db_models import *

@app.route("/")
@app.route("/main")
def home():
    return render_template("main.html")

gymlist = ["Αθήνα", "Θεσσαλονίκη", "Κρήτη"]
@app.route("/gyms")
def gyms():
    return render_template("gyms.html", gymlist = gymlist)

@app.route("/schedule")
def schedule():
    return render_template("schedule.html")

@app.route("/personnel")
def personnel():
    return render_template("personnel.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/subscription")
@app.route("/shop")
def shop():
    return render_template("shop.html")

@app.route("/account")
def account():
    return render_template("account.html")

@app.route("/admin", methods = ["GET", "POST"])
def admin():
    return render_template("admin.html")

newslist = []
@app.route("/news", methods = ["GET", "POST"])
def news():
    print(newslist)
    if request.method == "POST":
        session['new-article'] = request.form.get('article-info')
        newslist.append(session['new-article'])
        return redirect(url_for('news'))
    session.pop('new-article', None)
    return render_template("news.html", newslist = newslist[::-1])

if __name__ == "__main__":
    app.run(debug = True)
