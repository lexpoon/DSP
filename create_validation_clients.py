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

SYMBOLS = [' ', '/', '-', '&', ',', '\’','\‘', '\'', "'"]
global user_id_list
user_id_list = []

rules_df = pd.read_csv('rules_overview.csv')
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
        museum_name_list.append(museum_df.loc[museum_df['translationSetId'] == x].publicName.iloc[0])

    return museum_name_list


def get_feature():
    print('1. History\n2. Visual\n3. Culture\n4. Culture\n5. Naval\n6. Tech\n7. Ethnology\n8. Library\n9. Openair\n10. Parking\n11. Weelchair\n12. Disabled\n13. Trainstation\n14. Restaurant\n')
    feature = input('Choose a feature from the list above:\n')
    return feature

def get_random_museums(df, number):
    feature = get_feature()
    feature = int(feature) + 6
    column = df[df.columns[feature]]
    temp_df = df[(column == 1)]
    mylist = temp_df['translationSetId'].to_list()
    top_ten = random.choices(mylist,k=number)
    print(top_ten)
    return top_ten

# print(random.randint(0,9))
def create_new_client():
    client_id = ''.join(random.sample(string.ascii_lowercase, 10))
    number_of_museums = 10
    my_list = get_random_museums(rules_df, number_of_museums)
    df = pd.DataFrame()
    for id in my_list:
        count = random.randint(0,9)

        df = df.append({'clientid': client_id, 'translationSetId': id, 'count': count}, ignore_index=True)
    return df

frames = []
for i in range(10):
    temp_df = create_new_client()
    frames.append(temp_df)
df = pd.concat(frames)
print(df)
