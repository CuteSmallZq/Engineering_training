from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
import config,os
import json

# from test.test_orm import app,db

app = Flask(__name__)
app.config.from_object(config)
db = SQLAlchemy(app)
# char or string ?
asociation = db.Table('association',db.metadata,db.Column('uid',db.Integer,db.ForeignKey('user.u_id')),
                      db.Column('tid',db.Integer,db.ForeignKey('tag.id')),
                      )
class Comment(db.Model):
    __tablename__='comment'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    id2 = db.Column(db.Integer,primary_key=True)
    id3 = db.Column(db.Integer,primary_key=True)
    comment = db.Column(db.String(50),nullable=False)
class User(db.Model):
    __tablename__ = 'user'
    u_id = db.Column(db.Integer,primary_key=True,nullable=False,autoincrement=True)
    u_name = db.Column(db.String(20),nullable=True,unique=True)
    tags = db.relationship('Tag',secondary = asociation,backref="users" )
    def getMyName(self):
        return 'User'

class Tag(db.Model):
    __tablename__ = "tag"
    id = db.Column(db.Integer , primary_key=True , autoincrement=True)
    tag = db.Column(db.String(50) , nullable=False)


db.create_all()

def likeSearch(obj,like,attribution):
    # like = '%'+like+'%'
    str =obj.getMyName(obj).lower()+'.'+attribution+' like("%'+like+'%")'
    print(str)
    #print(text(str))
    result = obj.query.filter(text(str)).all()
    return result

def toDirection(objcts):
    attr = {}
    i=1
    for obj in objcts:
        ds = dir(obj)
        results= []
        for d in ds :
            ds.remove(d)if d.startswith('_')or d.startswith('get')or d.startswith('query')or d.startswith('meta')else results.append(d)

        for result in results:
            key = result+str(i)
            attr[key]=getattr(obj,result)
        i = i+1
    j=json.dumps(attr)
    #print (attr)
    return j

#def serachManytoMany():



if __name__ == '__main__':
    use=likeSearch(User,'dddd','u_name')

    print (toDirection(use))
    print(db.session.query(asociation).all())
    print(db.session.query(User.tags).all())
