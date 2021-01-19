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
from pandas import ExcelWriter

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

# df_rules_overview = df_rules_overview.astype(int)
# df_rules_overview.replace(1.0, value=1, inplace=True)
# df_rules_overview.replace(0.0, value=0, inplace=True)
# df_rules_overview.replace(1, value=True, inplace=True)
# df_rules_overview.replace(0, value=False, inplace=True)

feature_df = pd.read_csv("featurelist.csv")
all_features_list = feature_df['Name'].to_list()

df_x = pd.read_csv(f"{fileDir}/musea.csv", header=0)
museum_df = df_x[['translationSetId','publicName']]
museum_df = museum_df.drop_duplicates(subset=['publicName'])
museum_df = museum_df.sort_values('translationSetId')
museum_df = museum_df.reset_index(drop=True)
all_museums_list = museum_df['translationSetId'].to_list()

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
    ''' HIER MUSEUM DF UIT HALEN EN ERGENS BOVEN GLOBAL ERIN FIXEN'''

    recomm_amount = 10
    ind = np.argpartition(vector, -10)[-10:]
    idx = (-vector).argsort()[:recomm_amount]
    idx = idx.tolist()

    museum_name_list = []
    museum_id_list = []
    for x in idx:
        ''' MOET DE MUSEUM DATAFRAMES NOG CHECKEN - SORTEN OP MUSEUM NAAM OF ID?? ZODAT INDEX ALTIJD HETZELFDE IS'''
        museum_id_list.append(museum_df.loc[x].at['translationSetId'])
        museum_name_list.append(museum_df.loc[x].at['publicName'])
    return museum_name_list, museum_id_list

def update_vectors(new, old, count):

    myarray = np.array(new.values[0])
    myarray *= count
    new_array = np.transpose(myarray)
    myarray = old*new_array
    return myarray

def prepare_excel_file(mydict):
    with ExcelWriter("validation_excel.xlsx") as writer:
        for k, v in mydict.items():
            v.to_excel(writer, sheet_name=k)

def create_excel_sheet(row):
    museum_list = row['museum_id'].values[0]
    features = row['features'].values[0]
    df = create_validation(museum_list, features)

    return df

def create_statistical(df, museum_list, features, museum_dict, feature_dict):
    # deze totals gebruiken bij het delen van de sums/counts per musea/feature. Hiermee krijg je precision/recall/accuracy
    museum_total = len(museum_list)
    feature_total = len(features)
    feature_row = df.iloc[-1]

    for feature in features:
        data = int(feature_row[f'{feature}'])
        feature_dict[feature] = data + feature_dict.get(feature)

    for museum in museum_list:
        data = df.loc[df['translationSetId'] == museum]
        number = int(data['museum total'].values[0])
        museum_dict[museum] = number + museum_dict.get(museum)


def create_validation(museum_list, features):
    print('museums:', museum_list)
    print('features:', features )
    new_df = df_rules_overview['translationSetId']
    new_df = new_df.to_frame()
    for feature in features:
        correct_column = df_rules_overview[f'{feature}']
        new_df[f'{feature}'] = correct_column
    total_df_list = []
    for museum in museum_list:
        row = new_df.loc[(new_df['translationSetId'] == museum)]
        row['museumname'] = museum_df.loc[museum_df.translationSetId == museum]['publicName']
        # row.drop(columns='', inplace=True)

        # print(museum_df.loc[museum_df.translationSetId == museum])
        total_df_list.append(row)
    total_df = pd.concat(total_df_list)
    total_df.loc['feature total']= total_df.sum(numeric_only=True, axis=0)
    total_df.loc[:,'museum total'] = total_df.sum(numeric_only=True, axis=1)
    return total_df

def run_all_validation():
    client_vector_dict = {}
    client_features_dict = {}
    client_id_list = []
    input_df = get_dataframe()

    for index, row in input_df.iterrows():

        client = row['clientid']
        museum = row['translationSetId']

        ''' MOET NOG WAT DOEN MET DE COUNT VAN HIERONDER - VERWERKEN IN VECTOR MULTIPLICATION'''
        count = row['count']

        if client in client_id_list:
            vector = client_vector_dict.get(client)
        else:
            client_id_list.append(client)
            vector = np.ones(496, dtype=object)
            features = row['features']
            client_features_dict[client] = features

        museum_vector = vector_df[(vector_df['translationSetId'] == museum)].vector
        calculated_vector = update_vectors(museum_vector, vector, count)
        client_vector_dict[client] = calculated_vector

    df_vectors = pd.DataFrame()
    for k, v in client_vector_dict.items():
        museum_name_list, museum_id_list = convert_museumid_to_name(v)
        df_vectors = df_vectors.append({'clientid': k, 'museum_list': museum_name_list, 'museum_id': museum_id_list}, ignore_index=True)
    df_features = pd.DataFrame()
    for k, v in client_features_dict.items():
        df_features = df_features.append({'clientid': k, 'features': v}, ignore_index=True)

    df_total = df_vectors.merge(df_features, how='inner', on='clientid')

    print('\n\n\nFROM HERE--------------\n')
    museum_validation_dict = dict.fromkeys(all_museums_list, 0)
    feature_validation_dict = dict.fromkeys(all_features_list, 0)
    for index, row in df_total.iterrows():
        client = row['clientid']
        museum_list = row['museum_id']
        features = row['features']
        result_df = create_validation(museum_list, features)
        create_statistical(result_df, museum_list, features, museum_validation_dict, feature_validation_dict)

    clients_for_excel = (random.choices(client_id_list,k=10))
    dataframe_dict = {}
    for client_x in clients_for_excel:
        row = df_total[(df_total['clientid'] == client_x)]
        temp_df = create_excel_sheet(row)
        print(temp_df)
        dataframe_dict[client_x] = temp_df
        prepare_excel_file(dataframe_dict)

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
            vector = np.ones(496, dtype=object)

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
