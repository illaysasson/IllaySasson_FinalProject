### ----------------------------------------------------------- ###
### --- include all software packages and libraries needed ---- ###
### ----------------------------------------------------------- ###

from datetime import datetime
    
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms import Form, BooleanField, PasswordField
from wtforms import TextField, TextAreaField, SelectField, DateField
from wtforms import validators, ValidationError 

from wtforms.validators import DataRequired, Email, Length
### ----------------------------------------------------------- ###

class QueryFormStructure(FlaskForm):
    Country   = StringField('Country:  ')
    Region   = StringField('Region:  ')
    Rank   = StringField('Rank:  ')
    Submit = SubmitField('Submit')

class LoginFormStructure(FlaskForm):
    username   = StringField('Username:  ' , validators = [DataRequired('Username Required.')])
    password   = PasswordField('Password:  ' , validators = [DataRequired('Password Required.')])
    submit = SubmitField('Submit')


class UserRegistrationFormStructure(FlaskForm):
    FirstName  = StringField('First name:  ' , validators = [DataRequired('First Name Required.')])
    LastName   = StringField('Last name:  ' , validators = [DataRequired('Last Name Required.')])
    Gender = SelectField('Gender', choices = [('M', 'Male'), ('F', 'Female'), ('O', 'Other')])
    EmailAddr  = StringField('E-Mail:  ' , validators = [DataRequired('Email Address Required.'), Email()])
    username   = StringField('Username:  ' , validators = [DataRequired('Username Required.')])
    password   = PasswordField('Password:  ' , validators = [DataRequired('Password Required.'), Length(min=5, message='Password must be more than 5 characters.')])
    submit = SubmitField('Submit')