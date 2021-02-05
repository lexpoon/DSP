import csv
import os
import random
import collections
from collections import defaultdict
import shutil
from datetime import date, datetime
import pandas as pd
import numpy as np
from pandas import ExcelWriter

fileDir = os.path.dirname(os.path.realpath('__file__'))
currentdate = date.today().strftime('%Y.%m.%d')

from import_rules import vector_df, df_rules_overview, museum_df

SYMBOLS = [' ', '/', '-', '&', ',', '\’','\‘', '\'', "'"]

feature_df = pd.read_csv("Data/featurelist.csv")
all_features_list = feature_df['Name'].to_list()

# These are a few standard functions that are used in a lot of scripts
def move_files(filename):
    shutil.move("%s/%s" %(fileDir, filename), "%s/RESULTS/%s" %(fileDir, filename))


def create_file(filename, df):
    df.to_excel(filename, index=False)
    move_files(filename)


def clean_column(df, column):
    for symbol in SYMBOLS:
        df["%s" %column] = df["%s" %column].astype(str).str.replace(r'%s' % symbol,'')
    return df


def convert_museumid_to_name(vector):
    # This function sorts the vector scores, picks the highest numbers as index number, which is the museum
    ind = np.argpartition(vector, -10)[-10:]

    museum_name_list = []
    museum_id_list = []
    # Create id-list and name-list for the 10 recommendations
    for x in ind:
        museum_id_list.append(museum_df.loc[x].at['translationSetId'])
        museum_name_list.append(museum_df.loc[x].at['publicName'])
    return museum_name_list, museum_id_list


def update_vectors(museum_vector, client_vector, count):

    # The museum vector is created to an array. Aftwards multiplied the amount of clicks. This is mainly due to
    # our setup with counts and the system not being real-time

    museum_vector = np.array(museum_vector.values[0])
    client_vector *= count
    new_array = np.transpose(museum_vector)
    new_vector = client_vector*new_array
    return new_vector


def prepare_excel_file(mydict):
    with ExcelWriter("validation_excel.xlsx") as writer:
        for k, v in mydict.items():
            v.to_excel(writer, sheet_name=k)
    move_files('validation_excel.xlsx')


def create_excel_sheet(row):
    museum_list = row['museum_id'].values[0]
    features = row['features'].values[0]
    df = create_validation(museum_list, features)
    return df


def create_statistical(df, features, feature_correct_dict, feature_wrong_dict):
    feature_total = len(features)

    # This is the part where we control the threshold for a 'succesful' recommendation.
    # If the threshold is met, we add to correct. IF not, we add to incorrect
    # The threshold is manully added for a few features that occur in less than 10 museums
    threshold = 7
    if feature_total == 2:
        threshold = 5
    if feature_total > 2:
        threshold = 4
    correct_total = 0
    for feature in features:
        data = df.loc['feature total', feature]
        if feature == 'educative' or feature == 'art_galleries' or feature == 'science':
            threshold = 3
        if feature == 'military' or feature == 'churches' or feature == 'gardens' or feature == 'audiotour':
            threshold = 1
        if data >= threshold:
            feature_correct_dict[feature] += 1
            correct_total += 1
        else:
            feature_wrong_dict[feature] += 1
    pass_fail = correct_total-feature_total
    return pass_fail


def create_validation(museum_list, features):
    new_df = df_rules_overview['translationSetId']
    new_df = new_df.to_frame()
    for feature in features:
        correct_column = df_rules_overview[f'{feature}']
        new_df[f'{feature}'] = correct_column
    total_df_list = []
    for museum in museum_list:
        row = new_df.loc[(new_df['translationSetId'] == museum)]
        df_temp = pd.DataFrame()
        df_temp['museumname'] = museum_df.loc[museum_df.translationSetId == museum]['publicName']
        row.insert(1, 'museumname', df_temp['museumname'])
        total_df_list.append(row)
    total_df = pd.concat(total_df_list)
    total_df.loc['feature total']= total_df.sum(numeric_only=True, axis=0)
    total_df.loc[:,'museum total'] = total_df.sum(numeric_only=True, axis=1)
    return total_df


