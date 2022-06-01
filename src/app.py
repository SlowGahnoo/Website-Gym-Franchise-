from flask import Flask, redirect, url_for, render_template, request

app = Flask(__name__)

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

if __name__ == "__main__":
    app.run(debug = True)
