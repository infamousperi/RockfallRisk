import pandas as pd
import Calculations.calculations as cal


def get_out1():
    return _read_csv('Data/out_1.csv')


def get_out2():
    return _read_csv('Data/out_2.csv')


def _read_csv(filename):
    df = pd.read_csv(filename)
    df.columns = ['Date', 'Time', 'Mass [kg]', 'Velocity [m/s]']
    df['Kinetic Energy [kJ]'] = cal.calculate_kinetic_energy_kj(df['Mass [kg]'], df['Velocity [m/s]'])
    new_df = _convert_date(df)

    return new_df


def _convert_date(df):
    df['Date'] = pd.to_datetime(df['Date'], format='mixed').dt.strftime('%d/%m/%Y')
    df['Month'] = pd.to_datetime(df['Date'], format='%d/%m/%Y').dt.strftime('%m')
    return df
