"""This module contains the processes to preprocess the data.
"""

import pandas as pd

import logging

logging.basicConfig(level=logging.INFO)

def load_data(data_path):
    """
    Reads the dataset from a directory.
        Params:
            data_path (str): directory containing dataset in csv format.
        Returns:
            df: dataframe containing input data. NAs are dropped.
            """
    df = pd.read_csv(data_path, sep=';')
    df = df.dropna()
    return df


def run(data_path):
    """
    Main script to read and load data into dataframe.
        Params:
            data_path(str): directory containing dataset in csv.
        Returns:
            df: DataFrame containing input data.
            """
    logging.info("Loading and processing data...")
    df = load_data(data_path)
    logging.info(f"Dataset loaded: {df.shape[0]} rows, {df.shape[1]} columns.")
    return df
