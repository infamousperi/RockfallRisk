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


def simulate_gamma_distribution_rounded(df, n_simulations, sim_info, decimal_places=0):
    column = sim_info[1]
    isolated_data = df[column].dropna()

    # Calculate parameters for the gamma distribution
    mean_isolated_data = isolated_data.mean()
    variance_isolated_data = isolated_data.var()
    theta = variance_isolated_data / mean_isolated_data
    k = mean_isolated_data / theta

    # Simulate data using the gamma distribution
    simulated_data = gamma.rvs(a=k, scale=theta, size=n_simulations)

    # Round the simulated data
    rounded_simulated_data = [round(num, decimal_places) for num in simulated_data]

    # Ensure the first value is 0
    if len(rounded_simulated_data) > 0:
        rounded_simulated_data[0] = 0

    # Create DataFrame with rounded values
    simulated_df = pd.DataFrame(rounded_simulated_data, columns=[column])

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


def simulate_lognorm_distribution(df, n_simulations, sim_info):
    column = sim_info[1]
    isolated_data = df[column].dropna()

    # Calculate parameters for the lognorm distribution
    log_data = np.log(isolated_data[isolated_data > 0])  # Log-transform the data
    mu = log_data.mean()
    sigma = log_data.std()

    # Simulate data using the lognorm distribution
    simulated_data = lognorm.rvs(s=sigma, scale=np.exp(mu), size=n_simulations)
    simulated_df = pd.DataFrame(simulated_data, columns=[column])

    return simulated_df


def simulate_cauchy_distribution(df, n_simulations, sim_info):
    column = sim_info[1]
    isolated_data = df[column].dropna()

    # Calculate parameters for the Cauchy distribution
    location = isolated_data.median()
    scale = (isolated_data - isolated_data.median()).abs().mean()  # Manual calculation of MAD

    simulated_data = np.array([])

    # Simulate data in batches and filter for positive values
    while len(simulated_data) < n_simulations:
        batch_size = n_simulations - len(simulated_data)
        batch = cauchy.rvs(loc=location, scale=scale, size=batch_size * 10)  # Increase batch size
        positive_batch = batch[batch > 0][:batch_size]
        simulated_data = np.concatenate((simulated_data, positive_batch))

    simulated_df = pd.DataFrame(simulated_data[:n_simulations], columns=[column])

    return simulated_df
