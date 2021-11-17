from . import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(id):
  return User.query.get(int(id))

class User(UserMixin, db.Model):
  __tablename__ = 'users'
  
  
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(255))
  email = db.Column(db.String(255), unique=True, index=True)
  pass_secure = db.Column(db.String(255))
  profile_pic_path = db.Column(db.String)
  user_bio = db.Column(db.String(1500))
  crimes = db.relationship('Crime', backref='crime', lazy = "dynamic")
  comments = db.relationship('Comment', backref='comment', lazy='dynamic')
  upvotes = db.relationship('Upvote', backref='upvotes', lazy='dynamic')
  downvotes = db.relationship('Downvote', backref='downvotes', lazy='dynamic')
  
  @property
  def password(self):
    raise AttributeError('You are not authorized to access password attribute')
  
  @password.setter
  def password(self, password):
    self.pass_secure = generate_password_hash(password)
    
  def verify_password(self, password):
    return check_password_hash(self.pass_secure, password)
  
  def __repr__(self):
    return f'User {self.username}'


class Crime(db.Model):
  __tablename__='crimes'
  
  id = db.Column(db.Integer, primary_key=True)
  security_issue_description = db.Column(db.String)
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
  comments = db.relationship('Comment', backref='comments', lazy='dynamic')

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

  