import csv
import os
import random
import collections
from collections import defaultdict
import shutil
from datetime import date, datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
fileDir = os.path.dirname(os.path.realpath('__file__'))
currentdate = date.today().strftime('%Y.%m.%d')
# currentdate = '2019.04.02'
import json
# Import our other files
from reccommendations import top_ten_random


SYMBOLS = [' ', '/', '-', '&', ',', '\’','\‘', '\'', "'"]

user_id_list = ['x', 'y']


def move_files(filename):
    shutil.move("%s/%s" %(fileDir, filename), "%s/RESULTS/%s" %(fileDir, filename))

def create_file(filename, df):
    df.to_excel(filename, index=False)
    move_files(filename)

def clean_column(df, column):
    for symbol in SYMBOLS:
        df["%s" %column] = df["%s" %column].astype(str).str.replace(r'%s' % symbol,'')
    return df

''' STANDAARD '''

class Client:

    def __init__(self, user_id, country, location):
        self.id = user_id
        self.sessions = []
        self.location = location
        if country == 'Netherlands':
            self.dutch = True
        else:
            self.dutch = False

    def addSession(self, session):
        self.sessions.append(session)

    def create_province(self, df):
        self.province = df.loc[df['Gemeentenaam'] == self.location, 'Provincienaam']

def import_museum_file(file):
    pass

def get_city_list():
    df = pd.read_excel(f"{fileDir}\gemeentes1.xlsx", header=0)

    df.drop(['Gemeentecode'], axis=1, inplace=True)
    return df

def new_user(clientid, sessionid, city, province, id_list):
    global user_id_list
    client = Client(clientid, sessionid, city)
    user_id_list.append(client.id)
    client.create_province(province)

    if client.dutch:
        return []
    else:
        return top_ten_random(id_list)

def initial_run(clientid, sessionid, city, province, id_list):
    global user_id_list, sessions_id_list

    if clientid not in user_id_list:
        recommendation_list = new_user(clientid, sessionid, city, province, id_list)
    else:
        #hier opnieuw een oude client aanmaken op basis van oude ID, moet nog fixen
        client = Client()
        recommendation_list = known_user(client)
    return recommendation_list

# RUN IS KNOWN CODE HERE
def get_files_in_place():

    df = pd.read_csv(f"{fileDir}/musea.csv", header=0)
    museum_df = df['translationSetId']
    #returns the ID list (probably better for later
    # id_list = df['id'].tolist()
    #returns names of museums, to make output more readably
    id_list = df['publicName'].tolist()


    province_df = get_city_list()
    return museum_df, id_list, province_df
museum_df, id_list, province_df = get_files_in_place()
recom_list = initial_run(1,2,3, province_df, id_list)
print(recom_list)
