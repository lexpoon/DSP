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
        row['library'] = 1
    else:
        row['library'] = 0
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

def create_rules_overview_df(df_r):
    df.drop(['index', 'facilities', 'vector'], axis=1, inplace=True)
    print(df_r)

    return df_r
def create_row_vectors(row):

    index = row['index']
    vector = np.zeros(496, dtype=object)
    vector += 1
    if row['library'] != 0:
        vector += library_array
    if row['openair'] != 0:
        vector += openair_array
    if row['parking'] != 0:
        vector += parking_array
    if row['weelchair'] != 0:
        vector += weelchair_array
    if row['disabled'] != 0:
        vector += disabled_array
    if row['trainstation'] != 0:
        vector += trainstation_array
    if row['restaurant'] != 0:
        vector += restaurant_array
    if row['visual'] != 0:
        vector += visual_array
    if row['culture'] != 0:
        vector += culture_array
    if row['naval'] != 0:
        vector += naval_array
    if row['nature'] != 0:
        vector += nature_array
    if row['tech'] != 0:
        vector += tech_array
    if row['ethnology'] != 0:
        vector += ethnology_array
    if row['cluster0'] != 0:
        vector += cluster0_array
    if row['cluster1'] != 0:
        vector += cluster1_array
    if row['cluster2'] != 0:
        vector += cluster2_array
    if row['cluster3'] != 0:
        vector += cluster3_array
    if row['cluster4'] != 0:
        vector += cluster4_array
    if row['cluster5'] != 0:
        vector += cluster5_array
    if row['cluster6'] != 0:
        vector += cluster6_array
    if row['cluster7'] != 0:
        vector += cluster7_array
    if row['cluster8'] != 0:
        vector += cluster8_array
    if row['cluster9'] != 0:
        vector += cluster9_array
    if row['architectonic'] != 0:
        vector += architectonic_array
    if row['educative'] != 0:
        vector += educative_array
    if row['historic_location'] != 0:
        vector += historic_location_array
    if row['historic_museum'] != 0:
        vector += historic_museum_array
    if row['castles'] != 0:
        vector += castles_array
    if row['churches'] != 0:
        vector += churches_array
    if row['children'] != 0:
        vector += children_array
    if row['art_galleries'] != 0:
        vector += art_galleries_array
    if row['art_museum'] != 0:
        vector += art_museum_array
    if row['military'] != 0:
        vector += military_array
    if row['audiotour'] != 0:
        vector += audiotour_array
    if row['exhibition'] != 0:
        vector += exhibition_array
    if row['lecture'] != 0:
        vector += lecture_array
    if row['scavenger'] != 0:
        vector += scavenger_array

    # if row['amsterdam'] != 0:
    #     vector += amsterdam_array
    # if row['utrecht'] != 0:
    #     vector += utrecht_array
    # if row['denhaag'] != 0:
    #     vector += denhaag_array
    # if row['leiden'] != 0:
    #     vector += leiden_array
    # if row['arnhem'] != 0:
    #     vector += arnhem_array
    # if row['groningen'] != 0:
    #     vector += groningen_array
    # if row['rotterdam'] != 0:
    #     vector += rotterdam_array
    # if row['limburg'] != 0:
    #     vector += limburg_array
    # if row['friesland'] != 0:
    #     vector += friesland_array
    # if row['gelderland'] != 0:
    #     vector += gelderland_array
    # if row['drenthe'] != 0:
    #     vector += drenthe_array
    # if row['kasteel'] != 0:
    #     vector += kasteel_array

    vector[index] = 1
    return vector

# Create the dataframe from the museum file and so some cleaning
filename = 'musea.csv'
df = create_dataframe(filename)
df = df.drop_duplicates(subset=['publicName'])
df.rename(columns={'Unnamed: 0': "index"}, inplace=True)
df = df[['publicName', 'index', 'translationSetId', 'facilities']]
df = df.sort_values('translationSetId')
df = df.reset_index(drop=True)
# Import the extra categories from the visitor file
df_visitor = create_dataframe('final_museum.csv')
df = df.merge(df_visitor, how='left', left_on='translationSetId', right_on='translationSetId')
df = df.fillna(0)
# Add all the facilites as on its own columns
df[['library', 'openair', 'parking', 'weelchair', 'disabled', 'trainstation', 'restaurant']] = False
# For every facility add the increase/weight/update value which will be converted to the update arrays
df = df.apply(create_true_falses_multiplication, axis=1)
df.drop(columns='publicName_y', inplace=True)
df.rename(columns={'publicName_x': "publicName"}, inplace=True)


