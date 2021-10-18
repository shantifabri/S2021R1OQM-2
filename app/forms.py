from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, SubmitField
from wtforms.validators import InputRequired

class UserForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired()])

class GetTicketForm(FlaskForm):
    service = SelectField('Category', choices = [('Clothes', 'Clothes'), ('Watch', 'Watch')])
    submit = SubmitField('Get Ticket')
