import pandas as pd
from datetime import datetime, timedelta
from multiprocessing import Pool, cpu_count
import gc
import os
import tempfile
import shutil


def calculate_kinetic_energy_kj(mass, velocity):
    kinetic_energy_kj = (0.5 * mass * velocity ** 2) / 1000

    return kinetic_energy_kj


def calculate_timedelta(df):
    df['DateTime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], dayfirst=True)
    df['TimeDiffHours'] = df['DateTime'].diff().dt.total_seconds() / 3600
    df['TimeDiffHours'] = df['TimeDiffHours'].fillna(0)

    return df


def calculate_cumulative_mass_since_clearing(df1, df2):
    df1['Zone'] = 1
    df2['Zone'] = 2

    concatenated_df = pd.concat([df1, df2], ignore_index=True)
    concatenated_df['LastClearing'] = concatenated_df['DateTime'].apply(_last_clearing_datetime)

    concatenated_df = concatenated_df.sort_values('DateTime')
    concatenated_df['CumulativeMass_kg'] = concatenated_df.groupby('LastClearing')['Mass [kg]'].cumsum()
    concatenated_df['CumulativeMassInNet'] = concatenated_df['CumulativeMass_kg'] - concatenated_df['Mass [kg]']

    # Find the first event for each DateTime and get its CumulativeMassInNet
    first_events = concatenated_df.drop_duplicates('DateTime').set_index('DateTime')['CumulativeMassInNet']
    concatenated_df['CumulativeMassInNet'] = concatenated_df['DateTime'].map(first_events)
    result_df = concatenated_df[['DateTime', 'Zone', 'Mass [kg]', 'Velocity [m/s]', 'Kinetic Energy [kJ]', 'CumulativeMassInNet']]

    return result_df


def _last_clearing_datetime(event_datetime):
    clearing_datetime = event_datetime.replace(hour=23, minute=30, second=0, microsecond=0)

    if event_datetime < clearing_datetime:
        clearing_datetime -= timedelta(days=1)

    return clearing_datetime


def _process_group(args):
    group, idx = args
    group['LastClearing'] = group['DateTime'].apply(_sim_last_clearing_datetime)
    group['CumulativeMass_kg'] = group.groupby('LastClearing')['Mass [kg]'].cumsum()
    group['CumulativeMassInNet'] = group['CumulativeMass_kg'] - group['Mass [kg]']

    first_events = group.drop_duplicates('DateTime').set_index('DateTime')['CumulativeMassInNet']
    group['CumulativeMassInNet'] = group['DateTime'].map(first_events)

    processed_chunk = group[['Kinetic Energy [kJ]', 'CumulativeMassInNet']].apply(pd.to_numeric, downcast='float')

    # Directory for temporary files
    temp_dir = 'Data/Temp'
    os.makedirs(temp_dir, exist_ok=True)  # Ensure the directory exists

    # Save the processed chunk to a temporary file
    temp_file_path = os.path.join(temp_dir, f'processed_chunk_{idx}.csv')
    processed_chunk.to_csv(temp_file_path, index=False)

    return temp_file_path


def sim_calculate_cumulative_mass_since_clearing(df1, df2):
    # Assuming 'Year' is a column in df1 and df2
    start_year = min(df1['Year'].min(), df2['Year'].min())
    end_year = max(df1['Year'].max(), df2['Year'].max())

    data_chunks = []

    for start in range(start_year, end_year + 1, 10000):
        end = min(start + 9999, end_year)

        chunk1 = df1[(df1['Year'] >= start) & (df1['Year'] <= end)]
        chunk2 = df2[(df2['Year'] >= start) & (df2['Year'] <= end)]

        concatenated_chunk = pd.concat([chunk1, chunk2]).sort_values('DateTime')
        data_chunks.append(concatenated_chunk)

        del concatenated_chunk, chunk1, chunk2
        gc.collect()

    num_processes = min(cpu_count(), len(data_chunks))

    with Pool(processes=num_processes) as pool:
        temp_file_paths = pool.map(_process_group, [(chunk, idx) for idx, chunk in enumerate(data_chunks)])

    # Read and concatenate all the processed chunks
    result_chunks = [pd.read_csv(temp_file) for temp_file in temp_file_paths]
    result_df = pd.concat(result_chunks)

    # Clean up the temporary files
    for temp_file in temp_file_paths:
        os.remove(temp_file)

    # Explicitly trigger garbage collection
    gc.collect()

    return result_df


def _sim_last_clearing_datetime(event_datetime_str):
    # Extract the year, month, day, and time components from the string
    date_part, time_part = event_datetime_str.split(' ')
    year, month, day = map(int, date_part.split('-'))

    # Check if the event time is before the clearing time on the same day
    if time_part < "23:30":
        day -= 1
        # Check for rollover
        if day < 1:
            month -= 1
            if month < 1:
                year -= 1
                month = 12
            # Determine the last day of the new month
            day = 31 if month in {1, 3, 5, 7, 8, 10, 12} else 30 if month in {4, 6, 9,
                                                                              11} else 29 if year % 4 == 0 and (
                        year % 100 != 0 or year % 400 == 0) else 28

    # Construct the last clearing datetime string with correct year
    clearing_datetime_str = f"{year:04d}-{month:02d}-{day:02d} 02:30"
    return clearing_datetime_str