def create_output_dataframes(correct_dict, incorrect_dict):
    combined_df = pd.DataFrame()
    for k, v in correct_dict.items():
        correct = v
        wrong = incorrect_dict.get(k)
        total = correct + wrong
        if total == 0:
            total += 1
        percentage = correct/total
        combined_df = combined_df.append({'feature': k, 'correct': correct, 'wrong':wrong , 'percentage': percentage}, ignore_index=True)
    combined_df.to_csv('results validation.csv')
    move_files('results validation.csv')


def run_all_validation():
    client_vector_dict = {}
    client_features_dict = {}
    client_id_list = []
    from create_validation_clients import get_dataframe_validation

    # This function get the validation clients and afterwards creates the recommendations.
    input_df, clients_for_excel = get_dataframe_validation()
    # This function loops over all the instances in the collected clients with its corresponding clicks and counts
    for index, row in input_df.iterrows():
        client = row['clientid']
        museum = row['translationSetId']
        count = row['count']
        # If client already has a click, the vector is retrieved here
        if client in client_id_list:
            client_vector = client_vector_dict.get(client)
        else:
            # If the client is seen for the first time, a new vector is initialized here
            # The features are also stored, as this is used for some of the validaiton files
            client_id_list.append(client)
            client_vector = np.ones(505, dtype=object)
            features = row['features']
            client_features_dict[client] = features
        # This is where the vector is updated for the client. The function takes the museum vector, the museum vector and the number of clicks, which results in an updated client vector
        museum_vector = vector_df[(vector_df['translationSetId'] == museum)].vector
        calculated_vector = update_vectors(museum_vector, client_vector, count)
        client_vector_dict[client] = calculated_vector

    # The df_vectors contains the client id with the corresponding vectors. These are the base of the recommendation
    df_vectors = pd.DataFrame()
    for k, v in client_vector_dict.items():
        museum_name_list, museum_id_list = convert_museumid_to_name(v)
        df_vectors = df_vectors.append({'clientid': k, 'museum_list': museum_name_list, 'museum_id': museum_id_list}, ignore_index=True)
    df_features = pd.DataFrame()
    for k, v in client_features_dict.items():
        df_features = df_features.append({'clientid': k, 'features': v}, ignore_index=True)

    df_total = df_vectors.merge(df_features, how='inner', on='clientid')

    # The following functions are creating output files
    feature_correct_dict = dict.fromkeys(all_features_list, 0)
    feature_wrong_dict = dict.fromkeys(all_features_list, 0)
    correct_wrong_list = []
    for index, row in df_total.iterrows():
        museum_list = row['museum_id']
        features = row['features']
        result_df = create_validation(museum_list, features)
        correct_wrong_list.append(create_statistical(result_df, features, feature_correct_dict, feature_wrong_dict))
    correct= correct_wrong_list.count(0)
    wrong= len(correct_wrong_list)-correct
    total = wrong + correct
    print(f'Total correct recommendations: {correct}')
    print(f'Total wrong recommendations: {wrong}')
    print(f'Percentage correct: {correct/total}')

    create_output_dataframes(feature_correct_dict, feature_wrong_dict)
    dataframe_dict = {}
    for client_x in clients_for_excel:
        row = df_total[(df_total['clientid'] == client_x)]
        temp_df = create_excel_sheet(row)
        dataframe_dict[client_x] = temp_df
        prepare_excel_file(dataframe_dict)
    df_total.to_csv('result_client_museums.csv')
    move_files('result_client_museums.csv')


def run_all_train():
    client_vector_dict = {}
    client_id_list = []

    from analytics import analytics_df

    for index, row in analytics_df.iterrows():
        client = row['clientid']
        museum = row['translationSetId']
        count = row['count']
        if client in client_id_list:
            client_vector = client_vector_dict.get(client)
        else:
            client_id_list.append(client)
            client_vector = np.ones(505, dtype=object)

        museum_vector = vector_df[(vector_df['translationSetId'] == museum)].vector
        calculated_vector = update_vectors(museum_vector, client_vector, count)
        client_vector_dict[client] = calculated_vector

    df = pd.DataFrame()
    for k, v in client_vector_dict.items():
        museum_name_list, museum_id_list = convert_museumid_to_name(v)
        df = df.append({'clientid': k, 'museum_list': museum_name_list, 'museum_id': museum_id_list}, ignore_index=True)
    df.to_csv('result_client_museums.csv')
    move_files('result_client_museums.csv')


def run_script():
    antwoord = input('Run training please type 1, run validation please type 2:\n')
    if antwoord == '1':
        run_all_train()
    else:
        run_all_validation()


run_script()
