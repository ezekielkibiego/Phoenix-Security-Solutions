from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, ValidationError, BooleanField
from wtforms.validators import Required, Email, EqualTo
from ..models import User

class RegistrationForm(FlaskForm):
  email = StringField('Your Email Address', validators=[Required(), Email()])
  username = StringField('Enter Preferred Username', validators=[Required()])
  password = PasswordField('Password', validators=[Required(), EqualTo('password_confirm', message = 'Password and Password Confirm must match')])
  password_confirm = PasswordField('Confirm Password', validators=[Required()])
  submit = SubmitField('Sign Up')
  
  def validate_email(self, data_field):
    if User.query.filter_by(email = data_field.data).first():
      raise ValidationError("An account with that email address exists")
    
  def validate_username(self, data_field):
    if User.query.filter_by(username=data_field.data).first():
      raise ValidationError('That username is already taken. Please choose a different one')
    

class LoginForm(FlaskForm):
  email=StringField('Your Email Address', validators=[Required(), Email()])
  password = PasswordField('Password', validators=[Required()])
  remember = BooleanField('Remember Me')
  sumbit = SubmitField('Sign In')