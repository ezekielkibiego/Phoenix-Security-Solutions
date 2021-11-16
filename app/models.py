from . import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime

class User(db.Model):
  __tablename__ = 'users'
  
  
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(255))
  email = db.Column(db.String(255), unique=True, index=True)
  password = db.Column(db.String(255))
  profile_pic_path = db.Column(db.String)
  user_bio = db.Column(db.String(1500))
  crimes = db.relationship('Crime', backref='crime', lazy = "dynamic")
  comments = db.relationship('Comment', backref='comment', lazy='dynamic')
  upvotes = db.relationship('Upvote', backref='upvote', lazy='dynamic')
  downvotes = db.relationship('Downvote', backref='downvote', lazy='dynamic')

class Crime(db.Model):
  __tablename__='crimes'
  
  id = db.Column(db.Integer, primary_key=True)
  security_issue_description = db.Column(db.String)
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
  comments = db.relationship('Comment', backref='comment', lazy='dynamic')
  
class Comment(db.Model):
  __tablename__ = 'comments'
  
  id = db.Column(db.Integer, primary_key=True)
  proposed_solution = db.Column(db.String)
  crime_id = db.Column(db.Integer, db.ForeignKey('crimes.id'))
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
  
class Upvote(db.Model):
  __tablename__ = 'upvotes'
  
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
  
class Downvote(db.Model):
  __tablename__='downvotes'
  
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

  