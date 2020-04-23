### ------------------------------------------------------------ ###
### --- includes all software packages and libraries needed ---- ###
### ------------------------------------------------------------ ###

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
from IllaySasson_FinalProject.models.DataQuery import GetSortedSuicideRates
### ------------------------------------------------------------ ###


db_Functions = create_LocalDatabaseServiceRoutines() 
mutualtitle = 'Happiness & The Internet'

app.config['SECRET_KEY'] = '2212'

@app.route('/')
@app.route('/home')
def home():
	#Renders the Home page.
	return render_template(
		'index.html',
		title=mutualtitle,
		year=datetime.now().year,
	)

@app.route('/contact')
def contact():
	#Renders the Contact page.
	return render_template(
		'contact.html',
		title=mutualtitle,
		year=datetime.now().year,
		message='Your contact page.'
	)

@app.route('/about')
def about():
	#Renders the About page.
	return render_template(
		'about.html',
		title=mutualtitle,
		year=datetime.now().year,
		message='Your application description page.'
	)

@app.route('/data_model')
def data_model():
	#Renders the Data Model page.
	return render_template(
		'data_model.html',
		title=mutualtitle + ' - Data Model',
		year=datetime.now().year,
	)


@app.route('/data_internet_users')
def data_internet_users():
	#Renders the Internet Users Data page.

	#Reads and sorts the Internet Users dataset
	df = pd.read_csv(path.join(path.dirname(__file__), 'static/data/internet_users.csv'))
	df = df[['Country', 'Population', 'Population Rank', 'Internet Users', 'Percentage', 'Internet Users Rank']]
	df.sort_values(by='Country', inplace=True, ascending=True)
	
	#Turns the dataset into a displayable HTML table
	raw_data_table = df.to_html(classes = 'table table-hover')

	return render_template('data pages/data_internet_users.html', 
			raw_data_table = raw_data_table,
			title=mutualtitle + ' - Data Model',
			year=datetime.now().year,
		)

@app.route('/data_suicide_rates')
def data_suicide_rates():
	#Renders the Suicide Rates Data page.

	#Reads and sorts the Suicide Rates dataset
	dffull = pd.read_csv(path.join(path.dirname(__file__), 'static/data/suicide_rates.csv'))
	df = dffull[['Country', 'Sex', 'Suicides/100k Population']]
	df = df[df.Sex != 'Both sexes']
	df.sort_values(by='Country', inplace=True, ascending=True)
	
	#Turns the dataset into a displayable HTML table
	raw_data_table = df.to_html(classes = 'table table-hover')

	return render_template('data pages/data_suicide_rates.html',
			raw_data_table = raw_data_table,
			title=mutualtitle + ' - Data Model',
			year=datetime.now().year,
		)

@app.route('/data_wpr')
def data_wpr():
	#Renders the World Happiness Report Data page.

	#Reads and sorts the WPR dataset
	df = pd.read_csv(path.join(path.dirname(__file__), 'static/data/wpr.csv'))
	df = df.drop(['Lower Confidence Interval', 'Upper Confidence Interval'], axis=1)
	df_copy = "No Countries Selected"
	
	#Turns the dataset into a displayable HTML table
	raw_data_table = df.to_html(classes = 'table table-hover')

	return render_template('data pages/data_wpr.html', 
			raw_data_table = raw_data_table,
			title=mutualtitle + ' - Data Model',
			year=datetime.now().year,
		)


