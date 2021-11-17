from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, SubmitField
from wtforms.validators import Required

class CrimeForm(FlaskForm):
    title = StringField('Title', validators=[Required()])
    location = StringField('location',validators=[Required()])
    Description = TextAreaField('Your Security Crime Alert', validators=[Required()])
    submit = SubmitField('Crime Alert')