"""
Used structures and classes
"""
from os import path
import json
import pandas as pd

def create_LocalDatabaseServiceRoutines():
    return LocalDatabaseServiceRoutines()

class LocalDatabaseServiceRoutines(object):
    def __init__(self):
        self.name = 'Data base service routines'
        self.index = {}
        self.UsersDataFile = path.join(path.dirname(__file__), '..\\static\\Data\\users.csv')


    def ReadCSVUsersDB(self):
        df = pd.read_csv(self.UsersDataFile)
        return df


    def WriteCSVToFile_users(self, df):
        df.to_csv(self.UsersDataFile, index=False)


    def IsUserExist(self, UserName):
        df = self.ReadCSVUsersDB()
        df = df.set_index('username')
        return (UserName in df.index.values)


    def IsLoginGood(self, UserName, Password):
        df = self.ReadCSVUsersDB()
        df=df.reset_index()
        selection = [UserName]
        df = df[pd.DataFrame(df.username.tolist()).isin(selection).any(1)]

        df = df.set_index('password')
        return (Password in df.index.values)
     

    def AddNewUser(self, User):
        df = self.ReadCSVUsersDB()
        dfNew = pd.DataFrame([[User.FirstName.data, User.LastName.data, User.Gender.data, User.EmailAddr.data, User.username.data, User.password.data]], columns=['FirstName', 'LastName', 'Gender', 'EmailAddr',  'username', 'password'])
        dfComplete = df.append(dfNew, ignore_index=True)
        self.WriteCSVToFile_users(dfComplete)