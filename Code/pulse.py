import os
import time as time
from datetime import date,datetime,timedelta
import pandas as pd
import numpy as np
import shutil
import csv

def pulse_preprocessor(pulse_dir, format_data=True):
    df_ss = None  # session summaries
    for filename in os.listdir(pulse_dir):
        df = None
        f = os.path.join(pulse_dir, filename)

        if os.path.isfile(f):
            if 'merged' in f.lower():
                print(f + ' skipped.')
            else:
                # print(f+' processed.')
                if '_group+2_' in f.lower():  # string used to identify valid files.
                    df = pd.read_csv(f, sep=',')
                    if df_ss is not None:
                        df_ss = pd.concat([df_ss, df])
                    else:
                        df_ss = df

    df_ss = df_ss.drop_duplicates(keep='first')
    if format_data == True: df_ss = pulse_data_formatter(df_ss)
    df_ss.to_csv(os.path.join(pulse_dir, 'pulse_test_out_merged.csv'), sep=',')

    return (df_ss)

def pulse_data_formatter(df):
    #This formats Pulse heart rate data.
    #Data was part of an experiment from September/October 2023, but was never used with AMS data.
    df = df.drop(columns=['Session name', 'Phase name', 'Type'])
    # Non _ Symbols in variable names do not translate well to R, so I'm renaming basically everything to remove them.
    df = df.rename(columns={'Start time': 'Start_Time',
                            'End time': 'End_Time',
                            'HR min [bpm]': 'HR_min_bpm',
                            'HR avg [bpm]': 'HR_avg_bpm',
                            'HR max [bpm]': 'HR_max_bpm',
                            'HR min [%]': 'HR_min_percent',
                            'HR avg [%]': 'HR_avg_percent',
                            'HR max [%]': 'HR_max_percent',
                            'Time in HR zone 1 (50 - 59 %)': 'Seconds_in_HR_Zone_1',
                            'Time in HR zone 2 (60 - 69 %)': 'Seconds_in_HR_Zone_2',
                            'Time in HR zone 3 (70 - 79 %)': 'Seconds_in_HR_Zone_3',
                            'Time in HR zone 4 (80 - 89 %)': 'Seconds_in_HR_Zone_4',
                            'Time in HR zone 5 (90 - 100 %)': 'Seconds_in_HR_Zone_5',
                            'Total distance [m]': 'Total_Distance_meters',
                            'Distance / min [m/min]': 'Distance_per_minute',
                            'Maximum speed [km/h]': 'Maximum_Speed_kmph',
                            'Average speed [km/h]': 'Average_Speed_kmph',
                            'Distance in Speed zone 1 [m] (3.00 - 6.99 km/h)': 'Distance_in_Speed_Zone_1',
                            'Distance in Speed zone 2 [m] (7.00 - 10.99 km/h)': 'Distance_in_Speed_Zone_2',
                            'Distance in Speed zone 3 [m] (11.00 - 14.99 km/h)': 'Distance_in_Speed_Zone_3',
                            'Distance in Speed zone 4 [m] (15.00 - 18.99 km/h)': 'Distance_in_Speed_Zone_4',
                            'Distance in Speed zone 5 [m] (19.00- km/h)': 'Distance_in_Speed_Zone_5',
                            'Number of accelerations (-50.00 - -3.00 m/s²)': 'Acceleration_Count_Group_1',
                            'Number of accelerations (-2.99 - -2.00 m/s²)': 'Acceleration_Count_Group_2',
                            'Number of accelerations (-1.99 - -1.00 m/s²)': 'Acceleration_Count_Group_3',
                            'Number of accelerations (-0.99 - -0.50 m/s²)': 'Acceleration_Count_Group_4',
                            'Number of accelerations (0.50 - 0.99 m/s²)': 'Acceleration_Count_Group_5',
                            'Number of accelerations (1.00 - 1.99 m/s²)': 'Acceleration_Count_Group_6',
                            'Number of accelerations (2.00 - 2.99 m/s²)': 'Acceleration_Count_Group_7',
                            'Number of accelerations (3.00 - 50.00 m/s²)': 'Acceleration_Count_Group_8',
                            'Calories [kcal]': 'Calories_in_kcal',
                            'Training load score': 'Training_Load_Score',
                            'Cardio load': 'Cardio_Load',
                            'Recovery time [h]': 'Recovery_Time_in_h',
                            'Min RR interval': 'Min_RR_Interval',
                            'Max RR interval': 'Max_RR_Interval',
                            'Avg RR interval': 'Avg_RR_Interval',
                            'HRV (RMSSD)':'HRV_RMSSD'})

    df.columns = df.columns.str.replace(' ', '_')
    # I'm sure pd.to_datetime or datetime.strptime in a lambda would work for this, but the correct formatting is eluding me.
    df['Duration'] = df['Duration'].map(lambda x: hourminsec_to_seconds(x))
    df['Seconds_in_HR_Zone_1'] = df['Seconds_in_HR_Zone_1'].map(lambda x: hourminsec_to_seconds(x))
    df['Seconds_in_HR_Zone_2'] = df['Seconds_in_HR_Zone_2'].map(lambda x: hourminsec_to_seconds(x))
    df['Seconds_in_HR_Zone_3'] = df['Seconds_in_HR_Zone_3'].map(lambda x: hourminsec_to_seconds(x))
    df['Seconds_in_HR_Zone_4'] = df['Seconds_in_HR_Zone_4'].map(lambda x: hourminsec_to_seconds(x))
    df['Seconds_in_HR_Zone_5'] = df['Seconds_in_HR_Zone_5'].map(lambda x: hourminsec_to_seconds(x))

    df['Start_Time'] = pd.to_datetime(df['Start_Time'], dayfirst=True)
    df['End_Time'] = pd.to_datetime(df['End_Time'], dayfirst=True)
    return (df)