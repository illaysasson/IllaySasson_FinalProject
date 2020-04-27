### ------------------------------------------------------------ ###
### --- includes all software packages and libraries needed ---- ###
### ------------------------------------------------------------ ###

from os import path
import json
import pandas as pd
### ----------------------------------------------------------- ###


def create_LocalDatabaseServiceRoutines():
    return LocalDatabaseServiceRoutines()

class LocalDatabaseServiceRoutines(object):

    #Defines the class
    def __init__(self):
        self.name = 'Data base service routines'
        self.index = {}
        self.UsersDataFile = path.join(path.dirname(__file__), '..\\static\\Data\\users.csv')

    #Returns the users data as a dataset
    def ReadCSVUsersDB(self):
        df = pd.read_csv(self.UsersDataFile)
        return df

    #Saves the user's input into the users dataset
    def WriteCSVToFile_users(self, df):
        df.to_csv(self.UsersDataFile, index=False)

    #Checks if the username exists in the users dataset (Returns a boolean)
    def IsUserExist(self, UserName):
        df = self.ReadCSVUsersDB()
        df = df.set_index('username')
        return (UserName in df.index.values)

    #Checks if the username and password pair exist in the users dataset (Returns a boolean)
    def IsLoginGood(self, UserName, Password):
        df = self.ReadCSVUsersDB()
        df=df.reset_index()
        selection = [UserName]
        df = df[pd.DataFrame(df.username.tolist()).isin(selection).any(1)]
        df = df.set_index('password')
        return (Password in df.index.values)
     
    #Adds a new user to the users dataset
    def AddNewUser(self, User):
        df = self.ReadCSVUsersDB()
        dfNew = pd.DataFrame([[User.FirstName.data, User.LastName.data, User.Gender.data, User.EmailAddr.data, User.username.data, User.password.data]], columns=['FirstName', 'LastName', 'Gender', 'EmailAddr',  'username', 'password'])
        dfComplete = df.append(dfNew, ignore_index=True)
        self.WriteCSVToFile_users(dfComplete)