# Create the update arrays for all the facilities
# Feature group 1: Museum Themes (13 total)
visual_array = create_lists(df, 'visual', 2)
culture_array = create_lists(df, 'culture', 3)
naval_array = create_lists(df, 'naval', 3)
nature_array = create_lists(df, 'nature', 3)
tech_array = create_lists(df, 'tech', 3)
ethnology_array = create_lists(df, 'ethnology', 3)
architectonic_array = create_lists(df, 'architectonic', 3)
educative_array = create_lists(df, 'educative', 3)
art_museum_array = create_lists(df, 'art_museum', 3)
historic_museum_array = create_lists(df, 'historic_museum', 3)
science_array = create_lists(df, 'science', 3)
military_array = create_lists(df, 'military', 3)

# Feature group 2: Description subject (10 total)
cluster0_array = create_lists(df, 'cluster0', 3)
cluster1_array = create_lists(df, 'cluster1', 3)
cluster2_array = create_lists(df, 'cluster2', 3)
cluster3_array = create_lists(df, 'cluster3', 3)
cluster4_array = create_lists(df, 'cluster4', 3)
cluster5_array = create_lists(df, 'cluster5', 3)
cluster6_array = create_lists(df, 'cluster6', 3)
cluster7_array = create_lists(df, 'cluster7', 3)
cluster8_array = create_lists(df, 'cluster8', 3)
cluster9_array = create_lists(df, 'cluster9', 3)



# Feature group 3: Museum extra's (9 total)
art_galleries_array = create_lists(df, 'art_galleries', 3)
historic_location_array = create_lists(df, 'historic_location', 3)
castles_array = create_lists(df, 'castles', 3)
churches_array = create_lists(df, 'churches', 3)
children_array = create_lists(df, 'children', 3)
gardens_array = create_lists(df, 'gardens', 3)
audiotour_array = create_lists(df, 'audiotour', 3)
exhibition_array = create_lists(df, 'exhibition', 2)
lecture_array = create_lists(df, 'lecture', 2)
scavenger_array = create_lists(df, 'scavenger', 3)

# Feature group 4: Facilities (7 total)
library_array = create_lists(df, 'library', 2)
openair_array = create_lists(df, 'openair', 3)
parking_array = create_lists(df, 'parking', 2)
weelchair_array = create_lists(df, 'weelchair', 4)
disabled_array = create_lists(df, 'disabled', 5)
trainstation_array = create_lists(df, 'trainstation', 2)
restaurant_array = create_lists(df, 'restaurant', 2)


# # Deze hieronder houden? lijkt me beetje overdreven en niet veel vertellen over musea
# specialplaces_array = create_lists(df, 'specialplaces', 3)
# # nature history museum category left out
# # What about the category below, does it help our recommendation?
# specialty_array = create_lists(df, 'specialty', 3)
# zero_four_array = create_lists(df, 'zero_four', 2)
# five_eight_array = create_lists(df, 'five_eight', 2)
# nine_twelve_array = create_lists(df, 'nine_twelve', 2)
# activity_array = create_lists(df, 'activity', 2)


# amsterdam_array = create_lists(df, 'amsterdam', 4)
# utrecht_array = create_lists(df, 'utrecht', 5)
# denhaag_array = create_lists(df, 'denhaag', 5)
# leiden_array = create_lists(df, 'leiden', 5)
# arnhem_array = create_lists(df, 'arnhem', 5)
# groningen_array = create_lists(df, 'groningen', 5)
# rotterdam_array = create_lists(df, 'rotterdam', 5)
# limburg_array =create_lists(df, 'limburg', 5)
# friesland_array = create_lists(df, 'friesland', 5)
# gelderland_array = create_lists(df, 'gelderland', 5)
# drenthe_array = create_lists(df, 'drenthe', 5)
# kasteel_array = create_lists(df, 'kasteel', 5)

df['vector'] = df.apply(create_row_vectors, axis=1)

print(df['vector'].head(n=50))
vector_df = df[['translationSetId', 'vector']]

vector_df.to_csv('vector_csv.csv')

df_rules_overview = create_rules_overview_df(df)
df_rules_overview.to_csv('rules_overview.csv')
