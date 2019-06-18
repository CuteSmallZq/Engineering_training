from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand
# from test.test_orm import app,db


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:gaobaiqiqiu98@localhost:3306/workplace"
db = SQLAlchemy(app)
#char or string ?
class Movies (db.Model):
    __tablename__ = 'movie'
    mo_id = db.Column(db.Integer,primary_key=True)
    mo_English_name = db.Column(db.String(225),nullable=False,index=True)
    mo_name = db.Column(db.String(255),nullable=False,index=True)
    mo_introduction = db.Column(db.String(1000),nullable=False)
    mo_nation = db.Column(db.String(40),nullable=False)
    mo_heat = db.Column(db.Integer(),nullable=False)
    mo_picture = db.Column(db.String(5000),nullable=False)
    mo_length = db.Column(db.Integer,nullable=False)
    mo_score = db.Column(db.Integer,nullable=False)
    mo_date = db.Column(db.String(20),nullable=False)
    # mo_date = db.Column(db.Date,nullable=False)

class Music (db.Model):
    __tablename__ = 'music'
    mu_id = db.Column(db.Integer,primary_key=True)
    mu_name = db.Column(db.String(255),nullable=False,index=True)
    mu_introduction = db.Column(db.String(10000),nullable=False)
    mu_singer = db.Column(db.String(100),nullable=False)
    mu_heat = db.Column(db.Integer,nullable=False)
    mu_picture = db.Column(db.String(5000),nullable=False)
    mu_score = db.Column(db.Integer,nullable=False)
    mu_date = db.Column(db.String(20),nullable=False)
   # mu_date = db.Column(db.Date,nullable=False)


class Book(db.Model):
    __tablename__ = 'book'
    b_id = db.Column(db.Integer,primary_key=True)
    b_name = db.Column(db.String(255),nullable=False,index=True)
    b_introduction = db.Column(db.String(10000),nullable=False)
    b_pulishing_house = db.Column(db.String(500),nullable=False)
    b_writer = db.Column(db.String(100),nullable=False)
    b_score = db.Column(db.Integer,nullable=False)
    b_heat = db.Column(db.Integer,nullable=False)
    b_date = db.Column(db.String(20),nullable=False)


class User(db.Model):
    __tablename = 'user'
    u_id = db.Column(db.Integer,primary_key=True)
    u_name = db.Column(db.String(40),nullable=False,index=True)
    u_image = db.Column(db.String(1000),nullable=False)
    #todo
user_like_tags  = db.Table('userLikeTags',db.metadata,
                              db.Column('t_id',db.Integer,db.ForeignKey('tag.t_id')),
                              db.Column('u_id',db.Integer,db.ForeignKey('user.u_id')),
                              )

tag_associate_book = db.Table('tagToBook',db.metadata,
                              db.Column('t_id',db.Integer,db.ForeignKey('tag.t_id')),
                              db.Column('b_id',db.Integer,db.ForeignKey('book.b_id'))
                              )
tag_associate_movie = db.Table('tagToMovie',db.metadata,
                              db.Column('t_id',db.Integer,db.ForeignKey('tag.t_id')),
                              db.Column('mo_id',db.Integer,db.ForeignKey('movie.mo_id'))
                              )
tag_associate_music = db.Table('tagToMusic',db.metadata,
                              db.Column('t_id',db.Integer,db.ForeignKey('tag.t_id')),
                              db.Column('mu_id',db.Integer,db.ForeignKey('music.mu_id'))
                               )

class Tag(db.Model):
    __tablename__ = 'tag'
    t_id = db.Column(db.Integer,primary_key=True)
    t_tag = db.Column(db.String(100),nullable=False)
    movies = db.relationship('movie', secondary=tag_associate_movie, backref=db.backref('TagstoMovie'))
    books = db.relationship('book', secondary=tag_associate_book, backref=db.backref('TagstoBook'))
    music = db.relationship('music', secondary=tag_associate_music, backref=db.backref('TagstoMusic'))
    users = db.relationship('user', secondary=user_like_tags, backref=db.backref('UserlikeTags'))


class User_Comment_Movie(db.Model):
    __tablename__ = 'userComMovie'
    u_id = db.Column(db.Integer,primary_key=True)
    mo_id = db.Column(db.Integer,primary_key=True)
    mo_comment = db.Column(db.String(10000),nullable=False)
    mo_score = db.Column(db.Integer,nullable=False)


class User_to_Movie(db.Model):
    __tablename__ = 'userToMovie'
    u_id = db.Column(db.Integer,primary_key=True)
    mo_id = db.Column(db.Integer,primary_key=True)
    seen = db.Column(db.BOOLEAN,nullable=True)
    want = db.Column(db.BOOLEAN,nullable=True)

class User_Comment_Music(db.Model):
    __tablename__ = 'userComMusic'
    u_id = db.Column(db.Integer,primary_key=True)
    mu_id = db.Column(db.Integer,primary_key=True)
    mu_comment = db.Column(db.String(10000),nullable=False)
    mu_score = db.Column(db.Integer,nullable=False)


class User_to_Music(db.Model):
    __tablename__ = 'userToMusic'
    u_id = db.Column(db.Integer,primary_key=True)
    mu_id = db.Column(db.Integer,primary_key=True)
    listened = db.Column(db.BOOLEAN,nullable=True)
    want = db.Column(db.BOOLEAN,nullable=True)


class User_Comment_Book(db.Model):
    __tablename__ = 'userComBook'
    u_id = db.Column(db.Integer,primary_key=True)
    b_id = db.Column(db.Integer,primary_key=True)
    b_comment = db.Column(db.String(10000),nullable=False)
    mb_score = db.Column(db.Integer,nullable=False)


class User_to_Book(db.Model):
    __tablename__ = 'userToBook'
    u_id = db.Column(db.Integer,primary_key=True)
    b_id = db.Column(db.Integer,primary_key=True)
    seen = db.Column(db.BOOLEAN,nullable=True)
    want = db.Column(db.BOOLEAN,nullable=True)






manager = Manager(app)
migrate = Migrate(app,db)
manager.add_command('db',MigrateCommand)

if __name__ == '__main__':
    manager.run()

