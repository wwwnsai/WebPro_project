import ZODB, ZODB.FileStorage
import BTrees.OOBTree
from datetime import datetime
import transaction


from app.db.model import *
from app.auth.jwt_handler import *

from datetime import date
import calendar

storage = ZODB.FileStorage.FileStorage("app/db/database.fs")
db = ZODB.DB(storage)
connection = db.open()
root = connection.root()

print("Root: ", root)
if not hasattr(root, "users"):
    root.users = BTrees.OOBTree.BTree()
    
if not hasattr(root, "products"):
    root.products = BTrees.OOBTree.BTree()
    
if not hasattr(root, "borrowed"):
    root.borrowed = BTrees.OOBTree.BTree()

def setLockers():
    lockers = BTrees.OOBTree.BTree()
    for i in range(36):
        locker = Locker(i + 1, True)
        lockers[i] = locker
    transaction.commit()
    return lockers

def setLocker_dates(lockers):
    today = date.today()
    days_in_month = calendar.monthrange(today.year, today.month)[1]
    day = today.day
    month = today.month
    year = today.year

    locker_dates = BTrees.OOBTree.BTree()

    for i in range(days_in_month - day):
        date_str = f"{year}-{month}-{day + i}"
        locker_date = Locker_date(date_str, lockers, True)
        locker_dates[date_str] = locker_date

    transaction.commit()
    return locker_dates


if not hasattr(root, "lockers"):
    root.lockers = setLockers()
    transaction.commit()

if not hasattr(root, "locker_dates"):
    root.locker_dates = setLocker_dates(root.lockers)
    transaction.commit()
    print("Lockers database have been created")
else:
    print("Lockers already exist")
    
# if not hasattr(root, "lockers"):
#     root.lockers = setLockers()
#     root.locker_dates = setLocker_dates(root.lockers)
#     transaction.commit()

#     print("Lockers database have been created")
#     # setLocker_dates()
# else:
#     print("Lockers already exist")

#USER   
def checkDuplicateEmail(email):
    for user in root.users.values():
        if user.email == email:
            return True
    return False

def getPayload(token):
    return decodeJWT(token)

def checkUserExists(id):
    for user in root.users.values():
        if user.id == id:
            return True
    return False
    
def get_db():
    db = ZODB.DB(storage)
    connection = db.open()
    root = connection.root()
    return db

#ITEM
def checkDuplicateProduct(id):
    for product in root.products.values():
        if product.id == id:
            return True
    return False

def checkProductExists(id):
    for product in root.products.values():
        if product.id == id:
            return True
    return False

def checkProductAvailable(id):
    for product in root.products.values():
        if product.id == id:
            if product.status == True:
                return True
    return False

#BORROWED

#LOCKER

    