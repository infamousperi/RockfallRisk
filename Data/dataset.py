import pandas as pd
import Calculations.calculations as cal
from datetime import timedelta, datetime


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


def merge_simulated_data(mass, velocity, timediff):
    merged_df = mass.join(velocity['Velocity [m/s]']).join(timediff['TimeDiffHours'])
    merged_df['CumulativeTimeDiff'] = merged_df['TimeDiffHours'].cumsum()

    merged_df['Kinetic Energy [kJ]'] = cal.calculate_kinetic_energy_kj(merged_df['Mass [kg]'],
                                                                       merged_df['Velocity [m/s]'])
    merged_df['DateTime'] = merged_df['CumulativeTimeDiff'].apply(_custom_date_time)

    # Since we cannot use .dt accessor, manually extract date and time components
    merged_df['Year'] = merged_df['DateTime'].apply(lambda x: x.year)
    merged_df['Month'] = merged_df['DateTime'].apply(lambda x: x.month)
    merged_df['Day'] = merged_df['DateTime'].apply(lambda x: x.day)
    merged_df['Timestamp'] = merged_df['DateTime'].apply(lambda x: x.strftime('%H:%M'))

    result_df = merged_df[['DateTime', 'Year', 'Month', 'Day', 'Timestamp',
                           'Mass [kg]', 'Velocity [m/s]', 'Kinetic Energy [kJ]', 'TimeDiffHours']]

    return result_df


def _custom_date_time(hours, start_year=1, start_month=1, start_day=1):
    start_date = datetime(start_year, start_month, start_day)
    return start_date + timedelta(hours=hours)


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
