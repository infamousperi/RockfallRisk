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

    # Estimate the number of samples needed based on mean value
    estimated_samples = int(total_hours / mean_isolated_data) + 1

    # Sample the estimated number of values from the gamma distribution
    simulated_values = gamma.rvs(a=k, scale=theta, size=estimated_samples)

    # Round the values and calculate the cumulative sum
    rounded_values = np.round(simulated_values, decimal_places)
    cumulative_sum = np.cumsum(rounded_values)

    # Trim the array to the point where the cumulative sum just exceeds total_hours
    valid_indices = np.where(cumulative_sum <= total_hours)[0]
    if len(valid_indices) < len(cumulative_sum):
        # Include the next index to adjust the sum to match total_hours
        valid_indices = np.append(valid_indices, valid_indices[-1] + 1)

    # Adjust the last value to ensure the total matches exactly total_hours
    simulated_data = rounded_values[valid_indices]
    if cumulative_sum[valid_indices[-1]] > total_hours:
        simulated_data[-1] -= cumulative_sum[valid_indices[-1]] - total_hours

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

