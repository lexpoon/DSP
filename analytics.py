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
import matplotlib.pyplot as plt
fileDir = os.path.dirname(os.path.realpath('__file__'))
currentdate = date.today().strftime('%Y.%m.%d')
# currentdate = '2019.04.02'
import json
SYMBOLS = [' ', '/', '-', '&', ',', '\’','\‘', '\'', "'"]


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

def clean_rows_pageviews(row):
    data = row['dimensions']
    row['clientid'] = data[0]
    row['sessionid'] = data[1]
    row['date'] = data[2].split('T')[0]
    row['time']= data[2].split('T')[1]
    row['contentid'] = data[3]
    row['path'] = data[4]
    return row

# Deze functie gebruiken bij hele data set, hieronder wordt functie gebruikt waar maar 1000 instances worden geladen
def create_dataframe_pageviews(filename):
    with open(f"{fileDir}/Data/pageviews/{filename}", "r") as read_file:
        data = json.load(read_file)
    new_data = data['reports'][0]['data']['rows']
    df = pd.DataFrame.from_dict(new_data)
    df = df.apply(clean_rows_pageviews, axis=1)
    df.drop(columns=['dimensions', 'metrics'], inplace=True)
    return df

def count_content(df):
    count_series = df.groupby(['clientid', 'contentid']).size()
    new_df = count_series.to_frame(name = 'amount').reset_index()
    new_df.sort_values(by=['amount'], ascending=False, inplace=True)
    new_df.to_csv('full_run_vectors_counts.csv')
    return new_df

def run_all_analytics():
    # This function loops over all the json analytics files and returns a dataframe with client id, museums clicked and the number of times clicked
    path = f'{fileDir}/Data/pageviews/'
    frames = []
    for file in os.listdir(path):
        print(f'Reading files for: {file}\n')

        df_pageview = create_dataframe_pageviews(file)
        frames.append(df_pageview)
    df = pd.concat(frames)
    df.to_csv('full_run_vectors.csv')
    move_files('full_run_vectors.csv')
    return count_content(df)

analytics_df = run_all_analytics()
