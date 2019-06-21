from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
import config,os
import json

app = Flask(__name__)
app.config.from_object(config)
db = SQLAlchemy(app)




user_like_tags = db.Table('UserLikeTags', db.metadata,
                          db.Column('t_id', db.Integer, db.ForeignKey('tag.t_id')),
                          db.Column('u_id', db.Integer, db.ForeignKey('user.u_id')),
                          )

tag_associate_book = db.Table('tagToBook', db.metadata,
                              db.Column('t_id', db.Integer, db.ForeignKey('tag.t_id')),
                              db.Column('b_id', db.Integer, db.ForeignKey('book.b_id')),
                              db.Column('comment', db.String(50))
                              )
tag_associate_movie = db.Table('tagToMovie', db.metadata,
                               db.Column('t_id', db.Integer, db.ForeignKey('tag.t_id')),
                               db.Column('mo_id', db.Integer, db.ForeignKey('movie.mo_id')),
                               db.Column('comment', db.String(50))
                               )
tag_associate_music = db.Table('tagToMusic', db.metadata,
                               db.Column('t_id', db.Integer, db.ForeignKey('tag.t_id')),
                               db.Column('mu_id', db.Integer, db.ForeignKey('music.mu_id'))
                               )
user_comment_movie = db.Table('userCommentMovie',db.metadata,
                              db.Column('mo_id',db.Integer,db.ForeignKey('movie.mo_id')),
                              db.Column('u_id',db.Integer,db.ForeignKey('user.u_id')),
                              db.Column('comment',db.String(1000)),
                              db.Column('date',db.Date),
                              db.Column('score',db.Float))
user_comment_music = db.Table('userCommentMusic',db.metadata,
                              db.Column('mu_id',db.Integer,db.ForeignKey('music.mu_id')),
                              db.Column('u_id',db.Integer,db.ForeignKey('user.u_id')),
                              db.Column('comment',db.String(1000)),
                              db.Column('date',db.Date),
                              db.Column('score',db.Float))
user_comment_book = db.Table('userCommentBook',db.metadata,
                              db.Column('b_id',db.Integer,db.ForeignKey('book.b_id')),
                              db.Column('u_id',db.Integer,db.ForeignKey('user.u_id')),
                              db.Column('comment',db.String(1000)),
                              db.Column('date',db.Date),
                              db.Column('score',db.Float))

user_seen_movie = db.Table('userSeenMovie',db.metadata,
                           db.Column('u_id',db.Integer,db.ForeignKey('user.u_id')),
                           db.Column('mo_id',db.Integer,db.ForeignKey('movie.mo_id')),
                           db.Column('date',db.Date))
user_listened_music = db.Table('userListenedMusic',db.metadata,
                           db.Column('u_id',db.Integer,db.ForeignKey('user.u_id')),
                           db.Column('mu_id',db.Integer,db.ForeignKey('music.mu_id')),
                           db.Column('date',db.Date))
user_seen_book = db.Table('userSeenBook',db.metadata,
                           db.Column('u_id',db.Integer,db.ForeignKey('user.u_id')),
                           db.Column('b_id',db.Integer,db.ForeignKey('book.b_id')),
                           db.Column('date',db.Date))

user_want_movie = db.Table('userWantMovie',db.metadata,
                           db.Column('u_id',db.Integer,db.ForeignKey('user.u_id')),
                           db.Column('mo_id',db.Integer,db.ForeignKey('movie.mo_id')),
                           db.Column('date',db.Date))
user_want_music = db.Table('userWantMusic',db.metadata,
                           db.Column('u_id',db.Integer,db.ForeignKey('user.u_id')),
                           db.Column('mu_id',db.Integer,db.ForeignKey('music.mu_id')),
                           db.Column('date',db.Date))
user_want_book = db.Table('userWantBook',db.metadata,
                           db.Column('u_id',db.Integer,db.ForeignKey('user.u_id')),
                           db.Column('b_id',db.Integer,db.ForeignKey('book.b_id')),
                           db.Column('date',db.Date))


