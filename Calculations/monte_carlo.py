import pandas as pd
import numpy as np
from scipy.stats import gamma
from scipy.stats import norm
from scipy.stats import lognorm
from scipy.stats import cauchy


def simulate_gamma_distribution(df, n_simulations, sim_info):
    column = sim_info[1]
    isolated_data = df[column].dropna()

    # Calculate parameters for the gamma distribution
    mean_isolated_data = isolated_data.mean()
    variance_isolated_data = isolated_data.var()
    theta = variance_isolated_data / mean_isolated_data
    k = mean_isolated_data / theta

    # Simulate data using the gamma distribution
    simulated_data = gamma.rvs(a=k, scale=theta, size=n_simulations)
    simulated_df = pd.DataFrame(simulated_data, columns=[column])

    return simulated_df


def simulate_gamma_distribution_timediff(df, n_years, sim_info, decimal_places=0):
    column = sim_info[1]
    isolated_data = df[column].dropna()

    # Calculate parameters for the gamma distribution
    mean_isolated_data = isolated_data.mean()
    variance_isolated_data = isolated_data.var()
    theta = variance_isolated_data / mean_isolated_data
    k = mean_isolated_data / theta

    # Total hours to simulate
    total_hours = n_years * 8760
    current_sum = 0
    simulated_data = []

    # Simulate data until the sum reaches total_hours
    while current_sum < total_hours:
        simulated_value = gamma.rvs(a=k, scale=theta)
        rounded_value = round(simulated_value, decimal_places)
        current_sum += rounded_value

        if current_sum > total_hours:
            # Adjust the last value to match exactly total_hours
            rounded_value -= current_sum - total_hours

        simulated_data.append(rounded_value)

    # Ensure the first value is 0
    if len(simulated_data) > 0:
        simulated_data[0] = 0

    # Create DataFrame with rounded values
    simulated_df = pd.DataFrame(simulated_data, columns=[column])

    return simulated_df


def simulate_norm_distribution(df, n_simulations, sim_info):
    column = sim_info[1]
    isolated_data = df[column].dropna()

    # Calculate parameters for the normal distribution
    mean = isolated_data.mean()
    std_dev = isolated_data.std()

    # Simulate data using the normal distribution
    simulated_data = norm.rvs(loc=mean, scale=std_dev, size=n_simulations)
    simulated_df = pd.DataFrame(simulated_data, columns=[column])

    return simulated_df

