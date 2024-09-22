import pandas as pd

#File name
file_name = 'OOPDS.csv'
output_filename = 'OOPDS_filtered'

#Global parameters (applies to all classes)
undesired_day = ['FRI']
threshold_time = '16:00'

#Class specific parameter
required_lec_slot = 2
required_tut_slot = 1
undesired_lecturer = ['BAU YOON TECK']



#Obtaining and formating data
df = pd.read_csv( file_name, dtype={'START_TIME':str, 'END_TIME':str, 'ASSOCIATED_LEC_ID':str})
df['START_TIME'] = pd.to_datetime(df['START_TIME'], format='%H%M').dt.strftime('%H:%M') #date time (dt), string from time (str-f-time)
df['END_TIME'] = pd.to_datetime(df['END_TIME'], format='%H%M').dt.strftime('%H:%M')

#Filtering
df = df.dropna(subset=['LECTURER'])
df = df[~df['DAY'].isin(undesired_day)] #in Pandas, [ ] means "only get row the condition in it is true"
df = df[~df['LECTURER'].isin(undesired_lecturer)]
df = df[df['START_TIME'] < threshold_time]

#Dependency validation
##Check if the present lecture slot matches the filtered timetable
if required_lec_slot > 1:
    lec_slot_count_remain = df[df['CLASS_TYPE'] == 'LECTURE'].groupby('CLASS_ID').size()
    valid_lec_ids = lec_slot_count_remain[lec_slot_count_remain == required_lec_slot].index
    df = df[(df['CLASS_ID'].isin(valid_lec_ids)) | (df['CLASS_TYPE'] != 'LECTURE')]

df = df.reset_index(drop=True)
print(df)

##If tutorials are present, check Lec-Tut dependency
tutorial_present = not df[df['CLASS_TYPE'] == 'TUTORIAL'].empty

if tutorial_present:
    associated_lec_id_remain = (df[df['CLASS_TYPE'] == 'TUTORIAL'])['ASSOCIATED_LEC_ID'].unique() 
    df = df[(df['CLASS_ID'].isin(associated_lec_id_remain)) | (df['CLASS_TYPE'] != 'LECTURE')]

    remaining_lec_id = df[df['CLASS_TYPE']=='LECTURE']['CLASS_ID'].unique()
    df = df[(df['CLASS_TYPE'] != 'TUTORIAL') | (df['ASSOCIATED_LEC_ID'].isin(remaining_lec_id))] #condition order matter in Pandas
    

df = df.reset_index(drop=True)
print(df)
df.fillna('N/A', inplace=True)
df.to_csv(output_filename, index=False)
