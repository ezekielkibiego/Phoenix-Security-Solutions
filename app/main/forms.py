from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, SubmitField
from wtforms.validators import Required

class CrimeForm(FlaskForm):
    title = StringField('Title', validators=[Required()])
    location = StringField('Location',validators=[Required()])
    security_issue_description = TextAreaField('Your Security Crime Alert', validators=[Required()])
    submit = SubmitField('Post')