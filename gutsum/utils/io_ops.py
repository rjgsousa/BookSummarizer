import pandas as pd
import pickle


def to_pickle(obj, file_path):
    with open(file_path, 'wb') as file:
        pickle.dump(obj, file)


def load_pickle(file_path):
    with open(file_path, 'rb') as file:
        obj = pickle.load(file)
    return obj


def to_parquet(df, file_path):
    df.to_parquet(file_path, engine='pyarrow')


def load_parquet(file_path):
    return pd.read_parquet(file_path, engine='pyarrow')
