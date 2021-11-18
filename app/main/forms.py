from wtforms import StringField,TextAreaField, SubmitField, SelectField 
from wtforms.validators import Required, Email, Length
from flask_wtf import FlaskForm

class UpdateProfile(FlaskForm):
    name = StringField('Name', validators=[Required(), Length(1, 64)])
    username = StringField('Username', validators=[Required(), Length(1, 64)])
    email = StringField('Email', validators=[Required(), Length(1, 64), Email()])
    bio = TextAreaField('About...', validators=[Required(), Length(1, 100)])
    submit = SubmitField('Submit')
    
class CrimeForm(FlaskForm):
    title = StringField('Title', validators=[Required()])
    location = StringField('Location',validators=[Required()])
    security_issue_description = TextAreaField('Your Security Crime Alert', validators=[Required()])
    submit = SubmitField('Post')
    
class CommentForm(FlaskForm):
    proposed_solution = TextAreaField('Write your comment', validators=[Required()])
    submit = SubmitField('Submit')




