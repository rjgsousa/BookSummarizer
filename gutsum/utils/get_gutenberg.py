import yaml

import gutenbergpy.textget
import pandas as pd


def get_by_book_id(books_by_author: dict) -> pd.DataFrame:

    books_by_id = {'id': [], 'book': [], 'author': [], 'title': []}

    for author in books_by_author['authors']:
        author_name = author['author']
        books_from_author_name = author['list-of-books']
        for books in books_from_author_name:
            book_id = books['id']
            book_title = books['title']

            raw_book = gutenbergpy.textget.get_text_by_id(book_id)
            clean_book = gutenbergpy.textget.strip_headers(raw_book)

            books_by_id['id'].append(book_id)
            books_by_id['book'].append(clean_book)
            books_by_id['author'].append(author_name)
            books_by_id['title'].append(book_title)

    # convert to pandas
    df = pd.DataFrame(books_by_id)
    return df


if __name__ == "__main__":
    with open('../../config/books_to_process.yaml', 'r') as file:
        books_ids = yaml.safe_load(file)

    get_by_book_id(books_ids)

