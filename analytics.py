
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
print(pd.options.display.max_columns)

def clean_rows_pageviews(row):
    data = row['dimensions']
    row['clientid'] = data[0]
    row['sessionid'] = data[1]
    row['date'] = data[2].split('T')[0]
    row['time']= data[2].split('T')[1]
    row['contentid'] = data[3]
    row['path'] = data[4]
    return row

def clean_rows_sessions(row):
    data = row['dimensions']
    row['clientid'] = data[0]
    row['sessionid'] = data[1]
    row['country'] =data[3]
    row['city'] = data[4]
    row['source_left'] = data[5].split('/')[0]
    row['source_right'] = data[5].split('/')[1]

    return row

def clean_rows_events(row):
    data = row['dimensions']
    row['clientid'] = data[0]
    row['sessionid'] = data[1]
    row['date'] = data[2].split('T')[0]
    row['time']= data[2].split('T')[1]
    row['contentid'] = data[3]
    row['path'] = data[4]
    return row

# def clean_rows_conversions(row):
#     data = row['dimensions']
#     row['clientid'] = data[0]
#     row['sessionid'] = data[1]
#     row['date'] = data[2].split('T')[0]
#     row['time']= data[2].split('T')[1]
#     row['contentid'] = data[3]
#     row['path'] = data[4]
#     return row

def create_dataframe_pageviews():
    with open("Data/pageviews/pageviews-2020-07-29.json", "r") as read_file:
        data = json.load(read_file)
    new_data = data['reports'][0]['data']['rows']
    df = pd.DataFrame.from_dict(new_data)
    df = df.apply(clean_rows_pageviews, axis=1)

    df.drop(columns=['dimensions', 'metrics'], inplace=True)

    print('Reading files for: Pagevies\n')
    print(df.head())

    return df

def create_dataframe_sessions():
    with open("Data/sessions/sessions-2020-07-29.json", "r") as read_file:
        data = json.load(read_file)
    new_data = data['reports'][0]['data']['rows']
    df = pd.DataFrame.from_dict(new_data)
    df = df.apply(clean_rows_sessions, axis=1)

    df.drop(columns=['dimensions', 'metrics'], inplace=True)

    print('Reading files for: Sessions\n')
    print(df.head())
    print(df.source_right.unique())
    return df

# def create_dataframe_events():
#     with open("Data/events/events-2020-07-29.json", "r") as read_file:
#         data = json.load(read_file)
#     new_data = data['reports'][0]['data']['rows']
#     df = pd.DataFrame.from_dict(new_data)
#     df = df.apply(clean_rows, axis=1)
#
#     df.drop(columns=['dimensions', 'metrics'], inplace=True)
#
#     print('Reading files for: Events\n')
#     print(df.loc[df['contentid'] == 'b5023390-ced1-4210-a14c-23c349b2ee15'].count())
#     print(df.head())
#     df.loc[df['clientid'] == '0929.2360171582027101'].count()

#     return df

# def create_dataframe_conversions():
#     with open("Data/conversions/conversions-2020-07-29.json", "r") as read_file:
#         data = json.load(read_file)
#     new_data = data['reports'][0]['data']['rows']
#     df = pd.DataFrame.from_dict(new_data)
#     df = df.apply(clean_rows, axis=1)
#
#     df.drop(columns=['dimensions', 'metrics'], inplace=True)
#
#     print('Reading files for: Conversions\n')
#     print(df.loc[df['contentid'] == 'b5023390-ced1-4210-a14c-23c349b2ee15'].count())
#     print(df.head())
#
#     return df

df_pageview = create_dataframe_pageviews()
df_sessions = create_dataframe_sessions()

# df_events = create_dataframe_events()
# df_conversions = create_dataframe_conversions()
