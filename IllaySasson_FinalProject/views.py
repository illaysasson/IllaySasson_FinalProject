"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template
from IllaySasson_FinalProject import app
from IllaySasson_FinalProject.models.LocalDatabaseRoutines import create_LocalDatabaseServiceRoutines


from datetime import datetime
from flask import render_template, redirect, request


from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

import json 
import requests

import io
import base64

from os import path

from flask   import Flask, render_template, flash, request
from wtforms import Form, BooleanField, StringField, PasswordField, validators
from wtforms import TextField, TextAreaField, SubmitField, SelectField, DateField
from wtforms import ValidationError

from IllaySasson_FinalProject.models.QueryFormStructure import LoginFormStructure 
from IllaySasson_FinalProject.models.QueryFormStructure import UserRegistrationFormStructure 

db_Functions = create_LocalDatabaseServiceRoutines() 
mutualtitle = 'Happiness & The Internet'

app.config['SECRET_KEY'] = '2212'

@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title=mutualtitle,
        year=datetime.now().year,
    )

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title=mutualtitle,
        year=datetime.now().year,
        message='Your contact page.'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title=mutualtitle,
        year=datetime.now().year,
        message='Your application description page.'
    )

@app.route('/data_model')
def data_model():
    """Renders the about page."""
    return render_template(
        'data_model.html',
        title=mutualtitle + ' - Data Model',
        year=datetime.now().year,
    )


@app.route('/data_internet_users')
def data_internet_users():

    dffull = pd.read_csv(path.join(path.dirname(__file__), 'static/data/internet_users.csv'))
    df = dffull[['Country or Area', 'Population', 'Population Rank', 'Internet Users', 'Percentage', 'Internet Users Rank']]
    df.sort_values(by='Country or Area', inplace=True, ascending=True)
    
    raw_data_table = df.to_html(classes = 'table table-hover')

    return render_template('data pages/data_internet_users.html', 
            raw_data_table = raw_data_table,
            title=mutualtitle + ' - Data Model',
            year=datetime.now().year,
        )

@app.route('/data_suicide_rates')
def data_suicide_rates():

    dffull = pd.read_csv(path.join(path.dirname(__file__), 'static/data/suicide_rates.csv'))
    df = dffull[['Country', 'Sex', 'Suicides/100k Population']]
    df = df[df.Sex != 'Both sexes']
    df.sort_values(by='Country', inplace=True, ascending=True)
    
    raw_data_table = df.to_html(classes = 'table table-hover')

    return render_template('data pages/data_suicide_rates.html',
            raw_data_table = raw_data_table,
            title=mutualtitle + ' - Data Model',
            year=datetime.now().year,
        )

@app.route('/data_wpr')
def data_wpr():

    df = pd.read_csv(path.join(path.dirname(__file__), 'static/data/wpr.csv'))
    df = df.drop(['Lower Confidence Interval', 'Upper Confidence Interval'], axis=1)
    
    raw_data_table = df.to_html(classes = 'table table-hover')

    return render_template('data pages/data_wpr.html', 
            raw_data_table = raw_data_table,
            title=mutualtitle + ' - Data Model',
            year=datetime.now().year,
        )


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = UserRegistrationFormStructure(request.form)

    if (request.method == 'POST' and form.validate()):
        if (not db_Functions.IsUserExist(form.username.data)):
            db_Functions.AddNewUser(form)
            db_table = ""

            flash('Welcome '+ form.FirstName.data + " " + form.LastName.data + "!")
        else:
            flash('Error: User ' + form.username.data + ' already exists.')
            form = UserRegistrationFormStructure(request.form)

    return render_template(
        'register.html', 
        form=form, 
        title=mutualtitle + ' - Register',
        year=datetime.now().year,
        repository_name='Pandas',
        )


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginFormStructure(request.form)

    if (request.method == 'POST' and form.validate()):
        if (db_Functions.IsLoginGood(form.username.data, form.password.data)):
            flash('Login successful!'),
        else:
            flash('Incorrect username and/or password.')
   
    return render_template(
        'login.html',
        form=form, 
        title=mutualtitle + ' - Login',
        year=datetime.now().year,
        repository_name='Pandas',
        )



