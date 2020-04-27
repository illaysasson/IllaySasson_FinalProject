### ------------------------------------------------------------ ###
### --- includes all software packages and libraries needed ---- ###
### ------------------------------------------------------------ ###

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.transforms

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

import base64
import datetime
import io
from os import path
### ----------------------------------------------------------- ###


#Turns plot into displayable image
def PlotToIMG(fig):
    pngImage = io.BytesIO()
    FigureCanvas(fig).print_png(pngImage)
    pngImageB64String = "data:image/png;base64,"
    pngImageB64String += base64.b64encode(pngImage.getvalue()).decode('utf8')
    return pngImageB64String


#Returns a list of all available countries in the dataset
def GetCountriesChoice(df):
    df = df.rename(columns={'Country': 'Country'})
    df = df.groupby('Country').sum()
    l = df.index
    m = list(zip(l , l))
    return m

#Sorts and returns WPR dataset
def GetSortedWPR(df):
    df = df[['Country', 'Happiness Score']]
    df.sort_values(by='Happiness Score', inplace=True, ascending=False)
    return df

#Sorts and returns Internet Users dataset
def GetSortedInternetUsers(df):
    df = df[['Country', 'Percentage']]
    df['Percentage'] = df['Percentage'].astype(str)
    df['Percentage'] = df['Percentage'].str.rstrip('%').astype('float')
    df.sort_values(by='Percentage', inplace=True, ascending=False)
    return df

#Sorts and returns Suicide Rates dataset
def GetSortedSuicideRates(df):
    df = df[['Country', 'Sex', 'Suicides/100k Population']]
    df = df.loc[df['Sex'] == 'Both sexes']
    df = df[['Country', 'Suicides/100k Population']]
    return df

#Merges datasets and only includes countries that are present in both datasets
def MergeDatasets(df1, df2):
    return (pd.merge(df1, df2, on=['Country']))