import pandas as pd
import Calculations.calculations as cal
from datetime import timedelta, datetime
import numpy as np


def get_out1():
    return _read_csv('Data/out_1.csv')


def get_out2():
    return _read_csv('Data/out_2.csv')


def _read_csv(filename):
    df = pd.read_csv(filename)
    df.columns = ['Date', 'Time', 'Mass [kg]', 'Velocity [m/s]']
    df['Kinetic Energy [kJ]'] = cal.calculate_kinetic_energy_kj(df['Mass [kg]'], df['Velocity [m/s]'])
    df['Date'] = pd.to_datetime(df['Date'], format='mixed').dt.strftime('%d/%m/%Y')
    df = cal.calculate_timedelta(df)

    return df


def _custom_date_time(hours, start_year=1, start_month=1, start_day=1):
    # Ensure hours is numeric
    hours = float(hours)
    start_date = np.datetime64(f"{start_year:04d}-{start_month:02d}-{start_day:02d}")
    new_date = start_date + np.timedelta64(int(hours), 'h')

    # Format the date and time separately
    date_str = str(new_date).split('T')[0]  # Extract date part
    time_str = str(new_date).split('T')[1] if 'T' in str(new_date) else "00"  # Extract or set time part

    # Ensure time is in HH:MM format
    if len(time_str) <= 2:
        time_str += ':00'

    return f"{date_str} {time_str}"


def merge_simulated_data(mass, velocity, timediff):
    merged_df = mass.join(velocity['Velocity [m/s]']).join(timediff['TimeDiffHours'])
    merged_df['CumulativeTimeDiff'] = merged_df['TimeDiffHours'].cumsum()

    # Calculate kinetic energy and create DateTime column
    merged_df['Kinetic Energy [kJ]'] = cal.calculate_kinetic_energy_kj(merged_df['Mass [kg]'],
                                                                       merged_df['Velocity [m/s]'])
    merged_df['DateTime'] = merged_df['CumulativeTimeDiff'].apply(_custom_date_time)

    result_df = merged_df[
        ['DateTime', 'Mass [kg]', 'Velocity [m/s]', 'Kinetic Energy [kJ]',
         'TimeDiffHours']]

    return result_df


def replace_outliers_with_median(df):
    columns = ['Mass [kg]', 'Velocity [m/s]', 'TimeDiffHours']

    for col in columns:
        # Define the quartiles
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1

        # Define the boundaries for outliers
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR

        # Identify outliers
        outliers = (df[col] < lower_bound) | (df[col] > upper_bound)

        # Calculate mean without outliers
        median_without_outliers = df.loc[~outliers, col].median()

        # Replace outliers with median
        df.loc[outliers, col] = median_without_outliers

    return df
