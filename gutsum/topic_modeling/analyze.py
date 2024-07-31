import hashlib
import json
import logging
import os

import pandas as df

from gutsum.utils.get_gutenberg import get_by_book_id


def analyze_topics(documents):
    pass


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)

    prefix = 'data/cache'
    book_ids = {'list-of-books': [158]}

    data_md5 = hashlib.md5(json.dumps(book_ids, sort_keys=True).encode('utf-8')).hexdigest()

    file_path = os.path.join(prefix, data_md5)

    if not os.path.exists(file_path):
        logging.info('Downloading books..')
        books = get_by_book_id(book_ids['list-of-books'])
        books.to_parquet(file_path, engine='pyarrow')
    else:
        logging.info('Books already downloaded. Loading from disk..')
        books = df.read_parquet(file_path, engine='pyarrow')
