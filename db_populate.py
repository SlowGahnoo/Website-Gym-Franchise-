from src.app import *
# from src.database.db_models import *
from random import shuffle

print("Cleaning database")
db.drop_all()
print("Creating new database")
db.create_all()

try:
    print("Creating test user")
    test_user = Client(
            name = "John", 
            surname = "Doe", 
            phone = "2271044239",
    )
    test_account = Account(
            email = "test@test.com", 
            password = bcrypt.hashpw("test".encode('utf8'), bcrypt.gensalt()),
    )
    
    test_account.user = test_user
    db.session.add_all([test_user, test_account])
    
    print("Creating test article")
    articles = []
    articles.append(Article(
        title = "Πρώτο άρθρο",
        body  = "Αθλητισμός Ψυχική Υγεία: Η άθληση και εν γένει η σωματική κίνηση είναι πολύ ευεργετική για την ψυχική υγεία. Τα άτομα που ασκούνται τακτικά νιώθουν λιγότερο νευρικά, πιο καλοδιάθετα και ήρεμα, ενώ βιώνουν λιγότερο άγχος και τείνουν να είναι πιο ενδυναμωμένα σε δύσκολες καταστάσεις της καθημερινής ζωής."
        ))
    db.session.add_all(articles)
    
    
    print("Creating mockup gyms")
    gyms = []
    gyms.append(Gym(area = "Αθήνα", street =  "Λέκκα 14", postal_code = "105 62", phone = "210 3226844"))
    gyms.append(Gym(area = "Χανιά", street =  "Ακτή Κουντουριώτου 42", postal_code = "731 00", phone = "282 1094100 "))
    gyms.append(Gym(area = "Θεσσαλονίκη", street =  "Τσιμισκή 12", postal_code = "546 24", phone = "231 0257400"))
    gyms.append(Gym(area = "Ιωάννινα", street =  "Κωλέττη 5", postal_code = "454 44", phone = "2651 071771"))
    db.session.add_all(gyms)
    
    print("Creating trainers gyms")
    trainers = []
    trainers.append(Trainer(name = "Βικτόρια", surname = "Γεωγιάδου", phone = "229 7025600"))
    trainers.append(Trainer(name = "Φαίδων", surname = "Γιάγκος", phone = "210 3226844"))
    trainers.append(Trainer(name = "Δίκαιος", surname = "Κόρακας", phone = "255 2029088"))
    trainers.append(Trainer(name = "Ξενοφών", surname = "Παπαδόπουλος", phone = "229 2034088"))
    db.session.add_all(trainers)
    
    print("Matching a trainer with a gym")
    shuffle(gyms)
    shuffle(trainers)
    for gym, trainer in zip(gyms, trainers):
        gym.trainers.append(trainer)
    
    print("Creating mockup subscriptions")
    sub_plans = [(12, 150), (6, 120), (3, 100), (1, 40)]
    subscriptions = []
    for duration, cost in sub_plans:
        subscriptions.append(Subscription(duration = duration, cost = cost))
    db.session.add_all(subscriptions)
    
    print("Committing")
    db.session.commit()
    print("Done!")
except Exception as e:
    print(e)
    db.drop_all()
