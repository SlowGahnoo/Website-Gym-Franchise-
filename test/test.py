import sys
from src.app import app
from src.database.db_models import *
from src.database.dbman import DBManager
import unittest
import bcrypt
import sqlalchemy
import logging
sys.path.insert(0, "..")

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
dbman = DBManager(db, app)
dbman.dropAll()
dbman.createAll()
dbman.commit()

class TestDBManager(unittest.TestCase):
    def test_signup(self):
        # Test adding a user
        test_client = Client(
                name = "John", 
                surname = "Doe", 
                phone = "2271044239",
        )
        test_account = Account(
                email = "test@test.com", 
                password = bcrypt.hashpw("test".encode('utf8'), bcrypt.gensalt()),
        )
        dbman.pushNewAccount(test_client, test_account)
        dbman.commit()
        self.assertTrue(len(dbman.fetchTable(Account)) == 1)
        self.assertTrue(len(dbman.fetchTable(Client)) == 1)

        # Duplicate account should raise an exception
        with self.assertRaises(sqlalchemy.exc.IntegrityError):
            test_client = Client(
                    name = "John", 
                    surname = "Doe", 
                    phone = "2271044239",
            )
            test_account = Account(
                    email = "test@test.com", 
                    password = bcrypt.hashpw("test".encode('utf8'), bcrypt.gensalt()),
            )
            dbman.pushNewAccount(test_client, test_account)
            dbman.commit()
        
        # Rollback after exception
        dbman.rollback()

        # Test adding a second one
        test_client = Client(
                name = "Johnny", 
                surname = "Doe", 
                phone = "2281044239",
        )
        test_account = Account(
                email = "test2@test2.com", 
                password = bcrypt.hashpw("test2".encode('utf8'), bcrypt.gensalt()),
        )
        dbman.pushNewAccount(test_client, test_account)
        dbman.commit()
        self.assertTrue(len(dbman.fetchTable(Account)) == 2)
        self.assertTrue(len(dbman.fetchTable(Client)) == 2)
        logging.info("Passed signup test")

    def test_subcriptions(self):
        test_client = Client(
                name = "Subber", 
                surname = "Doe", 
                phone = "3281044239",
        )
        test_account = Account(
                email = "test3@test3.com", 
                password = bcrypt.hashpw("test3".encode('utf8'), bcrypt.gensalt()),
        )
        dbman.pushNewAccount(test_client, test_account)
        dbman.pushEntity(Subscription(duration = 12, cost = 150))
        dbman.commit()
        self.assertTrue(len(dbman.fetchTable(Subscription)) == 1)

        dbman.pushEntity(Subscription(duration = 6, cost = 120))
        dbman.commit()
        self.assertTrue(len(dbman.fetchTable(Subscription)) == 2)

        s = dbman.getSubscription(1)
        a = dbman.getAccount("test3@test3.com")
        dbman.setSubscription(s, a)
        dbman.commit()
        # Check is user is subscribed to model 1
        self.assertTrue(dbman.getClient(a.user_id).subscription.subscription == s)

        # Test case when an already subscribed user chooses another subscription
        s = dbman.getSubscription(2)
        a = dbman.getAccount("test3@test3.com")
        dbman.setSubscription(s, a)
        self.assertTrue(dbman.getClient(a.user_id).subscription.subscription == s)
        dbman.commit()

        # Check is user is subscribed to model 1
        self.assertTrue(dbman.getClient(a.user_id).subscription.subscription == s)
        logging.info("Passed subscription test")

    def test_articles(self):
        dbman.pushEntity(Article(title = "Article 1", body = "Body of text for article 1"))
        dbman.pushEntity(Article(title = "Article 2", body = "Body of text for article 2"))
        dbman.commit()
        articles = dbman.fetchTable(Article)
        self.assertTrue(len(articles) == 2)
        self.assertTrue(articles[0].title == "Article 1")
        self.assertTrue(articles[1].title == "Article 2")
        self.assertTrue(articles[0].body == "Body of text for article 1")
        self.assertTrue(articles[1].body == "Body of text for article 2")
        logging.info("Passed article test")
    
    def test_gyms_trainers(self):
        g = Gym(area = "Αθήνα", street =  "Λέκκα 14", postal_code = "105 62", phone = "210 3226844")
        t1 = Trainer(name = "Βικτόρια", surname = "Γεωγιάδου", phone = "229 7025600")
        t2 = Trainer(name = "Φαίδων", surname = "Γιάγκος", phone = "210 3226844")
        dbman.pushEntities([g, t1, t2])
        dbman.setTrainerGym(t1, g)
        dbman.setTrainerGym(t2, g)
        dbman.commit()
        self.assertTrue(len(g.trainers) == 2)
        self.assertTrue(g.trainers[0] == t1)
        self.assertTrue(g.trainers[1] == t2)
        logging.info("Passed gym trainers test")

        


if __name__ == "__main__": # pragma: no cover
    logging.basicConfig(level = logging.DEBUG)
    runner = unittest.TextTestRunner(verbosity = 2)
    unittest.main(testRunner = runner)
