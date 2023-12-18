import pandas as pd
from datetime import datetime, timedelta


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
    clearing_datetime = event_datetime.replace(hour=2, minute=30, second=0, microsecond=0)

    if event_datetime < clearing_datetime:
        clearing_datetime -= timedelta(days=1)

    return clearing_datetime


def sim_calculate_cumulative_mass_since_clearing(df1, df2):
    df1['Zone'] = 1
    df2['Zone'] = 2

    # Concatenate dataframes without resetting index to maintain original order for later operations
    concatenated_df = pd.concat([df1, df2])

    # Create a 'DateTime' string representation
    concatenated_df['DateTime'] = concatenated_df['Year'].astype(str) + '-' + \
                                  concatenated_df['Month'].astype(str).str.zfill(2) + '-' + \
                                  concatenated_df['Day'].astype(str).str.zfill(2) + ' ' + \
                                  concatenated_df['Timestamp']

    # Apply custom function to calculate the 'LastClearing' based on the 'DateTime' string
    concatenated_df['LastClearing'] = concatenated_df['DateTime'].apply(_sim_last_clearing_datetime)

    # Sort by 'DateTime' string
    concatenated_df = concatenated_df.sort_values('DateTime')

    # Calculate cumulative mass
    concatenated_df['CumulativeMass_kg'] = concatenated_df.groupby('LastClearing')['Mass [kg]'].cumsum()
    concatenated_df['CumulativeMassInNet'] = concatenated_df['CumulativeMass_kg'] - concatenated_df['Mass [kg]']

    # Find the first event for each 'DateTime' and get its 'CumulativeMassInNet'
    first_events = concatenated_df.drop_duplicates('DateTime').set_index('DateTime')['CumulativeMassInNet']
    concatenated_df['CumulativeMassInNet'] = concatenated_df['DateTime'].map(first_events)

    # Create the result dataframe with relevant columns
    result_df = concatenated_df[
        ['DateTime', 'Zone', 'Mass [kg]', 'Velocity [m/s]', 'Kinetic Energy [kJ]', 'CumulativeMassInNet']]

    return result_df


def _sim_last_clearing_datetime(event_datetime_str):
    # Extract the year, month, day, and time components from the string
    date_part, time_part = event_datetime_str.split(' ')
    year, month, day = map(int, date_part.split('-'))

    # Check if the event time is before the clearing time on the same day
    if time_part < "02:30":
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

