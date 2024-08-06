import logging
import os
import re

import nltk
import numpy as np
import pandas as pd
import yaml
from bertopic import BERTopic
from bertopic.representation import KeyBERTInspired
from hdbscan import HDBSCAN
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sentence_transformers import SentenceTransformer
from umap import UMAP

from booksum.utils.get_gutenberg import get_by_book_id
from booksum.utils.io_ops import to_pickle, to_parquet, load_pickle, load_parquet
from booksum.utils.hash import get_file_hash


def create_embeddings(bks: list, file_path, model="all-MiniLM-L6-v2", just_load=False):
    embedding_model = SentenceTransformer(model, trust_remote_code=True)
    if just_load:
        return embedding_model, None

    embeddings = embedding_model.encode(bks, show_progress_bar=True)

    # save embeddings
    to_pickle(embeddings, file_path)
    return embedding_model, embeddings


def analyze_topics(
        data_path_prefix: str,
        models_path_prefix: str,
        experiment_md5: str,
        bks: pd.DataFrame
):
    logging.getLogger().setLevel(logging.INFO)
    all_books = np.concatenate(bks['sentences'].tolist(), axis=0)

    # we start by applying BERTopic best practices
    # 1. embeddings
    embeddings_and_model_file_path = os.path.join(models_path_prefix, f"{experiment_md5}_embeddings.pkl")
    if not os.path.exists(embeddings_and_model_file_path):
        logging.info("Creating embeddings and model ...")
        embedding_model, embeddings = create_embeddings(all_books, embeddings_and_model_file_path)
    else:
        logging.info("Loading embeddings and model ...")
        embeddings = load_pickle(embeddings_and_model_file_path)
        embedding_model, _ = create_embeddings([], None, just_load=True)

    # 2. preventing stochastic behaviour
    umap_model = UMAP(n_neighbors=15, n_components=3, metric='cosine', random_state=65535)

    # 3. controlling the number of topics
    hdbscan_model = HDBSCAN(min_cluster_size=5, metric='euclidean', cluster_selection_method='eom',
                            prediction_data=True)

    # 4. Improving default representation by removing stopwords
    representation_model = KeyBERTInspired()

    # train BERTopic
    topic_model = BERTopic(
        # Pipeline models
        embedding_model=embedding_model,
        umap_model=umap_model,
        hdbscan_model=hdbscan_model,
        representation_model=representation_model,

        # Hyperparameters
        min_topic_size=50,
        top_n_words=3,
        verbose=True
    )

    # Train model
    topics, probs = topic_model.fit_transform(all_books, embeddings)

    topic_model_file_path = os.path.join(models_path_prefix, f"topic_model_{experiment_md5}.pkl")
    topic_model.save(topic_model_file_path, serialization="safetensors", save_ctfidf=True,
                     save_embedding_model=embedding_model)

    topics_file_path = os.path.join(data_path_prefix, f'topics_{experiment_md5}.parquet')
    to_pickle(topics, topics_file_path)


def clean_text(text):
    text = text.decode(encoding="utf-8")
    text = re.sub(r'[\n\t\r]', ' ', text)  # Remove newlines and tabs
    text = re.sub(r'\s+', ' ', text).strip()  # Remove multiple spaces
    return text


def preprocess(text):
    # Remove non-alphabetic characters
    text = re.sub(r'\W', ' ', text)

    # Tokenize
    tokens = nltk.word_tokenize(text)

    # Convert to lower case
    tokens = [token.lower() for token in tokens]

    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token not in stop_words]

    # Lemmatize
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(token) for token in tokens]

    return tokens


def clean_books(bks: pd.DataFrame) -> pd.DataFrame:
    bks['book-clean'] = bks['book'].apply(clean_text)
    bks['sentences'] = bks['book-clean'].apply(nltk.sent_tokenize)
    return bks


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)

    data_file_path_prefix = 'data/cache'
    data_processed_file_path_prefix = 'data/processed/'
    models_file_path_prefix = 'models/'
    cfg_kb_filepath = "config/books_to_process.yaml"

    with open(cfg_kb_filepath, 'r') as file:
        books_ids = yaml.safe_load(file)

    data_sha = get_file_hash(str(books_ids))
    logging.info(f"Data SHA {data_sha}")

    # raw file obtained directly from gutenberg catalogue
    file_path_raw = os.path.join(data_file_path_prefix, f"{data_sha}.parquet")
    # cleaned files
    file_path_clean = os.path.join(data_processed_file_path_prefix, f"{data_sha}_clean.parquet")

    if not os.path.exists(file_path_raw):
        logging.info('Downloading books..')
        books = get_by_book_id(books_ids)
        to_parquet(books, file_path_raw)

    if not os.path.exists(file_path_clean):
        logging.info('Books already downloaded. Loading from disk..')
        books = load_parquet(file_path_raw)

        books_clean = clean_books(books)
        to_parquet(books_clean, file_path_clean)

    books_clean = load_parquet(file_path_clean)
    analyze_topics(
        data_processed_file_path_prefix,
        models_file_path_prefix,
        experiment_md5=data_sha,
        bks=books_clean
    )
