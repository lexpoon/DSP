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
from import_rules import vector_df, df_rules_overview
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

    museum_name_list = []
    museum_id_list = []
    for x in idx:
        museum_id_list.append(museum_df.loc[x].at['translationSetId'])
        museum_name_list.append(museum_df.loc[x].at['publicName'])
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
def create_excel_sheet(client, museum_list, features):
    '''
    df = museum dataframe met alle onehot yes/no columns
    maak nieuwe df met alleen de columns die in de feature list staan
    dan misschien nog wat counts toevoegen
    '''
    new_df = pd.DataFrame()
    print(features)
    # features = literal_eval(features[1])
    # print(features[1])
    for feature in features:
        correct_column = df_rules_overview[f'{feature}']
        new_df = new_df.merge(correct_column)
    print(new_df)
    # for museum in museum_list:
    #     correct_column = df_rules_overview.loc[(df_rules_overview[f'{museum}'] == museum) ^ (df_rules_overview['column_name'] <= B)]
def run_all_validation():
    client_vector_dict = {}
    client_features_dict = {}
    client_id_list = []
    input_df = get_dataframe()

    for index, row in input_df.iterrows():
        client = row['clientid']
        museum = row['translationSetId']
        count = row['count']

        if client in client_id_list:
            vector = client_vector_dict.get(client)
        else:
            client_id_list.append(client)
            vector = new_user(client)
            features = row['features']
            client_features_dict[client] = features

        museum_vector = vector_df[(vector_df['translationSetId'] == museum)].vector
        calculated_vector = update_vectors(museum_vector, vector)
        client_vector_dict[client] = calculated_vector

    df_vectors = pd.DataFrame()
    for k, v in client_vector_dict.items():
        museum_name_list, museum_id_list = convert_museumid_to_name(v)
        df_vectors = df_vectors.append({'clientid': k, 'museum_list': museum_name_list, 'museum_id': museum_id_list}, ignore_index=True)
    df_features = pd.DataFrame()
    for k, v in client_features_dict.items():
        df_features = df_features.append({'clientid': k, 'features': v}, ignore_index=True)

    clients_for_excel = (random.choices(client_id_list,k=10))
    df_total = df_vectors.merge(df_features, how='inner', on='clientid')
    for client in clients_for_excel:
        row = df_total[(df_total['clientid'] == client)]
        museum_list = row['museum_list']
        # features = literal_eval(row['features'])
        features = row['features'].values
        create_excel_sheet(client, museum_list, features)
    df_total.to_csv('result_client_museums.csv')

def run_all_train():
    client_vector_dict = {}
    client_id_list = []
    '''HIER INPUT VAN ANALYTICS DATA IN GIEREN'''
    input_df = get_dataframe()
    print(input_df)

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

# run_all_train()
run_all_validation()
print(df_rules_overview.info())
