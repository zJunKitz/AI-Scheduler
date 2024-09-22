import pandas as pd
from Parameters import Parameters
from io import BytesIO

def find_unique (uploaded_csv, target_column):
    temp_csv = BytesIO(uploaded_csv.getvalue())
    df = pd.read_csv(temp_csv)
    content = df[target_column].unique().tolist()
    return content

def prune_timetable(df, params):
    df = df.dropna(subset = ['LECTURER'])
    df = df[~ df['DAY'].isin(params.undesired_days)] #not in undesired days
    df = df[~ df['LECTURER'].isin(params.undesired_lecturer)]
    df = df[df['START_TIME'] <= params.threshold_start_time]

    return df

def lec_slot_validation(df, params):
    lec_slot_remain = df[df['CLASS_TYPE'] == 'LECTURE'].groupby('CLASS_ID').size()
    #print(lec_slot_remain)
    valid_lec_ids = lec_slot_remain[lec_slot_remain == params.required_lec_slot].index
    #print(valid_lec_ids)
    df = df[(df['CLASS_ID'].isin(valid_lec_ids)) | (df['CLASS_TYPE'] != 'LECTURE')]

    return df

def lec_tut_dependency_validation(df, params):
    tutorial_present = not df[df['CLASS_TYPE'] == 'TUTORIAL'].empty

    if tutorial_present:
        #Lecture cannot exist if it has no associated tutorials
        asssociated_lec_id_remain = df[df['CLASS_TYPE'] == 'TUTORIAL']['ASSOCIATED_LEC_ID'].unique()
        df = df[(df['CLASS_ID'].isin(asssociated_lec_id_remain)) | (df['CLASS_TYPE'] != 'LECTURE')]

        #Tutorials cannot exist if it has no associated lecture
        remaining_lec_id = df[df['CLASS_TYPE'] == 'LECTURE']['CLASS_ID'].unique()
        df = df[(df['CLASS_TYPE'] != 'TUTORIAL') | (df['ASSOCIATED_LEC_ID'].isin(remaining_lec_id))]

    return df
        

def filter_timetable(file_name, params):
    #Opening the csv file
    df = pd.read_csv(file_name, dtype={'START_TIME': str, 'END_TIME': str, 'ASSOCIATED_LEC_ID': str})
    df['START_TIME'] = pd.to_datetime(df['START_TIME'], format='%H%M').dt.strftime('%H:%M') #date time (dt), string from time (str-f-time)
    df['END_TIME'] = pd.to_datetime(df['END_TIME'], format='%H%M').dt.strftime('%H:%M')
    params.determine_lec_slot(df)

    #print(params.threshold_start_time)

    #print("Before prunning:")
    #print(df)
    df = prune_timetable(df, params)

    #print("After prunning:")
    #print(df)
    df = lec_slot_validation(df, params)

    #print("After slot validation:")
    #print(df)
    df = lec_tut_dependency_validation(df, params)

    #print("After lec-tut validation:")
    #print(df)

    df = df.reset_index(drop=True)
    return df




