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

def convert_museumid_to_name(vector):
    df = pd.read_csv(f"{fileDir}/musea.csv", header=0)
    museum_df = df[['translationSetId','publicName']]
    # mylist  = np.argmax(vector)
    ind = np.argpartition(vector, -10)[-10:]

    n = 10
    idx = (-vector).argsort()[:n]
    idx = idx.tolist()
    print(idx)
    recom_list = []

    museum_name_list = []
    museum_id_list = []
    for x in idx:
        museum_id_list.append(museum_df.loc[x].at['translationSetId'])
        museum_name_list.append(museum_df.loc[x].at['publicName'])
    # print(museum_name_list)
    return museum_name_list, museum_id_list

def update_vectors(new, old):

    myarray = np.array(new.values[0])
    new_array = np.transpose(myarray)
    myarray = old*new_array
    return myarray

def new_user(clientid):
    vector = np.zeros(496, dtype=object)
    vector += 1.0
    return vector

def run_all():
    client_vector_dict = {}
    client_id_list = []
    input_df = get_dataframe()
    print(input_df)
    count = 0
    for index, row in input_df.iterrows():
        client = row['clientid']
        museum = row['translationSetId']
        count = row['count']


        if client in client_id_list:
            vector = client_vector_dict.get(client)
        else:
            client_id_list.append(client)
            vector = new_user(client)

        museum_vector = vector_df[(vector_df['translationSetId'] == museum)].vector
        calculated_vector = update_vectors(museum_vector, vector)
        client_vector_dict[client] = calculated_vector

    df = pd.DataFrame()
    for k, v in client_vector_dict.items():
        museum_name_list, museum_id_list = convert_museumid_to_name(v)
        df = df.append({'clientid': k, 'museum_list': museum_name_list, 'museum_id': museum_id_list}, ignore_index=True)
    df.to_csv('result_client_museums.csv')
run_all()
