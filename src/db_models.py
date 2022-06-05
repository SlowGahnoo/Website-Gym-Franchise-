from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# Definitions of database tables

class Account(db.Model):
    email         = db.Column(db.String(120), primary_key = True)
    password      = db.Column(db.String(72), nullable = False)
    creation_date = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    user_id       = db.Column(db.Integer, db.ForeignKey("user.id"))
    user          = db.relationship("User", back_populates = "account", uselist = False)

    def __repr__(self):
        return '<Account %r>'  % self.user

class User(db.Model):
    id      = db.Column(db.Integer, primary_key = True)
    name    = db.Column(db.String(80), nullable = False)
    surname = db.Column(db.String(80), nullable = False)
    phone   = db.Column(db.String(15), unique = True)
    account = db.relationship("Account", back_populates = "user",
            uselist = False)

    def __repr__(self):
        return '<User %r>'  % self.id

admin_article = db.Table('admin_article',
        db.Column('id_article', db.Integer, db.ForeignKey('article.id')),
        db.Column('id_admin', db.Integer, db.ForeignKey('admin.id'))
)

class Admin(User):
    id = db.Column(None, db.ForeignKey('user.id'), primary_key = True)

    authors = db.relationship('Article', secondary=admin_article, backref='authors')

    def __repr__(self):
        return '<Admin %r>' % self.id

    db.__tablename__ = 'admin'
    db.__mapper_args__ = {'polymorphic_identity': 'admin'}


class Article(db.Model):
    id       = db.Column(db.Integer, primary_key = True)
    title    = db.Column(db.String(80), nullable = False)
    body     = db.Column(db.Text, nullable = False)
    pub_date = db.Column(db.DateTime, nullable = False,
            default = datetime.utcnow)

    def __repr__(self):
        return '<Post %r>' % self.title

class Client_Subscription(db.Model):
    id_subcription = db.Column(db.ForeignKey('subscription.id'), 
            primary_key = True)
    id_client = db.Column(db.ForeignKey('client.id'),
            primary_key = True)
    purchase_date = db.Column(db.DateTime, nullable = False, 
            default = datetime.utcnow)

    client = db.relationship('Client', back_populates='subscription')
    subscription = db.relationship('Subscription', back_populates='clients')

class Client(User):
    id       = db.Column(None, db.ForeignKey('user.id'), primary_key = True)
    city     = db.Column(db.String(80))
    address  = db.Column(db.String(80))
    zip_code = db.Column(db.Integer)
    birthday = db.Column(db.DateTime)

    subscription = db.relationship('Client_Subscription', back_populates='client', uselist = False)
    gym = db.relationship("Gym_Client", back_populates = 'client', uselist = False)

    def __repr__(self):
        return '<Client %r>' % self.id

    db.__tablename__ = 'client'
    db.__mapper_args__ = {'polymorphic_identity': 'client'}

class Subscription(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    cost = db.Column(db.Float, nullable = False)
    duration = db.Column(db.Integer, nullable = False)
    clients = db.relationship('Client_Subscription', back_populates='subscription')

    def __repr__(self):
        return '<Subscription %r>' % self.id

trainer_gym = db.Table('trainer_gym',
        db.Column('id_trainer', db.Integer, db.ForeignKey('trainer.id')),
        db.Column('id_gym', db.Integer, db.ForeignKey('gym.id'))
)

class Gym(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    street = db.Column(db.String(80))
    area = db.Column(db.String(80))
    postal_code = db.Column(db.Integer)
    phone = db.Column(db.String(15))
    email = db.Column(db.String(120))

    trainers = db.relationship('Trainer', secondary=trainer_gym, back_populates = "gym")
    clients = db.relationship('Gym_Client', back_populates = 'gym')

    def __repr__(self):
        return '<Gym %r>' % self.id

class Trainer(User):
    id  = db.Column(None, db.ForeignKey('user.id'), primary_key = True)
    gym = db.relationship("Gym", secondary=trainer_gym, uselist = False)

    def __repr__(self):
        return '<Trainer %r>' % self.id

    db.__tablename__ = 'trainer'
    db.__mapper_args__ = {'polymorphic_identity': 'trainer'}


class Gym_Client(db.Model):
    id_gym = db.Column(db.ForeignKey('gym.id'), primary_key = True)
    id_client = db.Column(db.ForeignKey('client.id'), primary_key = True)
    enrollment_date = db.Column(db.DateTime, nullable = False, 
            default = datetime.utcnow)

    client = db.relationship('Client', back_populates = 'gym')
    gym = db.relationship('Gym', back_populates = 'clients')




