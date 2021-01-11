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
# from analytics import run_all_analytics
from create_validation_clients import get_dataframe
from import_rules import vector_df
SYMBOLS = [' ', '/', '-', '&', ',', '\’','\‘', '\'', "'"]
global user_id_list
user_id_list = []


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
from ast import literal_eval

def convert_museumid_to_name(recom_list):
    df = pd.read_csv(f"{fileDir}/musea.csv", header=0)
    museum_df = df[['translationSetId','publicName']]

    museum_name_list = []
    for x in recom_list:
        museum_name_list.append(museum_df.loc[museum_df['translationSetId'] == x].publicName.iloc[0])

    return museum_name_list

def update_vectors(new, old):

    myarray = np.array(new)
    myarray = old*myarray
    return myarray

def new_user(clientid):
    vector = np.zeros(496, dtype=object)
    vector += 1.0
    return vector


def run_all():
    client_vector_dict = {}
    client_id_list = []
    input_df = get_dataframe()
    count = 0
    for index, row in input_df.iterrows():
        client = row['clientid']
        museum = row['translationSetId']
        count = row['count']

        vector = client_vector_dict.get(client)

        if client in client_id_list:
            vector = client_vector_dict.get(client)
        else:
            client_id_list.append(client)
            vector = new_user(client)

        # update_vector = update_vector(vector, museum, count)
        # temp_df = df[(column == 1)]
        museum_vector = vector_df[(vector_df['translationSetId'] == museum)].vector

        calculated_vector = update_vectors(museum_vector, vector)
        # print(calculated_vector)
        count +=1
        client_vector_dict.update({client: calculated_vector})
        # museum_list = convert_museumid_to_name(recom_list)
    print(count)


run_all()
