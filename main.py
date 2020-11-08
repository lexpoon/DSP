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

def clean_rows(row):
    data = row['dimensions']
    # print(data)
    row['clientid'] = data[0]
    row['sessionid'] = data[1]
    row['date'] = data[2].split('T')[0]
    row['time']= data[2].split('T')[1]
    row['contentid'] = data[3]
    row['path'] = data[4]
    return row

def create_dataframe_pageviews():
    with open("Analytics/testpageviews.json", "r") as read_file:
        data = json.load(read_file)
    new_data = data['reports'][0]['data']['rows']
    df = pd.DataFrame.from_dict(new_data)
    df = df.apply(clean_rows, axis=1)

    df.drop(columns=['dimensions', 'metrics'], inplace=True)

    return df

df = create_dataframe_pageviews()


print(df.loc[df['contentid'] == 'b5023390-ced1-4210-a14c-23c349b2ee15'].count())

print(df.loc[df['contentid'] == 'b5023390-ced1-4210-a14c-23c349b2ee15'])
print(df.head())
