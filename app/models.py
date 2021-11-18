from . import db,login_manager
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
  title= db.Column(db.String(255))
  security_issue_description = db.Column(db.String)
  location= db.Column(db.String(255))
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

  time = db.Column(db.DateTime, default = datetime.utcnow)
  comments = db.relationship('Comment', backref='comments', lazy='dynamic')
  
  def save(self):
    db.session.add(self)
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def get_blog(id):
    crime = Crime.query.filter_by(id=id).first()
    return crime

  def __repr__(self):
    return f'Crime {self.title}'

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
    _tablename_ = 'upvotes'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    comment_id = db.Column(db.Integer, db.ForeignKey('comment.id'))

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_upvotes(cls, id):
        upvote = Upvote.query.filter_by(comment_id=id).all()
        return upvote

    def _repr_(self):
        return f'{self.user_id}:{self.comment_id}'


class Downvote(db.Model):
    _tablename_ = 'downvotes'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    comment_id = db.Column(db.Integer, db.ForeignKey('comment.id'))

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_downvotes(cls, id):
        downvote = Downvote.query.filter_by(comment_id=id).all()
        return downvote

    def _repr_(self):
        return f'{self.user_id}:{self.comment_id}'
