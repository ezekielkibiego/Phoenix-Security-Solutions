from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime

# @login_manager.user_loader
# def load_user(id):
#   return User.query.get(int(id))

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
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    proposed_solution = db.Column(db.String)
    crime_id = db.Column(db.Integer, db.ForeignKey('crimes.id'))
    

    def save_comment(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_comments(cls, blog_id):
        comments = Comment.query.filter_by(blog_id=blog_id).all()
        return comments

    @classmethod
    def get_comment_author(cls, user_id):
        author = User.query.filter_by(id=user_id).first()

        return author

    @classmethod
    def delete_comment(cls, id):
        comment = Comment.query.filter_by(id=id).first()
        db.session.delete(comment)
        db.session.commit()

class Upvote(db.Model):
    __tablename__ = 'upvotes'

    id = db.Column(db.Integer,primary_key=True)
    upvote = db.Column(db.Integer,default=1)
    crime_id = db.Column(db.Integer,db.ForeignKey('crimes.id'))
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))

    def save_upvotes(self):
        db.session.add(self)
        db.session.commit()


    def add_upvotes(cls,id):
        upvote_crime = Upvote(user = current_user, crime_id=id)
        upvote_crime.save_upvotes()

    @classmethod
    def get_upvotes(cls,id):
        upvote = Upvote.query.filter_by(crime_id=id).all()
        return upvote

    @classmethod
    def get_all_upvotes(cls,crime_id):
        upvotes = Upvote.query.order_by('id').all()
        return upvotes

    def __repr__(self):
        return f'{self.user_id}:{self.crime_id}'

class Downvote(db.Model):
    __tablename__ = 'downvotes'

    id = db.Column(db.Integer,primary_key=True)
    downvote = db.Column(db.Integer,default=1)
    crime_id = db.Column(db.Integer,db.ForeignKey('crimes.id'))
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))

    def save_downvotes(self):
        db.session.add(self)
        db.session.commit()


    def add_downvotes(cls,id):
        downvote_crime = Downvote(user = current_user, crime_id=id)
        downvote_crime.save_downvotes()

    
    @classmethod
    def get_downvotes(cls,id):
        downvote = Downvote.query.filter_by(crime_id=id).all()
        return downvote

    @classmethod
    def get_all_downvotes(cls,crime_id):
        downvote = Downvote.query.order_by('id').all()
        return downvote

    def __repr__(self):
        return f'{self.user_id}:{self.crime_id}'