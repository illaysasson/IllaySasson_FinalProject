### ----------------------------------------------------------- ###
### --- include all software packages and libraries needed ---- ###
### ----------------------------------------------------------- ###

from datetime import datetime
    
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms import Form, BooleanField, PasswordField
from wtforms import TextField, TextAreaField, SelectField, DateField
from wtforms import validators, ValidationError

from wtforms.validators import DataRequired
### ----------------------------------------------------------- ###

class LoginFormStructure(FlaskForm):
    username   = StringField('Username:  ' , validators = [DataRequired()])
    password   = PasswordField('Password:  ' , validators = [DataRequired()])
    submit = SubmitField('Submit')


class UserRegistrationFormStructure(FlaskForm):
    FirstName  = StringField('First name:  ' , validators = [DataRequired()])
    LastName   = StringField('Last name:  ' , validators = [DataRequired()])
    EmailAddr  = StringField('E-Mail:  ' , validators = [DataRequired()])
    username   = StringField('Username:  ' , validators = [DataRequired()])
    password   = PasswordField('Password:  ' , validators = [DataRequired()])
    submit = SubmitField('Submit')