@app.route('/data_query',  methods=['GET', 'POST'])
def data_query():
	#Renders the Data Query page.

	#Placeholder image instead of graph
	fig_image = 'static/images/waitingforinput.png'

	#Imports all datasets
	df_wpr = pd.read_csv(path.join(path.dirname(__file__), 'static/data/wpr.csv'))
	df_iu = pd.read_csv(path.join(path.dirname(__file__), 'static/data/internet_users.csv'))
	df_sr = pd.read_csv(path.join(path.dirname(__file__), 'static/data/suicide_rates.csv'))

	#Gets sorted datasets
	df_wpr = GetSortedWPR(df_wpr)
	df_iu = GetSortedInternetUsers(df_iu)
	df_sr = GetSortedSuicideRates(df_sr)


	#Merges the WPR and Internet Users datasets (Only includes countries that are present in both datasets)
	df = MergeDatasets(df_wpr, df_iu)

	#Merges the two datasets with the Suicide Rates dataset, sorts it and turns it into a displayable HTML table (Displays countries that have no Suicide Rates data)
	full_df = pd.merge(df, df_sr, how='left', on=['Country'])
	full_df.sort_values(by='Suicides/100k Population', inplace=True, ascending=True)
	full_df = full_df.to_html(classes = 'table table-hover')

	#Sets the list of countries to all the countries in the merged dataset
	form = QueryFormStructure(request.form)    
	form.countries.choices = GetCountriesChoice(df)  


	if (request.method == 'POST' ):

		#Gets the user's parameters for the query
		countries = form.countries.data
		sortby = form.sortby.data

		#Creates 2 empty lists for the percentage & happiness parameters
		percentage = []
		happiness = []

		#For each country, finds the percentage in the merged df and puts it in the percentage list with the same index as the country.
		for x in countries:
			percentage.append(df.loc[df['Country'] == x]['Percentage'].values[0])

		#For each country, finds the happiness in the merged df and puts it in the happiness list with the same index as the country.    
		for x in countries:
			happiness.append(df.loc[df['Country'] == x]['Happiness Score'].values[0])


		#Sorts the happiness score	/	percentage of internet users from large to small, depending on what the user chose
		if sortby == "% of Internet Users":
			index = np.argsort(percentage)
		else:
			index = np.argsort(happiness)
		

		#All the lists then are ordered so the countries, happiness and percentage will all share the same index
		happiness = np.array(happiness)[index]
		countries = np.array(countries)[index]
		percentage = np.array(percentage)[index]

		
		#Creates a horizontal bar graph with 2 X axes that share the same Y axis, and changes the size of the graph according to number of countries selected
		if len(countries) <= 30:
			fig, axes = plt.subplots(ncols=2, sharey=True, figsize=[8, 8])
		elif len(countries) <= 50:
			fig, axes = plt.subplots(ncols=2, sharey=True, figsize=[8, 12])
		elif len(countries) <= 100:
			fig, axes = plt.subplots(ncols=2, sharey=True, figsize=[8, 16])
		else:
			fig, axes = plt.subplots(ncols=2, sharey=True, figsize=[8, 22])
			
		#Defines the 2 X axes (Happiness & Percentage) and their shared Y axis (Countries)
		axes[0].barh(countries, happiness, align='center', color='#ed6255', zorder=10)
		axes[1].barh(countries, percentage, align='center', color='#6473e8', zorder=10)

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


		#Code that centers y labels (uses matplotlib.transforms framework):

		#Space between the 2 bar plots
		fig.tight_layout()
		fig.subplots_adjust(wspace=0.7)

		plt.setp(axes[0].yaxis.get_majorticklabels(), ha='center')

		#Creates offset
		dx = 62 / 72.
		dy = 0 / 72.
		offset = matplotlib.transforms.ScaledTranslation(dx, dy, fig.dpi_scale_trans)

		#Applies the offset to all labels
		for label in axes[0].yaxis.get_majorticklabels():
			label.set_transform(label.get_transform() + offset)

		#Turns the plot into a displayable image
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
	#Renders the Register page.

	form = UserRegistrationFormStructure(request.form)

	if (request.method == 'POST'):
		if form.validate(): #Checks if all the form validators' conditions are met
			if (not db_Functions.IsUserExist(form.username.data)): #Checks if the user that is trying to register exists already in the users dataset
				db_Functions.AddNewUser(form) #If not, adds the new user into the users dataset
				db_table = ""

				flash('Welcome '+ form.FirstName.data + " " + form.LastName.data + "!")
			else:
				flash('Error: User ' + form.username.data + ' already exists.') #If it already exists, returns an error
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
	#Renders the Login page.

	form = LoginFormStructure(request.form)

	if (request.method == 'POST' and form.validate()): #Checks if all the form validators' conditions are met
		if (db_Functions.IsLoginGood(form.username.data, form.password.data)): #Check if the username and password pair exist in the users dataset
			return redirect('data_query') #If it exists, redirects to the Data Query page
		else:
			flash('Incorrect username and/or password.') #If not, returns an error
			
	return render_template(
		'login.html',
		form=form, 
		title=mutualtitle + ' - Login',
		year=datetime.now().year,
		repository_name='Pandas',
		)