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
# Import our other files
from recommendations import top_ten_random
from analytics import run_all_analytics
from ast import literal_eval

SYMBOLS = [' ', '/', '-', '&', ',', '\’','\‘', '\'', "'"]
global user_id_list
user_id_list = []

analytics_df = run_all_analytics()

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

def convert_museumid_to_name(recom_list):
    df = pd.read_csv(f"{fileDir}/musea.csv", header=0)
    museum_df = df[['translationSetId','publicName']]

    museum_name_list = []
    for x in recom_list:
        museum_name_list.append(museum_df.loc[museum_df['translationSetId'] == x].publicName.iloc[0])

    return museum_name_list



class Client:
    id_list = []
    def __init__(self, user_id):
        self.id = user_id
        Client.id_list.append(user_id)
        self.vector = self.initialze_vector()

    def initialze_vector(self):
        vector = np.zeros(496, dtype=object)
        vector += 1
        return vector

    def update_vector(self, input_vec):
        self.vector *= input_vec


def update_vector(in_vector):
    pass

def new_user(clientid):
    global user_id_list
    user_id_list.append(clientid)

    vector = np.zeros(496, dtype=object)
    vector += 1


def initial_run(clientid, translationsetid, count):
    global user_id_list, sessions_id_list

    if clientid not in user_id_list:
        vector = new_user(clientid, translationsetid, count)

    else:
        #hier opnieuw een oude client aanmaken op basis van oude ID, moet nog fixen
        client = Client()
        recommendation_list = known_user(client)
    return recommendation_list


def run_all():

    input_df = run_all_analytics()
    for index, row in input_df.iterrows():

        recom_list = initial_run(row['clientid'], row['translationSetId'], row['count'])
        museum_list = convert_museumid_to_name(recom_list)


