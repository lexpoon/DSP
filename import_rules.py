import csv
import os
import string
import random
import collections
from collections import defaultdict
import shutil
from datetime import date, datetime
import pandas as pd
import numpy as np

fileDir = os.path.dirname(os.path.realpath('__file__'))
currentdate = date.today().strftime('%Y.%m.%d')
# currentdate = '2019.04.02'

SYMBOLS = [' ', '/', '-', '&', ',', '\’', '\‘', '\'', "'"]


def move_files(filename):
    shutil.move("%s/%s" % (fileDir, filename), "%s/RESULTS/%s" % (fileDir, filename))


def create_file(filename, df):
    df.to_excel(filename, index=False)
    move_files(filename)


def clean_column(df, column):
    for symbol in SYMBOLS:
        df["%s" % column] = df["%s" % column].astype(str).str.replace(r'%s' % symbol, '')
    return df


''' STANDAARD '''
from ast import literal_eval

def create_true_falses_addition(row):
    data = literal_eval(row['facilities'])
    if 'MuseumLibrary' in data:
        row['bieb'] = 3
    else:
        row['bieb'] = 0
    if 'OpenAir' in data:
        row['openair'] = 3
    else:
        row['openair'] = 0
    if 'Parking' in data:
        row['parking'] = 7
    else:
        row['parking'] = 0
    if 'WheelchairAccess' in data:
        row['weelchair'] = 10
    else:
        row['weelchair'] = 0
    if 'AccessibleDisabled' in data:
        row['disabled'] = 5
    else:
        row['disabled'] = 0
    if 'NearTrainStation' in data:
        row['trainstation'] = 8
    else:
        row['trainstation'] = 0
    if 'Restaurant' in data:
        row['restaurant'] = 1
    else:
        row['restaurant'] = 0
    return row

def create_true_falses_multiplication(row):
    data = literal_eval(row['facilities'])
    if 'MuseumLibrary' in data:
        row['bieb'] = 2
    else:
        row['bieb'] = 1
    if 'OpenAir' in data:
        row['openair'] = 4
    else:
        row['openair'] = 1
    if 'Parking' in data:
        row['parking'] = 2
    else:
        row['parking'] = 1
    if 'WheelchairAccess' in data:
        row['weelchair'] = 4
    else:
        row['weelchair'] = 1
    if 'AccessibleDisabled' in data:
        row['disabled'] = 5
    else:
        row['disabled'] = 1
    if 'NearTrainStation' in data:
        row['trainstation'] = 3
    else:
        row['trainstation'] = 1
    if 'Restaurant' in data:
        row['restaurant'] = 2
    else:
        row['restaurant'] = 1
    return row

# def create_true_falses_multiplication(row):
#     data = literal_eval(row['facilities'])
#     if 'MuseumLibrary' in data:
#         row['bieb'] = 2.07
#     else:
#         row['bieb'] = 1
#     if 'OpenAir' in data:
#         row['openair'] = 2.53
#     else:
#         row['openair'] = 1
#     if 'Parking' in data:
#         row['parking'] = 2.1
#     else:
#         row['parking'] = 1
#     if 'WheelchairAccess' in data:
#         row['weelchair'] = 3.26
#     else:
#         row['weelchair'] = 1
#     if 'AccessibleDisabled' in data:
#         row['disabled'] = 2.93
#     else:
#         row['disabled'] = 1
#     if 'NearTrainStation' in data:
#         row['trainstation'] = 3.26
#     else:
#         row['trainstation'] = 1
#     if 'Restaurant' in data:
#         row['restaurant'] = 1.88
#     else:
#         row['restaurant'] = 1
#     return row

def create_dataframe(filename):

    df = pd.read_csv(filename, encoding='utf-8')
    df_cleaned = df.drop_duplicates(subset=['publicName'])
    print(len(df_cleaned))
    return df_cleaned

def create_lists(df, x):
    mylist = df[f'{x}'].tolist()
    myarray = np.array(mylist)
    return myarray

def create_row_vectors(row):

    index = row['index']
    vector = np.zeros(496, dtype=object)
    vector += 1
    if row['bieb'] != 1:
        vector *= bieb_array
    if row['openair'] != 1:
        vector *= openair_array
    if row['parking'] != 1:
        vector *= parking_array
    if row['weelchair'] != 1:
        vector *= weelchair_array
    if row['disabled'] != 1:
        vector *= disabled_array
    if row['trainstation'] != 1:
        vector *= trainstation_array
    if row['restaurant'] != 1:
        vector *= restaurant_array
    vector[index] = 1
    return vector

# Create the dataframe from the museum file and so some cleaning
filename = 'musea.csv'
df = create_dataframe(filename)
df = df.drop_duplicates(subset=['publicName'])
df.rename(columns={'Unnamed: 0': "index"}, inplace=True)
# Add all the facilites as on its own columns
df[['bieb', 'openair', 'parking', 'weelchair', 'disabled', 'trainstation', 'restaurant']] = False
# For every facility add the increase/weight/update value which will be converted to the update arrays
df = df.apply(create_true_falses_multiplication, axis=1)

# Create the update arrays for all the facilities
bieb_array = create_lists(df, 'bieb')
openair_array = create_lists(df, 'openair')
parking_array = create_lists(df, 'parking')
weelchair_array = create_lists(df, 'weelchair')
disabled_array = create_lists(df, 'disabled')
trainstation_array = create_lists(df, 'trainstation')
restaurant_array = create_lists(df, 'restaurant')



print(df.head())
df['vector'] = df.apply(create_row_vectors, axis=1)

print(df['vector'].head(n=50))
vector_df = df[['publicName', 'translationSetId', 'vector']]

vector_df.to_csv('vector_csv.csv')