class User(db.Model):
    __tablename__ = 'user'
    u_id = db.Column(db.Integer,primary_key=True)
    #todo
    comMovies = db.relationship('ComMovie',secondary =user_comment_movie,backref = db.backref('usersWhoCom'))
    comMusic = db.relationship('ComMusic', secondary=user_comment_music, backref=db.backref('usersWhoCom'))
    comBooks = db.relationship('ComBooks', secondary=user_comment_book, backref=db.backref('usersWhoCom'))
    seenMovies = db.relationship('SeenMovie',secondary =user_seen_movie,backref = db.backref('usersWhoSeen'))
    seenMusic = db.relationship('SeenMusic', secondary=user_listened_music, backref=db.backref('usersWhoSeen'))
    seenBooks = db.relationship('SeenBooks', secondary=user_seen_book, backref=db.backref('usersWhoSeen'))
    wantMovies = db.relationship('WantMovie', secondary=user_want_movie, backref=db.backref('usersWhoWant'))
    wantMusic = db.relationship('WantMusic', secondary=user_want_music, backref=db.backref('usersWhoWant'))
    wantBooks = db.relationship('WantBooks', secondary=user_want_book, backref=db.backref('usersWhoWant'))



class Movie(db.Model):
    __tablename__ = 'movie'
    mo_id = db.Column(db.Integer, primary_key=True)
    mo_English_name = db.Column(db.String(225), nullable=True, index=True)
    mo_name = db.Column(db.String(255), nullable=True, index=True)
    mo_introduction = db.Column(db.String(1000), nullable=True)
    mo_nation = db.Column(db.String(40), nullable=True)
    mo_heat = db.Column(db.Integer(), nullable=True)
    mo_picture = db.Column(db.String(5000), nullable=True)
    mo_length = db.Column(db.Integer, nullable=True)
    mo_score = db.Column(db.Integer, nullable=True)
    mo_date = db.Column(db.String(20), nullable=True)


    def to_json(self):
        dict = self.__dict__
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        return dict



class Music(db.Model):
    __tablename__ = 'music'
    mu_id = db.Column(db.Integer, primary_key=True)
    mu_name = db.Column(db.String(255), nullable=True, index=True)
    mu_introduction = db.Column(db.String(1000), nullable=True)
    mu_singer = db.Column(db.String(100), nullable=True)
    mu_heat = db.Column(db.Integer, nullable=True)
    mu_picture = db.Column(db.String(5000), nullable=True)
    mu_score = db.Column(db.Integer, nullable=True)
    mu_date = db.Column(db.String(20), nullable=True)


    def to_json(self):
        dict = self.__dict__
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        return dict



class Book(db.Model):
    __tablename__ = 'book'
    b_id = db.Column(db.Integer, primary_key=True)
    b_name = db.Column(db.String(255), nullable=True, index=True)
    b_introduction = db.Column(db.String(1000), nullable=True)
    b_pulishing_house = db.Column(db.String(500), nullable=True)
    b_writer = db.Column(db.String(100), nullable=True)
    b_writer_intro = db.Column(db.String(1000), nullable=True)
    b_score = db.Column(db.Integer, nullable=True)
    b_heat = db.Column(db.Integer, nullable=True)
    b_date = db.Column(db.String(20), nullable=True)


    def to_json(self):
        dict = self.__dict__
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        return dict

class Tag(db.Model):
    __tablename__ = 'tag'
    t_id = db.Column(db.Integer, primary_key=True)
    t_tag = db.Column(db.String(100), nullable=False)
    movies = db.relationship('Movie', secondary=tag_associate_movie, backref=db.backref('TagstoMovie'))
    books = db.relationship('Book', secondary=tag_associate_book, backref=db.backref('TagstoBook'))
    music = db.relationship('Music', secondary=tag_associate_music, backref=db.backref('TagstoMusic'))
    users = db.relationship('User', secondary=user_like_tags, backref=db.backref('UserlikeTags'))



migrate = Migrate(app,db)
manager = Manager(app)
manager.add_command('db',MigrateCommand)
if __name__ == '__main__':
    manager.run()