import pandas as pd
import Calculations.calculations as cal
import numpy as np
from Calculations.calculations import calculate_kinetic_energy_kj
from multiprocessing import Pool, cpu_count
import gc
import os
import tempfile


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


# Custom Datetime for dates out of the range in Python
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


# Chunked process for merging simulated data, calculate Kinetic energy and Datetime
def _process_chunk(args):
    chunk, temp_dir, idx = args
    chunk['Kinetic Energy [kJ]'] = calculate_kinetic_energy_kj(chunk['Mass [kg]'], chunk['Velocity [m/s]'])
    chunk['DateTime'] = chunk['CumulativeTimeDiff'].apply(_custom_date_time)
    chunk['Year'] = chunk['DateTime'].apply(lambda x: x.split('-')[0])
    processed_chunk = chunk[['DateTime', 'Year', 'Mass [kg]', 'Kinetic Energy [kJ]']]

    # Save the processed chunk to a temporary file
    temp_file = os.path.join(temp_dir, f'processed_chunk_{idx}.csv')
    processed_chunk.to_csv(temp_file, index=False)
    return temp_file


def merge_simulated_data(mass, velocity, timediff):
    full_data = mass.join(velocity['Velocity [m/s]']).join(timediff['TimeDiffHours'])
    full_data['CumulativeTimeDiff'] = full_data['TimeDiffHours'].cumsum()

    ensure_directory_exists('Data/Temp')
    chunk_size = 100000

    chunks = [(full_data.iloc[i:i + chunk_size], 'Data/Temp', idx)
              for idx, i in enumerate(range(0, len(full_data), chunk_size))]

    num_processes = min(cpu_count(), len(chunks))

    # Create and manage a temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        with Pool(processes=num_processes) as pool:
            temp_files = pool.map(_process_chunk, [(chunk, temp_dir, idx) for chunk, _, idx in chunks])

        # Read and concatenate all the processed chunks
        concatenated_df = pd.concat([pd.read_csv(file) for file in temp_files])

        # Delete the temporary files
        for file in temp_files:
            os.remove(file)

    # Explicitly trigger garbage collection
    gc.collect()

    return concatenated_df


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


def ensure_directory_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)
