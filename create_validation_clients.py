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
fileDir = os.path.dirname(os.path.realpath('__file__'))
currentdate = date.today().strftime('%Y.%m.%d')
# currentdate = '2019.04.02'
# Import our other files
from recommendations import top_ten_random
from ast import literal_eval
from functools import reduce

SYMBOLS = [' ', '/', '-', '&', ',', '\’','\‘', '\'', "'"]
global user_id_list
user_id_list = []

rules_df = pd.read_csv('rules_overview.csv', header=0)
feature_df = pd.read_csv('featurelist.csv')


print(rules_df.head())
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
    print(full_name)
    return full_name

def choose_feature():
    print('1. History\n2. Visual\n3. Culture\n4. Naval\n5. Tech\n6. Ethnology\n7. Library\n8. Openair\n9. Parking\n10. Weelchair\n11. Disabled\n12. Trainstation\n13. Restaurant\n')
    feature = input('Choose a feature from the list above:\n')

    return feature

def get_feature_list(df, number_f):
    list_of_lists = []
    feature_list = []
    for x in range(number_f):
        feature = random.randint(1,13)
        # feature = get_feature()
        feature = int(feature) + 6

        column = df[df.columns[feature]]
        temp_df = df[(column == 1)]
        mylist = temp_df['translationSetId'].to_list()
        list_of_lists.append(mylist)
        feature = feature-6
        feature_name = make_feature_named(feature)
        feature_list.extend(feature_name)
    return list_of_lists, feature_list

def get_random_museums(df, number_m, number_f):

    # list_of_lists, feature_list = get_feature_list(df, number_f)
    # while not list_of_lists:
    #     print(f'empty for following features: {feature_list}')
        # list_of_lists, feature_list = get_feature_list(df, number_f)
        # return list_of_lists
    mylist = []
    while not mylist:
        list_of_lists, feature_list = get_feature_list(df, number_f)
        mylist = list(reduce(set.intersection, [set(item) for item in list_of_lists ]))

    top_ten = list(set(random.choices(mylist,k=number_m)))
    print(top_ten)

    return top_ten, feature_list

# print(random.randint(0,9))
def create_new_client():
    client_id = ''.join(random.sample(string.ascii_lowercase, 10))
    number_of_museums = 5
    my_list = []
    feature_list = []
    df = pd.DataFrame()
    number_of_features = random.randint(1,3)
    temp_list, features = get_random_museums(rules_df, number_of_museums, number_of_features)
    my_list.extend(temp_list)
    feature_list.extend(features)

    for id in my_list:
        count = random.randint(1,3)

        df = df.append({'clientid': client_id, 'translationSetId': id, 'count': count, 'features': feature_list}, ignore_index=True)
    return df


def get_dataframe():
    frames = []
    for i in range(10):
        temp_df = create_new_client()
        frames.append(temp_df)
    df = pd.concat(frames)
    return df

print(get_dataframe())


''' Er klopt niets van de features. Deze moeten even worden aangepast naar de juiste plek en combinatie met het inlezen van de tabel.'''
