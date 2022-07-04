from flask import Flask, redirect, url_for, render_template, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
from datetime import datetime
from dateutil.relativedelta import relativedelta
from dataclasses import dataclass
import bcrypt

app = Flask(__name__)

# Set SQLAlchemy engine
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
app.secret_key = 'test'
from .database import *
from .database.dbman import *
dbman = DBManager(db, app)

def login_account(a: Account):
    session['name']      = f"{a.user.name} {a.user.surname}"
    session['email']     = a.email
    session['logged-in'] = True
    session['basket']    = None

def logout_account():
    session.pop('name',      None)
    session.pop('email',     None)
    session.pop('logged-in', None)
    session.pop('basket',    None)

@app.route('/')
@app.route('/main')
def home():
    if 'logged-in' in session:
        name = session['name']
        return render_template('main.html', name = name)
    return render_template('main.html')

@app.route('/gyms')
def gyms():
    gymlist = dbman.fetchTable(Gym)
    return render_template('gyms.html', gymlist = gymlist)

@app.route('/schedule')
def schedule():
    return render_template('schedule.html')

@app.route('/personnel')
def personnel():
    trainerlist = dbman.fetchTable(Trainer)
    return render_template('personnel.html', trainerlist = trainerlist)

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/signup', methods = ['GET', 'POST'])
def signup():
    if 'logged-in' in session:
        return redirect(url_for('home'))
    if request.method == 'POST':
        try:
            c = Client(
                name     = request.form['name'],
                surname  = request.form['surname'],
                phone    = request.form['phone'],
                city     = request.form['town'],
                address  = request.form['address'],
                zip_code = request.form['zip-code'],
            )
            salt = bcrypt.gensalt()
            a = Account(
                email    = request.form['email'],
                password = bcrypt.hashpw(request.form['password'].encode('utf-8'), salt),
            )
            dbman.pushNewAccount(c, a)
            dbman.commit()
            login_account(a)
            return redirect(url_for('home'))
        except exc.IntegrityError as e:
            flash("User already exists")
    return render_template('signup.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if 'logged-in' in session:
        return redirect(url_for('home'))
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password'].encode('utf-8')
        a = dbman.getAccount(email = email)
        if a:
            if (matched := bcrypt.checkpw(password, a.password) == True):
                login_account(a)
                return redirect(url_for('home'))
            else:
                flash("Λάθος mail ή password")
        else:
            flash("Χρήστης δεν υπάρχει")

    return render_template('login.html')

@app.route('/logout')
def logout():
    if 'logged-in' in session:
        logout_account()
    return redirect(url_for('home'))

@app.route('/subscription')
def subscription():
    if 'logged-in' in session:
        a = dbman.getAccount(email = session['email'])
        c = dbman.getClient(_id = a.user_id)

        if c.subscription:
            subscription = c.subscription.subscription
            purchase_date = c.subscription.purchase_date
            time_left = str(purchase_date + relativedelta(months = subscription.duration) - datetime.today()).split('.')[0]
            return render_template('subscriptions.html',
                subscription_list = [subscription], purchase_date = purchase_date, time_left = time_left)
        return render_template('subscriptions.html')
    else:
        flash("Συνδεθείτε για να δείτε τη συνδρομή σας")
        return render_template('subscriptions.html')

@app.route('/confirm', methods = ["GET", "POST"])
def confirm():
    sid = session['basket']
    subscription = dbman.getSubscription(_id = sid)

    if request.method == "POST":
        confirm = request.values.get('confirm')
        if confirm == "yes":
            a = dbman.getAccount(email = session['email'])
            c = dbman.getClient(_id = a.user_id)
            dbman.setSubscription(s, a)
            session['basket'] = None
            return redirect(url_for('subscription'))
        else:
            return redirect(url_for('shop'))

    if subscription:
        return render_template('confirm.html', subscription_list = [subscription])
    else:
        return redirect(url_for('home'))


@app.route('/shop', methods = ["POST", "GET"])
def shop():
    subscription_list = dbman.fetchTable(Subscription)
    sid = 0
    if 'logged-in' in session:
        if request.method == "POST":
            session['basket'] = request.values.get('subscription')
            return redirect(url_for('confirm'))
    return render_template('shop.html', subscription_list = subscription_list)

@app.route('/account')
def account():
    if not 'logged-in' in session:
        flash("Δεν είστε συνδεδεμένος")
        return redirect(url_for('login'))
    a = dbman.getAccount(email = session['email'])
    return render_template('account.html', account = a)

@app.route('/admin', methods = ['GET', 'POST'])
def admin():
    return render_template('admin.html')

@app.route('/news', methods = ['GET', 'POST'])
def news():
    newslist = reversed(dbman.fetchTable(Article))
    if request.method == 'POST':
        title = request.form.get('title')
        session['new-article'] = request.form.get('article-info')
        dbman.pushEntity(Article(title = title, body = session['new-article']))
        dbman.commit()
        return redirect(url_for('news'))
    session.pop('new-article', None)
    return render_template('news.html', newslist = newslist)

if __name__ == "__main__":
    app.run(debug = True)
