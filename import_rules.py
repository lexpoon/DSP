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

def create_true_falses_multiplication(row):
    data = literal_eval(row['facilities'])

    # These are the vector updates based on the facilities column
    if 'MuseumLibrary' in data:
        row['bieb'] = 1
    else:
        row['bieb'] = 0
    if 'OpenAir' in data:
        row['openair'] = 1
    else:
        row['openair'] = 0
    if 'Parking' in data:
        row['parking'] = 1
    else:
        row['parking'] = 0
    if 'WheelchairAccess' in data:
        row['weelchair'] = 1
    else:
        row['weelchair'] = 0
    if 'AccessibleDisabled' in data:
        row['disabled'] = 1
    else:
        row['disabled'] = 0
    if 'NearTrainStation' in data:
        row['trainstation'] = 1
    else:
        row['trainstation'] = 0
    if 'Restaurant' in data:
        row['restaurant'] = 1
    else:
        row['restaurant'] = 0

    # These are the vector updates based on the categories found in the external museum data file

    return row

def create_dataframe(filename):

    df = pd.read_csv(filename, encoding='utf-8')
    df_cleaned = df.drop_duplicates(subset=['publicName'])
    print(len(df_cleaned))
    return df_cleaned

def apply_onehot(df):
    one_hot_cat = df.museaal_thema.str.get_dummies(', ')
    df = pd.concat([df, one_hot_cat], axis=1)
    print(df.info())
    return df

def create_lists(df, x, addition):
    mylist = df[f'{x}'].tolist()
    myarray = np.array(mylist)
    myarray *= addition
    myarray += 1
    return myarray


def create_row_vectors(row):

    index = row['index']
    vector = np.zeros(496, dtype=object)
    vector += 1
    if row['bieb'] != 0:
        vector *= bieb_array
    if row['openair'] != 0:
        vector *= openair_array
    if row['parking'] != 0:
        vector *= parking_array
    if row['weelchair'] != 0:
        vector *= weelchair_array
    if row['disabled'] != 0:
        vector *= disabled_array
    if row['trainstation'] != 0:
        vector *= trainstation_array
    if row['restaurant'] != 0:
        vector *= restaurant_array
    if row['History'] != 0:
        vector *= history_array
    if row['Visual'] != 0:
        vector *= visual_array
    if row['Culture'] != 0:
        vector *= culture_array
    if row['Naval'] != 0:
        vector *= naval_array
    if row['Nature'] != 0:
        vector *= nature_array
    if row['Tech'] != 0:
        vector *= tech_array
    if row['Ethnology'] != 0:
        vector *= ethnology_array

    vector[index] = 1
    return vector
def return_vector(df):
    return df
# Create the dataframe from the museum file and so some cleaning
filename = 'musea.csv'
df = create_dataframe(filename)
df = df.drop_duplicates(subset=['publicName'])
df.rename(columns={'Unnamed: 0': "index"}, inplace=True)
df = df[['publicName', 'index', 'translationSetId', 'facilities']]
df = df.sort_values('translationSetId')
df = df.reset_index(drop=True)

# Import the extra categories from the visitor file
df_visitor = create_dataframe('Notebooks/museua_visitors.csv')
df = df.merge(df_visitor, how='left', left_on='translationSetId', right_on='translationSetId')
df = df.fillna(0)
# Add all the facilites as on its own columns
df[['bieb', 'openair', 'parking', 'weelchair', 'disabled', 'trainstation', 'restaurant']] = False
# For every facility add the increase/weight/update value which will be converted to the update arrays
df = df.apply(create_true_falses_multiplication, axis=1)
df.drop(columns='publicName_y')
df.rename(columns={'publicName_x': "publicName"}, inplace=True)

df.to_csv('rules_overview.csv')
# Create the update arrays for all the facilities
bieb_array = create_lists(df, 'bieb', 2)
openair_array = create_lists(df, 'openair', 3)
parking_array = create_lists(df, 'parking', 2)
weelchair_array = create_lists(df, 'weelchair', 4)
disabled_array = create_lists(df, 'disabled', 5)
trainstation_array = create_lists(df, 'trainstation', 2)
restaurant_array = create_lists(df, 'restaurant', 2)
history_array = create_lists(df, 'History', 2)
visual_array = create_lists(df, 'Visual', 2)
culture_array = create_lists(df, 'Culture', 3)
naval_array = create_lists(df, 'Naval', 3)
nature_array = create_lists(df, 'Nature', 3)
tech_array = create_lists(df, 'Tech', 3)
ethnology_array = create_lists(df, 'Ethnology', 3)

print(df)
df['vector'] = df.apply(create_row_vectors, axis=1)

print(df['vector'].head(n=50))
vector_df = df[['translationSetId', 'vector']]

vector_df.to_csv('vector_csv.csv')
