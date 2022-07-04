from .db_models import *
from flask import Flask


class DBManager():
    """ Interface to manage the database of our Flask application """
    def dropAll(self):
        """ Empty the database """
        db.drop_all()

    def createAll(self):
        """ Create a new database """
        db.create_all()

    def rollback(self):
        """ Rollback to stable state after an exception has been raised """
        db.session.rollback()

    def __init__(self, db: SQLAlchemy, app: Flask):
        db.init_app(app)
        app.app_context().push()

    def fetchTable(self, table: db.Model) -> list:
        """ Get a list of elements of table rows """
        return table.query.all()

    def pushNewAccount(self, c: Client, a: Account):
        """ Push new account into the database """
        a.user = c
        db.session.add_all([a, c])

    def getAccount(self, email: str) -> Account:
        return (Account.query
                       .filter_by(email = email)
                       .first())

    def getClient(self, _id: int) -> Client:
        return (Client.query
                      .filter_by(id = _id)
                      .first())

    def pushEntity(self, entity: db.Model):
        """ Add new entity to table """
        db.session.add(entity)

    def pushEntities(self, entities: list[db.Model]):
        """ Add new entity to table """
        db.session.add_all(entities)

    def setTrainerGym(self, t: Trainer, g: Gym):
        """ Append trainer to gym """
        g.trainers.append(t)

    def getSubscription(self, _id: int) -> Subscription:
        """ Get subscription with id: _id """
        return (Subscription.query
                            .filter_by(id = _id)
                            .first())

    def setSubscription(self, s: Subscription, a: Account):
        """ Match Subscription with an account """
        c = (Client.query
                   .filter_by(id = a.user_id)
                   .first())

        if c.subscription:
            db.session.delete(c.subscription)
        s.clients.append(Client_Subscription(client = c))

    def commit(self):
        """ Commit changes to the database """
        db.session.commit()
