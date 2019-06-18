from exts import db
from models import *

#commit change
def commitChanges(change):
    db.session.add(change)
    db.session.commit()

def addItems(model:db.Model,add,string:String):
