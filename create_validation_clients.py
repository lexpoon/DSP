import csv
import os
import random, string
import collections
from collections import defaultdict
import shutil
from datetime import date, datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas import ExcelWriter
from ast import literal_eval
from functools import reduce

fileDir = os.path.dirname(os.path.realpath('__file__'))
currentdate = date.today().strftime('%Y.%m.%d')
SYMBOLS = [' ', '/', '-', '&', ',', '\’','\‘', '\'', "'"]

# Import needed dataframes
rules_df = pd.read_csv('Data/rules_overview.csv', header=0)
feature_df = pd.read_csv('Data/featurelist.csv')


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
        museum_name_list.extend(museum_df.loc[museum_df['translationSetId'] == x].publicName.iloc[0])
    return museum_name_list

def make_feature_named(feature):
    full_name = feature_df.loc[(feature_df['Number'] == feature), 'Name']
    return full_name

def choose_feature():
    print('1. History\n2. Visual\n3. Culture\n4. Naval\n5. Tech\n6. Ethnology\n7. Library\n8. Openair\n9. Parking\n10. Weelchair\n11. Disabled\n12. Trainstation\n13. Restaurant\n')
    feature = input('Choose a feature from the list above:\n')
    return feature
def return_feature(number):

    if number == 1:
        return random.randint(1,12), 3
    if number == 2:
        return random.randint(1,10), 15
    elif number == 3:
        return random.randint(1,9), 25
    else:
        return random.randint(1,7), 34

def get_feature_list(df, number_f):
    list_of_lists = []
    feature_list = []
    feature_list_numbers = []
    feature_group_list = []
    for x in range(number_f):
        feature_group = random.randint(1,4)
        feature, addup= return_feature(feature_group)
        while feature_group in feature_group_list:
            feature_group = random.randint(1,4)
            feature, addup = return_feature(feature_group)
        feature_list_numbers.append(feature)
        feature_group_list.append(feature_group)
        feature = int(feature) + addup
        column = df[df.columns[feature]]
        temp_df = df[(column == 1)]
        mylist = temp_df['translationSetId'].to_list()
        list_of_lists.append(mylist)
        feature = feature-3
        feature_name = make_feature_named(feature)
        feature_list.extend(feature_name)
    return list_of_lists, feature_list

def get_feature_list_demo(df, number_f):
    list_of_lists = []
    feature_list = []
    feature_list_numbers = []
    feature_group_list = []
    for x in range(number_f):
        feature_group = random.randint(1,4)
        feature, addup= return_feature(feature_group)
        while feature_group in feature_group_list:
            feature_group = random.randint(1,4)
            feature, addup = return_feature(feature_group)
        feature_list_numbers.append(feature)
        feature_group_list.append(feature_group)
        feature = int(feature) + addup
        column = df[df.columns[feature]]
        temp_df = df[(column == 1)]
        mylist = temp_df['translationSetId'].to_list()
        # assert isinstance(mylist, object)
        list_of_lists.append(mylist)
        feature = feature-3
        feature_name = make_feature_named(feature)
        feature_list.extend(feature_name)
    return list_of_lists, feature_list

def get_random_museums(df, number_m, number_f):
    mylist = []
    while not mylist:
        list_of_lists, feature_list = get_feature_list(df, number_f)
        mylist = list(reduce(set.intersection, [set(item) for item in list_of_lists ]))
    chosen_museums = list(set(random.choices(mylist,k=number_m)))
    return chosen_museums, feature_list

def get_museum_name(id):
    name = rules_df.loc[rules_df['translationSetId'] == id, 'publicName'].values[0]
    return name
def create_excel_file_input(df):
    client_list = list(set(df['clientid'].to_list()))
    clients_for_excel = (random.choices(client_list,k=30))
    with ExcelWriter("input_excel.xlsx") as writer:
        for client_x in clients_for_excel:
            row = df[(df['clientid'] == client_x)]
            row.drop(columns='translationSetId', inplace=True)

            row.to_excel(writer, sheet_name=client_x)
    move_files('input_excel.xlsx')
    return clients_for_excel
def create_new_client():
    client_id = ''.join(random.sample(string.ascii_lowercase, 10))
    number_of_museums = 3
    my_list = []
    feature_list = []
    df = pd.DataFrame()
    '''CHOOSE THE AMOUNT OF FEATURES HERE'''
    number_of_features = 3
    temp_list, features = get_random_museums(rules_df, number_of_museums, number_of_features)
    my_list.extend(temp_list)
    feature_list.extend(features)

    for id in my_list:
        count = 1
        museum_name = get_museum_name(id)
        df = df.append({'clientid': client_id, 'translationSetId': id,'museum_name': museum_name, 'count': count, 'features': feature_list}, ignore_index=True)

    return df

def get_dataframe_validation():
    frames = []
    for i in range(50):
        temp_df = create_new_client()
        frames.append(temp_df)
    df = pd.concat(frames)

    clients_for_excel = create_excel_file_input(df)
    return df, clients_for_excel

dataframe, clients_for_excel = get_dataframe_validation()
