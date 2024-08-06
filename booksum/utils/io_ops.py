import json
import os
import pickle

import pandas as pd
import yaml


class BookSumDataSetIO:
    def __init__(self, data_path):
        self.booksum = load_parquet(
            os.path.join(data_path, "booksum.parquet")
        )

    def get_booksum_summary_and_chapter_by_name_and_chapter(self, book_chapter_name):
        # just return the first entry
        book = self.booksum[(self.booksum["book_id"] == book_chapter_name)][['bid', 'summary', 'chapter']].iloc[0]
        book_parquet_ref = self.booksum[(self.booksum["book_id"] == book_chapter_name)].iloc[0].name
        summary_dict = book['summary']
        summary = json.loads(summary_dict)['summary']

        chapter = book['chapter']
        bid = book['bid']

        return bid, summary, chapter, book_parquet_ref

    def get_booksum_by_index(self, ix):
        book = self.booksum.iloc[ix][['bid', 'summary', 'chapter']]

        summary_dict = book['summary']
        summary = json.loads(summary_dict)['summary']

        chapter = book['chapter']

        return summary, chapter, ix

    def get_booksum_by_bid(self, bid):
        idx = self.booksum[self.booksum['bid'] == bid].iloc[0].name

        book = self.booksum.iloc[idx][['bid', 'summary', 'chapter']]

        summary_dict = book['summary']
        summary = json.loads(summary_dict)['summary']

        chapter = book['chapter']

        return summary, chapter, idx


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


# -------------------------------------------
# Get Settings Configuration
def get_settings(srv_root):
    config_file = os.path.join(
        srv_root, 'config/config_services.yaml'
    )
    with open(config_file, 'r') as fd:
        settings = yaml.safe_load(fd)

    return settings
