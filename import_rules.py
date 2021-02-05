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

    df = pd.read_csv(filename, encoding='utf-8', index_col=False, header=0)
    df_cleaned = df.drop_duplicates(subset=['publicName'])
    return df_cleaned

def apply_onehot(df):
    one_hot_cat = df.museaal_thema.str.get_dummies(', ')
    df = pd.concat([df, one_hot_cat], axis=1)
    return df

def create_lists(df, x, addition):
    mylist = df[f'{x}'].tolist()
    myarray = np.array(mylist)
    myarray *= addition
    myarray += 1
    return myarray

def create_rules_overview_df(df_r):
    df.drop(['index', 'facilities', 'vector'], axis=1, inplace=True)
    return df_r
def create_row_vectors(row):

    index = row['index']

    vector = np.ones(505, dtype=object)
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
    if row['exhibitions artists'] != 0:
        vector += exhibitionsartists_array
    if row['exp stories'] != 0:
        vector += expstories_array
    if row['historical collection'] != 0:
        vector += historical_collection_array
    if row['visual historical art'] != 0:
        vector += visual_historical_art_array
    if row['local history war'] != 0:
        vector += local_history_war_array
    if row['discovery anthropology'] != 0:
        vector += discoveryant_array
    if row['nature tech'] != 0:
        vector += nature_tech_array
    if row['castles cluster'] != 0:
        vector += castles_cluster_array
    if row['historical'] != 0:
        vector += historical_array
    if row['national speciality'] != 0:
        vector += national_speciality_array
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
    if row['scavenger'] != 0:
        vector += scavenger_array
    if row['science'] != 0:
        vector += science_array
    vector[index] = 0

    return vector

# Create the dataframe from the museum file and so some cleaning
filename = 'Data/Taxonomy_updated/musea.csv'
df = create_dataframe(filename)
df = df.drop_duplicates(subset=['publicName'])
df.rename(columns={'Unnamed: 0': "index"}, inplace=True)
df.drop(columns='index')
museum_df = df.sort_values('translationSetId')
museum_df.reset_index(inplace=True)
df = df[['publicName', 'translationSetId', 'facilities']]
df = df.sort_values('translationSetId')
df = df.reset_index(drop=True)

# Import the extra categories from the visitor file
df_visitor = create_dataframe('Data/musea_finalv2_Grae_adjusted.csv')
df_visitor = df_visitor.drop_duplicates(subset=['publicName'])
df = df.merge(df_visitor, how='left', left_on='translationSetId', right_on='translationSetId')
df = df.fillna(0)
df.reset_index(level=0, inplace=True)

# For every facility add the increase/weight/update value which will be converted to the update arrays
df = df.apply(create_true_falses_multiplication, axis=1)
df.drop(columns='publicName_y', inplace=True)
df.rename(columns={'publicName_x': "publicName"}, inplace=True)


# Create the update arrays for all the facilities
# Feature group 1: Museum Themes (12 total)
visual_array = create_lists(df, 'visual', 3)
culture_array = create_lists(df, 'culture', 2)
naval_array = create_lists(df, 'naval', 17)
nature_array = create_lists(df, 'nature', 10)
tech_array = create_lists(df, 'tech', 12)
ethnology_array = create_lists(df, 'ethnology', 26)
architectonic_array = create_lists(df, 'architectonic', 39)
educative_array = create_lists(df, 'educative', 72)
art_museum_array = create_lists(df, 'art_museum', 8)
historic_museum_array = create_lists(df, 'historic_museum', 5)
science_array = create_lists(df, 'science', 51)
military_array = create_lists(df, 'military', 168)
# Feature group 2: Description subject (10 total)
exhibitionsartists_array = create_lists(df, 'exhibitions artists', 7)
expstories_array = create_lists(df, 'exp stories', 6)
historical_collection_array = create_lists(df, 'historical collection', 24)
visual_historical_art_array = create_lists(df, 'visual historical art', 8)
local_history_war_array = create_lists(df, 'local history war', 26)
discoveryant_array = create_lists(df, 'discovery anthropology', 13)
nature_tech_array = create_lists(df, 'nature tech', 10)
castles_cluster_array = create_lists(df, 'castles cluster', 12)
historical_array = create_lists(df, 'historical', 19)
national_speciality_array = create_lists(df, 'national speciality', 12)
# Feature group 3: Museum extra's (9 total)
art_galleries_array = create_lists(df, 'art_galleries', 63)
historic_location_array = create_lists(df, 'historic_location', 28)
castles_array = create_lists(df, 'castles', 28)
churches_array = create_lists(df, 'churches', 126)
children_array = create_lists(df, 'children', 27)
gardens_array = create_lists(df, 'gardens', 84)
audiotour_array = create_lists(df, 'audiotour', 72)
exhibition_array = create_lists(df, 'exhibition', 2)
scavenger_array = create_lists(df, 'scavenger', 11)
# Feature group 4: Facilities (7 total)
library_array = create_lists(df, 'library', 3)
openair_array = create_lists(df, 'openair', 18)
parking_array = create_lists(df, 'parking', 2)
weelchair_array = create_lists(df, 'weelchair', 3)
disabled_array = create_lists(df, 'disabled', 23)
trainstation_array = create_lists(df, 'trainstation', 6)
restaurant_array = create_lists(df, 'restaurant', 4)

# Create final files with all the import rules and outcomes of the museum vectors
df['vector'] = df.apply(create_row_vectors, axis=1)
vector_df = df[['translationSetId', 'vector']]
vector_df.to_csv('vector_csv.csv')
move_files('vector_csv.csv')
df_rules_overview = create_rules_overview_df(df)
df_rules_overview.to_csv('rules_overview.csv')
shutil.move("%s/%s" % (fileDir, 'rules_overview.csv'), "%s/Data/%s" % (fileDir, 'rules_overview.csv'))
