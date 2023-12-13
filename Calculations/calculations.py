import pandas as pd
from datetime import timedelta


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
    concatenated_df['DateTime'] = pd.to_datetime(concatenated_df['Date'] + ' ' + concatenated_df['Time'], dayfirst=True)
    concatenated_df['LastClearing'] = concatenated_df['DateTime'].apply(_last_clearing_datetime)

    concatenated_df = concatenated_df.sort_values('DateTime')
    concatenated_df['CumulativeMass_kg'] = concatenated_df.groupby('LastClearing')['Mass [kg]'].cumsum()
    concatenated_df['CumulativeMassInNet'] = concatenated_df['CumulativeMass_kg'] - concatenated_df['Mass [kg]']

    # Find the first event for each DateTime and get its CumulativeMassInNet
    first_events = concatenated_df.drop_duplicates('DateTime').set_index('DateTime')['CumulativeMassInNet']
    concatenated_df['CumulativeMassInNet'] = concatenated_df['DateTime'].map(first_events)
    result_df = concatenated_df[['DateTime', 'Zone', 'Mass [kg]', 'Kinetic Energy [kJ]', 'CumulativeMassInNet']]

    return result_df


def _last_clearing_datetime(event_datetime):
    clearing_datetime = event_datetime.replace(hour=2, minute=0, second=0, microsecond=0)

    if event_datetime < clearing_datetime:
        clearing_datetime -= timedelta(days=1)

    return clearing_datetime
