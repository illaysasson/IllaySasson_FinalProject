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
from wtforms import StringField, SubmitField, SelectMultipleField
from wtforms.validators import DataRequired

import numpy as np
import matplotlib.pyplot as plt
from   matplotlib.figure import Figure
import matplotlib.transforms
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
from IllaySasson_FinalProject.models.QueryFormStructure import QueryFormStructure 

from IllaySasson_FinalProject.models.DataQuery import PlotToIMG 
from IllaySasson_FinalProject.models.DataQuery import GetCountriesChoice
from IllaySasson_FinalProject.models.DataQuery import MergeDatasets 
from IllaySasson_FinalProject.models.DataQuery import GetSortedInternetUsers
from IllaySasson_FinalProject.models.DataQuery import GetSortedWPR



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
	df = dffull[['Country', 'Population', 'Population Rank', 'Internet Users', 'Percentage', 'Internet Users Rank']]
	df.sort_values(by='Country', inplace=True, ascending=True)
	
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


@app.route('/data_query',  methods=['GET', 'POST'])
def data_query():

	fig_image = 'static/images/waitingforinput.png'
	full_df = ""

	df_wpr = pd.read_csv(path.join(path.dirname(__file__), 'static/data/wpr.csv'))
	df_iu = pd.read_csv(path.join(path.dirname(__file__), 'static/data/internet_users.csv'))

	#Gets sorted WPR & Internet Users dataset
	df_wpr = GetSortedWPR(df_wpr)
	df_iu = GetSortedInternetUsers(df_iu)

	#Merges both datasets (Only includes countries that are present in both datasets)
	df = MergeDatasets(df_wpr, df_iu)
	full_df = df.to_html(classes = 'table table-hover')


	form = QueryFormStructure(request.form)    
	#Sets the list of countries to all the countries in the merged dataset
	form.countries.choices = GetCountriesChoice(df)  

	 
	if (request.method == 'POST' ):

		#Gets the user's parameters for the query
		countries = form.countries.data

		#Creates 2 empty lists for the percentage & happiness parameters
		percentage = []
		happiness = []

		#For each country, finds the percentage in the merged df and puts it in the percentage list with the same index as the country.
		for x in countries:
			percentage.append(df.loc[df['Country'] == x]['Percentage'].values[0])

		#For each country, finds the happiness in the merged df and puts it in the happiness list with the same index as the country.    
		for x in countries:
			happiness.append(df.loc[df['Country'] == x]['Happiness Score'].values[0])

		#Orders the happiness list from small to large
		index = np.argsort(happiness)
		happiness = np.array(happiness)[index]

		#All the lists then are ordered so the percentage and country will match the happienss score and they all will share the same index.
		countries = np.array(countries)[index]
		percentage = np.array(percentage)[index]

		
		#Changes the size of the graph according to number of countries selected
		if len(countries) <= 30:
			fig, axes = plt.subplots(ncols=2, sharey=True, figsize=[8, 8])
		elif len(countries) <= 50:
			fig, axes = plt.subplots(ncols=2, sharey=True, figsize=[8, 12])
		elif len(countries) <= 100:
			fig, axes = plt.subplots(ncols=2, sharey=True, figsize=[8, 16])
		else:
			fig, axes = plt.subplots(ncols=2, sharey=True, figsize=[8, 22])
			
		#Defines 2 X axes that share the same Y axis
		axes[0].barh(countries, happiness, align='center', color='#de8071', zorder=10)
		axes[1].barh(countries, percentage, align='center', color='#5675d1', zorder=10)

		#Inverts the left x axis so both axes will start from the center
		axes[0].invert_xaxis()

		#Sets titles & labels
		axes[0].set(title='Happiness Score')
		axes[1].set(title='Percentage of Internet Users')
		axes[0].set(yticklabels=countries)
		axes[0].yaxis.tick_right()

		#Creates a grid for both X axes
		for ax in axes:
			ax.margins(0.03)
			ax.grid(True)


		#Space between the 2 bar plots
		fig.tight_layout()
		fig.subplots_adjust(wspace=0.7)
		
		fig_image = PlotToIMG(fig)


	return render_template('data_query.html', 
			form = form, 
			raw_data_table = full_df,
			fig_image = fig_image,
			title=mutualtitle + ' - Data Query',
			year=datetime.now().year,
		)


@app.route('/register', methods=['GET', 'POST'])
def register():
	form = UserRegistrationFormStructure(request.form)

	if (request.method == 'POST'):
		if form.validate():
			if (not db_Functions.IsUserExist(form.username.data)):
				db_Functions.AddNewUser(form)
				db_table = ""

				flash('Welcome '+ form.FirstName.data + " " + form.LastName.data + "!")
			else:
				flash('Error: User ' + form.username.data + ' already exists.')
				form = UserRegistrationFormStructure(request.form)
		else:
			flash('Some fields are invalid.')

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
			return redirect('data_query')
		else:
			flash('Incorrect username and/or password.')
   
	return render_template(
		'login.html',
		form=form, 
		title=mutualtitle + ' - Login',
		year=datetime.now().year,
		repository_name='Pandas',
		)


