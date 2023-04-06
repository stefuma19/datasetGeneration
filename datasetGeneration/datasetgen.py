import numpy as np
import pandas as pd


def generate_uniform(num_samples, dimensions):
    X = np.random.uniform(size=(num_samples, dimensions))
    print("Dataset with uniform distribution: {}".format(X.shape))
    return X


def generate_normal(num_samples, dimensions):
    X = np.random.normal(size=(num_samples, dimensions))
    # normalization process
    max = 0
    min = 0
    for i in range(0, dimensions):
        for j in range(0, num_samples):
            if X[j, i] < min:
                min = X[j, i]
        for j in range(0, num_samples):
            X[j, i] = X[j, i] - min
    for i in range(0, dimensions):
        for j in range(0, num_samples):
            if X[j, i] > max:
                max = X[j, i]
        for j in range(0, num_samples):
            X[j, i] = X[j, i] / max

    print("Dataset with normal distribution: {}".format(X.shape))
    return X


def generate_exponential(num_samples, dimensions):
    X = np.random.exponential(size=(num_samples, dimensions))
    # normalization process
    max = 0
    for i in range(0, dimensions):
        for j in range(0, num_samples):
            if X[j, i] > max:
                max = X[j, i]
        for j in range(0, num_samples):
            X[j, i] = X[j, i] / max
    print("Dataset with exponential distribution: {}".format(X.shape))
    return X


def generate_multivariate_normal(num_samples, mean, cov):
    X = np.random.multivariate_normal(mean, cov, size=num_samples)
    print("Dataset with multivariate normal distribution: {}".format(X.shape))
    return X


def save_dataset_to_csv(ds, output_filename):
    size = ds.shape[1]
    coords = []
    for i in range(size):
        coords.append('x' + str(i + 1))
    print(coords)

    df = pd.DataFrame(ds, columns=coords)
    # shift the index of the DataFrame to start from 1
    df.index = df.index + 1
    df.to_csv(output_filename, index=True)
    print("Dataset saved")
