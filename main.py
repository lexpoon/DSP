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
        self.province = df.loc[df['Gemeentenaam'] == self.location, 'Provincie']


def get_city_list():
    df = pd.read_csv(f"{fileDir}/Data/gemeentes.csv", header=0)

    df.drop(['Gemeentecode'], axis=1, inplace=True)
    return df

def new_user(client, province):
    global user_id_list

    user_id_list.append(client.id)



def initial_run(client, sessionid, city, province):
    global user_id_list, sessions_id_list

    if client.id not in user_id_list:
        new_user(client, province)

# RUN IS KNOWN CODE HERE


province_df = get_city_list()

initial_run(1,2,3, province_df)
